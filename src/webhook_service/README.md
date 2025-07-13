


# 📡 Webhook Service

Deze module verstuurt `trade_signal` events uit de outbox naar een extern HTTP endpoint.

## 📂 Bestand

`webhook_service.py`

## ⚙️ Functionaliteit

- Leest `outbox/events.jsonl`
- Filtert alleen `trade_signal` events
- Verstuurt deze via HTTP POST naar een extern endpoint
- Fouten worden gelogd, de service blijft draaien (fail-safe)

## 🚀 Usage

Start de webhook-service met:

```bash
python webhook_service.py --endpoint http://localhost:9000/webhook
```

### Parameters

| Parameter   | Beschrijving                               | Default                |
|-------------|--------------------------------------------|------------------------|
| `--outbox`  | Pad naar het outbox-bestand (`.jsonl`)     | `outbox/events.jsonl`   |
| `--endpoint`| Doel-URL voor de webhook POST-calls        | *Verplicht opgeven*     |

⚠ **Let op:** Gebruik bij voorkeur poort **9000** of een andere vrije poort. Poort 8000 is vaak al in gebruik.

## 🧪 Testen

De module is getest via:

`tests/integration/test_webhook_service.py`

Mocking gebeurt met `monkeypatch`, zodat er geen echte HTTP-calls plaatsvinden.

---