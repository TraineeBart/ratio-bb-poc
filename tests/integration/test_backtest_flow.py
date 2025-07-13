import pytest
import csv
import json
import os
from pathlib import Path
import requests

import sys
sys.path.insert(0, os.getcwd())
from src.run_once import main as run_once_main

@ pytest.fixture(autouse=True)
def clean_tmp(monkeypatch):
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

@ pytest.fixture
def capture_webhook(monkeypatch):
    """
    Stub requests.post om webhook-calls te capteren.
    """
    calls = []
    def fake_post(*args, **kwargs):
        # capture URL and JSON payload regardless of extra kwargs (e.g., timeout)
        url = args[0] if args else kwargs.get('url')
        payload = kwargs.get('json')
        headers = kwargs.get('headers')
        calls.append({'url': url, 'json': payload, 'headers': headers})
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
        return FakeResponse()
    monkeypatch.setattr(requests, "post", fake_post)
    return calls


def test_e2e_backtest_flow(clean_tmp, capture_webhook, monkeypatch):
    """
    End-to-end backtest:
      1. Draai run_once.py met sample_ticks.json
      2. Vergelijk tmp/output.csv met acceptance/expected_backtest.csv
      3. Controleer webhook-payloads tegen acceptance/expected_webhook.json
    """
    project_root = Path(__file__).parent.parent
    # Sample ticks en golden files
    sample_ticks = project_root / "test_ticks.json"
    expected_csv = project_root / "acceptance" / "expected_backtest.csv"
    expected_webhook = project_root / "acceptance" / "expected_webhook.json"

    # 1) Run backtest in-process
    monkeypatch.setattr(sys, "argv", ["run_once.py", "--replay", str(sample_ticks)])
    run_once_main()

    # 2) CSV-validatie
    output_csv = project_root / "tmp" / "output.csv"
    assert output_csv.exists(), "output.csv ontbreekt"

    with open(output_csv, newline='') as f_out, open(expected_csv, newline='') as f_exp:
        reader_out = csv.reader(f_out)
        reader_exp = csv.reader(f_exp)
        rows_out = list(reader_out)
        rows_exp = list(reader_exp)
    assert rows_out == rows_exp, "Output CSV komt niet overeen met golden file"

    # 3) Webhook-validatie
    with open(expected_webhook) as f:
        expected_payloads = json.load(f)

    # Vergelijk alleen de JSON-payloads uit de gekapte calls met de golden file
    actual_payloads = [call['json'] for call in capture_webhook]
    assert actual_payloads == expected_payloads, \
        f"Webhook payloads matchen niet met golden file: {actual_payloads} vs {expected_payloads}"
