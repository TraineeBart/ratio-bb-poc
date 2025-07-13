> **Snapshot** – Dit document beschrijft de testopzet op 2025-07-13. Voor actuele teststructuur zie `tests/README.md`.

# 📊 Test Overzicht - 2025-07-13

Doel:  
Volledig inzicht krijgen in de huidige testmappen en testbestanden, zodat verdere bouw zonder verrassingen kan plaatsvinden.

---

## 🗂️ tests/unit/

| Bestand | Beschrijving | Status | Actie |
|----------|--------------|--------|-------|
| test_bb_strategy.py | Test voor BB-strategie signalen | Draft | Uitbreiden |
| test_batching.py | Test slicing en batching helpers | OK | Behouden |
| test_candles.py | Test parsing van candle-data | OK | Behouden |
| test_enrich.py | Algemene enrichment test | OK | Behouden |
| test_enrich_ratio_15m.py | Enrichment ratio 15m test | OK | Behouden |
| test_enrich_ratio_60m.py | Enrichment ratio 60m test | OK | Behouden |
| test_enrich_tfuel_15m.py | Enrichment TFUEL 15m test | OK | Behouden |
| test_enrich_tfuel_60m.py | Enrichment TFUEL 60m test | OK | Behouden |
| test_enrich_theta_15m.py | Enrichment THETA 15m test | OK | Behouden |
| test_enrich_theta_60m.py | Enrichment THETA 60m test | OK | Behouden |
| test_executor.py | Test core-executor logica | OK | Behouden |
| test_kucoin_client.py | Test kucoin client | OK | Behouden |
| test_kucoin_fetcher.py | Test kucoin fetcher | OK | Behouden |
| test_kucoin_fetcher_wrapper.py | Test fetcher wrapper | OK | Behouden |
| test_kucoin_parser.py | Test kucoin parser | OK | Behouden |
| test_liquidity_helper.py | Test liquiditeitsberekening | OK | Behouden |
| test_main_on_signal.py | Test run_once op signaal | OK | Behouden |
| test_output_writer.py | Test output writer | OK | Behouden |
| test_run_once.py | Test run_once flow | OK | Behouden |
| test_strategy.py | Test strategiemodule | OK | Behouden |
| test_webhook.py | Test webhook calls met mock | Fragiel mocking | Patchinglocatie verbeteren |
| test_ws_replay.py | Test websocket replay functionaliteit | OK | Behouden |

> ✅ Alle tests in `unit/` zijn opgenomen in dit overzicht. Geen verdere actie nodig behalve de openstaande punten (BB-strategy afronden, webhook mocking verbeteren).

---

## 🗂️ tests/integration/

| Bestand | Beschrijving | Status | Actie |
|----------|--------------|--------|-------|
| test_full_backtest_flow.py | Volledige backtest flow | OK | Behouden |
| test_executor_batching.py | Test batching-logica binnen de executor | OK | Behouden |
| test_executor_integration.py | Test integratie van de executor | OK | Behouden |
| test_market_api.py | Test market API koppeling | OK | Behouden |
| test_orchestrator_ratio.py | Ratio flow integratie | OK | Behouden |
| test_orchestrator_tfuel.py | TFUEL flow integratie | OK | Behouden |
| test_orchestrator_theta.py | THETA flow integratie | OK | Behouden |
| test_smoke_orchestrator.py | Smoke test voor orchestrator | OK | Behouden |
| test_strategy_csv_flow.py | Strategie met CSV input | OK | Randgevallen toevoegen |
| test_strategy_main.py | End-to-end strategie test | Skip in CI | Behouden (optioneel draaien) |

---

## 🗂️ tests/live/

| Bestand | Beschrijving | Status | Actie |
|----------|--------------|--------|-------|
| test_dummy_snapshot.py | Test dummy snapshot mechanism | OK | Behouden |
| test_live_flow.py | End-to-end live flow test | Verwacht ticks i.p.v. candles | Fixen naar candle-logica |
| test_replay_flow.py | Replay van live data | OK | Behouden |
| test_strategy_csv_flow.py | Strategie run met CSV input | OK | Randgevallen toevoegen |

> 🔄 README was bijna volledig, maar is nu aangevuld met tick/candle uitleg.

---

## 🗂️ tests/data/

| Bestand | Beschrijving | Status | Actie |
|----------|--------------|--------|-------|
| test_candles_theta.csv | Theta candles testdata | OK | Valideren kolomnamen |
| test_candles_tfuel.csv | TFuel candles testdata | OK | Valideren kolomnamen |
| test_ticks.csv | Tick data testset | OK | Nagaan of nog nodig bij candlelogica |

> ✅ `tests/data/` README is volledig en actueel.

---

## 🗂️ Losse bestanden buiten mappen

| Bestand | Beschrijving | Status | Actie |
|----------|--------------|--------|-------|
| test_ratio_5m_snapshot.py | Snapshot test 5m ratio | OK | Labelen of verplaatsen |
| test_theta_5m_snapshot.py | Snapshot test 5m theta | OK | Labelen of verplaatsen |
| test_tfuel_5m_snapshot.py | Snapshot test 5m tfuel | OK | Labelen of verplaatsen |

---

## 📌 Samenvatting Acties

- [ ] BB-strategy test uitbreiden (`unit/`)
- [ ] Live flow aanpassen naar candle-logica (`live/`)
- [ ] Webhook mocking corrigeren naar juiste importlocatie (`unit/`)
- [ ] Snapshot tests verplaatsen of labelen
- [ ] Testdata valideren op kolomnamen en consistentie
- [x] README `unit/` gecontroleerd en actueel
- [x] README `integration/` bijgewerkt
- [x] README `live/` bijgewerkt
- [x] README `data/` gecontroleerd en actueel
