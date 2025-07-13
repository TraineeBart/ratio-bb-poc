# 📁 tests/integration/

Deze map bevat integratietests die meerdere onderdelen van het systeem samen testen. Denk aan end-to-end scenario's, live/replay testflows en batch-verwerking. De tests simuleren volledige runs en controleren zowel de gegenereerde output als eventuele side-effects zoals webhook-calls.

## Bestanden

- `test_full_backtest_flow.py`: Test het volledige pad van een live run met gesimuleerde WebSocket-ticks, inclusief output CSV-validatie.
- `test_market_api.py`: Test de wrapper rond de KuCoin API met gemockte HTTP-responses en validatie van filterlogica.
- `test_orchestrator_ratio.py`: Test of de orchestrator correct een batch-slice en simulatie uitvoert op basis van ratio-instellingen.
- `test_orchestrator_tfuel.py`: Test de volledige TFUEL-pipeline van verrijking tot CSV-output en foutafhandeling.
- `test_orchestrator_theta.py`: Test de orchestrator voor de THETA-pijplijn. Bevat tests voor de 'happy path' en foutafhandeling bij ontbrekende inputfiles. Doel is valideren dat verrijking, strategie en output integreren zoals verwacht.
- `test_strategy_csv_flow.py`: Valideert of een reeks candles correct wordt omgezet naar signalen binnen de strategy pipeline.
- `test_smoke_orchestrator.py`: Simpele smoke-test voor de TFUEL orchestrator `run_once` functie. Verifieert dat met dummy CSV-input het outputbestand wordt aangemaakt met juiste kolommen en signaalwaarden.
- `test_strategy_main.py`: Integreert het volledige strategy script in een end-to-end scenario. Laadt een kleine CSV als input, voert het script uit, en controleert of de output correct is. Momenteel staat deze test uitgeschakeld met `pytest.skip`, maar kan worden geactiveerd zodra de testdata en stabiliteit voldoende zijn.
- `test_executor_batching.py`: Test de batching-logica binnen de executor, inclusief slicing van orders volgens de liquiditeitsparameters.
- `test_executor_integration.py`: Integreert de executor met de volledige orderflow, controleert of batches correct worden verwerkt in de strategie.
- `test_webhook_service.py`: Test de webhook_service door trade_signal events uit een tijdelijke outbox te versturen naar een gemockt HTTP endpoint. Verifieert dat alleen de juiste events worden verstuurd zonder echte HTTP-calls.

## Verbeteringen op backlog

- De gebruikte inputbestanden (zoals `test_ticks.json`) staan nog niet in deze map. Overweeg ze hierheen te verplaatsen voor een betere afbakening.
- Snapshotvergelijkingen voor gegenereerde output kunnen worden toegevoegd zodra de structuur stabiel is.
- Validatie van orchestrator-uitvoer kan worden uitgebreid met asserts op logging of foutafhandeling.
- `test_strategy_main.py` kan weer ingeschakeld worden als de testdata en scripts stabiel zijn en is bedoeld voor integrale validatie van de strategy pipeline.

## Let op

Deze tests draaien niet als onderdeel van CI tenzij expliciet opgenomen in het testselectieproces.

## Verplaatste enrichment-tests

De enrichment-tests (`test_enrich_*.py`) zijn verplaatst naar deze map vanuit de root van `tests/`. Ze controleren of verrijkte CSV-bestanden voor ratio, TFUEL en THETA correct worden aangemaakt op verschillende tijdsintervallen (15m, 60m). Zie ook `tests/data/` voor de bijbehorende inputbestanden.