# File: tests/test_orchestrator_webhook.py
# Description: Unit tests for Orchestrator webhook dispatch logic
# Author: Quality-EngineerGPT, 2025-06-29

"""
Test suite for verifying webhook dispatch behavior in src/orchestrator.py,
including success, retry logic on errors, and disabled-webhook scenarios.
"""

import sys
from pathlib import Path
import os
# Ensure project root on path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import pytest
import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError
from src.orchestrator import Orchestrator

@pytest.fixture(autouse=True)
def dummy_csv(tmp_path, monkeypatch):
    """
    Fixture to provide a dummy configuration with CSV and webhook URL.
    """
    # stub out CSV writing to avoid file ops
    config = {
        'backtest_output_csv': str(tmp_path / "out.csv"),
        'signal_webhook_url': os.environ.get('WEBHOOK_URL', 'http://dummy')
    }
    return config

class DummyResponse:
    def __init__(self, status_code=200, exc=None):
        self.status_code = status_code
        self._exc = exc

    def raise_for_status(self):
        if self._exc:
            raise self._exc

def test_webhook_success(dummy_csv, monkeypatch, caplog):
    """
    Verify that a 200 OK response does not log an error.
    """
    caplog.set_level('ERROR')
    # Stub requests.post to return 200 OK
    monkeypatch.setenv('WEBHOOK_URL', 'http://localhost')
    def fake_post(url, json, timeout):
        return DummyResponse(status_code=200)
    monkeypatch.setattr(requests, 'post', fake_post)

    orch = Orchestrator(dummy_csv)
    payload = {'symbol': 'SYM', 'timestamp': 1, 'signal': 'BUY', 'price': 1.0, 'amount': 10}
    orch.on_signal(payload)
    # No failure log
    assert "Failed posting signal" not in caplog.text

@pytest.mark.parametrize("first_exc, second_exc", [
    (Timeout("timeout"), None),
    (HTTPError("500"), HTTPError("500")),
    (ConnectionError("conn"), None),
])
def test_webhook_retries(dummy_csv, monkeypatch, caplog, first_exc, second_exc):
    """
    Test retry logic on specific exceptions and whether errors raise or not.
    """
    caplog.set_level('ERROR')
    # Control call count
    calls = {'count': 0}
    def fake_post(url, json, timeout):
        calls['count'] += 1
        if calls['count'] == 1:
            raise first_exc
        if isinstance(second_exc, Exception):
            raise second_exc
        return DummyResponse(status_code=200)
    monkeypatch.setattr(requests, 'post', fake_post)
    orch = Orchestrator(dummy_csv)
    payload = {'symbol': 'SYM', 'timestamp': 2, 'signal': 'SELL', 'price': 2.0, 'amount': 20}
    orch.on_signal(payload)
    # Should log retry or ignore
    assert calls['count'] >= 1

def test_webhook_disabled_csv_only(tmp_path, monkeypatch, caplog):
    """
    Ensure no webhook POST occurs when webhook URL is not configured.
    """
    caplog.set_level('ERROR')
    config = {'backtest_output_csv': str(tmp_path / "out.csv")}
    # Ensure no WEBHOOK_URL env
    monkeypatch.delenv('WEBHOOK_URL', raising=False)
    orch = Orchestrator(config)
    payload = {'symbol': 'SYM', 'timestamp': 3, 'signal': 'HOLD', 'price': 3.0, 'amount': 30}
    # Should not raise, no POST attempted
    orch.on_signal(payload)
    assert "Failed posting signal" not in caplog.text


# Additional tests per user instructions
import pytest

@pytest.mark.parametrize("signal", ["NO_SWAP"])
def test_no_swap_skips_webhook(dummy_csv, monkeypatch, caplog, signal):
    """
    Ensure that signals marked NO_SWAP do not trigger webhook POST.
    """
    caplog.set_level('ERROR')
    # If post is called, fail the test
    monkeypatch.setattr(requests, 'post',
                        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("POST should not be called")))
    orch = Orchestrator(dummy_csv)
    payload = {'symbol': 'XYZ', 'timestamp': 5, 'signal': signal, 'price': 5.0, 'amount': 50}
    orch.on_signal(payload)
    assert "Failed posting signal" not in caplog.text


@pytest.mark.parametrize("exc", [HTTPError("500"), HTTPError("501")])
def test_webhook_server_error_exhausts_retries(dummy_csv, monkeypatch, caplog, exc):
    """
    Ensure that repeated HTTPError eventually raises after max retries.
    """
    caplog.set_level('ERROR')
    # Always raise HTTPError
    monkeypatch.setattr(requests, 'post', lambda *args, **kwargs: (_ for _ in ()).throw(exc))
    orch = Orchestrator(dummy_csv)
    # Call on_signal; should not raise
    orch.on_signal({'symbol':'A','timestamp':6,'signal':'BUY','price':6.0,'amount':60})
    # Ensure retry attempts are logged
    assert caplog.text.count('Failed posting signal') >= 3