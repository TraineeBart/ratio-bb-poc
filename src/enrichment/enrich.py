# ║ File: src/enrichment/enrich.py
# ║ Module: enrichment
# ║ Doel: Verrijkt een DataFrame met technische indicatoren zoals RSI en SMA's
# ║ Auteur: ArchitectGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import pandas as pd
import numpy as np

# Optioneel: gebruik TA-lib of pandas_ta in een latere fase

def enrich_dataframe(df: pd.DataFrame, rsi_period: int = 14, sma_period: int = 9) -> pd.DataFrame:
    """
    🧠 Functie: enrich_dataframe
    Verrijkt een DataFrame met RSI, SMA(RSI) en SMA(9) op de koers.

    ▶️ In:
        - df (pd.DataFrame): met minimaal kolom 'close'
        - rsi_period (int): standaard 14
        - sma_period (int): standaard 9
    ⏺ Out:
        - pd.DataFrame: oorspronkelijke df + extra kolommen: 'rsi', 'sma_rsi', 'sma_9'

    💡 Gebruikt:
        - pandas rolling + mean
    """
    df = df.copy()

    # 🔹 RSI berekening (eenvoudig, niet smoothed)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=rsi_period, min_periods=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period, min_periods=rsi_period).mean()

    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # 🔹 SMA van RSI
    df['sma_rsi'] = df['rsi'].rolling(window=sma_period).mean()

    # 🔹 SMA(9) van koers
    df['sma_9'] = df['close'].rolling(window=sma_period).mean()

    # ⚠️ Filter op complete rijen
    return df.dropna()