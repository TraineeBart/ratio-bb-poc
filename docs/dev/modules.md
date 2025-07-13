# 📦 Modules Overzicht

## Webhook Service

De **webhook_service** verstuurt `trade_signal` events vanuit de outbox naar een extern HTTP endpoint.

### Bestand
`src/webhook_service/webhook_service.py`

### Functie
- Leest `outbox/events.jsonl`
- Filtert op `event_type: trade_signal`
- Verstuurt deze events via HTTP POST naar een extern endpoint
- Robuust: fouten worden gelogd, service crasht niet

### Usage

Start de webhook-service met:

```bash
python src/webhook_service/webhook_service.py --endpoint http://localhost:9000/webhook
```

⚠ **Let op:**  
Poort 8000 is mogelijk al in gebruik in deze omgeving.  
Gebruik daarom bijvoorbeeld poort **9000** of een andere vrije poort voor je webhook endpoint.

### Testen

Er is een integratietest beschikbaar in:

`tests/integration/test_webhook_service.py`

De HTTP-call wordt daarin gemockt via `monkeypatch`.

---

## Batch Result Events

De Executor module schrijft na batch-executie een `batch_result` event naar de outbox.

### Bestand
`src/executor/execute_batch.py`

### Functie
- Verwerkt batches van signalen
- Maakt per batch een event aan met `type: batch_result`
- Schrijft deze events naar `outbox/events.jsonl` via `EventWriter`
- Events zijn compatible met de bestaande webhook flow

### Eventstructuur

| Veld        | Uitleg                          |
|-------------|--------------------------------|
| `batch_id`  | Uniek ID per batch              |
| `type`      | `batch_result`                  |
| `signals`   | Lijst van signalen met status   |
| `timestamp` | ISO 8601 tijd van verwerking    |

### Testen

De pipeline wordt getest via:

`tests/integration/test_batch_executor.py`