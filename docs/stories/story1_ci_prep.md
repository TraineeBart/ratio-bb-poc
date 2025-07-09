

# Story 1: CI-Data Preparation – Genereren historische dataset

**Rol:** Quality-EngineerGPT

## Context & Doel
In onze CI-pijplijn moeten end-to-end backtests automatisch kunnen draaien zonder handmatige data-uploads. Daarom zetten we vóór de pytest-fase een stap in om een historische CSV (`data/historical.csv`) aan te maken uit onze golden acceptance-bestanden.

## Taken
1. Voeg in `.github/workflows/ci.yml` vóór de test-stap een job-stap toe:
   ```yaml
   - name: Prepare historical data
     run: |
       mkdir -p data
       cp acceptance/expected_full_backtest.csv data/historical.csv
   ```
2. Verifieer dat `data/historical.csv` bestaat in de CI-omgeving vóór `pytest`.
3. Documenteer deze stap in `docs/CI_Coverage_Gates.md` onder “Data Preparation”.
4. Run `pytest tests/test_full_backtest_flow.py` en controleer dat de E2E-backtest slaagt.

## Acceptatiecriteria
- De CI-job vóór `pytest` maakt `data/historical.csv` aan en stopt niet op een ontbrekend bestand.
- `pytest tests/test_full_backtest_flow.py` loopt groen zonder errors.
- De stap is gedocumenteerd in `CI_Coverage_Gates.md` met voorbeeld YAML.

---

# Story 1: CI-Data Preparation – Resultaat

**Afgerond door:** Quality-EngineerGPT  
**Datum:** 2025-06-27

## Wat is bereikt
- In `.github/workflows/ci.yml` is de stap “Prepare historical data” toegevoegd en draait succesvol in CI.
- `data/historical.csv` wordt correct gegenereerd uit `acceptance/expected_full_backtest.csv` vóór het uitvoeren van pytest.
- `pytest tests/test_full_backtest_flow.py` slaagt zonder fouten.
- Documentatie in `docs/CI_Coverage_Gates.md` is bijgewerkt met de Data Preparation instructies.

## Leerpunten & Aanbevelingen
- Overweeg in de toekomst parameterisatie van de data-bron (niet alleen de acceptance directory).
- Voeg validatie toe om de timestamp in `historical.csv` te controleren voor regressie.