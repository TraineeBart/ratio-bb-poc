# 🗂️ Batching Layer

## Doel
Verwerkt signalen tot batches voor efficiënte uitvoering.

## Inhoud
- `batch_builder.py` – bouwt batches van signalen
- Toekomstig uitbreidbaar met slicing of zwaartepunten

## Afspraken
- Houd batching simpel voor deze fase: max 3 signalen per batch
- Geen directe koppeling naar executor of core logica

## Status
Actief – v1.0