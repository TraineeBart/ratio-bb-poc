# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/ws_client.py                                       │
# │ Module: ws_client                                            │
# │ Doel: Live websocket client voor tick data                   │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-04                                │
# │ Status: stable                                               │
# ╰──────────────────────────────────────────────────────────────╯

import threading
import time
import json
from typing import List, Callable, Dict
from src.client.kucoin_client import get_bullet_public
import uuid
# 🔹 Support environments without websocket-client installed (e.g., CI)
try:
    import websocket
except ImportError:
    import types
    websocket = types.ModuleType("websocket")
    # provide dummy WebSocketApp to allow attribute access
    websocket.WebSocketApp = lambda *args, **kwargs: None
    import sys
    sys.modules['websocket'] = websocket

class WSClient:
    """
    WebSocket client for live tick data.
    """

    def __init__(self, symbols: List[str], callback: Callable[[Dict], None] = None):
        """
        🧠 Functie: __init__
        Initialiseer de WebSocket-client met symbolen en callback.

        ▶️ In:
            - self (WSClient): instantie
            - symbols (List[str]): lijst van tick-symbolen om te volgen
            - callback (Callable[[Dict], None]): functie die wordt aangeroepen met elke ontvangen tick
        ⏺ Out:
            - None

        💡 Gebruikt:
            - Initialisatie van interne variabelen
        """
        self.symbols = symbols
        # 🔹 Callback kan optioneel zijn; gebruik noop indien niet meegegeven
        self.callback = callback if callback is not None else lambda data: None
        self._ws = None
        self._thread = None
        self._running = False
        self.ws_url = "wss://ws-api.kucoin.com/endpoint"
        self.bullet_token = None

    def _on_message(self, ws, message):
        """
        🧠 Functie: _on_message
        Verwerk binnenkomende WebSocket-berichten.

        ▶️ In:
            - self (WSClient): instantie
            - ws: WebSocket object
            - message (str): ontvangen bericht in JSON-formaat
        ⏺ Out:
            - None

        💡 Gebruikt:
            - json.loads om bericht te parsen
            - callback functie voor verwerking
        """
        print(f"WSClient: Received raw message: {message}")
        try:
            data = json.loads(message)
            print(f"WSClient: Parsed message: {data}")
            self.callback(data)
        except Exception:
            # 🔹 Fout bij parsen of callback, negeren
            pass

    def _on_error(self, ws, error):
        """
        🧠 Functie: _on_error
        Afhandeling van WebSocket fouten.

        ▶️ In:
            - self (WSClient): instantie
            - ws: WebSocket object
            - error: foutobject of bericht
        ⏺ Out:
            - None

        💡 Gebruikt:
            - TODO: logging/error handling placeholder
        """
        # 🔹 TODO: logging/error handling
        pass

    def _on_close(self, ws, close_status_code, close_msg):
        """
        🧠 Functie: _on_close
        Afhandeling bij sluiten van WebSocket verbinding.

        ▶️ In:
            - self (WSClient): instantie
            - ws: WebSocket object
            - close_status_code: sluitingsstatuscode
            - close_msg: sluitingsbericht
        ⏺ Out:
            - None

        💡 Gebruikt:
            - Zet running flag uit
        """
        self._running = False

    def _on_open(self, ws):
        """
        🧠 Functie: _on_open
        Verzend subscribe-bericht bij openen van de WebSocket.

        ▶️ In:
            - self (WSClient): instantie
            - ws: WebSocket object
        ⏺ Out:
            - None

        💡 Gebruikt:
            - Versturen van subscribe bericht met symbolen
        """
        print("WSClient: Connected to WebSocket")
        # 🔹 Stuur subscribe-bericht voor tick data per symbol
        for symbol in self.symbols:
            topic = f"/market/ticker:{symbol}"
            subscribe_msg = {
                "id": int(time.time()),
                "type": "subscribe",
                "topic": topic,
                "privateChannel": False,
                "response": True
            }
            ws.send(json.dumps(subscribe_msg))
            print(f"WSClient: Sent subscribe for topic {topic}")

    def _run(self):
        """
        🧠 Functie: _run
        Hoofdloop met automatische reconnect van de WebSocket.

        ▶️ In:
            - self (WSClient): instantie
        ⏺ Out:
            - None

        💡 Gebruikt:
            - websocket.WebSocketApp voor verbinding
            - time.sleep voor retry delay
        """
        while self._running:
            # 🔹 Retrieve bullet-public token and endpoint for WebSocket
            try:
                token_data = get_bullet_public()
                endpoint = token_data["endpoint"]
                token = token_data["token"]
                # Append token and a unique connectId to the WebSocket URL
                connect_id = str(uuid.uuid4())
                self.ws_url = f"{endpoint}?token={token}&connectId={connect_id}"
                self.bullet_token = token
                print(f"WSClient: Using WebSocket URL: {self.ws_url}")
            except Exception as e:
                print(f"WSClient: Failed to fetch bullet-public token: {e}")
                raise
            try:
                self._ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close
                )
                self._ws.run_forever(
                    ping_interval=20,   # stuur elke 20s een ping
                    ping_timeout=10     # wacht maximaal 10s op een pong
                )
            except Exception:
                # 🔹 retry na 5 seconden
                time.sleep(5)

    def start(self):
        """
        🧠 Functie: start
        Start de WebSocket-client in een aparte thread.

        ▶️ In:
            - self (WSClient): instantie met configuratie voor symbols en callback
        ⏺ Out:
            - None

        💡 Gebruikt:
            - threading.Thread voor achtergrond-executie
        """
        # 🔹 Start alleen als niet al lopend
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """
        🧠 Functie: stop
        Stop de WebSocket-client.

        ▶️ In:
            - self (WSClient): instantie
        ⏺ Out:
            - None

        💡 Gebruikt:
            - Sluit WebSocket verbinding en wacht op thread beëindiging
        """
        self._running = False
        if self._ws:
            self._ws.close()
        if self._thread:
            self._thread.join()