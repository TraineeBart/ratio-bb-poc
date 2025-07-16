# ╭───────────────────────────────────────────────────────────╮
# │ File: src/infra/ws_client_adapter.py                      │
# │ Module: infra                                             │
# │ Doel: Adapter voor WebSocket-client zodat deze            │
# │       eenvoudig in de orchestrator kan worden geïnjecteerd│
# │ Auteur: ArchitectGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: draft                                            │
# ╰───────────────────────────────────────────────────────────╯

import threading
import time
import asyncio
import websockets
import json
import logging
from datetime import datetime
from client.kucoin_client import get_bullet_public
import random

# Adapter voor live WebSocket tickdata
# Onderliggend kan dit bijvoorbeeld een KuCoinWSClient of MockClient zijn.
# Deze wrapper maakt het mogelijk om eenvoudig van implementatie te wisselen.

class WSClientAdapter:
    """
    🧠 Klasse: WSClientAdapter
    Wrapper om een WebSocket-client te gebruiken met een uniforme callback-structuur.

    ▶ In:
        - symbols (list[str]): lijst van te volgen trading pairs
        - callback (Callable): functie die aangeroepen wordt bij nieuwe ticks

    ⏺ Out:
        - Start en stop van de WebSocket-verbinding

    💡 Opmerkingen:
        - Deze adapter zorgt ervoor dat de orchestrator onafhankelijk blijft van de concrete WS-implementatie.
        - In deze draft-implementatie wordt een mock ticker gestart.
    """
    def __init__(self, symbols, callback, mode="sim"):
        self.symbols = symbols
        self.callback = callback
        self.mode = mode
        self._running = False
        self._thread = None
        self.last_price_theta = None
        self.last_price_tfuel = None

        if self.mode == "live":
            self.client = LiveWSClient(symbols, callback)
        else:
            self.client = MockWSClient(symbols, callback)
        self.client.parent = self

    async def start(self):
        await self.client.start()

    def stop(self):
        self.client.stop()

class MockWSClient:
    def __init__(self, symbols, callback):
        self.symbols = symbols
        self.callback = callback
        self._running = False
        self._thread = None
        self.parent = None

    def _mock_stream(self):
        base_price = 42.0
        while self._running:
            for symbol in self.symbols:
                fluctuation = random.uniform(-2.5, 2.5)  # Schommelingen rondom base_price
                tick = {
                    'symbol': symbol,
                    'price': base_price + fluctuation,
                    'timestamp': time.time()
                }
                if symbol == "THETA-USDT":
                    self.parent.last_price_theta = tick['price']
                elif symbol == "TFUEL-USDT":
                    self.parent.last_price_tfuel = tick['price']

                if self.parent.last_price_theta and self.parent.last_price_tfuel:
                    ratio = round(self.parent.last_price_theta / self.parent.last_price_tfuel, 4)
                else:
                    ratio = None

                self.callback(symbol, tick, ratio)
            time.sleep(1)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._mock_stream, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

class LiveWSClient:
    async def _ping_loop(self, ws, ping_interval):
        """
        🧠 Functie: _ping_loop
        Zorgt voor een periodieke ping naar KuCoin ongeacht tick-activiteit.
        Hiermee voorkomen we disconnects door ping timeouts.

        ▶ In:
            - ws: actieve WebSocket-verbinding
            - ping_interval: interval in seconden volgens KuCoin spec
        """
        try:
            if getattr(ws, 'closed', True):
                logging.warning("Ping loop startte met gesloten of ongeldige WS-socket. Stop pingen.")
                return
        except Exception as e:
            logging.warning(f"Ping loop check exception: {e}")
            return

        while self._running:
            try:
                if getattr(ws, 'closed', True):
                    logging.warning("WSClient ping loop detecteerde gesloten of ongeldige socket. Stop pingen.")
                    break
            except Exception as e:
                logging.warning(f"Ping loop check exception: {e}")
                break
            await asyncio.sleep(ping_interval)
            try:
                ping_msg = {"id": "ping-id", "type": "ping"}
                await ws.send(json.dumps(ping_msg))
                logging.debug("WSClient sent scheduled ping")
            except Exception as e:
                logging.warning(f"Ping loop error: {e}")
                break

    def __init__(self, symbols, callback):
        self.symbols = symbols
        self.callback = callback
        self._running = False
        self.parent = None

    async def start(self):
        self._running = True
        await self._run_ws()

    def stop(self):
        self._running = False

    async def _run_ws(self):
        while self._running:
            try:
                auth = get_bullet_public()
                url = f"{auth['endpoint']}?token={auth['token']}"
                ping_interval = auth.get('pingInterval', 50000) / 1000

                logging.info(f"WSClient connecting to {url}")

                try:
                    async with websockets.connect(url) as ws:
                        self._backoff = 1  # Reset backoff na succesvolle verbinding
                        ping_task = asyncio.create_task(self._ping_loop(ws, ping_interval))

                        for symbol in self.symbols:
                            subscribe_msg = {
                                "id": f"subscribe-{symbol}",
                                "type": "subscribe",
                                "topic": f"/market/ticker:{symbol}",
                                "privateChannel": False,
                                "response": True
                            }
                            await ws.send(json.dumps(subscribe_msg))

                        last_ping = time.time()

                        while self._running:
                            try:
                                message = await asyncio.wait_for(ws.recv(), timeout=ping_interval)
                                data = json.loads(message)

                                if data.get('type') == 'pong':
                                    logging.debug("WSClient received pong")
                                    continue

                                if 'data' in data:
                                    kucoin_time = data['data'].get('time')
                                    if kucoin_time:
                                        timestamp = datetime.utcfromtimestamp(kucoin_time / 1000).isoformat() + "Z"
                                    else:
                                        timestamp = datetime.utcnow().isoformat() + "Z"

                                    tick = {
                                        'symbol': data['topic'].split(":")[-1],
                                        'price': float(data['data']['price']),
                                        'timestamp': timestamp
                                    }
                                    if tick['symbol'] == "THETA-USDT":
                                        self.parent.last_price_theta = tick['price']
                                    elif tick['symbol'] == "TFUEL-USDT":
                                        self.parent.last_price_tfuel = tick['price']

                                    if self.parent.last_price_theta and self.parent.last_price_tfuel:
                                        ratio = round(self.parent.last_price_theta / self.parent.last_price_tfuel, 4)
                                    else:
                                        ratio = None

                                    logging.debug(f"Tick ontvangen: {tick}")
                                    self.callback(tick['symbol'], tick, ratio)

                            except asyncio.TimeoutError:
                                logging.debug("Timeout: geen message ontvangen binnen ping_interval, maar ping wordt nu al periodiek gestuurd.")
                                continue
                finally:
                    if 'ping_task' in locals():
                        ping_task.cancel()
                        try:
                            await ping_task
                        except asyncio.CancelledError:
                            logging.info("Ping task netjes geannuleerd na WS sluiting.")

            except Exception as e:
                logging.warning(f"WSClient reconnect due to error: {e}")

                # Exponential backoff bij reconnect
                if not hasattr(self, '_backoff'):
                    self._backoff = 1
                else:
                    self._backoff = min(self._backoff * 2, 30)  # Max 30 seconden

                logging.info(f"Backoff: wacht {self._backoff} seconden voor nieuwe connectie.")
                await asyncio.sleep(self._backoff)