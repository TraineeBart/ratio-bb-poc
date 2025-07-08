

# Configuration Reference

Alle configuratie-opties zijn te definiëren in `config.yaml` of via environment variables (in `.env`).

## Algemeen
- `symbols`: lijst van handelsparen, bijv. `"THETA-USDT,TFUEL-USDT"` of `["THETA-USDT", "TFUEL-USDT"]`
- `interval`: tijdsinterval voor candles, bijv. `"5m"`, `"15m"`, `"60m"`
- `webhook_url`: URL voor het verzenden van webhook-callbacks
- `historical_csv_path`: pad naar bestaande historische CSV voor backtests

## Fee & Slippage
- `fee_rate`: transactiekostenpercentage (bijv. `0.002` voor 0.2%)
- `slippage_rate`: slippage-percentage (bijv. `0.001` voor 0.1%)

## Batching
- `batching.window_hours`: aantal uren voor liquiditeitsgemiddelde (default: `24`)
- `batching.max_batches`: maximum aantal deelorders per totale order (default: `10`)

## API & Authenticatie (voor live mode)
- `kucoin_api_key`: API Key voor KuCoin
- `kucoin_api_secret`: API Secret voor KuCoin
- `kucoin_api_passphrase`: API Passphrase voor KuCoin

## Logging & Health
- `log_level`: logniveau voor de applicatie (`DEBUG`, `INFO`, `WARN`, `ERROR`)
- `health_port`: poortnummer voor de health endpoint (default: `8080`)

## Voorbeelden
```yaml
symbols: "THETA-USDT,TFUEL-USDT"
interval: "5m"
webhook_url: "http://localhost:9000"
historical_csv_path: "data/historical.csv"
fee_rate: 0.002
slippage_rate: 0.001
batching:
  window_hours: 24
  max_batches: 10
kucoin_api_key: "your_api_key"
kucoin_api_secret: "your_api_secret"
kucoin_api_passphrase: "your_passphrase"
log_level: "INFO"
health_port: 8080
```