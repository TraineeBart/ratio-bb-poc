import pytest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.kucoin_fetcher import fetch_klines
from src.client.kucoin_client import KucoinClient

class DummyClient:
    def __init__(self, data):
        self.data = data
    def get_candles(self, symbol, interval, start_ts, limit):
        return self.data

@pytest.fixture(autouse=True)
def patch_client(monkeypatch):
    sample = [
        ["1620000000", "1.0", "2.0", "0.5", "1.5", "100.0", "0"]
    ]
    monkeypatch.setattr(KucoinClient, "get_candles", lambda self, *args, **kwargs: sample)

def test_fetch_klines_returns_dataframe():
    df = fetch_klines("SYMBOL", "1m", 1620000000, limit=1)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]
    assert df.loc[0, "close"] == 1.5