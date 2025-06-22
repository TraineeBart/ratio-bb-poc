import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import time
from typing import Dict, Any
from src.ws_client import WSClient

class DummyWSClient(WSClient):
    def __init__(self):
        # Call parent without real connection args
        super().__init__({})
    def simulate_signal(self, symbol: str, signal: str, price: float, amount: float):
        # Directly call the internal emit method
        self._emit_signal(symbol, signal, price, amount)

def test_signal_callback_called(monkeypatch):
    # Freeze time for predictable timestamp
    monkeypatch.setattr(time, "time", lambda: 1620000000)
    received: Dict[str, Any] = {}

    def fake_callback(payload: Dict[str, Any]) -> None:
        received.update(payload)

    client = DummyWSClient()
    client.set_signal_callback(fake_callback)
    client.simulate_signal("THETA-USDT", "BUY", 1.23, 100)

    assert received == {
        "symbol": "THETA-USDT",
        "timestamp": 1620000000,
        "signal": "BUY",
        "price": 1.23,
        "amount": 100
    }

def test_no_callback_registered(monkeypatch):
    # Ensure no errors if callback is not set
    client = DummyWSClient()
    # Should not raise
    client.simulate_signal("RATIO-USDT", "SELL", 2.34, 50)

def test_callback_overwritten(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1620000100)
    calls = []

    def first_cb(payload: Dict[str, Any]) -> None:
        calls.append(("first", payload.copy()))

    def second_cb(payload: Dict[str, Any]) -> None:
        calls.append(("second", payload.copy()))

    client = DummyWSClient()
    client.set_signal_callback(first_cb)
    client.set_signal_callback(second_cb)
    client.simulate_signal("THETA-USDT", "HOLD", 3.45, 10)

    # Only second callback should be called
    assert len(calls) == 1
    tag, payload = calls[0]
    assert tag == "second"
    assert payload["signal"] == "HOLD"
    assert payload["price"] == 3.45
    assert payload["amount"] == 10
    assert payload["timestamp"] == 1620000100
