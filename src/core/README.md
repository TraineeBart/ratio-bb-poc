# 📦 Core Layer

## Doel

De `core/` map bevat de **handelslogica** van Ratio-BB-POC.  
Dit is de enige laag die bepaalt of er een BUY of SELL wordt gegenereerd, volledig los van infrastructuur of uitvoeringsdetails.

---

## Inhoud

| Bestand | Functie |
|----------|--------|
| `signal_generator.py` | Genereert `trade_signal` events op basis van ratio, voorraad en candledata |
| `candle_handler.py` | Verwerkt raw candles naar gestructureerde inputs voor de signaalgenerator |

---

## Combitrade-logica

- De beslissing om te BUY-en of SELL-en is afhankelijk van:
   - De huidige voorraad THETA en TFUEL
   - De ratio tussen deze twee munten
- De core kiest nooit absolute richtingen; alles is voorraadgedreven.

---

## Afspraken

- Alleen pure functies en dataclasses
- Geen imports van `infra`, `batching`, `executor` of `orchestration`
- Geen side-effects (geen print, logging of netwerk)
- Alle output gaat via eventreturn aan orchestration

---

## Status

Actief – v1.1  
Klaar voor uitbreiding naar geavanceerdere trade-criteria in volgende iteraties.