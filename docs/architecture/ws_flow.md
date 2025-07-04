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
        </ul>
      </li>
      <li><code>start()</code> methode speelt ticks af en roept callback aan met tick-gegevens</li>
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

---

## Notities

- Beide modules gebruiken dezelfde callback interface voor downstream verwerking.
- Het onderscheid tussen live en replay is duidelijk gescheiden in de architectuur.
- Absolute imports minimaliseren importfouten en verhogen de codekwaliteit.

---

## Volgende stappen voor DeveloperGPT

- Implementeer in `ws_client.py` en `ws_replay.py` de beschreven interfaces.
- Zorg dat alle imports absoluut zijn zoals hierboven beschreven.
- Wacht op review en definitieve acceptatie van deze architectuur door ProjectManagerGPT.
- Start daarna de implementatie van concrete functionaliteit conform dit document.
