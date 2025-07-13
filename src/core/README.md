# 📦 Core Layer

## Doel
Bevat de pure business logica van het project.  
Zonder afhankelijkheid van infrastructuur of externe services.

## Inhoud
- Signaalgeneratie (`signal_generator.py`)
- Event transformatie (`candle_handler.py`)

## Afspraken
- Alleen pure functies en dataclasses
- Geen imports van `infra` of `orchestration`
- Geen side-effects (print, logging, I/O)

## Status
Actief – v1.0