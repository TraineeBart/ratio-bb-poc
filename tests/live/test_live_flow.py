import os
import pandas as pd
import sys
from src.run_once import run_once_main
from src.ws_client import DummyWSClient
from tests.helpers import WebhookHandler
import requests



def test_basic_live_flow_smoke(monkeypatch, tmp_path, http_server):
    WebhookHandler.calls.clear()
    monkeypatch.setattr("src.run_once.requests.post", WebhookHandler.record)

    monkeypatch.setenv("MODE", "live")
    monkeypatch.setenv("WEBHOOK_URL", http_server)
    monkeypatch.setenv("CANDLE_PERIOD", "1T")
    monkeypatch.setenv("CSV_PATH", str(tmp_path / "output.csv"))
    monkeypatch.setattr("src.run_once.start_health_server", lambda port=8000: None)
    monkeypatch.setattr(
        "src.run_once.WSClient",
        lambda symbols, cb: DummyWSClient(symbols, cb, max_ticks=5, interval=1)
    )

    run_once_main(max_ticks=5)

    df = pd.read_csv(tmp_path / "output.csv")
    assert len(df) == 6  # 1 dummy + 5 actual ticks
    assert df['price'].isna().sum() == 1  # The dummy row has NaN price
    assert set(df.columns) >= {"timestamp", "symbol", "price", "signal"}

    assert len(WebhookHandler.calls) == 5
    for call in WebhookHandler.calls:
        assert all(k in call for k in ["timestamp", "symbol", "price", "signal"])