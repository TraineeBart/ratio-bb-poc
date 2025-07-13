# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_webhook.py                                  │
# │ Module: tests.test_webhook                                   │
# │ Doel: Unit-tests voor de webhook dispatch helper             │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: draft                                                │
# ╰──────────────────────────────────────────────────────────────╯
import os
import pytest
import requests
from src.outputs.webhook import dispatch_webhook

def test_dispatch_webhook_happy(monkeypatch):
    """
    🧪 Test: dispatch_webhook happy path
    Verifies that requests.post is called with correct URL, payload, and timeout.
    """
    # Arrange
    test_url = "https://example.com/hook"
    monkeypatch.setenv("WEBHOOK_URL", test_url)

    calls = []
    def fake_post(url, json=None, timeout=None):
        calls.append((url, json, timeout))
        class DummyResponse:
            def raise_for_status(self): pass
        return DummyResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    payload = {"foo": "bar"}
    # Act
    dispatch_webhook(payload, timeout=15)

    # Assert
    assert calls == [(test_url, payload, 15)]

def test_dispatch_webhook_no_url():
    """
    🧪 Test: dispatch_webhook raises EnvironmentError if WEBHOOK_URL missing
    """
    # Ensure the environment variable is not set
    os.environ.pop("WEBHOOK_URL", None)

    with pytest.raises(EnvironmentError) as exc:
        dispatch_webhook({"foo": "bar"})

    assert "WEBHOOK_URL environment variable not set" in str(exc.value)

def test_dispatch_webhook_http_error(monkeypatch):
    """
    🧪 Test: dispatch_webhook propagates HTTP errors
    """
    # Arrange
    test_url = "https://example.com/hook"
    monkeypatch.setenv("WEBHOOK_URL", test_url)

    def fake_post_error(url, json=None, timeout=None):
        class DummyResponse:
            def raise_for_status(self):
                raise requests.exceptions.Timeout("timeout error")
        return DummyResponse()

    monkeypatch.setattr(requests, "post", fake_post_error)

    # Act & Assert
    with pytest.raises(requests.exceptions.Timeout):
        dispatch_webhook({"foo": "bar"}, timeout=20)
