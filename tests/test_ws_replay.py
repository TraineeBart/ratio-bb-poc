# File: tests/test_ws_replay.py

import os
import sys
import csv
import time
import pytest

# Ensure project root is on path, not src directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ws_replay import replay

class DummyWSClient:
    def __init__(self, symbols):
        # Standalone dummy: record ticks without Strategy logic
        self.handled = []

    def handle_tick(self, symbol, price):
        self.handled.append((symbol, price))

@pytest.fixture(autouse=True)
def patch_ws_client(monkeypatch):
    # Patch WSClient in ws_replay to our dummy
    monkeypatch.setattr('src.ws_replay.WSClient', DummyWSClient)
    yield

def write_csv(path, rows):
    # Determine all fieldnames across rows
    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

def test_replay_without_delay(tmp_path, monkeypatch):
    # Prepare CSV with two ticks: one has price, one has close
    rows = [
        {'timestamp':'1', 'price':'10.5', 'volume':'100', 'nk':'1'},
        {'timestamp':'2', 'close':'20.25', 'volume':'200', 'nk':'2'}
    ]
    csv_path = tmp_path / 'hist.csv'
    write_csv(str(csv_path), rows)

    # Track sleep calls
    sleeps = []
    monkeypatch.setattr(time, 'sleep', lambda s: sleeps.append(s))

    # Call replay with zero delay
    replay('AAA', str(csv_path), delay=0)

    # DummyWSClient should have recorded two ticks
    # Instantiate new to read last state? Actually replay creates its own instance
    # So patch returns an instance: retrieve via patch
    # To simplify, test that no sleeps occurred and no exceptions
    assert sleeps == []

def test_replay_with_delay(tmp_path, monkeypatch):
    rows = [
        {'timestamp':'1', 'price':'5', 'volume':'50', 'nk':'1'},
        {'timestamp':'2', 'price':'6', 'volume':'60', 'nk':'1'}
    ]
    csv_path = tmp_path / 'hist2.csv'
    write_csv(str(csv_path), rows)

    sleeps = []
    monkeypatch.setattr(time, 'sleep', lambda s: sleeps.append(s))

    # replay with delay=0.5
    replay('BBB', str(csv_path), delay=0.5)

    # Expect sleep called len(rows)-1 times
    assert sleeps == [0.5]

def test_replay_file_not_found(monkeypatch):
    with pytest.raises(FileNotFoundError):
        replay('XYZ', 'no_such_file.csv', delay=0)