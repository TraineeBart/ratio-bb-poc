from typing import Dict
import pandas as pd

class Strategy:
    def __init__(self, data: pd.DataFrame, config: Dict):
        self.data = data
        self.config = config

    def run(self):
        # Existing run method implementation
        pass

    def generate_signal(self, tick: dict) -> str:
        price = float(tick.get('price', 0))
        span = self.config.get('short_ema_span', 9)
        # Compute EMA over existing data + this tick
        prices = pd.concat([self.data['price'], pd.Series([price])], ignore_index=True)
        ema = prices.ewm(span=span, adjust=False).mean().iloc[-1]
        if price > ema:
            return "BUY"
        elif price < ema:
            return "SELL"
        else:
            return "HOLD"