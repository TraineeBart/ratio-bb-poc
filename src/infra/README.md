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
| `ws_client_adapter.py` | Adapter voor WebSocket clients. Ondersteunt live-mode via KuCoin met token-auth en sim-mode via MockWSClient. |

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
- WebSocket-verbindingen worden opgezet via `ws_client_adapter.py`, inclusief dynamisch ophalen van tokens via KuCoin REST API (`bullet-public`).

---

## Afspraken

- **Infra** bevat geen handelslogica.
- I/O gebeurt altijd via `EventWriter`.
- Externe afhankelijkheden worden via dependency injection toegevoegd.
- Geschikt voor uitbreiding met storage-clients of externe API-koppelingen.
- WebSocket-clients moeten fallback en reconnect logic bevatten voor robuustheid.

---

## Status

Actief – v1.1  
Klaar voor uitbreiding naar live-API adapters of opslagconnecties.

## Update 2025-07-15

- `WSClientAdapter` is volledig aangepast naar `async` gedrag.
- Threading is verwijderd. WebSocket draait nu in dezelfde asyncio-eventloop als de pipeline.
- Ping/pong en reconnects zijn getest en stabiel bij live gebruik.

```
- Exponential backoff toegevoegd bij reconnects (1s → max 30s).
- Ping-loop stopt veilig bij gesloten socket, voorkomt race conditions.
- Alle KuCoin-specifieke WS-logica is vastgelegd in `docs/infra/kucoin_ws_notes.md`.
```