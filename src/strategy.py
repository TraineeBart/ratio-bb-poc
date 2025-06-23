import pandas as pd

class Strategy:
    """
    Trading strategy: computes EMA, filters by thresholds, and generates signals.
    """

    def __init__(self, data: pd.DataFrame, config: dict = None, *, ema_span: int = None, nk_thr: float = None, vol_thr: float = None):
        """
        Initialize the strategy.

        Two calling conventions supported:
        - Strategy(df, config_dict)
        - Strategy(df, ema_span=..., nk_thr=..., vol_thr=...)
        """
        self.data = data.copy()

        # Determine parameters
        if config is not None:
            # Config keys: short_ema_span, nk_threshold, volume_threshold
            self.ema_span = config.get('short_ema_span', config.get('ema_span'))
            self.nk_thr = config.get('nk_threshold', 0)
            self.vol_thr = config.get('volume_threshold', 0)
        else:
            self.ema_span = ema_span
            self.nk_thr = nk_thr
            self.vol_thr = vol_thr

        # Validate parameters
        if self.ema_span is None:
            raise ValueError("EMA span must be provided")
        if self.nk_thr is None or self.vol_thr is None:
            raise ValueError("nk_thr and vol_thr must be provided")

    def compute_ema(self, span: int = None) -> pd.Series:
        """
        Compute exponential moving average over 'price' column.
        """
        span_val = span or self.ema_span
        return self.data['price'].ewm(span=span_val, adjust=False).mean()

    def apply_filters(self) -> pd.DataFrame:
        """
        Apply filters on nk and volume thresholds.
        """
        # Compute EMA column
        ema_col = f"ema_{self.ema_span}"
        self.data[ema_col] = self.compute_ema()

        # Filter rows
        return self.data[(self.data['nk'] >= self.nk_thr) & (self.data['volume'] >= self.vol_thr)].reset_index(drop=True)

    def run(self) -> pd.DataFrame:
        """
        Run the full strategy: compute EMA and filter.
        """
        return self.apply_filters()

    def generate_signal(self, df) -> str:
        """
        Generate signal for a single tick (dict or Series) or DataFrame of ticks.
        Returns a single signal string if input is single, else returns DataFrame with 'signal' column.
        """
        import pandas as _pd  # local import to avoid top-level pd confusion
        single = False
        if isinstance(df, dict):
            df = pd.DataFrame([df])
            single = True
        elif isinstance(df, _pd.Series):
            df = df.to_frame().T
            single = True

        ema_key = f"ema_{self.ema_span}"
        signals = []
        for _, row in df.iterrows():
            price = row.get('price', None)
            ema = row.get(ema_key, None)
            if ema is None or price is None:
                sig = 'HOLD'
            elif price > ema:
                sig = 'BUY'
            elif price < ema:
                sig = 'SELL'
            else:
                sig = 'HOLD'
            signals.append(sig)

        if single:
            return signals[0]
        df['signal'] = signals
        return df
