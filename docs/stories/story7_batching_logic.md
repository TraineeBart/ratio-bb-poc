

# Story 7: Batching-Logic Module – Implementatie en Tests

**Rollen:**
- **Data-EngineerGPT:** Implementeert raw-data helper en unittests.
- **ArchitectGPT:** Ontwerpt API voor batch-slicing, schrijft unittests.

## Context & Doel
We splitsen grote limit-orders in beheersbare batches op basis van 24-uurs liquiditeit. Hiervoor gebruiken we de raw CSV’s:
- `/opt/tradingbot/data/{symbol_base}/5m/{symbol_base}-5m-full.csv` (met volume-kolom).

## Taken

### Data-EngineerGPT
1. **Implementatie** in `src/liquidity_helper.py`:
   - `get_average_liquidity(symbol: str, window_hours: int) -> float`
   - Lees raw CSV, converteer timestamp, filter op laatste `window_hours`, filter `volume > 0`, return gemiddelde volume of `0.0`.
2. **Unittests** in `tests/test_liquidity_helper.py`:
   - Happy path en edge-cases (bestand niet gevonden, lege data, negatieve `window_hours`).

### ArchitectGPT
1. **Implementatie** in `src/batching.py`:
   - `compute_batches(amount_in: float, avg_liquidity: float, max_batches: int = 10) -> List[float]`
   - Verdeel `amount_in` in ≤ `max_batches` gelijke delen; fallback bij zero/negatieve inputs.
2. **Unittests** in `tests/test_batching.py`:
   - Test batch-aantallen, som van batches en edge-cases.

## Acceptatiecriteria
- Coverage 100% voor `liquidity_helper.py` en `batching.py`.
- Alle unittests draaien groen.
- CI-pijplijn faalt niet na toevoeging van tests.