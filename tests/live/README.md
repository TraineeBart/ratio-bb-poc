# Live Tests

Deze map bevat tests die gericht zijn op het valideren van de live data-verwerking en simulatie binnen het project. 

## Overzicht van bestanden

## Bekende aandachtspunten

- De huidige `test_live_flow.py` gebruikt tick-data als input, terwijl het productiesysteem candles verwerkt. Dit wordt in een volgende iteratie aangepast.
- Snapshot tests draaien **niet standaard in CI** vanwege mogelijke instabiliteit bij dynamische data. Ze zijn bedoeld voor lokale validatie.

- **test_dummy_snapshot.py**  
  Een eenvoudige voorbeeldtest die snapshot testing demonstreert. Dit is bedoeld als basis om later meer complexe live-data tests te ontwikkelen.

- **test_live_flow.py**  
  Test de integratie en flow van live data binnen de tradingbot, inclusief de verwerking van ticks en candles.

- **test_replay_flow.py**  
  Valideert het opnieuw afspelen van historische data (replay) voor simulaties en backtesting.

- **test_strategy_csv_flow.py**  
  Test de tradingstrategie op basis van vooraf gedefinieerde CSV-testdata in plaats van live data, wat betrouwbaarder is voor regressietesten.

---

Snapshot testing is een handige techniek om regressies te voorkomen en om complexe outputs snel te valideren. In de toekomst kunnen hier meer geavanceerde live data scenario's worden toegevoegd.

---

*Dit document is onderdeel van het testbeheerproces en wordt regelmatig bijgewerkt bij aanpassingen in de live data-verwerking.*
