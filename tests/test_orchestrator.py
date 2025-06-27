import pytest
import os, sys
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator import Orchestrator

class DummyWS:
    def __init__(self, config):
        self.callback = None
    def set_signal_callback(self, cb):
        self.callback = cb
    def run_forever(self):
        # simulate two signals
        for sig in [
            {"timestamp":"t1","symbol":"A","price":1,"signal":"BUY"},
            {"timestamp":"t2","symbol":"B","price":2,"signal":"SELL"}
        ]:
            self.callback(sig)

@pytest.fixture(autouse=True)
def isolate_fs(tmp_path, monkeypatch):
    # Change working dir to tmp_path
    monkeypatch.chdir(tmp_path)
    # Patch WSClient in orchestrator to use DummyWS
    import src.orchestrator as orchestrator
    monkeypatch.setattr(orchestrator, "WSClient", DummyWS)
    yield

def test_run_live_writes_and_posts(monkeypatch, tmp_path):
    # Stub WEBHOOK_URL env var
    webhook_calls = []
    monkeypatch.setenv("WEBHOOK_URL", "https://example.com/hook")
    # Mock requests.post to capture calls
    import requests
    class DummyResponse:
        def __init__(self, status_code=200):
            self.status_code = status_code
        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(f"Status {self.status_code}")
    def fake_post(url, json=None, timeout=None):
        webhook_calls.append((url, json))
        return DummyResponse(200)
    monkeypatch.setattr(requests, "post", fake_post)

    orch = Orchestrator(config={})
    orch.run_live()

    # CSV should have two rows
    csv_file = tmp_path / "tmp" / "output.csv"
    assert csv_file.exists()
    with open(csv_file, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["symbol"] == "A"
    assert rows[1]["symbol"] == "B"

    # Webhook was called twice
    assert len(webhook_calls) == 2
    assert webhook_calls[0][0] == "https://example.com/hook"
