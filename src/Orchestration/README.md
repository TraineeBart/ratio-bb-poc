# 🎛️ Orchestration Layer

## Doel
Stuurt de flow aan van signalen → batches → executor → eventwriter.

## Inhoud
- `run_once.py` – main orchestration loop
- `run_all.py` – (toekomstig) loop over meerdere runs

## Afspraken
- Alleen orchestratie: geen business logica of infrastructuur
- Gebruik dependency injection voor writers en executor

## Status
Actief – v1.0
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