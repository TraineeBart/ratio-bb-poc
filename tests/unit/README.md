

# 🧪 Unit Tests

Deze map bevat unittests voor individuele modules en functies binnen het project.

## 🎯 Doel
Elke test valideert een specifieke functionaliteit op module-niveau, los van de rest van het systeem. Dit helpt om fouten snel te lokaliseren en om regressies vroegtijdig te detecteren.

## 📂 Overzicht van testbestanden

| Bestand                        | Doel                                                                     |
|-------------------------------|---------------------------------------------------------------------------|
| test_enrich_ratio_15m.py      | Test de verrijkingslogica voor ratio-data op 15-minutenbasis              |
| test_enrich_ratio_60m.py      | Test de verrijkingslogica voor ratio-data op 60-minutenbasis              |
| test_enrich_tfuel_15m.py      | Test de verrijkingslogica voor TFUEL-data op 15-minutenbasis              |
| test_enrich_tfuel_60m.py      | Test de verrijkingslogica voor TFUEL-data op 60-minutenbasis              |
| test_enrich_theta_15m.py      | Test de verrijkingslogica voor THETA-data op 15-minutenbasis              |
| test_enrich_theta_60m.py      | Test de verrijkingslogica voor THETA-data op 60-minutenbasis              |

## 🛠️ Uitvoering

Draai deze tests via:

```bash
pytest tests/unit/
```

of om alleen specifieke tests te draaien:

```bash
pytest tests/unit/test_enrich_theta_15m.py
```
# 🧪 Unit Tests

Deze map bevat unittests voor individuele modules en functies binnen het project.

## 🎯 Doel
Elke test valideert een specifieke functionaliteit op module-niveau, los van de rest van het systeem. Dit helpt om fouten snel te lokaliseren en om regressies vroegtijdig te detecteren.

## 📂 Overzicht van testbestanden

| Bestand                        | Doel                                                                     |
|-------------------------------|---------------------------------------------------------------------------|
| test_enrich_ratio_15m.py      | Test de verrijkingslogica voor ratio-data op 15-minutenbasis              |
| test_enrich_ratio_60m.py      | Test de verrijkingslogica voor ratio-data op 60-minutenbasis              |
| test_enrich_tfuel_15m.py      | Test de verrijkingslogica voor TFUEL-data op 15-minutenbasis              |
| test_enrich_tfuel_60m.py      | Test de verrijkingslogica voor TFUEL-data op 60-minutenbasis              |
| test_enrich_theta_15m.py      | Test de verrijkingslogica voor THETA-data op 15-minutenbasis              |
| test_enrich_theta_60m.py      | Test de verrijkingslogica voor THETA-data op 60-minutenbasis              |
| test_kucoin_client.py         | Unit tests voor KuCoin API client en communicatie                         |
| test_kucoin_fetcher.py        | Unit tests voor KuCoin data fetcher component                             |
| test_kucoin_parser.py         | Unit tests voor parsing van KuCoin data                                   |
| test_executor.py              | Test de uitvoering van orders en tradinglogica                            |
| test_batching.py              | Test de logica voor het opsplitsen van orders in batches                 |
| test_run_once.py              | Test de run_once module, inclusief event-loop en tick verwerking          |
| test_strategy.py              | Unit tests voor tradingstrategie functies                                |
| test_webhook.py               | Test de webhook communicatie en aanroepen via mocks                      |
| test_ws_replay.py             | Unit tests voor websocket replay en event simulatie                      |
| test_candles.py               | Tests voor candle-verwerking en aggregatie                               |
| test_liquidity_helper.py      | Test hulpfuncties voor liquiditeitsberekeningen                          |
| test_main_on_signal.py        | Test hoofdlogica bij signalen                                            |
| test_output_writer.py         | Test de output naar CSV of andere formats                                |

## 📈 Testarchitectuur en scope

- Unit tests zijn gericht op afzonderlijke functies en modules zonder externe afhankelijkheden.
- Mocking wordt intensief toegepast om netwerkcommunicatie, websockets en IO te simuleren.
- Functionele integratietests en end-to-end tests worden elders ondergebracht (bijv. `tests/integration/` en `tests/live/`).
- Deze map vormt de basis voor snelle feedback bij codewijzigingen.

## 🛠️ Uitvoering

Draai deze tests via:

```bash
pytest tests/unit/
```

of om alleen specifieke tests te draaien:

```bash
pytest tests/unit/test_enrich_theta_15m.py
```

---

*Dit bestand wordt regelmatig bijgewerkt met nieuwe inzichten over de tests en structuur.*
---

## Voorbeeld: test_batching.py

- Unit test voor `compute_batches()` functie in `src/batching.py`.
- Behandelt verdeling van orders in batches op basis van liquiditeit en limieten.
- Test diverse randgevallen en foutafhandeling.
- Helder, compleet en stabiel.
- Geeft goed voorbeeld van unit testing met focus op functionele dekking.

**Aanbeveling:**
- Behouden als referentie voor unit tests.
- Gebruik als voorbeeld voor nieuwe unit tests.

---

### test_bb_strategy.py

**Doel:**  
Test de Bollinger Band (BB) ratio strategie op correcte signaalgeneratie bij gesimuleerde koersdata.  
Bevat validaties voor aanwezigheid van verwachte kolommen en redelijke signaalverdeling.

**Status:**  
Draft, functioneel maar verdient verdere uitbreiding en verfijning.  
Nuttig als voorbeeld voor strategie-gerelateerde unittests.

**Aanbeveling:**  
Behoud deze test als referentie voor toekomstige strategie-validaties.  
Breid uit met realistischere datasets en scenario’s voor robuustheid.

---