


# 🧪 Test – Webhook verwerking batch_result events

## Doel
Verifieer dat de webhook-service correct omgaat met `batch_result` events en deze via HTTP POST verzendt.

## Testscenario

1️⃣ Maak een dummy `batch_result` event aan:

```json
{"event_type":"batch_result","batch_id":"test-123","signals":[{"signal":"BUY","status":"executed"}],"timestamp":"2025-07-13T16:00:00Z"}
```

2️⃣ Plaats dit event in `outbox/events.jsonl` samen met bestaande `trade_signal` events.

3️⃣ Start de webhook-service met een lokale test endpoint, bijvoorbeeld via `http://webhook.site` of een mock server.

4️⃣ Controleer de logs van de webhook-service:

```
INFO Versturen batch_result: batch_id=test-123, aantal signalen=1
```

5️⃣ Verifieer dat het HTTP POST verzoek correct is verzonden naar de endpoint.

## Verwachte uitkomst

- Beide eventtypes (`trade_signal` en `batch_result`) worden verstuurd via HTTP POST.
- De webhook logt het aantal signalen in de batch.

## Uitbreiding

- In een volgende iteratie deze test automatiseren in `tests/integration/test_webhook_service.py` met `monkeypatch` voor `requests.post`.