# File: src/strategy.py

import pandas as pd
from developer import load_config

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
        nk_thr = self.config.get('nk_threshold', 0)
        vol_thr = self.config.get('volume_threshold', 0)
        df = self.data
        return df[(df['nk'] >= nk_thr) & (df['volume'] >= vol_thr)]

    def compute_ema(self, span):
        return pd.Series(self.data['price'].ewm(span=span, adjust=False).mean(), name=f'ema_{span}')

    def run(self):
        df = self.apply_filters()
        span = self.config.get('short_ema_span', 9)
        df[f'ema_{span}'] = self.compute_ema(span)
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

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run backtest on historical data')
    parser.add_argument('--data', required=True, help='Path to CSV data')
    parser.add_argument('--output', default='output.csv', help='Output CSV')
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    config = load_config()
    strat = Strategy(df, config)
    result = strat.run()
    result.to_csv(args.output, index=False)
    print(f"Backtest complete, saved to {args.output}")
