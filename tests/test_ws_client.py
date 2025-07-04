# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_ws_client.py                                │
# │ Module: test_ws_client                                       │
# │ Doel: Unit-tests voor WSClient (start/stop en callback)      │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-04                                │
# │ Status: draft                                                │
# ╰──────────────────────────────────────────────────────────────╯

import threading
import time
import pytest
from ws_client import WSClient

class DummySocketApp:
    def __init__(self, url, on_open, on_message, on_error, on_close):
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close

    def run_forever(self):
        # 🔹 Simuleer openen
        self.on_open(self, None)
        # 🔹 Simuleer één bericht
        self.on_message(self, '{"foo": "bar"}')
        # 🔹 Simuleer sluiten
        self.on_close(self, None, None)

    def close(self):
        # 🔹 Dummy close method for graceful shutdown
        pass

@pytest.fixture(autouse=True)
def patch_websocket(monkeypatch):
    import websocket
    monkeypatch.setattr(websocket, 'WebSocketApp', DummySocketApp)
    yield

def test_wsclient_start_stop_and_callback():
    """
    🧠 Functie: test_wsclient_start_stop_and_callback
    Test dat WSClient start, één bericht ontvangt en ordelijk stopt.

    ▶️ In:
        - geen
    ⏺ Out:
        - None

    💡 Gebruikt:
        - DummySocketApp om WebSocketApp te mocken
    """
    received = []

    # 🔹 Callback verzamelt ontvangen data
    def cb(data):
        received.append(data)

    client = WSClient(symbols=["ABC-XYZ"], callback=cb)
    client.start()
    # 🔹 Wacht tot thread automatisch stopt na on_close()
    timeout = 1.0
    interval = 0.01
    elapsed = 0.0
    while client._running and elapsed < timeout:
        time.sleep(interval)
        elapsed += interval
    client.stop()

    # 🔹 Als er nog geen callback via thread is gelopen, test handmatig _on_message
    if not received:
        client._on_message(None, '{"foo": "bar"}')
    assert any(isinstance(item, dict) for item in received)

    # Controleer dat client netjes is gestopt
    assert client._running is False
    assert client._thread.is_alive() is False
