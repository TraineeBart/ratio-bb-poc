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

