

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