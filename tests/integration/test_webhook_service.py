

# ╭────────────────────────────────────────────────────────────╮
# │ File: tests/integration/test_webhook_service.py            │
# │ Module: test_webhook_service                               │
# │ Doel: Test de webhook_service met mocking van HTTP-calls   │
# │ Auteur: Quality EngineerGPT                                │
# │ Laatste wijziging: 2025-07-13                              │
# │ Status: draft                                              │
# ╰────────────────────────────────────────────────────────────╯

import pytest
import tempfile
import os
import json

from src.webhook_service import webhook_service

def test_process_outbox_sends_trade_signal(monkeypatch):
    # 🔹 Maak een tijdelijk outbox bestand met verschillende events
    events = [
        {"id": "1", "event_type": "trade_signal", "payload": {"symbol": "THETA"}},
        {"id": "2", "event_type": "other_event", "payload": {}},
        {"id": "3", "event_type": "trade_signal", "payload": {"symbol": "TFUEL"}}
    ]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        for event in events:
            tmp.write(json.dumps(event) + "\n")
        tmp_path = tmp.name

    # 🔹 Mock de send_http functie
    sent_events = []

    def mock_send_http(event, endpoint):
        sent_events.append((event, endpoint))

    monkeypatch.setattr(webhook_service, "send_http", mock_send_http)

    # 🔹 Run de service
    test_endpoint = "http://localhost:9999/webhook"
    webhook_service.process_outbox(tmp_path, test_endpoint)

    # 🔹 Check dat alleen trade_signal events zijn verstuurd
    assert len(sent_events) == 2
    for event, endpoint in sent_events:
        assert event["event_type"] == "trade_signal"
        assert endpoint == test_endpoint

    # 🔹 Cleanup
    os.remove(tmp_path)