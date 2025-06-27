# File: src/kucoin_fetcher.py

import pandas as pd

from src.client.kucoin_client import KucoinClient
from src.parser.kucoin_parser import parse_klines

def fetch_klines(
    symbol: str,
    interval: str,
    start_ts: int,
    limit: int = 1000
) -> pd.DataFrame:
    """
    Haal candlestick-data op en geef terug als DataFrame.
    """
    client = KucoinClient()
    raw_data = client.get_candles(symbol, interval, start_ts, limit)
    candles = parse_klines(raw_data)

    # Converteer list van dataclasses naar DataFrame in juiste kolomvolgorde
    rows = [
        [c.time, c.open, c.high, c.low, c.close, c.volume]
        for c in candles
    ]
    df = pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "volume"])
    df = df.astype({
        "time": int,
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })
    return df