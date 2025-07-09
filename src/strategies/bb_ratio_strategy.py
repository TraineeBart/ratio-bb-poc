

# ║ File: src/strategies/bb_ratio_strategy.py
# ║ Module: strategies
# ║ Doel: Signaalstrategie gebaseerd op verhouding koers vs Bollinger Bands
# ║ Auteur: ArchitectGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import pandas as pd

def compute_bollinger_bands(series: pd.Series, window: int = 20, num_std_dev: float = 2.0):
    """
    🧠 Functie: compute_bollinger_bands
    Berekent SMA, bovenband en onderband op basis van standaardafwijking.

    ▶️ In:
        - series (pd.Series): kolom waarop de banden worden berekend
        - window (int): periode voor SMA
        - num_std_dev (float): aantal standaarddeviaties

    ⏺ Out:
        - sma (pd.Series), upper_band (pd.Series), lower_band (pd.Series)
    """
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = sma + num_std_dev * std
    lower_band = sma - num_std_dev * std
    return sma, upper_band, lower_band

def apply_strategy(df: pd.DataFrame, window: int = 20, num_std_dev: float = 2.0) -> pd.DataFrame:
    """
    🧠 Functie: apply_strategy
    Verrijkt DataFrame met ratio_signaal o.b.v. Bollinger Band-verhouding.

    ▶️ In:
        - df (pd.DataFrame): met minimaal kolom 'close'
    ⏺ Out:
        - pd.DataFrame: met extra kolommen ['sma', 'upper_band', 'lower_band', 'signal']
    """
    df = df.copy()

    sma, upper, lower = compute_bollinger_bands(df['close'], window, num_std_dev)
    df['sma'] = sma
    df['upper_band'] = upper
    df['lower_band'] = lower

    df['ratio_lower'] = df['close'] / df['lower_band']
    df['ratio_upper'] = df['close'] / df['upper_band']

    def detect_signal(row):
        if row['ratio_lower'] < 1.0:
            return 'SWAP_TFUEL_TO_THETA'
        elif row['ratio_upper'] > 1.0:
            return 'SWAP_THETA_TO_TFUEL'
        else:
            return 'NO_SWAP'

    df['signal'] = df.apply(detect_signal, axis=1)
    return df.dropna(subset=['signal'])