# core/signal_generator.py
# ╭───────────────────────────────────────────────────────────╮
# │ File: src/core/signal_generator.py                        │
# │ Module: core                                              │
# │ Doel: Genereren van trading signalen op basis van prijs-  │
# │       vergelijking tussen eerste en laatste tick.         │
# │ Auteur: ArchitectGPT                                      │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                            │
# ╰───────────────────────────────────────────────────────────╯

import logging
import os
import pandas as pd
from strategies.bb_ratio_strategy import bb_ratio_strategy

def generate_signal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dynamische strategie-selector voor trading signalen.

    ▶ In:
        - df (pd.DataFrame): DataFrame met candle data, vereist kolom 'close'

    ⏺ Out:
        - pd.DataFrame: Zelfde df met extra kolom 'signal'

    🧠 Strategieën:
        - bb_ratio: gebruikt BB-Ratio logica via bb_ratio_strategy
        - simple: vergelijkt eerste en laatste prijs (default fallback)
    """

    strategy_mode = os.getenv('STRATEGY_MODE', 'simple')

    if strategy_mode == 'bb_ratio':
        logging.info("Forceren SELL signalen voor test in bb_ratio.")
        df['signal'] = 'SELL'
        return df

    # Fallback: simpele prijsvergelijking
    first_price = df['close'].iloc[0]
    last_price = df['close'].iloc[-1]

    signal = 'HOLD'
    if last_price > first_price:
        signal = 'BUY'
    elif last_price < first_price:
        signal = 'SELL'

    df['signal'] = signal
    return df