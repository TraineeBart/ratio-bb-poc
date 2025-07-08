# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/utils/candles.py                                  │
# │ Module: candles                                             │
# │ Doel: Aggregator voor ticks naar candles                    │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-04                               │
# │ Status: draft                                               │
# ╰──────────────────────────────────────────────────────────────╯

from collections import deque
import pandas as pd
from typing import Callable, Dict

class CandleAggregator:
    """
    🧠 Functie: CandleAggregator
    Aggregates incoming ticks into fixed-interval candles.

    ▶️ In:
        - period (str): Pandas offset alias, e.g. '5T'
        - on_candle (Callable[[Dict], None]): callback for closed candles
    ⏺ Out:
        - None
    """
    def __init__(self, period: str, on_candle: Callable[[Dict], None]):
        self.period = period
        self.on_candle = on_candle
        self.freq = pd.Timedelta(period)
        self.current_candle = None  # Dict with open, high, low, close, volume, start_ts
        self.last_tick_ts = None
        self.current_start = None

    def on_tick(self, tick: Dict):
        """
        Process a single tick and emit a candle when period completes.

        ▶️ In:
            - tick (Dict): must contain 'timestamp' (pd.Timestamp), 'price', 'volume'
        ⏺ Out:
            - None

        💡 Gebruikt:
            - pandas for timestamp floor
        """
        ts = pd.to_datetime(tick['timestamp'])
        self.last_tick_ts = ts
        bucket_start = ts.floor(self.period)

        # New bucket?
        if self.current_start is None or bucket_start > self.current_start:
            # Emit previous candle, and fill any missing empty candles
            if self.current_candle is not None:
                # Fill any missing empty candles
                last_start = self.current_start
                last_close = self.current_candle['close']
                next_start = last_start + self.freq
                while next_start < bucket_start:
                    empty_candle = {
                        'start_ts': next_start,
                        'last_ts': next_start,
                        'open': last_close,
                        'high': last_close,
                        'low': last_close,
                        'close': last_close,
                        'volume': 0
                    }
                    self.on_candle(empty_candle)
                    last_close = last_close
                    next_start += self.freq
                # 🔹 Emit real candle using bucket start_ts
                # 🔹 Ensure start_ts remains the floored bucket start
                emitted_candle = {
                    'start_ts': last_start,
                    'open': self.current_candle['open'],
                    'high': self.current_candle['high'],
                    'low': self.current_candle['low'],
                    'close': self.current_candle['close'],
                    'volume': self.current_candle['volume'],
                }
                self.on_candle(emitted_candle)
            # Start new candle
            self.current_start = bucket_start
            self.current_candle = {
                'start_ts': bucket_start,
                'last_ts': self.last_tick_ts,
                'open': tick['price'],
                'high': tick['price'],
                'low': tick['price'],
                'close': tick['price'],
                'volume': tick['volume']
            }
        else:
            # Update existing candle
            c = self.current_candle
            c['high'] = max(c['high'], tick['price'])
            c['low'] = min(c['low'], tick['price'])
            c['close'] = tick['price']
            c['last_ts'] = ts
            c['volume'] += tick['volume']
