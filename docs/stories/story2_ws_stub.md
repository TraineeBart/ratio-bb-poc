# Story 2: WSClient Stub Alignment – Tests en Signature Fix

**Rol:** DeveloperGPT

## Context & Doel
Tijdens end-to-end backtest-tests bleek de `stub_ws_client` fixture in `tests/test_full_backtest_flow.py` een foutieve constructor-signature te gebruiken. De product-API verwacht `WSClient(symbols, callback)`, maar de stub miste de `callback` parameter. Hierdoor faalden de live-mode tests.

## Taken
1. Pas de `stub_ws_client` fixture aan in `tests/test_full_backtest_flow.py`:
   - Definieer `DummyWSClient(symbols, callback)` en sla `callback` op.
   - Zorg dat `start()` calls `callback` met test-ticks.
2. Update eventuele andere tests met gelijksoortige stubs (bijv. `tests/test_ws_client_callback.py`) om de nieuwe signature te gebruiken.
3. Verifieer dat `tests/test_full_backtest_flow.py` en alle WS-client tests groen draaien.
4. Controleer de coverage: WSClient-module moet ≥ 90% blijven.

## Acceptatiecriteria
- `pytest tests/test_full_backtest_flow.py` en WS-client tests (`tests/test_ws_client_*.py`) lopen groen zonder TypeError.
- Stub-signature klopt, en callback wordt daadwerkelijk aangeroepen in de fixture.
- Coverage voor `src/ws_client.py` blijft ≥ 90%.

---

# Story 2: WSClient Stub Alignment – Resultaat

**Afgerond door:** DeveloperGPT  
**Datum:** 2025-06-28

## Wat is bereikt
- `stub_ws_client` fixture is aangepast naar `DummyWSClient(symbols, callback)`.
- Alle relevante tests zijn bijgewerkt en draaien groen.
- Coverage voor `src/ws_client.py` is gehandhaafd op ≥ 94%.
- E2E live-mode backtest tests slagen zonder errors.

## Leerpunten & Aanbevelingen
- Zorg bij toekomstige fixtures altijd voor overeenstemming met de constructor-signature.
- Documenteer de stub-implementatie in een test-helper voor hergebruik.

