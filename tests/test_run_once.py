# File: tests/test_run_once.py

import os
import sys
import json
import csv
import pytest
import requests

# Make sure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.run_once import main

@pytest.fixture(autouse=True)
def isolate_fs(monkeypatch, tmp_path):
    # switch working directory to tmp_path
    monkeypatch.chdir(tmp_path)
    # patch load_config to minimal config
    fake_cfg = {
        'symbols': ['AAA'],
        'historical_csv_path': 'tmp/historical.csv',
        'webhook_url': 'https://example.com/hook'
    }
    monkeypatch.setattr('src.run_once.load_config', lambda: fake_cfg)
    yield

def write_json_ticks(path, ticks):
    with open(path, 'w') as f:
        json.dump(ticks, f)

def read_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

def test_replay_success(monkeypatch, tmp_path, capsys):
    # Prepare JSON file
    ticks = [
        {'symbol': 'AAA', 'price': 1.0, 'timestamp': 1620000000},
        {'symbol': 'AAA', 'price': 2.0, 'timestamp': 1620000060}
    ]
    json_path = tmp_path / 'ticks.json'
    write_json_ticks(str(json_path), ticks)
    # Patch requests.post to capture calls
    posts = []
    def fake_post(url, json=None, timeout=None):
        posts.append((url, json))
        class R: 
            def raise_for_status(self): pass
        return R()
    monkeypatch.setattr(requests, 'post', fake_post)

    # Run in replay mode by setting argv
    monkeypatch.setenv('PYTEST_RUNNING', '1')  # ensure monkeypatch fixture is used
    sys.argv = ['run_once', '--replay', str(json_path)]
    main()
    # Check CSV output
    rows = read_csv('tmp/output.csv')
    assert len(rows) == 1  # single signal at end
    # Check POST called once
    assert posts and posts[0][0] == 'https://example.com/hook'
    # Check stdout printed JSON of signal
    captured = capsys.readouterr()
    output = json.loads(captured.out.strip())
    assert isinstance(output, dict)
    assert output['signal'] in ['BUY','SELL','HOLD']

def test_replay_file_not_found():
    sys.argv = ['run_once', '--replay', 'nonexistent.json']
    with pytest.raises(FileNotFoundError):
        main()

def test_live_success(monkeypatch, tmp_path, capsys):
    # Prepare historical CSV
    hist_path = tmp_path / 'historical.csv'
    with open(hist_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['price','nk','volume'])
        writer.writerow([1.0,1,100])
        writer.writerow([2.0,1,100])
        writer.writerow([3.0,1,100])
    # Configure config to point to our CSV
    monkeypatch.setenv('HISTORICAL_CSV_PATH', str(hist_path))
    cfg = {
        'symbols': ['AAA'],
        'historical_csv_path': str(hist_path),
        'webhook_url': 'https://example.com/hook'
    }
    monkeypatch.setattr('src.run_once.load_config', lambda: cfg)
    # Patch requests.post
    posts = []
    monkeypatch.setattr(requests, 'post', lambda url, json=None, timeout=None: type('R', (), {'raise_for_status': lambda s: None})())
    # Run live mode
    sys.argv = ['run_once']
    main()
    # Validate CSV and stdout
    rows = read_csv('tmp/output.csv')
    assert len(rows) == 1
    out = capsys.readouterr().out
    assert '"signal"' in out

def test_live_file_not_found(monkeypatch):
    # Config points to missing file
    cfg = {'historical_csv_path': 'missing.csv'}
    monkeypatch.setattr('src.run_once.load_config', lambda: cfg)
    sys.argv = ['run_once']
    with pytest.raises(FileNotFoundError):
        main()
