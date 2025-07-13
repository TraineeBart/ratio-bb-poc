# Ratio-BB-POC - Uitgebreid Onderzoeksrapport en Aanbevelingen

## Management Summary

Dit rapport geeft een diepgaand overzicht van de huidige status van het Ratio-BB-POC projectcode, de belangrijkste bevindingen rondom data-, test- en architectuuraspecten, en praktische aanbevelingen per bestand en map. Het doel is een helder kader te bieden voor verdere ontwikkeling en afronding van de proof of concept (POC).

Belangrijke inzichten:

- Focus verschuiven van tick-data naar candle-data in de tests en live flow.
- Verminderen van complexe websocket mocks in tests; statische CSV-testdata als stabiel alternatief.
- Heldere afbakening en opschoning van testmappen met passende README.md documentatie.
- Verbeteren van patching van network calls in tests (zoals `requests.post`) op correcte importlocaties.
- Monitoring en rapportage van event flow en timing voor live en testomgevingen.
- Herstelpunten vastleggen met Git om terugval te faciliteren bij grote wijzigingen.

Deze bevindingen vormen het fundament voor een stabiele, betrouwbare en uitbreidbare POC.

---

# Bevindingen en Actiepunten per Bestand / Map

## Algemeen

- Git-branching: Herstelpunt vastgelegd op `feature/docs-structure`.  
- Opschoning: Overbodige tests en oude flows verwijderd, mappenstructuur helder met duidelijke README.md bestanden.  
- Tests: Unit-, integratie- en live-tests gescheiden en gedocumenteerd in respectievelijke folders met testdata in aparte `tests/data/`.

---

## Map: `/src/`

### Belangrijkste bestanden

- `run_once.py`
- `strategy.py`
- `ws_client.py`
- `batching.py`
- `executor.py`
- `enrich_indicators.py`

### Bevindingen

- `run_once.py` werkt op candle-sluiting; output naar CSV en webhook gebeurt per candle, niet per tick.  
- `strategy.py` bevat core logica voor trading signalen, functioneel maar kan uitgebreid worden met meer robuustheid.  
- `ws_client.py` en mocks hiervoor zijn complex in tests, wat tot onstabiele testuitkomsten leidt.

### Aanbevelingen

- Bewaar code in huidige structuur, documenteer flow en verantwoordelijkheden.  
- Overweeg uitbreiding en refactoring van `strategy.py` na afronding POC.  
- Houd websocket mocks minimaal in tests; focus op testdata met candles.

---

## Map: `/tests/`

### Structuur

- `unit/`: Unit tests op moduleniveau, mocks en snelle validaties.  
- `integration/`: End-to-end tests die meerdere modules samenbrengen.  
- `live/`: Tests die de volledige live flow simuleren of met data werken.

### Aanbevelingen

- Documenteer en houd README.md actueel per map.  
- Verwijder verouderde tests na beoordeling, behoud nuttige tests met aanpassingen.  
- Versterk mocking en patching waar nodig (bijv. `requests.post` patch in `run_once.py` context).

---

## Specifieke Testbestanden

### `tests/live/test_live_flow.py`

- Probleem: Verwacht meerdere regels per tick, terwijl output candle-gebaseerd is met 1 regel per candle.  
- Webhook mock faalt door patch op verkeerde locatie.  
- Actie: Pas test aan op candle output, patch correct, voeg logging toe.

### `tests/live/test_strategy_csv_flow.py`

- Verwerkt testdata in CSV-formaat, geeft stabiele basis.  
- Problemen met kolomnamen en data types opgelost door data cleaning.  
- Actie: Behouden, uitbreiden voor robuustheid.

### `tests/unit/test_batching.py`

- Testt batching logica goed, stabiel en volledig.  
- Actie: Behouden als referentie.

### `tests/unit/test_bb_strategy.py`

- Draft status, test BB strategie signaalgeneratie.  
- Actie: Uitbreiden met realistische scenario’s.

### `tests/integration/test_full_backtest_flow.py`

- Test complexe flow integratie, stabiel.  
- Actie: Behouden, documenteren.

### `tests/integration/test_market_api.py`

- Tests API client, stabiel.  
- Actie: Behouden of integreren met integratietests.

### `tests/integration/test_orchestrator_*.py`

- Tests orchestrator modules per munt (Theta, Tfuel, ratio).  
- Actie: Behouden, documenteren status en onderhoud.

### Overige tests

- Snapshot tests: Uitgesloten van CI voor stabiliteit.  
- Webhook tests: Moeten patchen op correcte plek, stabiliseren met dummy data.

---

# Aanbevelingen voor de Volgende Fasen

1. **Test Stabilisatierondes**  
   - Focus op correcte patching, testdata en mocks.  
   - Splits tests op in unit (functionaliteit) en integratie (flow).  
   - Gebruik statische CSV-testdata ipv live websocket mocks voor stabiliteit.

2. **Documentatie en Proces**  
   - Hou README.md’s actueel met status per map.  
   - Regelmatig refactoren en cleanup om overzicht te behouden.

3. **Functionaliteitsuitbreiding**  
   - Voeg robuustere error handling toe in strategie.  
   - Verken gebruik van hogere timeframe data voor betrouwbaardere signalen.

4. **CI/CD Verbeteringen**  
   - Optimaliseer CI met selective test runs en uitsluiting van instabiele tests.  
   - Automatiseer rapportage van testcoverage en fouten.

5. **Opschonen en Archiveren**  
   - Verwijder of archiveer oude, ongebruikte tests en scripts.  
   - Centraliseer testdata en configureer `.gitignore` correct.

---

# Hoe PDF genereren?

Je kunt deze Markdown met tools als:

- **Pandoc**: `pandoc rapport.md -o rapport.pdf`  
- **VSCode** met Markdown PDF extension  
- **Typora**: exporteren naar PDF  
- **Online converters**

---

*Wil je hulp met een PDF-conversie? Laat het weten.*

---

# Slotopmerking

Dit rapport vormt een solide basis voor de projectmanager om het team te sturen richting een stabiele, functionele POC. De focus ligt op stabiliteit, duidelijkheid en onderhoudbaarheid, zonder de flexibiliteit te verliezen om later te kunnen uitbreiden.

---