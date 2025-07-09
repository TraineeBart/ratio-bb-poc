

# Iteratie 3 – Quality-EngineerGPT

**Datum:** 2025-06-27  
**Rol:** Quality-EngineerGPT  
**Versie:** v1.0  

## Samenvatting  
Deze sessie richtte zich op het uitbreiden van testcoverage voor bestaande modules, het toevoegen van integratietests en het stabiliseren van de CI-pijplijn.

## Bereikt  
1. **Coverage-analyse**  
   - Parser (`src/parser/kucoin_parser.py`): 100% coverage door tests voor missing/extra velden en datatype-validatie.  
   - WS-modules (`src/ws_client.py` & `src/ws_replay.py`): tests cover 94% en 100%.  
2. **Integratietest backtest-flow**  
   - Tests voor full backtest-flow (`tests/test_full_backtest_flow.py`) uitgebreid met live- vs replay-route, golden files validatie.  
   - Coverage voor `src/run_once.py` replay-branch naar 62%.  
3. **CI & Documentation**  
   - CI-pipeline geüpdatet met integratietest-stappen en golden files voorbereiding.  
   - README-testsectie bijgewerkt met instructies voor golden files.  

## Vragen & Volgende Stappen  
- Voer full backtest integratietest zonder replay uit en vergelijk met golden data.  
- Verhoog coverage van `src/run_once.py` naar ≥ 80% voor live-branch.  
- Schrijf unit-tests voor `src/strategy.py` core functies (compute_bbands, detect_signal).  
- Stel coverage-gates in voor nieuwe tests en modules.