


# 📡 KuCoin WebSocket Notes – Ratio-BB-POC

## ⚙️ Algemene eigenschappen

- KuCoin WebSocket gebruikt een **bullet token** via `POST /api/v1/bullet-public`
- De WebSocket URL is dynamisch en bevat een tijdelijke token als queryparameter.

## 🔄 Ping/Pong gedrag

- KuCoin verwacht **altijd client-pings**, ook als de server zelf pings stuurt.
- De `pingInterval` in de API response is een advies; in de praktijk verbreekt KuCoin soms al na 30 seconden.
- De client moet zelf pingen met een vast interval (bijv. elke 20-25s) ongeacht andere netwerkactiviteit.

## ❗️ Veelvoorkomende issues

| Probleem | Oorzaak |
|----------|---------|
| 1011 Internal Error | Ping timeout of server reset |
| timed out during opening handshake | Netwerk of DNS-issues bij connectie |
| 'NoneType' object has no attribute 'resume_reading' | Ping-task draait door na socket-sluiting |

## 🛠️ Implementatierichtlijnen

- Gebruik **`asyncio.create_task`** voor een aparte ping-loop.
- Stop de ping-loop netjes als de WebSocket sluit.
- Gebruik `getattr(ws, 'closed', True)` voor veilige controle op gesloten verbindingen.
- Voeg exponential backoff toe bij reconnects om rate limits te voorkomen.

## 🔍 Referentie

- [KuCoin WebSocket API Docs](https://www.kucoin.com/docs/websocket/bullet)
- [KuCoin Market Data WS](https://www.kucoin.com/docs/websocket/spot-market/overview)