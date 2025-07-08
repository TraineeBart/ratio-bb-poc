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