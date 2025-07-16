# 🎛️ Orchestration Layer

## Doel

De `orchestration/` layer coördineert de volledige pipeline-flow van Ratio-BB-POC:

```
Candle → Signaal → Batch → Executor → Outbox → Webhook
```

Deze laag bevat geen handelslogica of infrastructuurcode, maar verbindt de componenten.

---

## Inhoud

| Bestand | Functie |
|----------|---------|
| `run_once.py` | Voert één pipeline-cyclus uit (5m candle, testbaar) |
| `run_all.py` | (Backlog) Doorlopende loop voor live trading of simulatie |

---

## Verantwoordelijkheid

- Ontvangt candles of ticks als input
- Roept `SignalGenerator` aan voor signalen
- Batches signalen via `BatchBuilder`
- Roept `Executor` aan voor batchverwerking
- Schrijft output via `EventWriter` naar de outbox

---

## Afspraken

- **Geen business logica** in deze laag
- Gebruik **dependency injection** voor:
   - Writer (bijv. EventWriter)
   - Executor (batch of real)
- Scheiding van concerns: orchestration is alleen coördinatie

---

## Status

- Actief – versie 1.0
- Klaar voor uitbreiding naar `run_all.py` live loop in volgende iteratie

## Update 2025-07-15

- `run_live` gebruikt nu `await ws.start()` i.p.v. `ws.start()` om dubbele eventloops te voorkomen.
- De WebSocket-client draait volledig in de hoofd-eventloop zonder threading.
- Tick-logging is verplaatst naar `DEBUG` niveau voor betere overzichtelijkheid tijdens live runs.
- Exponential backoff toegevoegd aan WebSocket reconnect-logica.
- Ping-loop draait asynchroon en stopt netjes bij disconnects.
- Orchestrator is nu volledig compatibel met de verbeterde infra WS-client.