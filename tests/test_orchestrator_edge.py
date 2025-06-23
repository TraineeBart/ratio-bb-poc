# File: tests/test_orchestrator_edge.py
import os
import csv
import pytest
import requests
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.orchestrator import Orchestrator

# Reuse fixtures from existing tests
@pytest.fixture(autouse=True)
def isolate_tmp(monkeypatch, tmp_path):
    # Redirect backtest_output_csv to tmp directory
    monkeypatch.setenv('WEBHOOK_URL', 'https://env-hook')
    yield tmp_path


def test_on_signal_env_priority(monkeypatch, tmp_path, capsys):
    # env WEBHOOK_URL should take precedence over config
    monkeypatch.setenv('WEBHOOK_URL', 'https://env-priority')
    cfg = {'signal_webhook_url': 'https://cfg-hook', 'backtest_output_csv': str(tmp_path / 'out.csv')}
    orch = Orchestrator(config=cfg)

    calls = []
    def fake_post(url, json=None, timeout=None):
        calls.append(url)
        class R: 
            def raise_for_status(self): pass
        return R()
    monkeypatch.setattr(requests, 'post', fake_post)

    # Trigger on_signal
    payload = {'symbol': 'X','timestamp': 'ts','price': 1,'signal': 'BUY'}
    orch.on_signal(payload)

    # CSV created with header and row
    csv_file = cfg['backtest_output_csv']
    with open(csv_file, newline='') as f:
        rows = list(csv.DictReader(f))
    assert rows and rows[0]['signal'] == 'BUY'

    # POST should use env URL
    assert calls == ['https://env-priority']


def test_on_signal_cfg_fallback(monkeypatch, tmp_path):
    # remove env
    monkeypatch.delenv('WEBHOOK_URL', raising=False)
    # fallback to config
    cfg = {'signal_webhook_url': 'https://cfg-only', 'backtest_output_csv': str(tmp_path / 'out2.csv')}
    orch = Orchestrator(config=cfg)
    calls = []
    def fake_post(url, json=None, timeout=None):
        calls.append(url)
        class R:
            def raise_for_status(self): pass
        return R()
    monkeypatch.setattr(requests, 'post', fake_post)
    payload = {'symbol':'Y','timestamp':'t2','price':2,'signal':'SELL'}
    orch.on_signal(payload)
    # POST to cfg
    assert calls == ['https://cfg-only']


def test_directory_creation(monkeypatch, tmp_path):
    monkeypatch.delenv('WEBHOOK_URL', raising=False)
    # provide nested dir
    out = tmp_path / 'nested' / 'dir' / 'file.csv'
    cfg = {'signal_webhook_url': 'https://h','backtest_output_csv': str(out)}
    orch = Orchestrator(config=cfg)
    calls = []
    monkeypatch.setattr(requests, 'post', lambda url, json=None, timeout=None: type('R', (), {'raise_for_status': lambda self: None})())
    payload = {'symbol':'Z','timestamp':'ts3','price':3,'signal':'HOLD'}
    orch.on_signal(payload)
    # ensure parent dirs created
    assert out.parent.exists()
    # file exists
    assert out.exists()
