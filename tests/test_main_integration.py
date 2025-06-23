# File: tests/test_main_integration.py
import sys
import os
import json
import types
import pytest
import requests

# Ensure src and project root are on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import main
from src.run_once import main as run_once_main

@pytest.fixture(autouse=True)
def isolate_environment(tmp_path, monkeypatch):
    # Change working directory to temp
    monkeypatch.chdir(tmp_path)
    # Stub webhook URL
    monkeypatch.setenv('WEBHOOK_URL', 'https://example.com/hook')
    # Capture POST calls
    post_calls = []
    def fake_post(url, json=None, timeout=None):
        post_calls.append((url, json))
        return types.SimpleNamespace(raise_for_status=lambda: None, url=url, json=json)
    monkeypatch.setattr('requests.post', fake_post)
    # Provide container for calls
    return {'post_calls': post_calls, 'tmp_path': tmp_path}

def test_replay_flow(isolate_environment):
    # Create replay JSON file
    ticks = [
        {'timestamp': 1620000000, 'price': 1.0, 'signal': 'BUY'},
        {'timestamp': 1620000060, 'price': 2.0, 'signal': 'SELL'}
    ]
    replay_path = isolate_environment['tmp_path'] / 'replay.json'
    replay_path.write_text(json.dumps(ticks))
    # Set args
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv('PYTEST_RUNNING', '1')
    sys_argv = sys.argv.copy()
    sys.argv[:] = ['run_once', '--replay', str(replay_path)]
    try:
        run_once_main()
    finally:
        sys.argv[:] = sys_argv
        monkeypatch.undo()
    # Validate CSV output
    csv_file = isolate_environment['tmp_path'] / 'tmp' / 'output.csv'
    assert csv_file.exists()
    # Validate webhook calls
    assert isolate_environment['post_calls'], "No POST calls made in replay flow"

def test_live_flow(isolate_environment, monkeypatch):
    # Stub WSClient to call on_signal twice
    from src.ws_client import WSClient
    class DummyClient(WSClient):
        def run(self):
            # simulate signals
            self._signal_callback({'symbol': 'S', 'price': 10, 'signal': 'BUY', 'timestamp': 't'})
            self._signal_callback({'symbol': 'S', 'price': 5, 'signal': 'SELL', 'timestamp': 't'})
    monkeypatch.setattr('main.WSClient', DummyClient)
    # Run without args
    sys_argv = sys.argv.copy()
    sys.argv[:] = ['main.py']
    try:
        main()
    finally:
        sys.argv[:] = sys_argv
    # Validate CSV and webhook
    csv_file = isolate_environment['tmp_path'] / 'tmp' / 'output.csv'
    assert csv_file.exists()
    assert len(isolate_environment['post_calls']) == 2
