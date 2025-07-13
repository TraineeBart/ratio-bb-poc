# 📂 Broncode Overzicht - 2025-07-13

Doel:  
Volledig inzicht in de `src/`-structuur van Ratio-BB-POC en bepalen welke onderdelen core, I/O, orchestratie of helper zijn.

---

## 🗂️ Overzicht `src/`

| Bestand / Map | Functie | Actie |
|---------------|---------|-------|
| backtester.py | Core backtest flow | ✅ Behouden |
| batching.py | Helpers voor order batching | ✅ Behouden |
| client/kucoin_client.py | KuCoin API client | 🔄 Samenvoegen met `kucoin_client.py` in root of opschonen |
| developer.py | Tools voor ontwikkelaar/debug | 🔄 Overwegen apart te zetten in `/dev-tools/` |
| enrichment/enrich.py | Verrijking candles met indicatoren | ✅ Behouden |
| executor.py | Order execution logic | ✅ Behouden |
| kucoin_client.py | (Dubbel) KuCoin client | 🔄 Samenvoegen met `client/kucoin_client.py` |
| kucoin_fetcher.py | KuCoin data ophalen | ✅ Behouden |
| kucoin_test.py | Testbestand, hoort niet in `src/` | ❌ Verplaatsen naar `tests/` |
| liquidity_helper.py | Berekening liquiditeit | ✅ Behouden |
| models/kucoin_models.py | Datamodellen KuCoin | ✅ Behouden |
| orchestrator_ratio.py | Orchestratie ratio-flow | ✅ Behouden |
| orchestrator_tfuel.py | Orchestratie TFUEL-flow | ✅ Behouden |
| orchestrator_theta.py | Orchestratie THETA-flow | ✅ Behouden |
| outputs/output_writer.py | Schrijven van output naar file | ✅ Behouden |
| outputs/webhook.py | Webhook aansturing | 🔄 Loskoppelen tot aparte service |
| parser/kucoin_parser.py | Parsing KuCoin data | ✅ Behouden |
| run_all.py | Run alle processen | 🔄 Overwegen te splitsen |
| run_once.py | Orchestration van 1 run | 🔄 Webhook loskoppelen |
| strategies/basic_strategy.py | Placeholder basisstrategie | 🔄 Herzien of verwijderen |
| strategies/bb_ratio_strategy.py | BB-ratio strategie | ✅ Behouden |
| strategy.py | Core strategie (buy/sell logica) | ✅ Behouden |
| test_ws.py | Testbestand in `src/` | ❌ Verplaatsen naar `tests/` |
| utils/candles.py | Candle helper functies | ✅ Behouden |
| utils/market_api.py | Markt API helpers | ✅ Behouden |
| utils/timezone.py | Tijdszone helpers | ✅ Behouden |
| ws_client.py | WebSocket client | 🔄 Opschonen (heartbeat/subscribe separeren?) |
| ws_replay.py | Replay van websocket data | ✅ Behouden |

---

## 📌 Samenvatting Acties

- [ ] Dubbele KuCoin clients samenvoegen of opschonen
- [ ] `test_ws.py` en `kucoin_test.py` verplaatsen naar `tests/`
- [ ] Webhook loskoppelen naar aparte service
- [ ] Overbodige scripts zoals `run_all.py` en `basic_strategy.py` heroverwegen
- [ ] `developer.py` naar aparte dev-tools sectie of markeren als experimenteel