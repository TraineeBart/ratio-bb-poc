# ╭───────────────────────────────────────────────────────────╮
# │ File: src/strategies/bb_ratio_strategy.py                 │
# │ Module: strategies                                        │
# │ Doel: Implementatie van de BB-Ratio trading strategie    │
# │ Auteur: DeveloperGPT                                      │
# │ Laatste wijziging: 2025-07-15                            │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯

import logging
from typing import Any
import pandas as pd

logger = logging.getLogger(__name__)

def bb_ratio_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    🧠 Functie: bb_ratio_strategy
    Implementatie van de BB-Ratio trading strategie op basis van Bollinger Bands.

    ▶ In:
        - df (pd.DataFrame): DataFrame met minimaal de kolom 'close' met slotkoersen.

    ⏺ Out:
        - pd.DataFrame: Uitgebreide DataFrame met toegevoegde kolommen:
          'sma', 'upper_band', 'lower_band', 'signal' (trade signaal).

    💡 Gebruikt:
        - pandas voor data-manipulatie en berekeningen van Bollinger Bands.
    """
    window = 20
    no_of_std = 2

    df = df.copy()
    df['sma'] = df['close'].rolling(window).mean()
    df['stddev'] = df['close'].rolling(window).std()
    df['upper_band'] = df['sma'] + (no_of_std * df['stddev'])
    df['lower_band'] = df['sma'] - (no_of_std * df['stddev'])

    def signal(row: Any) -> str:
        if row['close'] < row['lower_band']:
            return 'SWAP_TFUEL_TO_THETA'
        elif row['close'] > row['upper_band']:
            return 'SWAP_THETA_TO_TFUEL'
        else:
            return 'NO_SWAP'

    df['signal'] = df.apply(signal, axis=1)

    logger.debug("BB-Ratio strategy signals computed")

    df.drop(columns=['stddev'], inplace=True)

    return df
