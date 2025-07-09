

# Story 3: Refactor apply_filters() – Pandas-waarschuwingen vermijden

**Rol:** DeveloperGPT

## Context & Doel
In `src/strategy.py` ontstonden SettingWithCopyWarning-waarschuwingen door toewijzingen op slices. Om data-integriteit en codekwaliteit te waarborgen, refactoren we de `apply_filters()` en `run()` methoden om expliciet gebruik te maken van `.loc[]` en `.copy()`.

## Taken
1. Pas in `src/strategy.py` de `apply_filters()` methode aan:
   - Vervang `df[(df['nk'] >= nk_thr) & (df['volume'] >= vol_thr)]` door `df.loc[(df['nk'] >= nk_thr) & (df['volume'] >= vol_thr)].copy()`.
2. Refactor de `run()` methode:
   - Verwijder dubbele `.copy()`.
   - Gebruik `df.loc[:, f'ema_{span}'] = ema.loc[df.index]` voor kolomtoewijzingen.
3. Voeg inline comments toe die uitleggen waarom `.loc` en `.copy()` nodig zijn.
4. Draai `pytest tests/test_strategy.py tests/test_strategy_main.py` en verifieer dat er geen SettingWithCopyWarning meer verschijnt.
5. Borgen in codekwaliteit: check met `flake8` en `pytest` dat de wijzigingen geen nieuwe warnings of errors introduceren.

## Acceptatiecriteria
- Er verschijnen geen SettingWithCopyWarning meer bij het uitvoeren van de strategy-tests.
- Alle strategy-gerelateerde tests lopen groen zonder nieuwe errors.
- Code voldoet aan PEP8 en geen flake8-issues.

---

# Story 3: Refactor apply_filters() – Resultaat

**Afgerond door:** DeveloperGPT  
**Datum:** 2025-06-29

## Wat is bereikt
- `apply_filters()` gebruikt nu `.loc[]` en `.copy()` om chained assignments te voorkomen.
- `run()` methode is aangepast met expliciete `.loc[]` kolomtoewijzingen.
- Geen SettingWithCopyWarning meer bij `pytest tests/test_strategy*.py`.
- Flake8 en pytest rapporteren 0 fouten/warnings.

## Leerpunten & Aanbevelingen
- Documenteer Pandas-best practices voor slicing en copy in een centrale coding-guideline.
- Overweeg migratie van deze logica naar toekomstige strategy-modules in `/src/strategies/`.
