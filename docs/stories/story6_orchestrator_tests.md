

# Story 6: Orchestrator Modules – Unit Tests

**Rol:** DeveloperGPT

## Context & Doel
De `orchestrator`-modules regelen de end-to-end signal-to-webhook flow binnen `run_once.py` voor verschillende assets:
- `src/orchestrator.py` (TFUEL)
- `src/orchestrator_theta.py` (THETA)
- `src/orchestrator_ratio.py` (Ratio)

Tot nu toe ontbreken er unit-tests voor deze modules. Het doel is om met gerichte tests de betrouwbaarheid en dekking te verhogen naar ≥ 80% per module.

## Taken
1. Identificeer alle publieke functies en methoden in de drie orchestrator-bestanden (bijv. `handle_signal()`, `write_csv()`, `dispatch_webhook()`).
2. Maak aparte testbestanden:
   - `tests/test_orchestrator_tfuel.py`
   - `tests/test_orchestrator_theta.py`
   - `tests/test_orchestrator_ratio.py`
3. Schrijf in elk testbestand:
   - Happy path: correcte CSV-lijnen en webhook-aanroepen voor het bijbehorende asset.
   - Foutscenario’s: misvormde input en I/O-excepties.
   - Directory- en file-management (aanmaken van `tmp/` als deze ontbreekt).
4. Mock externe afhankelijkheden (`csv.writer`, `requests.post`) om tests onafhankelijk te maken.
5. Verifieer dat de coverage voor elke orchestrator-module ≥ 80%.

## Acceptatiecriteria
- De drie testbestanden draaien volledig groen.
- Coverage-rapport toont minimaal 80% voor elk orchestrator-script.
- CI-pijplijn blijft groen na integratie van de nieuwe tests.