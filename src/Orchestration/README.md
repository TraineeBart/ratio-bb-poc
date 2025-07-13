# 🎛️ Orchestration Layer

## Doel
Stuurt de flow aan van signalen → batches → executor → eventwriter.

## Inhoud
- `run_once.py` – main orchestration loop
- `run_all.py` – (toekomstig) loop over meerdere runs

## Afspraken
- Alleen orchestratie: geen business logica of infrastructuur
- Gebruik dependency injection voor writers en executor

## Status
Actief – v1.0