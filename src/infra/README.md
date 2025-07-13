# 🔧 Infrastructure Layer

## Doel

De `infra/` map bevat de infrastructuurlaag van Ratio-BB-POC.  
Dit is de output- en interfacinglaag tussen de core-logica en de buitenwereld.

---

## Inhoud

| Bestand | Functie |
|----------|--------|
| `event_writer.py` | Schrijft events naar `outbox/events.jsonl`. Ondersteunt `trade_signal` en `batch_result` events. |
| `ws_client_adapter.py` | Adapter voor WebSocket clients. Kan live-data ophalen of mock-data leveren voor tests. |

---

## Eventtypen

| Event Type | Gebruik |
|------------|---------|
| `trade_signal` | Losse signalen van core naar outbox/webhook |
| `batch_result` | Batch-uitkomsten van executor naar outbox/webhook |

---

## Werking

- Events worden altijd geschreven naar `outbox/events.jsonl` als JSON-lines.
- De `webhook_service` leest deze outbox en stuurt ze door naar HTTP endpoints.

---

## Afspraken

- **Infra** bevat geen handelslogica.
- I/O gebeurt altijd via `EventWriter`.
- Externe afhankelijkheden worden via dependency injection toegevoegd.
- Geschikt voor uitbreiding met storage-clients of externe API-koppelingen.

---

## Status

Actief – v1.1  
Klaar voor uitbreiding naar live-API adapters of opslagconnecties.