

# Migratie Roadmap – Ratio Trades V3

Deze roadmap beschrijft de gefaseerde overgang van de huidige PoC-codebase naar een modulair, onderhoudbaar en uitbreidbaar architectuur.

## Fase 0: PoC Stabilisatie (v0.1)
- Verifieer end-to-end live- en replay-flow met volledige testdekking.
- Documenteer en archiveer verouderde scripts (`backtester.py`, `src/developer.py`).
- Organiseer `docs/`-map met spec, data model en story-documentatie.

## Fase 1: Modularisatie Strategie (v0.2)
- Verplaats `strategy.py` logica naar aparte modules in `src/strategies/`:
  - `src/strategies/bbands.py`
  - `src/strategies/signal.py`
- Definieer duidelijke interfaces per strategy (init, apply, signal).
- Update unittests om modules afzonderlijk te testen.

## Fase 2: Centralisatie Configuratie & DI (v0.3)
- Introduceer dependency injection (bijv. via `injector` of `dependency_injector`).
- Centraliseer config-loading en credentials in `src/config.py`.
- Verwijder hard-coded paden en parameters, gebruik `config.yaml` of env-vars.

## Fase 3: Persistente Data Opslag (v0.4)
- Vervang tijdelijke CSV’s door een eenvoudige database (SQLite/PostgreSQL).
- Bouw een Data Access Layer (`src/db/`).
- Migreer `tmp/output.csv` en `data/historical.csv` naar DB-tabellen.

## Fase 4: Live Monitoring & Metrics (v0.5)
- Exposeer een HTTP-metrics endpoint (Prometheus-compatible).
- Bouw een eenvoudige dashboard (bv. met Streamlit of FastAPI).
- Stel alerts in (bijv. via Telegram of Slack bij falende healthchecks).

## Fase 5: Strategie-extensies & AI Agents (v1.0)
- Definieer een plugin-framework voor strategieën (laadbare modules).
- Integreer AI Agents voor hyperparameter-search op historische data.
- Implementeer experiment-tracking (Optuna, MLflow).

---

> **Opmerking:** de versienummers zijn indicatief; doel is stapsgewijs migreren zonder downtime of regressies.