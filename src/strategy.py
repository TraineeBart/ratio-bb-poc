# DEPRECATED – vervangen door modules in /src/strategies/
# File: src/strategy.py

# Path: /opt/ratio-bb-poc/src/strategy.py
# File: src/strategy.py

# Path: /opt/ratio-bb-poc/src/strategy.py
import argparse
import json
import pandas as pd
from src.developer import load_config
import logging

logging.basicConfig(level=logging.INFO)

"""
Module: Strategy and utility functions for trading signals.

This module provides:
- compute_bbands: Bollinger Bands calculation.
- detect_signal: determine swap signals based on band ratios.
- Strategy class: EMA-based filtering and signal generation.

Responsibilities:
- compute_bbands: calculate SMA, upper/lower bands, and ratios.
- detect_signal: simple threshold logic for swap decisions.
- Strategy: applies filters, computes EMA, and generates simple BUY/SELL/HOLD signals.
"""

# Compute Bollinger Bands and ratios

def compute_bbands(df: pd.DataFrame, window: int, stddev: float) -> pd.DataFrame:
    """
    Bereken voor elke rij in df de Bollinger Bands en ratio's.

    Args:
        df: DataFrame met ten minste een 'price'-kolom.
        window: aantal periodes voor het voortschrijdend gemiddelde (SMA).
        stddev: factor voor de standaarddeviatie (σ).

    Returns:
        DataFrame met extra kolommen:
        - 'sma'
        - 'upper'
        - 'lower'
        - 'ratio_lower'
        - 'ratio_upper'
    """
    # Bereken het eenvoudige voortschrijdend gemiddelde (SMA)
    sma = df['price'].rolling(window).mean()
    # Bereken de standaarddeviatie over dezelfde window
    sigma = df['price'].rolling(window).std(ddof=0)
    # Bepaal de boven- en onderband
    upper = sma + stddev * sigma
    lower = sma - stddev * sigma
    # Ratio's ten opzichte van de bands
    ratio_lower = df['price'] / lower
    ratio_upper = df['price'] / upper
    # Voeg de nieuwe kolommen toe aan een kopie van df en retourneer
    result = df.copy()
    result['sma'] = sma
    result['upper'] = upper
    result['lower'] = lower
    result['ratio_lower'] = ratio_lower
    result['ratio_upper'] = ratio_upper
    return result

class Strategy:
    def __init__(self, data, config):
        self.data = data.copy()
        self.config = config

    def apply_filters(self):
        """
        Filter data by NK and volume thresholds from config.

        Uses .loc[] and .copy() to avoid pandas SettingWithCopyWarning when mutating the returned DataFrame.
        """
        nk_thr = self.config.get('nk_threshold', 0)
        vol_thr = self.config.get('volume_threshold', 0)
        df = self.data
        # Use .loc and .copy() to avoid SettingWithCopyWarning on subsequent mutations
        filtered_df = df.loc[(df['nk'] >= nk_thr) & (df['volume'] >= vol_thr)].copy()
        return filtered_df

    def compute_ema(self, span):
        """
        Compute exponential moving average (EMA) of price with given span.
        """
        return self.data['price'].ewm(span=span, adjust=False).mean()

    def run(self):
        """
        Apply filters and append EMA column for configured short span.

        apply_filters already returns a copy, so no need for an extra .copy().
        Uses .loc for assignment to avoid chained assignment warnings.
        """
        # apply_filters already returns a copy, no need for an extra copy
        df = self.apply_filters()
        span = self.config.get('short_ema_span', 9)
        ema = self.compute_ema(span)
        # Use .loc for assignment to avoid chained assignment warnings
        df.loc[:, f'ema_{span}'] = ema.loc[df.index]
        return df

    def generate_signal(self, tick: dict) -> str:
        """
        Eenvoudige crossover op basis van korte EMA:
        - BUY  als prijs > EMA
        - SELL als prijs < EMA
        - HOLD anders (of bij ontbrekende EMA)
        """
        # bepaal de sleutel voor de korte EMA
        span = self.config.get('short_ema_span', 9)
        ema_key = f"ema_{span}"
        price = tick.get('price')
        ema = tick.get(ema_key)
        if ema is None or price is None:
            return 'HOLD'
        if price > ema:
            return 'BUY'
        if price < ema:
            return 'SELL'
        return 'HOLD'

def detect_signal(latest_row: pd.Series) -> str:
    """
    Bepaal het swap-signaal op basis van de laatste Bollinger-ratio’s.

    Args:
        latest_row: pd.Series met ten minste:
                    - 'ratio_lower'
                    - 'ratio_upper'

    Returns:
        Eén van:
        - 'SWAP_TFUEL_TO_THETA'  als prijs < lower band (ratio_lower < 1.0)
        - 'SWAP_THETA_TO_TFUEL'  als prijs > upper band (ratio_upper > 1.0)
        - 'NO_SWAP'             anders
    """
    lower_ratio = latest_row.get('ratio_lower')
    upper_ratio = latest_row.get('ratio_upper')

    # Als de prijs onder de onderste band is, swap van TFUEL naar THETA
    if lower_ratio is not None and lower_ratio < 1.0:
        return 'SWAP_TFUEL_TO_THETA'
    # Als de prijs boven de bovenste band is, swap van THETA naar TFUEL
    if upper_ratio is not None and upper_ratio > 1.0:
        return 'SWAP_THETA_TO_TFUEL'
    # In alle andere gevallen geen swap
    return 'NO_SWAP'

def run_main():
    parser = argparse.ArgumentParser(description='Run backtest on historical data')
    parser.add_argument('--data', required=True, help='Path to CSV data')
    parser.add_argument('--output', default='output.csv', help='Output CSV')
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    config = load_config()
    strat = Strategy(df, config)
    result = strat.run()
    # 🔹 Compute actual signal based on last row
    from src.strategy import detect_signal  # or relative import if needed
    last_signal = detect_signal(result.iloc[-1])
    result.to_csv(args.output, index=False)
    output_dict = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "output_file": args.output,
        "signal": last_signal
    }
    print(json.dumps(output_dict))

if __name__ == '__main__':
    run_main()


# Voeg functie toe om tick en candle te combineren en een signaal te berekenen
def process_tick_with_candle(tick: dict, candle: dict) -> dict:
    """
    Combineer tick- en candledata en bereken een eenvoudig signaal.

    Args:
        tick (dict): Bevat o.a. 'timestamp', 'symbol', 'price'
        candle (dict): Bevat candle-informatie zoals open, close, high, low, volume

    Returns:
        dict: Verrijkte tick met eventueel signaalinformatie
    """
    # Combineer data
    combined = tick.copy()
    combined.update({
        'open': candle.get('open'),
        'close': candle.get('close'),
        'high': candle.get('high'),
        'low': candle.get('low'),
        'volume': candle.get('volume'),
    })

    print("[STRATEGY] Received tick:", tick)
    # Dummy logic: BUY als prijs > close, SELL als prijs < close
    price = tick.get('price')
    close = candle.get('close')
    if price is None or close is None:
        combined['signal'] = 'HOLD'
    elif price > close:
        combined['signal'] = 'BUY'
    elif price < close:
        combined['signal'] = 'SELL'
    else:
        combined['signal'] = 'HOLD'

    return combined
