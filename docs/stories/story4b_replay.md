

# Story 4b: WSReplay & CSV-Parsing – Robuuste Replay Implementatie

**Rol:** DeveloperGPT

## Context & Doel
Om historische backtests betrouwbaar en reproduceerbaar te maken, speelt `WSReplay` CSV-bestanden af als tick-events. De huidige implementatie mist robuuste parsing, error-handling en consistentie met de live WebSocket-feed. Deze story richt zich op het verbeteren van `WSReplay`, de CSV-parser en bijbehorende tests.

## Taken
1. Implementeer in `src/ws_replay.py`:
   - Constructor-signature `WSReplay(csv_path: str, callback: Callable[[dict], None], speed: float = 1.0)`
   - Robuuste parsing van kolommen, inclusief `timestamp` (ISO-formaat) en `volume`.
   - Optionele kolommen (bijv. `nk`) negeren zonder errors.
   - Gebruik `pandas.read_csv()` met `parse_dates=['timestamp']` en `.sort_values()`.
2. Voeg methoden `start()` en `stop()` toe met achtergrond-threading voor replay.
3. Maak unit-tests in `tests/test_ws_replay.py` voor:
   - Afspelen van een korte CSV met 3 ticks.
   - Vervolg van parsing bij ontbrekende kolom (mismatched columns).
   - Correcte aanroep van `callback` per tick.
4. Update of maak fixtures in `tests/conftest.py` indien nodig voor tijdelijke CSV-bestanden.
5. Verifieer dat tests groen draaien en coverage voor `src/ws_replay.py` ≥ 90%.

## Acceptatiecriteria
- `pytest tests/test_ws_replay.py` slaagt groen voor alle scenario’s.
- CSV-replay flow werkt zonder exceptions bij extra/ontbrekende kolommen.
- Coverage voor `src/ws_replay.py` ≥ 90%.

---

# Story 4b: WSReplay & CSV-Parsing – Resultaat

**Afgerond door:** DeveloperGPT  
**Datum:** 2025-06-26

## Wat is bereikt
- `WSReplay` ondersteunt nu de juiste constructor-signature en optionele `speed` parameter.
- CSV-parsing is robuust gemaakt met `parse_dates=['timestamp']` en kolomvalidatie.
- `start()` en `stop()` methoden beheren de replay-thread correct.
- Unit-tests voor replay en edge-cases draaien groen.
- Coverage voor `src/ws_replay.py` bedraagt 100%.

## Leerpunten & Aanbevelingen
- Documenteer de configuratie-opties van `WSReplay` in `ws_flow.md`.
- Overweeg extra tests voor performance bij grote CSV-bestanden.