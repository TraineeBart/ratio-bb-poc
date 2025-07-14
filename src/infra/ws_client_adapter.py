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
from datetime import datetime
from client.kucoin_client import get_bullet_public

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

        if self.mode == "live":
            self.client = LiveWSClient(symbols, callback)
        else:
            self.client = MockWSClient(symbols, callback)

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()

class MockWSClient:
    def __init__(self, symbols, callback):
        self.symbols = symbols
        self.callback = callback
        self._running = False
        self._thread = None

    def _mock_stream(self):
        while self._running:
            for symbol in self.symbols:
                tick = {'symbol': symbol, 'price': 42.0, 'timestamp': time.time()}
                self.callback(symbol, tick)
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
    def __init__(self, symbols, callback):
        self.symbols = symbols
        self.callback = callback
        self._running = False

    def start(self):
        self._running = True
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_until_complete, args=(self._run_ws(),), daemon=True).start()

    def stop(self):
        self._running = False

    async def _run_ws(self):
        auth = get_bullet_public()
        url = f"{auth['endpoint']}?token={auth['token']}"
        ping_interval = auth.get('pingInterval', 50000) / 1000  # omzetten naar seconden

        while self._running:
            try:
                async with websockets.connect(url) as ws:
                    subscribe_msg = {
                        "id": "test",
                        "type": "subscribe",
                        "topic": f"/market/ticker:{','.join(self.symbols)}",
                        "privateChannel": False,
                        "response": True
                    }
                    await ws.send(json.dumps(subscribe_msg))

                    last_ping = time.time()

                    while self._running:
                        if time.time() - last_ping > ping_interval:
                            ping_msg = {"id": "ping-id", "type": "ping"}
                            await ws.send(json.dumps(ping_msg))
                            last_ping = time.time()

                        message = await ws.recv()
                        data = json.loads(message)

                        if 'data' in data:
                            tick = {
                                'symbol': data['topic'].split(":")[-1],
                                'price': float(data['data']['price']),
                                'timestamp': datetime.utcnow().isoformat() + "Z"
                            }
                            self.callback(tick['symbol'], tick)
            except Exception as e:
                print(f"WS reconnect due to error: {e}")
                await asyncio.sleep(5)