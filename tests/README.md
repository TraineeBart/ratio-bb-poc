# 🧪 Testoverzicht – Ratio BB POC

Dit bestand beschrijft de verschillende testtypes binnen dit project, inclusief waarom bepaalde tests zijn uitgeschakeld en hoe ze in de toekomst weer kunnen worden geactiveerd.

---

## ✅ Actieve tests

- `test_orchestrator.py`: test de main orchestrator flow en validatie van gegenereerde signalen.
- `test_bb_strategy.py`: valideert signalen op basis van de BB-ratio-strategie.
- `test_output_writer.py`: controleert het correct wegschrijven van bestanden.
- `test_enrich.py`: test de berekening van RSI en SMA-indicatoren.
- `test_theta_5m_snapshot.py`: snapshottest van kolomnamen van de verrijkte 15m dataset van Theta.

## 🟡 Tijdelijk uitgeschakeld

Deze tests zijn momenteel genegeerd in CI vanwege specifieke issues. Zie issue #42.

| Bestand                         | Reden                                                                 |
|----------------------------------|------------------------------------------------------------------------|
| `test_backtest_flow.py`         | Timezone mismatch bij timestamp-vergelijking tussen output en golden file |
| `test_full_backtest_flow.py`    | Symbol/price mismatch door gebruik van verouderde sample-data          |
| `test_strategy_main.py`         | Verwacht `"signal"` in stdout, maar huidige implementatie print JSON-object |

⚠️ Let op: sommige uitgeschakelde tests gebruiken legacy-modules zoals `strategy.py`. Deze modules zijn verouderd en worden mogelijk volledig vervangen door nieuwe implementaties in `src/strategies/`. Tijdens een toekomstige code review moet nadrukkelijk worden beoordeeld of deze oude modules en bijbehorende tests definitief verwijderd of gemigreerd moeten worden.

## 📌 Herinnering

- Deze tests moeten opnieuw worden geactiveerd zodra:
  - De golden files zijn geüpdatet met consistente timezone-timestamps.
  - De CLI-output van `strategy.py` is geharmoniseerd met wat de test verwacht.
  - De `run_once` backtest flow werkt met recente en representatieve data.
- De `ema_2` test in `test_strategy_main.py` is vervangen door `ema_9`. Dit moet teruggezet worden zodra de definitieve `strategy.py` klaar is. Zie issue #42.
- Coverage-checks zijn tijdelijk uitgeschakeld tijdens de migratie naar modulaire structuur. Zodra de modules in `src/` zijn gestabiliseerd, worden de `--cov` en `fail-under` instellingen opnieuw geactiveerd. Zie commit <TODO> voor referentie.

---

## 🔧 Test draaien

Gebruik:

```bash
pytest -v --cov=src --cov-report=term-missing
```

CI-configuratie: `.github/workflows/ci.yml`

---

Laatste update: juli 2025