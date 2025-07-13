import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import requests
from requests.exceptions import HTTPError, Timeout
import pandas as pd

from src.kucoin_fetcher import fetch_klines
from src.client.kucoin_client import KucoinClientError


# Fixtures for mock API responses
@pytest.fixture
def sample_success_response():
    # Standard successful response with 3 candles (timestamp in ms and price strings)
    return {
        "data": [
            ["1622505600000", "100.0", "110.0", "90.0", "105.0", "1000.0", "0.0"],
            ["1622505660000", "105.0", "115.0", "95.0", "110.0", "1500.5", "0.0"],
            ["1622505720000", "110.0", "120.0", "100.0", "115.0", "2000.75", "0.0"],
        ]
    }

@pytest.fixture
def sample_empty_response():
    # Empty data list
    return {"data": []}


# --- Successful fetch tests ---

def test_fetch_klines_structure_and_types(monkeypatch, sample_success_response):
    """
    Verify DataFrame has correct columns, types, and sample values for a standard response.
    """
    captured = {}
    
    def mock_get(url, params=None, timeout=None):
        # Capture request parameters
        captured['url'] = url
        captured['params'] = params
        class MockResponse:
            status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return sample_success_response
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)

    df = fetch_klines(symbol="THETA-USDT", interval="1m", start_ts=1622505600000, limit=3)

    # Columns and order
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]

    # Data types
    assert pd.api.types.is_integer_dtype(df['time'])
    for col in ["open", "high", "low", "close", "volume"]:
        assert pd.api.types.is_float_dtype(df[col])

    # Sample value integrity
    assert df.loc[0, 'time'] == 1622505600000
    assert pytest.approx(df.loc[1, 'close']) == 110.0

    # Verify URL parameters mapping
    assert captured['params']['symbol'] == "THETA-USDT"
    assert captured['params']['granularity'] == 60  # 1m -> 60s
    assert captured['params']['startAt'] == 1622505600000
    assert captured['params']['limit'] == 3


def test_empty_response_returns_empty_df(monkeypatch, sample_empty_response):
    """
    When API returns an empty 'data' list, expect an empty DataFrame with correct columns.
    """
    def mock_get(url, params=None, timeout=None):
        class MockResponse:
            status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return sample_empty_response
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    df = fetch_klines("TFUEL-USDT", "1h", 1622505600000, limit=10)

    assert df.empty
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]


def test_missing_data_key_returns_empty_df(monkeypatch):
    """
    Simulate a 200-response missing the 'data' key: expect empty DataFrame.
    """
    def mock_get(url, params=None, timeout=None):
        class MockResponse:
            status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return {}  # no 'data' key
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    df = fetch_klines("THETA-USDT", "1m", 1622505600000)
    assert df.empty
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]


# --- Error handling tests ---

@pytest.mark.parametrize("status_code", [404, 500])
def test_http_error_status_raises(monkeypatch, status_code):
    """
    HTTP 4xx and 5xx status codes should raise HTTPError via raise_for_status().
    """
    def mock_get(url, params=None, timeout=None):
        sc = status_code
        class MockResponse:
            status_code = sc
            def raise_for_status(self):
                raise HTTPError(f"HTTP {sc}")
            def json(self):
                return {}
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    with pytest.raises(HTTPError):
        fetch_klines("TFUEL-USDT", "1h", 1622505600000)


def test_timeout_exception_propagates(monkeypatch):
    """
    Simulate a Timeout exception from requests.get and ensure it's propagated.
    """
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: (_ for _ in ()).throw(Timeout()))
    with pytest.raises(KucoinClientError):
        fetch_klines("THETA-USDT", "1m", 1622505600000)


# --- Parameterization tests ---

@pytest.mark.parametrize(
    "interval,expected_granularity",
    [
        ("1m", 60),
        ("5m", 300),
        ("1h", 3600),
        ("1d", 86400),
    ]
)
def test_parametrized_intervals(monkeypatch, sample_success_response, interval, expected_granularity):
    """
    Test that different interval strings map to correct granularity seconds in request params.
    """
    captured = {}

    def mock_get(url, params=None, timeout=None):
        captured['params'] = params
        class MockResponse:
            status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return sample_success_response
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    fetch_klines("TFUEL-USDT", interval, 1622505600000, limit=123)

    assert captured['params']['granularity'] == expected_granularity
    assert captured['params']['symbol'] == "TFUEL-USDT"
    assert captured['params']['startAt'] == 1622505600000
    assert captured['params']['limit'] == 123
