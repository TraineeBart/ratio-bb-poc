
"""
🧪 Test Webhook Service Sanity

Deze test controleert of de webhook-service correct een 'trade_signal' event oppakt uit de outbox
en doorstuurt naar een HTTP-endpoint.

Belangrijk:
- Alleen 'trade_signal' events worden verstuurd
- Er wordt getest met een dummy endpoint zodat geen echte HTTP-calls worden gemaakt
- De omruillogica (THETA → TFUEL) wordt via het event gecontroleerd

"""


# ╭───────────────────────────────────────────────────────────╮
# │ File: tests/integration/test_webhook_service_sanity.py    │
# │ Module: tests.integration                                 │
# │ Doel: Sanity-check integratietest voor webhook-service    │
# │ Auteur: QualityEngineerGPT                                │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                            │
# ╰───────────────────────────────────────────────────────────╯

import tempfile
import json
import os
import pytest
from src.webhook_service.webhook_service import process_outbox

class DummyEndpoint:
    def __init__(self):
        self.received = []
    def post(self, url, json):
        self.received.append(json)
        return DummyResponse()

class DummyResponse:
    def raise_for_status(self):
        pass

def test_webhook_service_sanity(monkeypatch, tmp_path):
    """
    🧠 Functie: test_webhook_service_sanity
    Test of de webhook-service correct trade_signal events doorstuurt.

    ▶ In:
        - monkeypatch (fixture): voor het mocken van requests.post
        - tmp_path (Path): tijdelijke directory
    ⏺ Out:
        - Geen return; asserts controleren dat 1 event is verzonden

    💡 Gebruikt:
        - process_outbox uit src.webhook_service.webhook_service
    """
    # Maak een dummy event aan met de verwachte structuur
    event = {
        "event_type": "trade_signal",
        "timestamp": "2025-07-13T12:00:00Z",
        "payload": {
            "from_asset": "THETA",
            "to_asset": "TFUEL",
            "action": "SELL",
            "amount": 10000,
            "price": 8.07
        }
    }

    # Schrijf het event naar een tijdelijke outbox file
    outbox_file = tmp_path / "events.jsonl"
    with open(outbox_file, "w") as f:
        f.write(json.dumps(event) + "\n")

    # Mock de requests.post functie zodat er geen echte HTTP-call plaatsvindt
    dummy = DummyEndpoint()
    monkeypatch.setattr("src.webhook_service.webhook_service.requests.post", dummy.post)

    # Roep de webhook-service aan om de outbox te verwerken
    process_outbox(str(outbox_file), "http://dummy-endpoint")

    # Controleer of precies 1 event is verstuurd en dat de omruilrichting correct is
    assert len(dummy.received) == 1
    assert dummy.received[0]["payload"]["from_asset"] == "THETA"