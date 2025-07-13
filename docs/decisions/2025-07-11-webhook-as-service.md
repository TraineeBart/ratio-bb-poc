# Architectuurbesluit: Webhook als Aparte Service

**Datum:** 2025-07-11  
**Project:** Ratio-BB-POC  
**Status:** Goedgekeurd  

## Context

In de huidige POC is de webhook-aanroep direct gekoppeld aan de strategie-uitvoering (`run_once.py`).  
Dit leidt tot complexiteit in testen, onderhoud en debugging, omdat fouten in de output (webhook) de kernlogica kunnen verstoren.

## Besluit

De webhook-functionaliteit wordt losgetrokken van de core-logica en ingericht als **aparte service**.

## Implementatie

- **Core-strategie**: Schrijft signalen weg naar een event-log of outbox (bijv. JSON, SQLite, Redis).
- **Webhook-service**: Leest de outbox en stuurt de events via HTTP POST naar de ingestelde endpoints.
- **Fallback & robustness**: De core mag nooit falen door webhook-problemen. Webhook-service hanteert eigen retry & logging.
- **Tests**: Strategie en webhook worden los getest. End-to-end tests combineren ze indien gewenst.

## Voordelen

- Betere foutisolatie en debugbaarheid  
- Testbare core zonder afhankelijkheid van netwerk  
- Voorbereid op uitbreidingen (bijv. meerdere outputs, async verwerking)

## Mogelijke risico’s

- Extra proces/service beheren (complexiteit groeit iets)  
- Synchronisatie tussen event-log en webhook-service moet goed gemonitord worden

## Actiepunten

- Documentatie updaten  
- Taken aanmaken voor implementatieplan