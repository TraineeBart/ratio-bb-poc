# Besluit & Plan van Aanpak – Webhook als Service & Testarchitectuur Ratio-BB-POC

**Datum:** 2025-07-11  
**Project:** Ratio-BB-POC  
**Status:** Goedgekeurd – Referentiedocument (Gebruik bij alle code reviews en vervolgontwikkelingen)

---

## 🎯 Context & Waarom dit document?

Dit document legt **één waarheid** vast over de gemaakte keuzes rondom de testarchitectuur en webhook-integratie van het Ratio-BB-POC project.  
Doel: 100% duidelijkheid voor huidige én toekomstige teamleden, inclusief AI-rollen, zodat er **geen herinterpretaties of afwijkingen ontstaan**.

---

## 🔧 Besluit: Webhook als Aparte Service

### Probleem

- Webhook-calls zaten direct in `run_once.py`
- Dit leidde tot:
  - Testcomplexiteit (lastig mocken van netwerkverkeer)
  - Debuggingproblemen (onduidelijk of fout in core, input of webhook lag)
  - Risico’s op 75%-valkuil: onnodige technische schuld bij eindfase POC

### Beslissing

De webhook wordt losgekoppeld van de strategie en ingericht als **aparte service**:

- Core-strategie schrijft signalen naar een event-log / outbox (JSON, SQLite of Redis)
- De webhook-service leest deze events en verstuurt ze via HTTP POST
- Fouten in webhook hebben **geen invloed** op de core
- Testen worden eenvoudiger, omdat core- en outputlogica gescheiden zijn

---

## 🗂️ Testarchitectuur: Nieuwe indeling

| Map | Doel |
|-----|------|
| `/tests/unit/` | Testen van losse modules (pure functies, geen I/O) |
| `/tests/integration/` | Testen van volledige strategie met CSV-input, zonder netwerkcalls |
| `/tests/live/` | Tests met echte WebSocket/live connecties, **optioneel** in CI |

### Testdata

- Alle testdata gaat naar `/tests/data/`  
- CSV’s worden gebruikt voor integratietests

### Mocking

- In integratietests wordt de webhook-service **niet aangeroepen**  
- Webhook wordt apart getest met dummy data

---

## ⚙️ CI/CD Strategie

- **Unit- en integratietests draaien standaard in CI**
- **Live-tests zijn optioneel / apart aanroepbaar**
- Testcoverage per testgroep wordt gerapporteerd
- Instabiele live-tests mogen **nooit CI-blokkades veroorzaken**

---

## 🗓️ Plan van Aanpak

### Fase 1 – Opschoning & Fundering (week 1-2)

- Herstructureren testmappen
- Verwijderen oude tests
- Fixen van patching netwerkverkeer in tests
- Documenteren README’s per testmap

### Fase 2 – Webhook als Service (week 2-4)

- Ontwerpen event-output (JSON, SQLite of Redis)
- Aanpassen `run_once.py` om naar event-outbox te schrijven
- Bouwen van `webhook_service.py` als aparte consumer
- Implementeren van retry/fallback in webhook-service
- Losse tests voor webhook-service

### Fase 3 – CI/CD Verbetering (week 4-5)

- Pipelines splitsen: unit / integration / live
- Rapportage testcoverage
- Eventueel: end-to-end test als monitoring run

### Fase 4 – Documentatie & Borging (week 5-6)

- Vastleggen van dit document in `/docs/decisions/`
- Usage-documentatie van de webhook-service
- Update van dev-documentatie & modules-overzicht

---

## 🚧 Risico’s & Beheersing

| Risico | Maatregel |
|--------|-----------|
| Extra complexiteit webhook-service | Start klein met JSON-lines of SQLite; Redis is optioneel voor later |
| Synchronisatie problemen | Losse tests voor outbox en webhook-service, monitoring van queue status |
| Overschrijving van besluit door andere reviews | Gebruik dit document als **referentie bij alle code reviews en GPT-interacties** |

---

## 📌 Slotopmerking

Dit document is bedoeld als **vaste leidraad** voor het team, inclusief alle AI-ondersteuning.  
Bij twijfel of discussie over de teststrategie of webhook-implementatie:  
**Gebruik dit bestand als uitgangspunt – geen afwijkingen tenzij dit document wordt geüpdatet en opnieuw geaccordeerd.**