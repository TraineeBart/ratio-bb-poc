📋 Project Taskboard – Ratio-BB-POC

**Doel:** Overzicht van openstaande taken, status en voortgang.  
Gebruik dit bord als referentie bij samenwerking met specialistische GPT’s.

---

## ✅ Besluiten (referentie)

> **Hoofdprioriteit blijft het opschonen en afronden van de pipeline; Telegram signaleringsbot is een tussendoel.**

- **Webhook wordt losgekoppeld en als aparte service gebouwd**  
- **Testinfrastructuur wordt opgeschoond en heringericht naar unit/integration/live structuur**  
- **Outbox-structuur wordt als JSON-lines bestand gerealiseerd (`outbox/events.jsonl`), via een EventWriter klasse**  
- **Webhook-service verwerkt events uit de outbox naar HTTP, met fallback en logging**  
- **Cleanup van outbox wordt als aparte taak gedefinieerd (bijv. periodiek herschrijven)**  
- **Concurrentie bij outbox schrijven wordt in de POC-fase niet geoptimaliseerd; sequentieel schrijven is voldoende**

---

## 🚧 Openstaande Taken

### 🗂️ Structuur & Code

| Nr | Taak | Status |
|----|-----------------------------------------------------------------------------------------------|----|
| 1  | Controleer en voltooi testmappenstructuur (`unit/`, `integration/`, `live/`)                  | ✅ |
| 2  | Standaardiseer CSV-testdata in `tests/data/` (kolommen, types, validatie).                    | ✅ |
| 3  | Zet outbox-structuur op voor event-log (JSON-lines, via EventWriter).                         | ✅ |
| 4  | Bouw webhook-service als los script in `src/webhook_service/`.                                | ✅ |
| 11 | Los dubbele `kucoin_client.py` op (verwijder duplicatie)                                      | 🔄 |
| 12 | Herzie en vereenvoudig `run_all.py` / `run_once.py`                                           | ✅ |
| 13 | Verplaats `test_ws.py` en `kucoin_test.py` naar `tests/`                                      | 🔄 |
| 14 | Isoleer of label `developer.py` als experimenteel                                             | 🔄 |
| 15 | Voeg `src/README.md` toe met overzicht en afspraken                                           | 🔄 |
| 16 | Ontwerp en implementeer cleanup-mechanisme voor outbox                                        | 🔄 |
| 17 | Schrijf unit- en integratietests voor de refactor van `run_once.py` (Quality EngineerGPT)     | 🔄 |
| 18 | Update CI-checks en coverage-rapportage voor de nieuwe structuur (Quality EngineerGPT)        | 🔄 |
| 19 | Koppel batching/executor aan de nieuwe pipeline structuur (DeveloperGPT)                      | ✅ |
| 20 | Voeg README per modulemap toe: `core/`, `infra/`, `orchestration/` (StructuurbeheerderGPT).   | ✅ |
| 21 | Opruimen verouderde pipeline-bestanden (oude `run_once.py`, dev-tools, snapshots)             | 🔄 |
| 22 | Koppel batches aan outbox/webhook flow zodat batch-resultaten ook via webhook verwerkt worden | ✅ |
| 25 | Implementeer parallelle batchverwerking in executor (configurabel maken)                      | 🔄 |
| 26 | Automatiseer webhook batch-result tests (mock endpoint)                                       | 🔄 |
| 27 | Voltooi volledige `run_all.py` loop inclusief batch-pipeline                                  | 🔄 |
| 24 | Integreer batchtests in CI pipeline                                                           | 🔄 |

### 🛰️ Live Signaleringsbot – Telegram Scope

| Nr | Taak | Status |
|----|----------------------------------------------------------------|----|
| 28 | Voltooi `run_all.py` loop voor continue live-signaalverwerking | 🔄 |
| 29 | Activeer live WebSocket feed of mock-feed voor real-time data  | 🔄 |
| 30 | Bouw Telegram webhook-integratie voor `batch_result` meldingen | 🔄 |
| 31 | Formatteer meldingen met actie, volume, ratio en batch-info    | 🔄 |
| 32 | Test live pipeline met voorraad-simulatie en Telegram output   | 🔄 |

---

### 🧪 Testen & CI

| Nr | Taak | Status |
|----|-------------------------------------------------------|----|
| 5 | Pas integratietests aan naar CSV-input en mock webhook | ✅ |
| 6 | Splits CI-workflow in unit/integration/live            | 🔄 |
| 7 | Voeg testcoverage-rapportage toe per testgroep         | 🔄 |
| 24 | Integreer batchtests in CI pipeline                   | 🔄 |

---

### 📝 Documentatie

| Nr | Taak | Status |
|----|------------------------------------------------------|----|
| 8 | Update README’s in `tests/` en `tests/data/`          | 🔄 |
| 9 | Documenteer webhook-service in `docs/dev/modules.md`  | ✅ |
| 10 | Documenteer besluit in `/docs/decisions/` (afgerond) | ✅ |

---

## 🔄 Workflow gebruik

- **Bij een werksessie met GPT’s**: Verwijs naar taaknummers (“Bekijk taak #4”)
- **Voortgang bijhouden**: Markeer taken als ✅ of 🔄 of ❌ in dit document
- **Geen nieuwe taken toevoegen zonder akkoord via PM-rol**

---</file>