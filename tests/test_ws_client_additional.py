# File: tests/test_ws_client_additional.py
import os
import sys
import pandas as pd
import pytest

# Ensure src package is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ws_client import WSClient

class DummyExec:
    def simulate_order(self, price, amount):
        return price + 0.5, amount - 0.1

@pytest.fixture(autouse=True)
def setup_clients(monkeypatch):
    # Monkeypatch load_config to return minimal config
    fake_cfg = {
        'kucoin_api_key': 'key',
        'kucoin_api_secret': 'secret',
        'kucoin_passphrase': 'pass',
        'ema_span': 9,
        'nk_threshold': 0,
        'volume_filter': 0,
        'tick_amount': 1.0
    }
    monkeypatch.setattr('src.ws_client.load_config', lambda: fake_cfg)
    # Monkeypatch RestClient and KucoinSocketManager
    monkeypatch.setattr('src.ws_client.RestClient', lambda *args, **kwargs: None)
    class DummyKSM:
        @staticmethod
        async def create(loop, rest_client, on_message):
            return DummyKSM()
        async def subscribe(self, topic):
            pass
    monkeypatch.setattr('src.ws_client.KucoinSocketManager', DummyKSM)
    yield

@pytest.fixture
def client(monkeypatch):
    # Instantiate client and replace exec_mod
    cl = WSClient(symbols=["SYM"])
    cl.exec_mod = DummyExec()
    return cl

def test_no_callback_does_not_raise(client):
    client.set_signal_callback(None)
    # Monkeypatch strategy.run to return empty DataFrame
    client.strat.run = lambda: pd.DataFrame()
    # Should not raise when handling tick
    client.handle_tick("SYM", 10.0)

@pytest.mark.parametrize("signal_type, price_above", [
    ("BUY", True),
    ("SELL", False),
])
def test_signal_callback_called(client, signal_type, price_above):
    last_price = 10.0
    ema_col = f"ema_{client.ema_span}"
    # Create DataFrame simulating a signal
    df = pd.DataFrame([{ "price": last_price, ema_col: (last_price - 1) if signal_type=="BUY" else (last_price + 1) }])
    client.strat.run = lambda: df

    received = {}
    def callback(payload):
        received.update(payload)

    client.set_signal_callback(callback)
    client.handle_tick("SYM", last_price)

    assert received["symbol"] == "SYM"
    assert received["signal"] == signal_type
    assert isinstance(received["timestamp"], int)
    assert received["price"] == last_price
    assert received["amount"] == pytest.approx(client.tick_amount - 0.1)

def test_callback_exception_propagates(client):
    last_price = 10.0
    ema_col = f"ema_{client.ema_span}"
    df = pd.DataFrame([{ "price": last_price, ema_col: last_price - 1 }])
    client.strat.run = lambda: df

    def bad_callback(payload):
        raise RuntimeError("callback error")

    client.set_signal_callback(bad_callback)
    with pytest.raises(RuntimeError):
        client.handle_tick("SYM", last_price)
