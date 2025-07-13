# core/signal_generator.py
# ╭───────────────────────────────────────────────────────────╮
# │ File: src/core/signal_generator.py                        │
# │ Module: core                                              │
# │ Doel: Genereren van trading signalen op basis van prijs- │
# │       vergelijking tussen eerste en laatste tick.         │
# │ Auteur: ArchitectGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯

def generate_signal(first_price: float, last_price: float) -> str:
    """
    🧠 Functie: generate_signal
    Bepaalt een trading signaal op basis van de prijsbeweging tussen 
    de eerste en de laatste prijs in een reeks ticks.

    ▶ In:
        - first_price (float): de prijs van de eerste tick in de periode
        - last_price (float): de prijs van de laatste tick in de periode

    ⏺ Out:
        - str: 'BUY', 'SELL' of 'HOLD'

    💡 Gebruikt:
        - Geen externe afhankelijkheden, pure core logica
    """

    # 🔹 Basisvergelijking om trendrichting te bepalen.
    if last_price > first_price:
        return 'BUY'
    elif last_price < first_price:
        return 'SELL'
    
    # 🔹 Geen beweging → neutraal signaal
    return 'HOLD'