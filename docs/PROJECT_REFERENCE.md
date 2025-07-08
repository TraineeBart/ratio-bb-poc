

# Project Reference Overview – Ratio Trades V3

Dit document dient als **centrale referentie** voor alle belangrijke projectbestanden, canvassen en documentatie.

## 1. Documentstructuur

| Bestandsnaam                           | Beschrijving                                                                             | Canvas ID                         |
|----------------------------------------|------------------------------------------------------------------------------------------|-----------------------------------|
| `docs/PROJECT_SPEC.md`                 | Project specificatie: scope, doelen, kernfunctionaliteiten en acceptatiecriteria         | 68627813bb38                      |
| `docs/CI_Coverage_Gates.md`            | CI-pijplijn en coverage-gates, matrixconfigs en Telegram-notificatie                     | 686bd51fdf4081918c2ef08fdf19b1af  |
| `docs/MIGRATION_ROADMAP.md`            | Gefaseerde migratieroadmap naar een modulair en onderhoudbaar architectuur               | 686bea50abcdef12                  |
| `docs/architecture/ws_flow.md`         | Technische flow voor WSClient en WSReplay, imports en methode-interfaces                 | 686bce9001234abcd5678             |
| `docs/architecture/data_model.md`      | Datamodel-entiteiten: Tick, Candle, Batch en Ratio                                       | 686bdf66097081918c5da016fa6ace6c  |
| `docs/stories/story1_ci_prep.md`       | Story 1: CI-Data Preparation en resultaten                                               | 686be1111111111111111111111111111 |
| `docs/stories/story2_ws_stub.md`       | Story 2: WSClient Stub Alignment en resultaten                                           | 686be2222222222222222222222222222 |
| `docs/stories/story3_filters.md`       | Story 3: Refactor apply_filters en resultaten                                            | 686be3333333333333333333333333333 |
| `docs/stories/story4_arch_imports.md`  | Story 4a: Architectuur import- en interface-richtlijnen en resultaten                    | 686be4444444444444444444444444444 |
| `docs/stories/story4b_replay.md`       | Story 4b: WSReplay CSV-parsing en tests en resultaten                                    | 686be5555555555555555555555555555 |
| `docs/stories/story5_live_integration.md` | Story 5: Live Data Integratie & Staging en resultaten                                 | 686be6666666666666666666666666666 |

## 2. Missende onderdelen

- Live monitoring & metrics endpoint (Prometheus, Streamlit of FastAPI).  
- API Reference voor alle modules (`src/ws_client`, `src/strategy`, `src/executor`).  
- Data persistence (database-ontwerp en access layer).  

## 3. Onderhoud & Updates

- **CI-sync**: controleer wekelijkse de actualiteit van de CI-pijplijn en coverage-gates.  
- **Canvas index**: werk bij na elke nieuwe story of canvas-update.  
- **Document review**: plan maandelijkse reviews voor dit referentiedocument.
