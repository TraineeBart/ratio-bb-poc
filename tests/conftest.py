# tests/conftest.py

import sys
import os
import pytest

# Voeg project-root toe aan sys.path zodat 'src' module vindbaar is
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(autouse=True)
def set_webhook_url_env(monkeypatch):
    """
    Fixture om automatisch de WEBHOOK_URL omgeving variabele te zetten
    zodat dispatch_webhook tests de endpoint kennen.
    """
    monkeypatch.setenv("WEBHOOK_URL", "http://localhost:5001/webhook")

import threading
from http.server import HTTPServer
from tests.helpers import WebhookHandler

@pytest.fixture(scope="function")
def http_server():
    WebhookHandler.calls.clear()

    class PatchedWebhookHandler(WebhookHandler):
        def do_POST(self):
            if self.path == "/webhook":
                super().do_POST()
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(("localhost", 0), PatchedWebhookHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield f"http://localhost:{port}/webhook"

    server.shutdown()
    thread.join()