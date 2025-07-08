# Architectuur: WS Flow

## Modules en importbeleid

- `src/ws_client.py` - Live websocket client module
- `src/ws_replay.py` - Replay client module, speelt ticks af uit CSV-bestand

### Importregels

- Gebruik altijd **absolute imports** vanaf de projectroot `src/`
- Voorbeelden:
  ```python
  from src.ws_client import WSClient
  from src.ws_replay import WSReplay
  ```

---

## Constructor Interfaces

<dl>
  <dt>WSClient</dt>
  <dd>
    <ul>
      <li>Constructor parameters: 
        <ul>
          <li><code>symbols: List[str]</code> - lijst van symbolen die live gevolgd worden</li>
          <li><code>callback: Callable[[Dict], None]</code> - functie die live tick-data ontvangt</li>
        </ul>
      </li>
      <li>Methoden:
        <ul>
          <li><code>start()</code> - opent de WebSocket en start het ontvangen van live ticks</li>
          <li><code>stop()</code> - sluit de WebSocket en stopt het ontvangen van ticks</li>
        </ul>
      </li>
    </ul>
  </dd>
</dl>

<dl>
  <dt>WSReplay</dt>
  <dd>
    <ul>
      <li>Constructor parameters:
        <ul>
          <li><code>csv_path: str</code> - pad naar CSV-bestand met historische tickdata</li>
          <li><code>callback: Callable[[Dict], None]</code> - functie die tick-data ontvangt tijdens replay</li>
          <li><code>speed: float = 1.0</code> (optioneel) - afspeelsnelheid van de replay (1.0 = realtime)</li>
        </ul>
      </li>
      <li>Methoden:
        <ul>
          <li><code>start()</code> - speelt ticks af en roept callback aan met tick-gegevens</li>
          <li><code>stop()</code> - stopt het afspelen van ticks</li>
        </ul>
      </li>
    </ul>
  </dd>
</dl>

---

## Flow beschrijving

### Live modus

```python
ws_client = WSClient(symbols=["THETA-USDT"], callback=on_tick)
ws_client.start()  # Open WebSocket en ontvang live ticks
```

### Replay modus

```python
ws_replay = WSReplay(csv_path="data/theta_ticks.csv", callback=on_tick)
ws_replay.start()  # Speelt tickdata af via callback in timestampvolgorde
```

> `on_tick` is een callback functie die tick data verwerkt binnen de downstream logica.

### Flowdiagram (Mermaid)

```mermaid
graph LR
  A[Init WSClient(symbols, callback)] --> B[start()]
  B --> C{Modus?}
  C -->|Live| D[WSClient._run → on_open → on_message → callback]
  C -->|Replay| E[WSReplay._run → read CSV → tick events → callback]
  D --> F[heartbeat & reconnect]
  E --> F
  F --> G[Downstream: strategy processing]
```

---

## Notities

- Beide modules gebruiken dezelfde callback interface voor downstream verwerking.
- Live- en replay-logica delen dezelfde callback-interface, maar hanteren afzonderlijke implementaties (_run loops).
- De `speed` parameter in WSReplay regelt de afspeelsnelheid van de replay, waarbij 1.0 realtime betekent.

---

## Volgende stappen voor DeveloperGPT

- Implementeer in `src/ws_client.py` en `src/ws_replay.py` de beschreven constructor-interfaces, methoden en callback-callbackflow.
- Start daarna de implementatie van concrete functionaliteit conform dit document.
