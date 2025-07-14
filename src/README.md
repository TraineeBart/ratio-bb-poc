# 🗂️ Ratio-BB-POC – `src/` Directory

## 🎯 Doel van deze map

De `src/`-directory bevat alle **kerncode** van het Ratio-BB-POC project.  
De structuur is modulair opgebouwd volgens de scheiding tussen:

- **Core strategie** – Signaalgeneratie en voorraadbeheer
- **Infra & Connectors** – Outbox, webhook-service, websocket clients
- **Batching & Executor** – Groeperen van signalen en uitvoeren van batches
- **Orchestration** – `run_once.py` en `run_all.py` voor workflow-aansturing
- **Legacy & Experimental** – Oude code en experimentele tools

---

## 🗺️ Structuuroverzicht

| Map / Bestand | Doel |
|---------------|------|
| `batching/` | BatchBuilder voor signalen naar batches |
| `core/` | Handelslogica en voorraadbeheer |
| `executor/` | BatchExecutor, voert batches uit |
| `infra/` | EventWriter, outbox, WebSocket adapter |
| `webhook_service/` | Verzenden van events naar HTTP endpoints |
| `orchestration/` | Orchestration via `run_once.py` en `run_all.py` |
| `client/` | KuCoin client voor live data |
| `utils/` | Tijdzone helper |
| `experimental/` | Experimentele tools, zoals `developer.py` |
| `legacy/` | Oude orchestrators, parsers, strategies en test-helpers |

---

## 🔧 Afbakening & Afspraken

- **Geen tests in `src/`**  
  → Alle tests staan in `tests/`

- **Geen losse scripts in `src/` root**  
  → Gebruik `orchestration/` of `experimental/` voor losse tools

- **Legacy en experimental code is verplaatst naar aparte mappen**

---

## 📄 Documentatie & Review

- Volledig overzicht van de `src/` map:  
  → Zie: `/docs/reviews/src-overview-2025-07-13.md`

- CI en teststatus:  
  → Zie: `/docs/dev/modules.md`

---

## ✅ Status

- Pipeline is opgeschoond en modulair
- Klaar voor verdere uitbreiding naar live feed en Telegram notificaties