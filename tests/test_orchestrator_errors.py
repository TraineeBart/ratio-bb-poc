import os
import csv
import logging
import pytest
import requests
import sys

# Zorg dat src/ op de Python-path staat
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator import Orchestrator

class DummyWS:
    def __init__(self, config):
        self.callback = None
    def set_signal_callback(self, cb):
        self.callback = cb
    def run_forever(self):
        pass

@pytest.fixture(autouse=True)
def isolate_fs(monkeypatch, tmp_path):
    # Werk in een tijdelijke directory
    monkeypatch.chdir(tmp_path)
    # Patch WSClient zodat run_live niet blokkeert
    import src.orchestrator as orch_mod
    monkeypatch.setattr(orch_mod, 'WSClient', DummyWS)
    yield

def test_on_signal_http_error_logs(monkeypatch, caplog):
    caplog.set_level(logging.ERROR)
    # Stel env-variabele in
    monkeypatch.setenv('WEBHOOK_URL', 'https://example.com/hook')

    # Forceer een HTTPError bij post
    def fake_post(url, json=None, timeout=None):
        resp = type('R', (), {
            'raise_for_status': lambda self: (_ for _ in ()).throw(requests.HTTPError('fail'))
        })()
        return resp
    monkeypatch.setattr(requests, 'post', fake_post)

    orch = Orchestrator(config={})
    payload = {'symbol':'X','timestamp':'t','signal':'BUY','price':1,'amount':1}
    orch.on_signal(payload)

    # Controleer dat een ERROR-log is gemaakt
    assert any('Failed posting signal to webhook' in rec.message for rec in caplog.records)

def test_on_signal_config_fallback(monkeypatch):
    # Verwijder env-variabele
    monkeypatch.delenv('WEBHOOK_URL', raising=False)
    # Config bevat fallback URL en custom CSV-pad
    cfg = {'signal_webhook_url':'https://cfg-hook','backtest_output_csv':'custom.csv'}
    orch = Orchestrator(config=cfg)

    calls = []
    # Mock post zodat we de url en payload vastleggen
    def fake_post(url, json=None, timeout=None):
        calls.append((url,json))
        return type('R', (), {'raise_for_status': lambda self: None})()
    monkeypatch.setattr(requests, 'post', fake_post)

    payload = {'symbol':'Y','timestamp':'t2','signal':'SELL','price':2,'amount':2}
    orch.on_signal(payload)

    # Controleer dat custom.csv bestaat en de juiste rij bevat
    assert os.path.isfile('custom.csv')
    with open('custom.csv', newline='') as f:
        rows = list(csv.DictReader(f))
    assert rows[0]['symbol'] == 'Y'

    # Controleer dat de post is verstuurd naar de config-URL
    assert len(calls) == 1 and calls[0][0] == 'https://cfg-hook'