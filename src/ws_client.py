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

    def __init__(self, symbols: List[str], callback: Callable[[Dict], None]):
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
        self.callback = callback
        self._ws = None
        self._thread = None
        self._running = False
        self.ws_url = "wss://ws.kucoin.com/endpoint"

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
        try:
            data = json.loads(message)
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
        # 🔹 Stuur subscribe-bericht voor alle symbols
        subscribe_msg = {
            "type": "subscribe",
            "symbols": self.symbols
        }
        ws.send(json.dumps(subscribe_msg))

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
            try:
                self._ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close
                )
                self._ws.run_forever()
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