# File: src/parser/kucoin_parser.py

from typing import List, Any
from src.models.kucoin_models import Candle

def parse_klines(data: Any) -> List[Candle]:
    """
    Zet raw kline-list om naar een lijst van Candle-dataclasses.
    KuCoin-structuur per item: [time, open, close, high, low, volume, turnover]
    """
    candles: List[Candle] = []
    for item in data:
        time, open_p, close_p, high_p, low_p, volume, *_ = item
        candles.append(Candle(
            time=int(time),
            open=float(open_p),
            high=float(high_p),
            low=float(low_p),
            close=float(close_p),
            volume=float(volume)
        ))
    return candles