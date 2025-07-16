# ╭───────────────────────────────────────────────────────────╮
# │ File: src/core/candle_handler.py                         │
# │ Module: core                                              │
# │ Doel: Transformeren van candledata naar event-structuur  │
# │ Auteur: ArchitectGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯

# core/candle_handler.py

def candle_to_event(candle: dict, symbol: str) -> dict:
    """
    🧠 Functie: candle_to_event
    Zet een candle-structuur om naar een event-dictionary voor de batch pipeline.

    ▶ In:
        - candle (dict): bevat candle data met 'timestamp' en 'close'
        - symbol (str): symbool van de asset, bijvoorbeeld 'THETA-USDT'

    ⏺ Out:
        - dict: gestandaardiseerde event data met timestamp, symbol, price, signal

    ⚠️ Gebruik deze functie **alleen voor candles met 'close'.**
    Voor ticks gebruik je `tick_to_event()` (zie orchestration/run_once.py).
    """

    # 🔹 Transformeer candle naar event; initieel met 'HOLD' signaal.
    return {
        'timestamp': candle['timestamp'],
        'symbol': symbol,
        'price': float(candle.get('close', candle.get('price'))),
        'signal': 'HOLD'  # ⚠ Hier kan in een latere stap signaalinjectie plaatsvinden
    }