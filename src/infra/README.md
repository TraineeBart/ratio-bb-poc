# 🔧 Infrastructure Layer

## Doel
Bevat adapters, writers en clients voor externe systemen of I/O.

## Inhoud
- EventWriter (CSV, Webhook, MultiWriter)
- WebSocketClient Adapter (Mock of KuCoin WS)
- Uitbreidbaar met storage of API-clients

## Afspraken
- Hier zit de afhankelijkheid naar externe services
- Dependency Injection via interfaces waar mogelijk

## Status
Actief – v1.0