# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_market_api.py                               │
# │ Module: test_market_api                                      │
# │ Doel: Test voor fetch_recent_trades uit market_api           │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-05                                │
# │ Status: draft                                                │
# ╰──────────────────────────────────────────────────────────────╯
import pytest
from datetime import datetime, timedelta
from src.utils.market_api import fetch_recent_trades

class DummyResp:
    def __init__(self, data):
        self._data = data
        self.status_code = 200
    def raise_for_status(self):
        pass
    def json(self):
        return {"data": self._data}

def test_fetch_recent_trades_filters_and_converts(monkeypatch):
    """
    🧠 Functie: test_fetch_recent_trades_filters_and_converts
    Test dat fetch_recent_trades alleen ticks na 'since' retourneert en juiste types converteert.

    ▶️ In:
        - symbol (str): symbool dat wordt doorgegeven aan de API
        - since (datetime): timestamp waarvanaf trades worden gefilterd
    ⏺ Out:
        - List[dict]: ieder dict heeft keys 'timestamp' (datetime), 'price' (float), 'volume' (float)

    💡 Gebruikt:
        - src.utils.market_api.fetch_recent_trades
    """
    # Stel een 'since' tijdstip in op nu minus 2 seconden
    now = datetime.utcnow()
    since = now - timedelta(seconds=2)

    # Maak dummy entries: één net vóór since, één erna
    # time in API is nanoseconds since epoch
    ts_before = int((since - timedelta(milliseconds=1)).timestamp() * 1e9)
    ts_after  = int((since + timedelta(milliseconds=1)).timestamp() * 1e9)
    dummy_data = [
        {"time": str(ts_before), "price": "10.5", "size": "100"},
        {"time": str(ts_after),  "price": "20.25", "size": "50.5"},
    ]

    # Mock requests.get
    def fake_get(*args, **kwargs):
        params = kwargs.get("params", {})
        assert "symbol" in params
        return DummyResp(dummy_data)
    monkeypatch.setattr("src.utils.market_api.requests.get", fake_get)

    ticks = fetch_recent_trades("FOO-BAR", since)

    # We verwachten precies één tick (de tweede)
    assert len(ticks) == 1
    tick = ticks[0]

    # Timestamp moet een datetime na 'since' zijn
    assert isinstance(tick["timestamp"], datetime)
    assert tick["timestamp"] > since

    # Price en volume als floats
    assert tick["price"] == 20.25
    assert tick["volume"] == 50.5