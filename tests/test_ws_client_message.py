# File: tests/test_ws_client_message.py

import os
import sys
import asyncio
import json
import pandas as pd
import pytest

test_price = 3.0

# Ensure src is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ws_client import WSClient

class DummyExec:
    def __init__(self):
        self.calls = []

    def simulate_order(self, price, amount):
        # record inputs
        self.calls.append((price, amount))
        # return dummy slip price and net amount
        return price + 1.0, amount - 0.5

class DummyKSM:
    @classmethod
    async def create(cls, loop, rest_client, on_message):
        # return object capturing on_message handler
        inst = cls()
        inst.on_message = on_message
        return inst

    async def subscribe(self, topic):
        pass

@pytest.fixture(autouse=True)
def setup_client(monkeypatch):
    # minimal config
    fake_cfg = {
        'kucoin_api_key':'key',
        'kucoin_api_secret':'secret',
        'kucoin_passphrase':'pass',
        'ema_span':3,
        'nk_threshold':0,
        'volume_filter':0,
        'tick_amount':2.0
    }
    # patch load_config, RestClient, and KSM
    monkeypatch.setattr('src.ws_client.load_config', lambda: fake_cfg)
    monkeypatch.setattr('src.ws_client.RestClient', lambda *args, **kwargs: None)
    monkeypatch.setattr('src.ws_client.KucoinSocketManager', DummyKSM)
    yield

@pytest.fixture
def client():
    # Instantiate WSClient and replace exec_mod
    cl = WSClient(symbols=['AAA'])
    cl.exec_mod = DummyExec()
    # Pre-fill tick_buffer so handle_tick sees two ticks
    cl.tick_buffer = pd.DataFrame([
        {'price':1.0, 'volume':2.0, 'nk':1},
        {'price':2.0, 'volume':2.0, 'nk':1},
    ])
    # Bypass EMA logic in strategy
    cl.strat.run = lambda: pd.DataFrame([{
        'price': test_price,
        'volume': cl.tick_buffer.iloc[-1]['volume'],
        'nk': 1,
        f'ema_{cl.ema_span}': 0
    }])
    return cl

def test_on_message_triggers_handle_tick_and_signal(client):
    # Simulate incoming ticker message
    msg = {
        'topic': '/market/ticker:AAA',
        'data': {'price': str(test_price)}
    }
    # Before _on_message, no simulate_order calls
    assert client.exec_mod.calls == []
    # Invoke the async message handler
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client._on_message(msg))
    # After handling, simulate_order should have been called once with correct args
    assert client.exec_mod.calls == [(test_price, 2.0)]
