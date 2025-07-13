# Rapport: Status en aanbevelingen Ratio BB POC - juli 2025

## 1. Introductie

Dit rapport geeft een uitgebreide analyse van de huidige status van het Ratio BB Proof of Concept (POC) project, met name gericht op de testinfrastructuur en data handling.  
Het doel is om helderheid te scheppen over wat goed werkt, welke knelpunten er zijn, en hoe we gericht verder kunnen bouwen aan een robuust, betrouwbaar en onderhoudbaar systeem.

## 2. Hoofdbevindingen

### 2.1 Testomgeving en testdata

- De testomgeving bestaat uit een mix van unit-, integratie- en live tests verdeeld over meerdere mappen (`tests/unit`, `tests/integration`, `tests/live`).  
- Testdata is verspreid aanwezig in CSV-bestanden in `tests/data`, gebruikt voor statische tests met candles en ticks.  
- Er is onduidelijkheid en mismatch tussen het gebruik van ticks en candles in tests versus productiegedrag.  
- Live flow tests gebruiken WebSocket mocks, die moeilijk stabiel te houden zijn en niet altijd realistische event flows simuleren.

### 2.2 WebSocket mocks en event flow

- WebSocket mocks veroorzaken inconsistenties in testresultaten doordat ticks niet altijd leiden tot candle-aggregatie en webhook triggers.  
- Patching van `requests.post` voor webhook mocks gebeurt vaak op verkeerde importlocaties, waardoor calls niet geregistreerd worden.  
- Testen verwachten meerdere regels output (ticks), maar in werkelijkheid wordt output op candle-niveau gegenereerd, waardoor tests falen.

### 2.3 Testdata en formats

- CSV-formaten verschillen in kolomnamen en structuur (timestamp vs start_ts), wat leidt tot parsingproblemen in tests.  
- Testdata mist consistente timestamps en harmonisatie tussen ticks en candles.  
- Er is behoefte aan een vaste set testdata met duidelijke documentatie en consistente formats.

### 2.4 Documentatie en structuur

- README-bestanden zijn gedeeltelijk bijgewerkt maar bevatten nog niet alle inzichten over testdoelen en data.  
- Mappenstructuur en testindeling zijn grotendeels duidelijk, maar noodzaak tot opschoning en herindeling is vastgesteld.  
- Verouderde tests en mock-bestanden zijn grotendeels opgeschoond, maar er blijven vragen over welke tests actief en kritisch zijn.

---

## 3. Analyse per bestand en map

### 3.1 `src/` map

- **`run_once.py`**  
  Bevat core event loop, candle aggregatie en webhook calls.  
  Moet getest worden op candle-gebaseerde output en correcte webhook trigger.  
- **`strategy.py`**  
  Tradinglogica en signaalverwerking.  
  Unit tests aanwezig, uitbreiden met realistische scenario's aanbevolen.  
- **`ws_client.py`**  
  WebSocket client en replay client.  
  Complex in mocking; aanbeveling is beperkt gebruik in tests, focus op integratietests met CSV-data.  

### 3.2 `tests/unit/` map

- Bevat voornamelijk functie- en modultests voor verrijking, kucoin client, candle aggregatie, strategie.  
- Testen zijn stabiel en snel, aanbevolen te behouden en uit te breiden.  
- Mocking van netwerkcommunicatie beperkt hier gebruikt.

### 3.3 `tests/integration/` map

- Focus op samenhang tussen modules, validatie van output op CSV-basis.  
- Bevat belangrijke tests voor executor, orchestrator, markt API, backtest flow.  
- Aanbevolen: uitbreiden met integratie van nieuwe CSV testdata sets en validaties.

### 3.4 `tests/live/` map

- Live flow tests met WebSocket mocks.  
- Moeilijkheden met betrouwbaarheid en consistentie.  
- Aanbevolen: vereenvoudigen en beperken tot minimale flow-validatie.  

### 3.5 `tests/data/` map

- Bevat CSV-testdata voor ticks en candles.  
- Moet uitgebreid worden met consistente en goed gedocumenteerde datasets.  
- `README.md` moet testdata-formaten en gebruik helder beschrijven.

### 3.6 Overige configuratie en documentatie

- `.github/workflows/ci.yml` regelt test runs, opname van snapshot uitsluitingen.  
- `README.md` in tests map moet volledig en actueel zijn over teststrategie en mappenindeling.  

## 4. Aanbevelingen per bestand en map

### 4.1 `src/` map

| Bestand        | Acties                                                                                                         | Prioriteit |
|----------------|---------------------------------------------------------------------------------------------------------------|------------|
| `run_once.py`  | - Verfijn event loop zodat candle-aggregatie consequent is.<br>- Zorg dat webhook triggers consistent en testbaar zijn.<br>- Verbeter logging en maak evt. event callbacks testbaar. | Hoog       |
| `strategy.py`  | - Behoud en breid unit tests uit.<br>- Maak strategie functies goed modulair en documenteer parameters.<br>- Valideer trading logica op edge cases. | Middel     |
| `ws_client.py` | - Verminder complexiteit in mocks.<br>- Overweeg alleen replay functionaliteit in tests te gebruiken.<br>- Verplaats live websocket communicatie uit unit tests. | Hoog       |

### 4.2 `tests/unit/` map

- Behoud alle verrijkings- en modultests.<br>
- Voeg testdata en scenario’s toe met focus op stabiliteit en regressiebescherming.<br>
- Vermijd netwerkmocking tenzij strikt noodzakelijk.<br>
- Documenteer duidelijk testdoelen en dependencies in `README.md`.

### 4.3 `tests/integration/` map

- Breid tests uit met de nieuwe statische CSV datasets.<br>
- Valideer output consistentie na integratie van mocks en real data.<br>
- Beperk snapshot tests tot noodzakelijke kritieke paden.<br>
- Voeg integratietests toe voor order batching en orchestrator modules.

### 4.4 `tests/live/` map

- Vereenvoudig live flow tests.<br>
- Overweeg om live websocket mocks te vervangen door statische csv-gebaseerde tests.<br>
- Maak testfocus helder: validatie van end-to-end flow in kleine stappen.<br>
- Documenteer beperkingen en verwachtingen in README.md.

### 4.5 `tests/data/` map

- Voeg consistente, goed gedocumenteerde testdata toe (ticks en candles).<br>
- Harmoniseer kolomnamen en tijdformaten.<br>
- Documenteer gebruik en beperkingen van datasets.<br>
- Voeg testdata-validatie scripts toe om integriteit te waarborgen.

### 4.6 Configuratie en documentatie

- Update `.github/workflows/ci.yml` om snapshots uit te sluiten waar nodig.<br>
- Verbeter `tests/README.md` met teststructuur en richtlijnen.<br>
- Voeg documentatie toe voor testdata formats en mocking aanpak.<br>
- Zorg dat README-bestanden per map actueel blijven en met referenties naar issues.

---

## 5. Concrete volgende stappen en prioritering

| Stap                                            | Doel                                        | Prioriteit | Verantwoordelijke |
|-------------------------------------------------|---------------------------------------------|------------|-------------------|
| 1. Stabiliseer en pas tests aan op candle output | Zorg dat tests realistische flow volgen     | Hoog       | Developer/Test    |
| 2. Refactor mocks en patching in live tests      | Voorkom flaky tests en verkeerde patching   | Hoog       | Developer/Test    |
| 3. Harmoniseer testdata formats en documentatie  | Eenduidigheid en onderhoudbaarheid          | Middel     | Developer/Analist |
| 4. Opschonen en documenteren tests en data mappen| Overzicht en makkelijk onderhoud             | Middel     | Projectmanager    |
| 5. Uitbreiden integratietests met statische data | Betrouwbare validatie zonder live afhankelijkheden | Middel     | Developer/Test    |
| 6. Verbeter CI workflows en test automatisering  | Continuïteit en feedbackloop verbeteren     | Laag       | DevOps            |
| 7. Rapportage en kennisdeling                      | Team op dezelfde lijn houden                 | Laag       | Projectmanager    |

---

## 6. Bijlagen

### 6.1 Samenvatting issues live_flow

- Webhook calls niet geregistreerd door patching op verkeerde locatie.<br>
- Output CSV gebaseerd op candles, tests verwachten ticks.<br>
- Timing in tests wijkt af van productiegedrag.<br>
- WebSocket mocks veroorzaken complexiteit en instabiliteit.

### 6.2 Testdata formats

- Gebruik `timestamp` als standaard tijdkolom.<br>
- CSV’s moeten consistent kolomnamen en tijdzones hanteren.<br>
- Testdata splitsen in ticks (voor fetch/simulatie) en candles (voor trading en analyse).

## 7. Per-bestand status en aanbevelingen

### 7.1 Src map - Belangrijkste codebestanden

| Bestand          | Status               | Aanbeveling / Opmerking                               | Rol              |
|------------------|----------------------|-------------------------------------------------------|------------------|
| run_once.py      | Actief, kritisch     | Verfijnen event loop en patchen webhook calls correct | Developer/Test   |
| strategy.py      | Actief, stabiel      | Uitbreiden unit tests, edge cases valideren           | Developer/Test   |
| ws_client.py     | Complex, deels mock  | Vereenvoudigen mocks, meer replay ipv live mocks      | Developer/Test   |
| batching.py      | Stabiel              | Behouden, evt. uitbreiden met integratietests         | Developer/Test   |
| executor.py      | Stabiel              | Behouden, continue onderhoud                           | Developer/Test   |

### 7.2 Tests/unit - Unittests

- **Te behouden en uitbreiden:**  
  Verrijkings- en logica tests (`test_enrich_*.py`), `test_batching.py`, `test_strategy.py`, `test_executor.py`, `test_run_once.py`.  
- **Actie:**  
  Documentatie up-to-date houden in `tests/unit/README.md`.  
- **Rol:**  
  Developer/Test

### 7.3 Tests/integration - Integratietests

- **Belangrijk:**  
  `test_full_backtest_flow.py`, `test_executor_integration.py`, orchestrator tests (`test_orchestrator_*.py`).  
- **Actie:**  
  Uitbreiden met statische CSV testdata, snapshots beperken tot cruciale paden.  
- **Rol:**  
  Developer/Test

### 7.4 Tests/live - E2E tests

- **Status:**  
  Complex door live WS mocks, instabiel.  
- **Aanpak:**  
  Focus verleggen naar CSV-gebaseerde tests, vereenvoudigen mocks.  
- **Rol:**  
  Developer/Test

### 7.5 Tests/data - Testdata

- **Status:**  
  Relevante ticks & candles data aanwezig.  
- **Actie:**  
  Harmoniseren kolomnamen, toevoegen documentatie, valideren integriteit.  
- **Rol:**  
  Analist/Projectmanager

### 7.6 Overige bestanden

| Bestand                        | Status        | Aanbeveling                                      | Rol              |
|--------------------------------|---------------|--------------------------------------------------|------------------|
| .github/workflows/ci.yml       | Actief        | CI uitbreiden met test skips, stabiliteitschecks | DevOps           |
| docs/                          | Actueel       | Documentatie structureel bijwerken               | Projectmanager   |
| Dockerfile, docker-compose.yml | Productief    | Behouden, documenteren                           | DevOps           |

---

## 8. Rolafbakening en taken

| Rol              | Taken                                                                                      |
|------------------|-------------------------------------------------------------------------------------------|
| Projectmanager   | Overzicht, prioriteren, bewaken voortgang, faciliteren communicatie                        |
| Developer       | Codeverbetering, testverbetering, mocks vereenvoudigen, unit/integratie tests schrijven   |
| Tester/QA       | Testcases schrijven, valideren, CI integratie en monitoring                               |
| Analist         | Data-analyse, testdata validatie, consistentie bewaken                                  |
| DevOps          | CI/CD pipeline, containers, infrastructuurbeheer                                       |

---

## 9. Prioriteitenlijst

1. Fixen en stabiliseren van live flow tests (webhook patching, event flow)  
2. Overgang van live WS mocks naar statische CSV-gebaseerde E2E tests  
3. Documentatie compleet maken en up-to-date houden per map  
4. Uitbreiden en verbeteren unit en integratietests met focus op robuustheid  
5. Optimaliseren CI workflow met skip- en retry-mechanismen  
6. Vastleggen en valideren testdata formats en tooling  

---

## 10. Volgende stappen

- **Teamoverleg:** Prioriteiten bespreken, rolverdeling bevestigen  
- **Roadmap:** Concrete taken toewijzen per sprint/iteratie  
- **Monitoring:** Regelmatige statusupdates en test coverage reviews  
- **Documentatie:** Continue bijwerken om kennis vast te leggen  

---

*Dit rapport dient als leidraad voor gefocust voortbouwen op een stabiele basis.*