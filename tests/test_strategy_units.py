# File: src/strategy.py
import pandas as pd

class Strategy:
    def __init__(self, data: pd.DataFrame, ema_span: int = None, nk_thr: float = None, vol_thr: float = None, config: dict = None):
        self.data = data.copy()
        if config is not None:
            self.ema_span = config.get('short_ema_span')
            self.nk_thr = config.get('nk_threshold')
            self.vol_thr = config.get('volume_threshold')
        else:
            self.ema_span = ema_span
            self.nk_thr = nk_thr
            self.vol_thr = vol_thr

    def compute_ema(self):
        return self.data['price'].ewm(span=self.ema_span, adjust=False).mean()

    def apply_filters(self):
        filtered = self.data
        if self.nk_thr is not None:
            filtered = filtered[filtered['nk'] >= self.nk_thr]
        if self.vol_thr is not None:
            filtered = filtered[filtered['volume'] >= self.vol_thr]
        return filtered

    def generate_signal(self, df):
        last_row = df.iloc[-1]
        last_price = last_row['price']
        last_ema = last_row[f'ema_{self.ema_span}']
        if last_price > last_ema:
            signal = 'BUY'
        elif last_price < last_ema:
            signal = 'SELL'
        else:
            signal = 'HOLD'
        return pd.DataFrame([{'signal': signal}])
