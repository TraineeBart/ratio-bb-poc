# infra/event_writer.py

# ╭───────────────────────────────────────────────────────────╮
# │ File: src/infra/event_writer.py                          │
# │ Module: infra                                            │
# │ Doel: Abstractie en implementaties voor het wegschrijven │
# │       van events naar CSV en webhooks.                   │
# │ Auteur: ArchitectGPT                                    │
# │ Laatste wijziging: 2025-07-13                           │
# │ Status: stable                                          │
# ╰───────────────────────────────────────────────────────────╯

"""
📄 EventWriter – Context binnen Ratio-BB-POC:

In deze infrastructuur wordt 'SELL' niet letterlijk als verkopen naar fiat gezien,
maar als een omruilactie:

- Bij een hoge ratio:
    "SELL" betekent THETA → USDT → TFUEL
- Bij een lage ratio:
    "SELL" betekent TFUEL → USDT → THETA

De daadwerkelijke order-flow bestaat altijd uit 2 stappen via USDT, omdat er geen direct THETA/TFUEL pair is.
"""

# infra/event_writer.py
# Implementaties van event-writers voor CSV en webhooks

import os
import csv
import requests
from typing import Protocol
import json

class EventWriterProtocol(Protocol):
    """
    🧠 Interface: EventWriterProtocol
    Definieert de standaard interface voor event-writers. 
    Elke implementatie moet een write(event: dict) methode bevatten.
    """
    def write(self, event: dict) -> None: ...

class CsvWriter(EventWriterProtocol):
    """
    🧠 Klasse: CsvWriter
    Schrijft events naar een CSV-bestand.

    ▶ In:
        - path (str): pad naar de CSV output file

    ⏺ Out:
        - Geen directe output; schrijft naar bestandssysteem.

    💡 Opmerkingen:
        - Maakt de directory aan als deze nog niet bestaat.
        - Initialiseert de header als het bestand nog niet bestaat.
    """
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        if not os.path.isfile(self.path):
            with open(self.path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp','from_asset','to_asset','price','action'])

    def write(self, event: dict) -> None:
        with open(self.path, 'a', newline='') as f:
            writer = csv.writer(f)
            payload = event.get('payload', {})
            writer.writerow([
                event.get('timestamp', 'N/A'),
                payload.get('from_asset', 'N/A'),
                payload.get('to_asset', 'N/A'),
                payload.get('price', event.get('price', 'N/A')),
                payload.get('action', event.get('signal', 'N/A'))
            ])

class JsonlWriter(EventWriterProtocol):
    """
    🧠 Klasse: JsonlWriter
    Schrijft events naar een JSONL-bestand (één JSON per regel).

    ▶ In:
        - path (str): pad naar de JSONL output file

    ⏺ Out:
        - Geen directe output; schrijft naar bestandssysteem.
    """
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def write(self, event: dict) -> None:
        with open(self.path, 'a') as f:
            f.write(json.dumps(event) + "\n")

class WebhookWriter(EventWriterProtocol):
    """
    🧠 Klasse: WebhookWriter
    Verstuurt events via een HTTP POST naar een webhook endpoint.

    ▶ In:
        - url (str): de endpoint URL voor de webhook

    ⏺ Out:
        - Geen directe output; side-effect is HTTP POST.

    💡 Opmerkingen:
        - Verstuurt de event dict als JSON payload.
    """
    def __init__(self, url: str):
        self.url = url

    def write(self, event: dict) -> None:
        requests.post(self.url, json=event, timeout=5)

class MultiEventWriter(EventWriterProtocol):
    """
    🧠 Klasse: MultiEventWriter
    Stuurt events naar meerdere onderliggende writers (fan-out).

    ▶ In:
        - writers (list[EventWriterProtocol]): lijst van writers

    ⏺ Out:
        - Geen directe output; fan-out naar alle onderliggende writers.

    💡 Opmerkingen:
        - Combineert CSV logging, webhooks of andere vormen van output.
    """
    def __init__(self, writers: list[EventWriterProtocol]):
        self.writers = writers

    def write(self, event: dict) -> None:
        for w in self.writers:
            w.write(event)