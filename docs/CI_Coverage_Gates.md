# CI Coverage Gates & Rapportage

Dit document beschrijft de configuratie en het onderhoud van coverage-gates in onze GitHub Actions CI-pipeline.

## Doel
- Borgen dat kritische modules minimaal de gestelde testdekking behalen.
- Automatisch falen van de CI-build wanneer een module onder de drempel zakt.
- Helder inzicht geven in per-module coverage-statistieken.

## Modules & Drempels
| Module                        | Pad                              | Minimale Coverage |
|-------------------------------|----------------------------------|-------------------|
| Strategy                      | `src/strategy.py`                | 90%               |
| Run-once                      | `src/run_once.py`                | 80%               |
| Executor                      | `src/executor.py`                | 80%               |
| KuCoin-client                 | `src/client/kucoin_client.py`    | 80%               |
| WS-client                     | `src/ws_client.py`               | 80%               |
| WS-replay                     | `src/ws_replay.py`               | 80%               |
| Parser                        | `src/parser/`                    | 80%               |
| Models                        | `src/models/`                    | 80%               |
| Orchestrator                  | `src/orchestrator.py`            | 80%               |

## Data Preparation
- Voor de full-backtest E2E-tests moet altijd `data/historical.csv` aanwezig zijn.
- Voeg in `.github/workflows/ci.yml` vóór de pytest-stap een shell-opdracht toe:
  ```yaml
  - name: Prepare historical data
    run: |
      mkdir -p data
      cp acceptance/expected_full_backtest.csv data/historical.csv
  ```
- Hiermee wordt tijdens elke CI-run de directory `data` aangemaakt en het bestand `historical.csv` gevuld met de golden file uit `acceptance`.

> **Tip:** Bij een gate-failure geeft de CI automatisch een melding met de behaalde dekking en de vereiste drempel.

## Hoe werkt het?
1. De CI-pipeline voert `pytest --cov=src --cov-report=xml:coverage.xml --cov-report=term-missing` uit.
2. Voor elke module in de matrix wordt `coverage report --fail-under=<drempel> --include=<pad>` aangeroepen.
3. Als een module onder de drempel zit, faalt de build met een duidelijke foutmelding.

## Nieuwe module toevoegen
1. In `.github/workflows/ci.yml` voeg je in de `matrix.coverage-gates` sectie een regel toe met pad en percentage, bijvoorbeeld:
   ```yaml
   matrix:
     coverage-gates:
       src/new_module.py: 75
   ```
2. Werk deze documentatie bij en voeg de module & drempel toe in de tabel.
3. Test lokaal met:
   ```bash
   pytest --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing
   ```
4. Commit, push en open een PR; de CI valideert automatisch de nieuwe gate.

## Troubleshooting
- Bekijk in de CI-logs de daadwerkelijke coverage voor het falende module-pad.
- Voeg extra tests toe of pas de drempel aan om de gate te halen.