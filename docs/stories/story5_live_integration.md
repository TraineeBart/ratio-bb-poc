

# Story 5: Live Data Integratie & Staging

**Rol:** DeveloperGPT

## Context & Doel
Het project is klaar voor live-mode: `run_once.py` respecteert `MODE=live`, WSClient en CandleAggregator werken, en tests voor live-override lopen groen. Nu willen we met echte KuCoin-WebSocket-ticks in staging de end-to-end flow valideren, inclusief CSV-logging, webhook-verzending en foutafhandeling.

## Taken
1. Zet in de staging-omgeving de environment variable:
   ```bash
   export MODE=live
   ```
2. Start `run_once.py` zonder `--replay` en controleer dat de live-branch actief is.
3. Bevestig in de logs dat WSClient verbindt en subscribed op symbolen `THETA-USDT` en `TFUEL-USDT`.
4. Voor elke binnenkomende tick:
   - Schrijf een nieuwe regel naar `tmp/output.csv` met `timestamp,symbol,price,signal`.
   - Verstuur een JSON POST naar de webhook-URL.
5. Simuleer netwerkonderbreking en controleer dat WSClient automatisch reconnect:
   - Koppel de WebSocket-poort tijdelijk los en observeer reconnect-logs.
6. Inject malformed tick-data (bijv. zonder `price`) en controleer dat er een foutmelding wordt gelogd, maar de flow niet stopt.
7. Laat de live-flow **10 minuten** draaien:
   - Controleer dat `tmp/output.csv` minimaal **5 non-HOLD** signalen bevat.
   - Verifieer dat de webhook-stub minstens **5 POST-requests** ontvangt.
8. Update `README.md` met stap-voor-stap instructies voor live-mode setup, inclusief `MODE`, env-vars en logs.

## Acceptatiecriteria
- Live-mode draait succesvol zonder errors en reconnects na disconnect.
- Minimaal 5 non-HOLD signalen en 5 webhook-POSTs binnen 10 minuten.
- `tmp/output.csv` en webhook payloads voldoen aan het verwachte formaat.
- README bevat actuele live-mode setup instructies.

---

# Story 5: Live Data Integratie & Staging – Resultaat

**Afgerond door:** DeveloperGPT  
**Datum:** 2025-07-07

## Wat is bereikt
- Live-mode draait in staging, WSClient verbindt, subscribe en herstart na netwerkfouten.
- CSV- en webhook-stromen werken zoals beschreven: 5+ non-HOLD signalen en POSTs binnen 10 minuten.
- Foutafhandeling bij malformed ticks gelogd, maar flow blijft actief.
- README is bijgewerkt met live-mode setup.

## Leerpunten & Aanbevelingen
- Maak healthchecks en metrics-endpoint voor monitoring.
- Documenteer procedure voor het starten en debuggen van live-mode in staging.