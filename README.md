# Ratio BB PoC

Proof-of-concept for the Ratio BB trading strategy.

## Repository structure
- `src/` - source modules (developer, strategy, executor, orchestrator)
- `config/` - configuration file `config.yaml`
- `orders/` - order test wrapper
- `data/` - historical data (e.g., `historical.csv`)
- `logs/` - runtime logs
- `main.py` - entry point

## KuCoin Fetcher

### Usage

```python
from src.kucoin_fetcher import fetch_klines

# Example: haal 100 candles van 5m-interval op voor THETA-USDT sinds een bepaalde timestamp
df = fetch_klines("THETA-USDT", "5m", start_ts=1620000000, limit=100)
print(df.head())
```

+## Live Mode Setup
+
+Volg deze stappen om de end-to-end live-flow in staging (of lokaal) te draaien:
+
+1. **Activeer live-mode**  
+   ```bash
+   export MODE=live
+   ```
+
+2. **API-credentials**  
+   Plaats je KuCoin-sleutels (`API_KEY`, `API_SECRET`, eventueel `API_PASSPHRASE`) in een `.env` in de project-root:
+   ```
+   API_KEY=<your_key>
+   API_SECRET=<your_secret>
+   API_PASSPHRASE=<your_passphrase>
+   ```
+
+3. **Start container**  
+   ```bash
+   docker-compose up --build -d
+   ```
+
+4. **Mount tmp/**  
+   Zorg dat in `docker-compose.yml` je `./tmp:/app/tmp` hebt staan, zodat alle CSV’s ook op de host zichtbaar zijn.
+
+5. **Logs monitoren**  
+   Volg de live-logs met:
+   ```bash
+   docker logs ratio-live -f
+   ```
+
+6. **Healthcheck**  
+   Controleer kort daarna of de service gezond is:
+   ```bash
+   curl http://<host>:8000/health
+   # verwacht 200 OK
+   ```
+
+7. **Ticks ophalen**  
+   Haal de meest recente tick op voor een symbool:
+   ```bash
+   curl http://<host>:8000/ticks?symbol=THETA-USDT
+   ```
+
+8. **Output CSV**  
+   Bekijk `tmp/output.csv` op je host voor realtime tick- en signal-logs.

 (… eventuele vervolg-secties …)