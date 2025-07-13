# 📁 tests/data/

Deze map bevat testdatasets in CSV-formaat die gebruikt worden voor offline tests van de tradingstrategie. 
De bestanden in deze map simuleren tick- of candledata om E2E-flows te testen zonder live verbinding of webhooks.

## Voorbeelden van gebruik
- `test_strategy_csv_flow.py` gebruikt `test_ticks.csv` om de strategie-module te testen.
- `test_replay_flow.py` kan een volledige candle-reconstructie simuleren op basis van deze data.
- `test_candles_theta.csv` en `test_candles_tfuel.csv` worden gebruikt in tests waarin de signalen gegenereerd worden op basis van candledata in plaats van losse ticks.

## Richtlijnen
- Voeg hier alleen synthetisch gegenereerde of anoniem gemaakte datasets toe.
- Gebruik duidelijke bestandsnamen zoals `test_ticks.csv`, `sample_replay_data.csv`.
- Vermijd productiedata in deze map.
- Houd testcandles synchroon met het formaat dat de live flow genereert (kolomnamen, tijdstempelformaat).

## 🔁 Opmerking over kolomnamen

De kolom `timestamp` in deze testbestanden komt overeen met de kolom `start_ts` in de live candle-aggregatie flow.  
We hebben dit aangepast voor compatibiliteit met `load_csv_as_dicts()` tijdens het testen. Houd dit verschil in gedachten bij synchronisatie van live- en testdata.

## Laatst bijgewerkt
2025-07-09
