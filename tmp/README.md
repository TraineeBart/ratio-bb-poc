

# tmp/

Deze map wordt gebruikt voor tijdelijke runtime-bestanden die automatisch worden gegenereerd tijdens het uitvoeren van de container of testflows.

## Bestanden
- `output.csv` — Bevat gegenereerde signalen of ticks tijdens live- of replay-tests.
- `candles_THETA-USDT.log` — Logbestand met gegeneerde 5m candles voor THETA.
- `candles_TFUEL-USDT.log` — Logbestand met gegeneerde 5m candles voor TFUEL.

## Richtlijnen
- Bestanden in deze map worden niet gecommit naar git (zie `.gitignore`).
- De inhoud mag op elk moment veilig verwijderd worden.
- Gebruik deze map niet voor permanente opslag of testdata.