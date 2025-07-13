import os
import csv
import tempfile
import requests
import json
import pytest

# Zorg dat main.py geïmporteerd kan worden
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

from main import on_signal

class DummyResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"Status {self.status_code}")

@pytest.fixture(autouse=True)
def isolate_fs(tmp_path, monkeypatch):
    # Gebruik een tmp dir voor tmp/ en logs/
    monkeypatch.chdir(tmp_path)
    yield

def test_on_signal_writes_csv_and_posts(monkeypatch, tmp_path):
    # Stub webhook URL env
    webhook_url = "https://example.com/hook"
    monkeypatch.setenv("WEBHOOK_URL", webhook_url)

    # Mock requests.post
    calls = []
    def fake_post(url, json=None, timeout=None):
        calls.append((url, json))
        return DummyResponse(200)
    monkeypatch.setattr(requests, "post", fake_post)

    payload = {
        "symbol": "THETA-USDT",
        "price": 2.34,
        "signal": "BUY"
    }

    # Call handler
    on_signal(payload.copy())

    # Verify CSV
    csv_file = tmp_path / "tmp" / "output.csv"
    assert csv_file.exists()
    with open(csv_file, newline="") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 1
    row = reader[0]
    assert row["symbol"] == "THETA-USDT"
    assert float(row["price"]) == 2.34
    assert row["signal"] == "BUY"
    assert "timestamp" in row and row["timestamp"].endswith("Z") is False  # ISO format

    # Verify webhook log
    log_file = tmp_path / "logs" / "webhook.log"
    assert log_file.exists()
    with open(log_file) as f:
        log_content = f.read()
    assert "POST" in log_content

    # Verify requests.post was called once
    assert len(calls) == 1
    assert calls[0][0] == webhook_url
    assert calls[0][1]["symbol"] == "THETA-USDT"