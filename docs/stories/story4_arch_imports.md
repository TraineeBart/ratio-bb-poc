# Story 4a: Architectuur – Import- en Interface-Richtlijnen

**Rol:** ArchitectGPT

## Context & Doel
Voor een consistente en onderhoudbare codebase moeten alle modules eenduidige imports en interfaces gebruiken. Dit voorkomt misverstanden tussen live- en replay-implementaties en maakt testing eenvoudiger.

## Taken
1. Definieer in `docs/architecture/ws_flow.md` de importconventie:
   - Gebruik altijd absolute imports:  
     ```python
     from src.ws_client import WSClient
     from src.ws_replay import WSReplay
     ```
2. Leg constructor-signatures vast:
   - **WSClient**: `WSClient(symbols: list[str], callback: Callable[[dict], None])`
   - **WSReplay**: `WSReplay(csv_path: str, callback: Callable[[dict], None], speed: float = 1.0)`
3. Bepaal methoden en hun rol:
   - `start()`, `stop()`
   - Interne functies: `_on_open()`, `_on_message()`, `_run()`
4. Documenteer in de canvas “Architect Tickets Iteratie1” welke modules en tests hierop vertrouwen.
5. Verifieer dat alle tests voor WSClient en WSReplay (unit en integratie) nog groen draaien.

## Acceptatiecriteria
- `docs/architecture/ws_flow.md` bevat de juiste importstatements en constructor-definities.
- De interfaces zijn consistent tussen documentatie en code (unit-tests slaan niet meer mis op signature).
- Canvas “Architect Tickets Iteratie1” is bijgewerkt met een link naar deze story en relevante tickets.

---

# Story 4a: Architectuur – Resultaat

**Afgerond door:** ArchitectGPT  
**Datum:** 2025-06-26

## Wat is bereikt
- Alle modules gebruiken nu absolute imports zoals gedefinieerd.
- Constructor-signatures en methoden zijn in de documentatie en code gesynchroniseerd.
- Architect-tickets (nrs. 1 en 2) in de canvas zijn als “Done” gemarkeerd.
- WSClient- en WSReplay-tests draaien zonder import- of signature-fouten.

## Leerpunten & Aanbevelingen
- Houd documentatie altijd dicht bij de code bij major interface-wijzigingen.
- Overweeg een pre-commit hook die absolute imports afdwingt.