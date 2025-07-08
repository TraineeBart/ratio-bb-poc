

# Project Specification – Ratio Trades V3

## 🎯 Doel
Ontwikkel een betrouwbare Proof of Concept (PoC) voor een geautomatiseerde tradingbot die de **Ratio-Bollinger Band (Ratio-BB)** strategie hanteert om crypto-paren (TFUEL-USDT en THETA-USDT) te verhandelen via limit orders. De PoC moet zowel historische backtests als real-time live trading ondersteunen, met volledige testdekking en robuuste foutafhandeling.

## 📦 Scope

### In Scope
1. **Strategiecore**  
   - Berekening van SMA, Standard Deviation, en Bollinger Bands.  
   - Ratio-berekening (`prijs / onderband` en `prijs / bovenband`).  
   - Signalering: `SWAP_TFUEL_TO_THETA`, `SWAP_THETA_TO_TFUEL`, `NO_SWAP`.

2. **Backtester & Replay**  
   - CLI-backtest met `--replay <json>` op tickniveau.  
   - E2E-backtest met historische CSV (`data/historical.csv`).  
  - Vergelijking output CSV en webhook payloads met zogeheten **golden files**
    (referentiebestanden met de verwachte testoutput, opgeslagen in `acceptance/`).

3. **Live Trading**  
   - WebSocket-client (`WSClient`) voor real-time ticks.  
   - Callback-architectuur naar strategiemodule.  
   - Limit-order simulatie met batching op basis van 24u-liquiditeit.

4. **Architectuur & Infrastructuur**  
   - Docker & Docker Compose setup voor lokale staging.  
   - Volume-mounts (`./tmp`, `./logs`).  
   - CI-pijplijn met matrix-testing, coverage-gates en data-preparation.

5. **Teststrategie**  
   - Unit-tests voor kernmodules (`strategy.py`, `executor.py`, `ws_client.py`, `ws_replay.py`).  
   - Integratie- en E2E-tests (`run_once.py`, orchestrator).  
   - Coverage ≥ 90% voor strategie en ≥ 80% voor andere modules.

### Out Of Scope
- Productieorder-API naar echte exchanges.  
- UI/dashboard buiten CLI of eenvoudige merkbare metrics.  
- Dataopslag in een database (behalve tijdelijke CSV & logs).  
- Geavanceerde hyperparameter-search of AI-agentflows.

## 🛠️ Kernfunctionaliteiten

1. **apply_filters()**: selecteert rijen op `nk ≥ threshold` en `volume ≥ threshold`; genereert signals.  
2. **compute_bbands()**: berekent bands en ratio’s.  
3. **simulate_order()**: splitst grote limit-orders in batches gebaseerd op de gemiddelde 24-uurs liquiditeit (orderboek-grootte) en past fee-berekening toe.  
4. **WSClient**: onderhoudt websocket verbinding, herstart na disconnects, stuurt ticks naar callback.  
5. **WSReplay**: speelt oudere CSV-ticks af met simulatietiming, valideert kolommen.  
6. **run_once.py**: orkestreert replay- of live-flow, schrijft `tmp/output.csv`, verstuurt webhooks.

## ✅ Acceptatiecriteria

- `pytest` slaagt zonder fouten of warnings voor alle tests (unit, integration, E2E).  
- Backtests (replay & live override) produceren identieke output CSV- en webhook-golden-paringen.  
- Live-mode draait minimaal 10 minuten in staging, met ≥ 5 non-HOLD signals en reconnects na netwerkgaps.  
- Coverage: strategie ≥ 90%, overige modules ≥ 80%.  
- Documentatie en README zijn up-to-date met setup- en usage-instructies.

## 📅 Roadmap & Iteraties

- **Iteratie 1**: setup projectstructuur, CI, core strategy en replay-tests (afgerond).  
- **Iteratie 2**: WSClient live/replay synchronisatie, logging, applicatie refactors (afgerond).  
- **Iteratie 3**: Live-mode integratie & staging validatie (in progress).  
- **Iteratie 4**: Backfill, metrics & monitoring, hyperparameter-flow (gepland).  