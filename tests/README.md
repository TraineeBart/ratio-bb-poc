# 🧪 Testoverzicht – Ratio BB POC

Dit bestand beschrijft de verschillende testtypes binnen dit project, inclusief waarom bepaalde tests zijn uitgeschakeld en hoe ze in de toekomst weer kunnen worden geactiveerd.

---

## ✅ Actieve tests

- `test_orchestrator.py`: test de main orchestrator flow en validatie van gegenereerde signalen.
- `test_bb_strategy.py`: valideert signalen op basis van de BB-ratio-strategie.
- `test_output_writer.py`: controleert het correct wegschrijven van bestanden.
- `test_enrich.py`: test de berekening van RSI en SMA-indicatoren.
- `test_strategy_csv_flow.py`: valideert of de strategie correcte signalen genereert op basis van tick- en candledata in CSV-vorm.
- `test_batch_executor.py`: valideert de integratie van BatchBuilder en Executor, inclusief batching van signalen en uitvoering van batches.

## 🟡 Tijdelijk uitgeschakeld

Deze tests zijn momenteel genegeerd in CI vanwege specifieke issues. Zie issue #42.

| Bestand                         | Reden                                                                       |
|----------------------------------|----------------------------------------------------------------------------|
| `test_backtest_flow.py`         | Timezone mismatch bij timestamp-vergelijking tussen output en golden file   |
| `test_full_backtest_flow.py`    | Symbol/price mismatch door gebruik van verouderde sample-data               |
| `test_strategy_main.py`         | Verwacht `"signal"` in stdout, maar huidige implementatie print JSON-object |

### 🧪 Snapshot-tests alleen lokaal actief

Snapshot-tests zoals `test_ratio_5m_snapshot.py`, `test_tfuel_5m_snapshot.py` en `test_theta_5m_snapshot.py` slagen lokaal, maar falen in de CI-pipeline door ontbrekende testdata op GitHub.

👉 Deze tests zijn wél waardevol tijdens lokale ontwikkeling (bijv. op de VPS), maar worden bewust uitgesloten van CI totdat een representatief testdataset beschikbaar is in de repository of via mocking.

⚠️ Let op: sommige uitgeschakelde tests gebruiken legacy-modules zoals `strategy.py`. Deze modules zijn verouderd en worden mogelijk volledig vervangen door nieuwe implementaties in `src/strategies/`. Tijdens een toekomstige code review moet nadrukkelijk worden beoordeeld of deze oude modules en bijbehorende tests definitief verwijderd of gemigreerd moeten worden.

## 🧪 Enrichment tests

De enrichmenttests voor ratio, THETA en TFUEL (5m, 15m, 60m) zijn verplaatst naar `tests/unit/`.  
Ze testen of de gegenereerde kolommen (zoals RSI, SMA9, BB-ratio) correct zijn op basis van bekende CSV-input.

Deze tests zijn bedoeld als unit-validatie van `enrich_dataframe(...)` en vormen een aanvulling op de replaytests en integratietests.

## 📌 Herinnering

- Deze tests moeten opnieuw worden geactiveerd zodra:
  - De golden files zijn geüpdatet met consistente timezone-timestamps.
  - De CLI-output van `strategy.py` is geharmoniseerd met wat de test verwacht.
  - De `run_once` backtest flow werkt met recente en representatieve data.
- De `ema_2` test in `test_strategy_main.py` is vervangen door `ema_9`. Dit moet teruggezet worden zodra de definitieve `strategy.py` klaar is. Zie issue #42.
- Coverage-checks zijn tijdelijk uitgeschakeld tijdens de migratie naar modulaire structuur. Zodra de modules in `src/` zijn gestabiliseerd, worden de `--cov` en `fail-under` instellingen opnieuw geactiveerd. Zie commit 3616324 voor referentie.
- Snapshot-tests uitsluiten van CI is tijdelijk. Zie issue #43 voor het opnemen van testdata of alternatieve mocking.
- De `test_strategy_csv_flow.py` is toegevoegd als regressietest met vaste tick/candle samples. Houd deze test actueel bij wijzigingen aan `process_tick_with_candle(...)`.

## 🔄 Replay- en CSV-gebaseerde tests

- `test_strategy_csv_flow.py`: valideert of de strategie correcte signalen genereert op basis van tick- en candledata in CSV-vorm. Deze test vervangt deels live end-to-end tests voor logische validatie.

## 🔗 Batch- en Executor pipeline tests

- `test_batch_executor.py`: valideert de end-to-end pipeline van signalen naar batches, batch-executie en resultaatcontrole. Dit is een integratietest en bedoeld als brug tussen core-logica en uitvoering.

👉 Deze test is de basis voor verdere uitbreidingen van de executielaag, zoals parallelle verwerking of koppeling aan real trading clients.

---

## 🔧 Test draaien

Gebruik:

```bash
pytest -v --cov=src --cov-report=term-missing
```

CI-configuratie: `.github/workflows/ci.yml`

---
### 💡 Designbeslissing: Alleen `close` als prijsbron

De enrichmentlogica gebruikt standaard de kolom `close` voor alle prijsafhankelijke berekeningen.  
Andere kolommen (`open`, `high`, `low`) worden genegeerd tenzij expliciet anders gedefinieerd in een strategie.

✅ Hierdoor zijn enrichment, ratio-berekeningen en signal-generatie altijd synchroon qua prijsbron.


Laatste update: juli 2025

## End-to-End Live-Flow Tests

To write in-process live-mode tests:

1. **Call `run_once_main(max_ticks=N)`**  
   - This replaces the old CLI `main()` and stops after `N` ticks.
   - Example:
     ```python
     from src.run_once import run_once_main
     run_once_main(max_ticks=5)
     ```

2. **Use `DummyWSClient`**  
   - The `run_once_main` function references `WSClient`, which you can monkeypatch to `DummyWSClient` to emit controlled ticks.
   - Example:
     ```python
     from src.ws_client import DummyWSClient
     monkeypatch.setattr("src.run_once.WSClient", lambda symbols, cb: DummyWSClient(symbols, cb, max_ticks=5))
     ```

3. **Capture webhook calls via `http_server` fixture**  
   - Import the fixture from `tests/helpers.py`.
   - The fixture yields the server URL and populates `WebhookHandler.calls` with JSON payloads.
   - Example:
     ```python
     def test_live_flow(http_server, monkeypatch):
         monkeypatch.setenv("WEBHOOK_URL", http_server)
         # setup DummyWSClient...
         run_once_main(max_ticks=5)
         assert len(WebhookHandler.calls) == 5
     ```

4. **Run tests**  
   ```bash
   pytest tests/test_executor_integration.py tests/test_full_backtest_flow.py --maxfail=1 -q
   ```