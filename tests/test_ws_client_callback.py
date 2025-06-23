

# File: tests/test_ws_client_callback.py

import sys
import os
import time
import asyncio
import pandas as pd
import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ws_client import WSClient

class DummyStrategy:
    def __init__(self, df):
        self._df = df

    def run(self):
        return self._df

@pytest.fixture(autouse=True)
def patch_time(monkeypatch):
    # Freeze time for predictable timestamp
    monkeypatch.setattr(time, 'time', lambda: 1620000000)
    yield

def test_emit_signal_direct(monkeypatch):
    client = WSClient(symbols=["SYM"])
    received = {}
    def cb(payload):
        received.update(payload)

    client.set_signal_callback(cb)
    # Directly call emit
    client._emit_signal("SYM", "BUY", 1.23, 4.56)

    assert received["symbol"] == "SYM"
    assert received["signal"] == "BUY"
    assert received["price"] == 1.23
    assert received["amount"] == 4.56
    # timestamp from patched time.time()
    assert isinstance(received["timestamp"], int)
    assert received["timestamp"] == 1620000000

@pytest.mark.parametrize("last_price, last_ema, expected_signal", [
    (10.0, 9.0, "BUY"),
    (10.0, 11.0, "SELL"),
    (10.0, 10.0, "HOLD"),
])
def test_handle_tick_signals(monkeypatch, last_price, last_ema, expected_signal):
    # Create a DataFrame row with price and ema
    df = pd.DataFrame([{"price": last_price, f"ema_9": last_ema, "volume": 100, "nk": 1}])
    client = WSClient(symbols=["SYM"])
    client.ema_span = 9
    client.strat = DummyStrategy(df)
    # Stub execution module to avoid missing simulate_order
    class DummyExec:
        def simulate_order(self, price, amount):
            return price, amount
    client.exec_mod = DummyExec()

    received = {}
    client.set_signal_callback(lambda p: received.update(p))
    client.handle_tick("SYM", last_price)

    assert received["signal"] == expected_signal
    assert received["symbol"] == "SYM"
    assert received["price"] == last_price
    # amount should be set to client.tick_amount if HOLD, or result of simulate_order for BUY/SELL
    assert "amount" in received

@pytest.mark.asyncio
async def test_on_message_triggers_callback(monkeypatch):
    # Prepare client and stub handle_tick
    client = WSClient(symbols=["SYM"])
    calls = []
    monkeypatch.setattr(client, "handle_tick", lambda sym, price: calls.append((sym, price)))

    # Register a callback to capture final payload
    payloads = []
    def cb(p):
        payloads.append(p)
    client.set_signal_callback(cb)

    # Prepare a fake message
    msg = {"topic": "/market/ticker:SYM", "data": {"price": "7.5"}}

    # Invoke the async message handler
    await client._on_message(msg)

    # handle_tick should have been called
    assert calls == [("SYM", 7.5)]
    # and callback should be called via emit inside handle_tick or _on_message
    assert payloads, "Callback was not invoked"