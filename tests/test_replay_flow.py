import json
import sys
from src.run_once import run_once_main
from tests.helpers import WebhookHandler


def test_replay_flow_smoke(tmp_path, monkeypatch, http_server):
    replay_file = tmp_path / "dummy_replay.json"
    dummy_ticks = [
        {"timestamp": "2025-07-08T10:00:00Z", "symbol": "THETA", "price": 0.08, "signal": "BUY"},
        {"timestamp": "2025-07-08T10:00:05Z", "symbol": "THETA", "price": 0.081, "signal": "SELL"},
    ]
    replay_file.write_text(json.dumps(dummy_ticks))

    sys.argv = ["run_once.py", "--replay", str(replay_file)]
    monkeypatch.delenv("MODE", raising=False)
    monkeypatch.setenv("WEBHOOK_URL", http_server)

    run_once_main()

    assert len(WebhookHandler.calls) == 2
    for call in WebhookHandler.calls:
        assert "signal" in call