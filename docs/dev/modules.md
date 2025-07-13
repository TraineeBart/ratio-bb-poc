# 📦 Modules Overzicht – Ratio-BB-POC

---

## 🔧 Kernmodules

| Module | Beschrijving |
|---------|--------------|
| **core/** | Bevat de handelslogica: signaalgeneratie, voorraadbeheer |
| **infra/** | Schrijft events naar de outbox via `EventWriter`. Verzorgt de koppeling naar de webhook-service |
| **orchestration/** | Stuurt de pipeline aan via `run_once.py` |
| **batching/** | Bundelt individuele signalen tot batches op basis van liquiditeitswindow en voorraad |
| **executor/** | Verwerkt batches en geeft resultaten terug |
| **webhook_service/** | Verstuurt outbox-events (zowel `trade_signal` als `batch_result`) naar HTTP endpoints |

---

## 🔄 Dataflow

```mermaid
graph LR
    A[Candle Data] --> B[Signal Generator (core)]
    B --> C[BatchBuilder (batching)]
    C --> D[Executor (executor)]
    D --> E[EventWriter (infra)]
    E --> F[Webhook Service (webhook_service)]
```

---

## 📂 Bestandsoverzicht

### **Webhook Service**

- **Bestand**: `src/webhook_service/webhook_service.py`
- **Doel**: 
  - Leest `outbox/events.jsonl`
  - Filtert op `trade_signal` en `batch_result`
  - Verstuurt via HTTP POST
  - Robuuste foutafhandeling

#### Usage:

```bash
python src/webhook_service/webhook_service.py --endpoint http://localhost:9000/webhook
```

#### Test:

- `tests/integration/test_webhook_service.py`

---

### **Batch Result Events**

- **Bestand**: `src/executor/execute_batch.py`
- **Doel**: 
  - Verwerkt batches
  - Schrijft `batch_result` events naar de outbox via `EventWriter`

#### Eventstructuur:

| Veld        | Uitleg                          |
|-------------|--------------------------------|
| `batch_id`  | Uniek ID per batch              |
| `type`      | `batch_result`                  |
| `signals`   | Lijst van signalen met status   |
| `timestamp` | ISO 8601 tijd van verwerking    |

#### Test:

- `tests/integration/test_batch_executor.py`

---

## 📝 Documentatie

Voor uitgebreide beslissingen en ontwerpkeuzes, zie:

- `/docs/decisions/`
- `/docs/reviews/`
- `/docs/project-taskboard.md`