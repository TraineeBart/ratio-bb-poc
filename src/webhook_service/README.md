# 📡 Webhook Service

De webhook-service verzendt events uit de outbox naar een extern HTTP endpoint.

---

## 📂 Bestand

`webhook_service.py`

---

## ⚙️ Functionaliteit

- Leest `outbox/events.jsonl`
- Verwerkt de volgende event types:
  - `trade_signal`
  - `batch_result`
- Verstuurt events via HTTP POST naar een extern endpoint
- Logt fouten per event, maar blijft draaien (fail-safe)

---

## 🗂️ Event Types

| Type           | Beschrijving |
|----------------|--------------|
| `trade_signal` | Losse BUY/SELL signalen |
| `batch_result` | Batch-uitkomsten met lijst van signalen en status per item |

---

## 🧾 Batch Result Structuur

```json
{
  "batch_id": "uuid-1234",
  "type": "batch_result",
  "signals": [
    {"id": "sig-1", "action": "BUY", "status": "executed"},
    {"id": "sig-2", "action": "SELL", "status": "executed"}
  ],
  "timestamp": "2025-07-13T12:00:00Z"
}
```

---

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

---

## 🔄 Foutafhandeling

- Netwerkfouten per event worden gelogd
- De service blijft draaien; mislukte events worden overgeslagen tenzij een retry-mechanisme is geactiveerd (backlog)

---

## 🧪 Testen

De module is getest via:

- `tests/integration/test_webhook_service.py`

Mocking gebeurt met `monkeypatch`, zodat er geen echte HTTP-calls plaatsvinden.

---