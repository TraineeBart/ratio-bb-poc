import os
import sys
import json
import csv
import pytest
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, os.getcwd())
from src.run_once import main as run_once_main

@pytest.fixture(autouse=True)
def clean_tmp():
    """
    Maak de tmp-map schoon voor elke test.
    """
    tmp_dir = Path(os.getcwd()) / "tmp"
    if tmp_dir.exists():
        for f in tmp_dir.iterdir():
            if f.is_file():
                f.unlink()
    else:
        tmp_dir.mkdir()
    yield

@pytest.fixture
def capture_webhook(monkeypatch):
    """
    Stub requests.post om webhook-calls te capteren.
    """
    calls = []
    import requests
    def fake_post(*args, **kwargs):
        # capture only JSON payloads
        payload = kwargs.get('json')
        calls.append(payload)
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
        return FakeResponse()
    # Override webhook URL
    monkeypatch.setenv('WEBHOOK_URL', 'http://localhost:9000')
    monkeypatch.setattr(requests, 'post', fake_post)
    return calls

@pytest.fixture
def stub_ws_client(monkeypatch):
    """
    Stub WSClient to emit ticks from test_ticks.json for live mode.
    """
    sample_ticks_path = Path(os.getcwd()) / 'test_ticks.json'
    sample_ticks = json.load(open(sample_ticks_path))
    import src.ws_client as ws_module
    class DummyWSClient:
        def __init__(self, url, callback):
            self.callback = callback
        def start(self):
            for tick in sample_ticks:
                self.callback(tick)
        def stop(self):
            pass
    # Force live mode (no --replay)
    monkeypatch.setenv('MODE', 'live')
    monkeypatch.setattr(ws_module, 'WSClient', DummyWSClient)

def test_full_backtest_flow(clean_tmp, capture_webhook, stub_ws_client, monkeypatch):
    """
    End-to-end full backtest (live mode):
      1. Run run_once without --replay
      2. Validate CSV against golden file
      3. Validate webhook payloads
    """
    # 1) Run backtest in-process (live mode)
    monkeypatch.setattr(sys, 'argv', ['run_once.py'])
    run_once_main()

    project_root = Path(os.getcwd())
    # 2) CSV-validatie
    output_csv = project_root / 'tmp' / 'output.csv'
    expected_csv = project_root / 'acceptance' / 'expected_full_backtest.csv'
    assert output_csv.exists(), 'output.csv ontbreekt'
    with open(output_csv, newline='') as f_out, open(expected_csv, newline='') as f_exp:
        rows_out = list(csv.reader(f_out))
        rows_exp = list(csv.reader(f_exp))
    assert rows_out == rows_exp, 'Output CSV komt niet overeen met golden file'

    # 3) Webhook-validatie
    expected_webhook = project_root / 'acceptance' / 'expected_full_webhook.json'
    expected_payloads = json.load(open(expected_webhook))
    assert capture_webhook == expected_payloads, \
        f"Webhook payloads matchen niet: {capture_webhook} vs {expected_payloads}"