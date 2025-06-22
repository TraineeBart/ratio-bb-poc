import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from typing import Any, List
import requests
from requests.exceptions import HTTPError, Timeout
from src.client.kucoin_client import _interval_to_seconds, KucoinClient

def test_interval_to_seconds_valid():
    assert _interval_to_seconds("5m") == 5 * 60
    assert _interval_to_seconds("1h") == 3600
    assert _interval_to_seconds("2d") == 2 * 86400

@pytest.mark.parametrize("interval", ["3x", "10s", "", "m5"])
def test_interval_to_seconds_invalid(interval):
    with pytest.raises(ValueError):
        _interval_to_seconds(interval)

class DummyResponse:
    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self._data = data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise HTTPError(f"HTTP {self.status_code}")

    def json(self) -> Any:
        return {"data": self._data}

def test_get_candles_success(monkeypatch):
    sample = [["1620000000", "1.0", "2.0", "0.5", "1.5", "100.0", "0"]]
    called = {}
    def fake_get(url, params=None, timeout=None):
        called['url'] = url
        called['params'] = params
        return DummyResponse(200, sample)

    monkeypatch.setattr(requests, "get", fake_get)

    client = KucoinClient()
    result: List[Any] = client.get_candles("THETA-USDT", "1m", 1620000000, limit=5)
    assert result == sample
    assert called['url'].endswith("/market/candles")
    assert called['params']['symbol'] == "THETA-USDT"
    assert 'granularity' in called['params']
    assert called['params']['startAt'] == 1620000000
    assert called['params']['limit'] == 5

@pytest.mark.parametrize("code", [404, 500])
def test_get_candles_http_error(monkeypatch, code):
    def fake_get(url, params=None, timeout=None):
        return DummyResponse(code, [])

    monkeypatch.setattr(requests, "get", fake_get)
    client = KucoinClient()
    with pytest.raises(HTTPError):
        client.get_candles("RATIO-USDT", "5m", 1620000000)

def test_get_candles_timeout(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        raise Timeout()

    monkeypatch.setattr(requests, "get", fake_get)
    client = KucoinClient()
    with pytest.raises(Timeout):
        client.get_candles("RATIO-USDT", "1h", 1620000000)