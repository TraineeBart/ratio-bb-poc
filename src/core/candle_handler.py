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
    Zet een candle-structuur om naar een event-dictionary die gebruikt wordt
    voor output naar CSV of webhook.

    ▶ In:
        - candle (dict): bevat candle data met 'start_ts' en 'close'
        - symbol (str): symbool van de asset, bijvoorbeeld 'THETA-USDT'

    ⏺ Out:
        - dict: gestandaardiseerde event data met timestamp, symbol, price, signal

    💡 Gebruikt:
        - Pure core logica, geen externe afhankelijkheden
    """

    # 🔹 Transformeer candle naar event; initieel met 'HOLD' signaal.
    return {
        'timestamp': candle['start_ts'].isoformat(),
        'symbol': symbol,
        'price': float(candle['close']),
        'signal': 'HOLD'  # ⚠ Hier kan in een latere stap signaalinjectie plaatsvinden
    }