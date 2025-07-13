import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from typing import Any, List
import requests
from requests.exceptions import HTTPError, Timeout
from src.client.kucoin_client import _interval_to_seconds, KucoinClient, KucoinClientError

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
    with pytest.raises(KucoinClientError):
        client.get_candles("RATIO-USDT", "1h", 1620000000)

# --- Retry logic tests for KucoinClient ---
import logging
import pytest
from requests.exceptions import RequestException, HTTPError
from src.client.kucoin_client import KucoinClient, KucoinClientError

# Dummy response to simulate successful API calls
def _dummy_success_response():
    class Resp:
        def raise_for_status(self):
            pass
        def json(self):
            return {"success": True}
    return Resp()

def _make_http_error(status):
    class FakeResponse:
        def __init__(self):
            self.status_code = status
    return HTTPError(f"HTTP {status}", response=FakeResponse())

@pytest.fixture
def retry_client():
    return KucoinClient(api_key="test", api_secret="test")

@pytest.mark.parametrize("rate_limit_exceptions", [1, 2])
def test_retry_on_http_429(monkeypatch, caplog, retry_client, rate_limit_exceptions):
    """
    Simuleer opeenvolgende RateLimitError (HTTP 429) gevolgd door succes.
    Assert dat na retries de call slaagt en log 'Retrying after rate limit'.
    """
    calls = {"count": 0}

    def fake_request(*args, **kwargs):
        if calls["count"] < rate_limit_exceptions:
            calls["count"] += 1
            raise _make_http_error(429)
        return _dummy_success_response()

    monkeypatch.setattr(requests, "get", fake_request)
    caplog.set_level(logging.INFO)

    result = retry_client.get_candles("THETA-USDT", "1m", 1620000000)
    assert result == []
    assert calls["count"] == rate_limit_exceptions
    assert "Rate limit hit" in caplog.text

@pytest.mark.parametrize("network_exceptions", [1, 2])
def test_retry_on_network_error(monkeypatch, caplog, retry_client, network_exceptions):
    """
    Simuleer opeenvolgende RequestException gevolgd door succes.
    Assert back-off en log 'Retrying after network error'.
    """
    calls = {"count": 0}

    def fake_request(*args, **kwargs):
        if calls["count"] < network_exceptions:
            calls["count"] += 1
            raise RequestException("Network failure")
        return _dummy_success_response()

    monkeypatch.setattr(requests, "get", fake_request)
    caplog.set_level(logging.INFO)

    result = retry_client.get_candles("THETA-USDT", "1m", 1620000000)
    assert result == []
    assert calls["count"] == network_exceptions
    assert "Network error, retrying" in caplog.text

def test_max_retries_exceeded_raises(monkeypatch, retry_client):
    """
    Simuleer altijd fout (HTTP 500 enz.). Na max retries moet HTTPError komen.
    """
    def always_fail(*args, **kwargs):
        raise _make_http_error(500)

    monkeypatch.setattr(requests, "get", always_fail)
    with pytest.raises(HTTPError):
        retry_client.get_candles("THETA-USDT", "1m", 1620000000)