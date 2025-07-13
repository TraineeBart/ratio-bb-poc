# Ratio BB PoC

Refer to the project specification for details: `docs/PROJECT_SPEC.md`

Proof-of-concept for the Ratio BB trading strategy.

## Repository structure
- `src/`                       - core modules (strategy, executor, orchestrator, ws_client, ws_replay, liquidity_helper, batching)
- `scripts/`                   - utility scripts (data fetchers, audit_feed)
- `config/`                    - configuration files (config.yaml)
- `docs/`                      - project documentation (stories, architecture, configuration reference)
- `data/`                      - historical data feeds and enriched outputs
- `tmp/`                       - runtime CSV outputs
- `logs/`                      - application logs
- `.github/`                   - CI/CD workflows
- `docker-compose.yml`         - container orchestration
- `.env`                       - environment variables for local development

## KuCoin Fetcher

### Usage

```python
from src.kucoin_fetcher import fetch_klines

# Example: haal 100 candles van 5m-interval op voor THETA-USDT sinds een bepaalde timestamp
df = fetch_klines("THETA-USDT", "5m", start_ts=1620000000, limit=100)
print(df.head())
```

### Audit Feed Script
Controleer de kwaliteit van raw CSV feeds:
```bash
python3 scripts/audit_feed.py \
  --paths /opt/tradingbot/data/theta/5m/theta-5m-full.csv \
          /opt/tradingbot/data/tfuel/5m/tfuel-5m-full.csv
```

## Running the PoC

Volg deze stappen om de end-to-end live-flow in staging (of lokaal) te draaien:

1. **Activeer live-mode**  
   ```bash
   export MODE=live
   ```

2. **API-credentials**  
   Plaats je KuCoin-sleutels (`API_KEY`, `API_SECRET`, eventueel `API_PASSPHRASE`) in een `.env` in de project-root:
   ```
   API_KEY=<your_key>
   API_SECRET=<your_secret>
   API_PASSPHRASE=<your_passphrase>
   ```

3. **Start container**  
   ```bash
   docker-compose up --build -d
   ```

4. **Mount tmp/**  
   Zorg dat in `docker-compose.yml` je `./tmp:/app/tmp` hebt staan, zodat alle CSV’s ook op de host zichtbaar zijn.

5. **Logs monitoren**  
   Volg de live-logs met:
   ```bash
   docker logs ratio-live -f
   ```

6. **Healthcheck**  
   ```bash
   curl http://localhost:8080/health
   ```

7. **Ticks ophalen**  
   Haal de meest recente tick op voor een symbool:
   ```bash
   curl http://<host>:8000/ticks?symbol=THETA-USDT
   ```

8. **Output CSV**  
   Bekijk `tmp/output.csv` op je host voor realtime tick- en signal-logs.

 (… eventuele vervolg-secties …)

## Batching Configuration & Testing

The executor supports splitting large orders into manageable batches based on average liquidity.

### Configuration

In your `config/config.yaml` (or equivalent), add:

```yaml
batching:
  window_hours: <int>      # number of hours to calculate average liquidity
  max_batches: <int>       # maximum number of batches per order
```

- `window_hours`: period in hours over which liquidity is averaged.
- `max_batches`: maximum number of slices to split the order into.

### Running Tests

We have both unit and integration tests to validate batching behavior.

1. **Unit Tests**  
   Run tests for the executor batching logic:
   ```bash
   pytest tests/test_executor_batching.py --maxfail=1 -q
   ```

2. **Integration Test**  
   Validate end-to-end batching flow:
   ```bash
   pytest tests/test_executor_integration.py --maxfail=1 -q
   ```

3. **Full Test Suite with Coverage**  
   To run all tests and view coverage:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

## Documentation
See `docs/` for detailed guides:
- `docs/PROJECT_SPEC.md`      Project specification
- `docs/configuration.md`     Configuration reference
- `docs/architecture/`        Architecture diagrams and data model
- `docs/stories/`             Story definitions and progress
# Ratio-BB-POC

Proof-of-Concept voor de Ratio-BB tradingstrategie met modulaire event-driven architectuur.

---

## 🧭 Projectoverzicht

Ratio-BB-POC is een trading pipeline waarin signalen worden gegenereerd, gebatcht, uitgevoerd en via een eventflow worden gelogd of verzonden via webhook.  
De opzet is schaalbaar, testbaar en geschikt voor real-time of gesimuleerde uitvoering.

---

## 📂 Repository Structuur

| Map | Inhoud |
|-----|--------|
| `src/core/` | Kernlogica voor signaalgeneratie en voorraadbeheer |
| `src/infra/` | EventWriter, outbox, webhook integratie |
| `src/orchestration/` | Orchestrator `run_once.py` |
| `src/batching/` | BatchBuilder voor groeperen van signalen |
| `src/executor/` | BatchExecutor voor uitvoeren van batches |
| `src/webhook_service/` | Verwerkt outbox-events naar HTTP POST |
| `tests/` | Unit, integration en live tests |
| `docs/` | Documentatie en beslislogs |
| `config/` | Configuratiebestanden (yaml) |
| `tmp/` | Tijdelijke outputs en CSV logs |
| `.github/` | CI/CD workflows |
| `docker-compose.yml` | Container orchestration |

---

## 🔄 Eventflow

```
Candle → Signaal → Batch → Executor → Outbox → Webhook → Extern Systeem
```

- Zowel individuele `trade_signal` als `batch_result` events worden verwerkt via dezelfde eventflow.

---

## 🚀 Running the PoC

1. **Activeer live-mode**  
   ```bash
   export MODE=live
   ```

2. **API-credentials**  
   Plaats je KuCoin-sleutels in `.env`

3. **Start container**  
   ```bash
   docker-compose up --build -d
   ```

4. **Volg logs**  
   ```bash
   docker logs ratio-live -f
   ```

5. **Healthcheck**  
   ```bash
   curl http://localhost:8080/health
   ```

---

## ⚙️ Batching Configuratie

Voeg in `config/config.yaml` toe:

```yaml
batching:
  window_hours: 24
  max_batches: 5
```

---

## 🧪 Testen

1. **Unit tests**

```bash
pytest tests/unit/
```

2. **Integratietests**

```bash
pytest tests/integration/
```

3. **Volledige test suite**

```bash
pytest --cov=src --cov-report=term-missing
```

---

## 📄 Documentatie

Zie `docs/` voor uitgebreide uitleg:

- `docs/decisions/` – Beslislogboek
- `docs/reviews/` – Code reviews en snapshots
- `docs/dev/modules.md` – Overzicht modules
- `docs/project-taskboard.md` – Actuele takenlijst