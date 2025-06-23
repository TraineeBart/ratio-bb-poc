# File: tests/test_ws_client_run.py

import os
import sys
import asyncio
import pytest

# Ensure src is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ws_client import WSClient

class DummyKSM:
    last = None

    def __init__(self, loop, rest_client, on_message):
        # record init args
        self.loop = loop
        self.rest_client = rest_client
        self.on_message = on_message
        self.subscribed = []

    @classmethod
    async def create(cls, loop, rest_client, on_message):
        # simulate creation and capture instance
        instance = cls(loop, rest_client, on_message)
        cls.last = instance
        return instance

    async def subscribe(self, topic):
        # record topic
        self.subscribed.append(topic)
        # once subscribed to all symbols, raise CancelledError to exit
        if len(self.subscribed) >= len(self.loop.symbols):
            raise asyncio.CancelledError()
        return

@pytest.fixture(autouse=True)
def setup_client(monkeypatch):
    # minimal config
    fake_cfg = {
        'kucoin_api_key': 'key',
        'kucoin_api_secret': 'secret',
        'kucoin_passphrase': 'pass',
        'ema_span': 9,
        'nk_threshold': 0,
        'volume_filter': 0,
        'tick_amount': 1.0
    }
    # patch load_config
    monkeypatch.setattr('src.ws_client.load_config', lambda: fake_cfg)
    # patch RestClient
    monkeypatch.setattr('src.ws_client.RestClient', lambda *args, **kwargs: None)
    # patch KucoinSocketManager to DummyKSM
    monkeypatch.setattr('src.ws_client.KucoinSocketManager', DummyKSM)
    yield

@pytest.fixture
def client_symbols():
    return ["AAA-USDT", "BBB-USDT"]

def test_run_subscribes_to_all_symbols(client_symbols):
    # Create client with two symbols
    client = WSClient(symbols=client_symbols)
    # Use local loop and attach symbols list
    loop = asyncio.get_event_loop()
    loop.symbols = client_symbols

    # Running _run_async should subscribe to each symbol and then cancel
    with pytest.raises(asyncio.CancelledError):
        loop.run_until_complete(client._run_async())

    # After cancellation, DummyKSM.last holds the instance
    ksm = DummyKSM.last
    expected_topics = [f"/market/ticker:{sym}" for sym in client_symbols]
    assert ksm.subscribed == expected_topics
