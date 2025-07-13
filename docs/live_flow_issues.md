# Bevindingen en actiepunten Live Flow & Tests

## Bestand: `/opt/ratio-bb-poc/src/run_once.py`

### Bevindingen
- Output naar `output.csv` gebeurt op candle-sluiting, niet per tick. Hierdoor bevat CSV minder regels dan test verwacht.
- Webhook wordt gestuurd bij candle-sluiting via `requests.post`.
- Tests patchen `requests.post` maar WebhookHandler registreert geen calls, waarschijnlijk patch op verkeerde plek of verkeerde import.
- `DummyWSClient` genereert ticks maar callback lijkt niet direct Webhook te triggeren; mogelijk mismatch in event flow.
- Timing in tests (max_ticks=5 met 1s interval) wijkt af van productie-interval van 5 minuten candles.
- DummyWSClient levert tick events sneller dan productie, wat kan leiden tot timing issues in testvalidatie.

### Impact op tests
- `test_live_flow.py` faalt omdat:
  - Verwacht 6 regels (1 dummy + 5 ticks), krijgt 1 regel (1 candle).
  - Webhook calls blijven leeg.
- Onvoldoende synchronisatie tussen mock WSClient events en live candle generation.
- Patch van `requests.post` moet op exact dezelfde import-locatie als in run_once.py plaatsvinden.
- Testdata en mocking zijn nog niet volledig afgestemd op candle-gebaseerde output.

### Aanbevolen actie
- Verifiëren dat patch in tests correct geplaatst wordt op gebruikte `requests.post` (bijv. `src.run_once.requests.post`).
- Onderzoeken event flow: zorgen dat tick events leiden tot candle sluiting en webhook trigger.
- Overwegen test aan te passen aan candle-gebaseerde output ipv tick-gebaseerde output.
- Testinterval en max_ticks aanpassen voor realistischere simulatie.
- Documenteren expected flow en timing in README/tests.md.
- Overwegen aparte test met dummy csv data ipv live websocket mock voor stabiliteit.

---

## Bestand: `/opt/ratio-bb-poc/tests/test_live_flow.py`

### Bevindingen
- Test faalt vanwege mismatch in aantal regels in CSV en lege WebhookHandler.calls.
- Patching `requests.post` lijkt niet effectief.
- Mogelijke onvolledige of incorrecte mocking setup.
- Test verwacht WebhookHandler.calls met 5 entries, terwijl geen calls geregistreerd worden.
- CSV output bevat enkel één dummyregel, geen meerdere ticks/candles.

### Aanbevolen actie
- Test herschrijven om candle output te gebruiken.
- Mocking verbeteren: patchen van `requests.post` exact daar waar die in run_once.py wordt geïmporteerd.
- Toevoegen logs om patch werking te verifiëren.
- Overwegen om test op te splitsen: unit test voor candle aggregatie + integratie test met csv files.

---

## Algemeen

### Prioriteiten
- Hoog: Webhook mocking fixen om tests betrouwbaar te maken.
- Middel: Test output aanpassen aan candle-aggregatie.
- Laag: Eventuele extra logging voor betere debugging.
- Langetermijn: Stabiliteit verbeteren door testen op basis van statische csv testdata ipv live websocket simulatie.

---

## Links en referenties

- [Git commit xxxyyy] Updates run_once.py candle handling
- Tests folder `/tests` en documentatie in `/docs`
- Discussie en analyse sessies juli 2025

---

*Dit document wordt regelmatig bijgewerkt na voortgang en nieuwe inzichten.*