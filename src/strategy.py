import pandas as pd
from developer import load_config

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
        Genereer een signaal op basis van nk-waarde en threshold:
        - 'SELL' als nk > nk_threshold
        - 'BUY'  als nk < nk_threshold
        - 'HOLD' anders
        """
        nk_value = tick.get('nk', 0)
        threshold = self.config.get('nk_threshold', 0)
        if nk_value > threshold:
            return 'SELL'
        elif nk_value < threshold:
            return 'BUY'
        else:
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
