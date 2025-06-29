import csv
import time
import pytest
from pathlib import Path
from src.ws_replay import replay

@pytest.fixture(autouse=True)
def stub_wsclient(monkeypatch):
    """
    Stub WSClient zodat we calls naar handle_tick kunnen vangen.
    """
    calls = []
    class DummyWSClient:
        def __init__(self, symbols):
            pass
        def handle_tick(self, symbol, price):
            calls.append((symbol, price))
    import src.ws_replay as replay_mod
    monkeypatch.setattr(replay_mod, 'WSClient', DummyWSClient)
    return calls

def make_csv(tmp_path, rows, headers=None):
    """
    Schrijf een lijst van dicts naar een CSV-file.
    """
    path = tmp_path / "ticks.csv"
    if headers is None:
        headers = rows[0].keys() if rows else []
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return str(path)

def test_replay_empty(tmp_path, stub_wsclient):
    # Alleen header, geen data
    p = tmp_path / "empty.csv"
    with open(p, 'w', newline='') as f:
        f.write('timestamp,price,close,volume,nk\n')
    result = replay('XYZ', str(p), delay=0)
    assert result is None
    assert stub_wsclient == []

def test_replay_single_and_malformed(tmp_path, stub_wsclient):
    rows = [
        {'timestamp': '1', 'price': '10.0', 'close': '', 'volume': '100', 'nk': '1'},
        {'timestamp': '2', 'price': 'bad',  'close': '', 'volume': '',    'nk': ''}
    ]
    csv_path = make_csv(tmp_path, rows)
    result = replay('SYM', csv_path, delay=0)
    assert stub_wsclient == [('SYM', 10.0)]

def test_replay_single_close_priority(tmp_path, stub_wsclient):
    rows = [
        {'timestamp': '1', 'price': '5.0', 'close': '6.5', 'volume': '10', 'nk': '1'},
    ]
    csv_path = make_csv(tmp_path, rows)
    result = replay('AAA', csv_path, delay=0)
    assert stub_wsclient == [('AAA', 6.5)]

def test_replay_multiple_and_delay(tmp_path, stub_wsclient, monkeypatch):
    rows = [
        {'timestamp': '1', 'price': '1.0', 'close': '',  'volume': '1', 'nk': '1'},
        {'timestamp': '2', 'price': '2.0', 'close': '',  'volume': '1', 'nk': '1'},
        {'timestamp': '3', 'price': '3.0', 'close': '',  'volume': '1', 'nk': '1'},
    ]
    csv_path = make_csv(tmp_path, rows)
    sleep_calls = []
    monkeypatch.setattr(time, 'sleep', lambda s: sleep_calls.append(s))
    result = replay('BBB', csv_path, delay=0.01)
    assert stub_wsclient == [('BBB', 1.0), ('BBB', 2.0), ('BBB', 3.0)]
    assert sleep_calls == [0.01, 0.01]

def test_replay_order_and_stop(tmp_path, stub_wsclient):
    rows = [
        {'timestamp': '10', 'price': '10', 'close': '', 'volume': '1', 'nk': '1'},
        {'timestamp': '20', 'price': '20', 'close': '', 'volume': '1', 'nk': '1'},
    ]
    csv_path = make_csv(tmp_path, rows)
    result = replay('CCC', csv_path, delay=0)
    assert stub_wsclient == [('CCC', 10.0), ('CCC', 20.0)]