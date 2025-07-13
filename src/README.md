# 🗂️ Ratio-BB-POC – `src/` Directory

## 🎯 Doel van deze map

De `src/`-directory bevat alle **kerncode** van het Ratio-BB-POC project.  
Het is gestructureerd volgens de scheiding tussen:

- **Core strategie** – Buy/sell beslissingen en tradinglogica
- **I/O & Connectors** – WebSocket clients, API-connecties, webhook calls
- **Orchestration** – `run_once`, orchestrators voor workflows
- **Helpers & Utilities** – Batchhelpers, liquiditeit, parsing, etc.

---

## 🗺️ Structuuroverzicht

| Map / Bestand | Doel |
|---------------|------|
| `strategy.py` | Hoofdlogica voor buy/sell beslissingen |
| `strategies/` | Verschillende implementaties van strategieën |
| `executor.py` | Uitvoeren van trades (TFUEL/THETA) |
| `outputs/` | Output naar files of webhook (wordt losgekoppeld) |
| `ws_client.py` | WebSocket verbindingen (real-time data) |
| `kucoin_client.py` / `client/kucoin_client.py` | KuCoin API-connectie (opschonen gepland) |
| `orchestrator_*` | Aanroepen van workflows per token of ratio |
| `utils/` | Hulpfuncties zoals candles, tijdzone, API-calls |
| `enrichment/` | Verrijking van data met indicatoren |
| `models/` | Datamodellen voor dataflow (bijv. KuCoin) |
| `run_once.py` | Orchestration voor één run (loskoppeling webhook gepland) |
| `developer.py` | Tools voor debug / ontwikkeling (apart zetten gepland) |

---

## 🧹 Afbakening & Afspraken

- **Geen tests in `src/`**  
  → Testbestanden horen thuis in `tests/`, niet in `src/`
  
- **Geen dev-tools of experimenten in `src/`**  
  → `developer.py` wordt verplaatst of gelabeld als experimenteel
  
- **Webhooks worden losgekoppeld**  
  → Zie: `/docs/decisions/2025-07-11-webhook-and-test-architecture-plan.md`

---

## 📄 Documentatie & Review

- **Volledig overzicht van de `src/` map**:  
  → Zie: `/docs/reviews/src-overview-2025-07-13.md`

---

## 🚧 Openstaande punten

- Webhook loskoppelen naar aparte service
- Dubbele KuCoin clients samenvoegen
- Testbestanden (`test_ws.py`, `kucoin_test.py`) verplaatsen naar `tests/`

---