

# File: src/kucoin_fetcher.py

from typing import Any
import requests
import pandas as pd

def fetch_klines(
    symbol: str,
    interval: str,
    start_ts: int,
    limit: int = 1000
) -> pd.DataFrame:
    """
    Fetch candlestick (K-line) data from KuCoin.

    Args:
        symbol: Trading pair symbol, e.g. "THETA-USDT".
        interval: Time interval for candles, e.g. "5m", "1h".
        start_ts: Unix timestamp in seconds to start fetching from.
        limit: Maximum number of candles to retrieve (max 1000).

    Returns:
        DataFrame with columns ["time","open","high","low","close","volume"].
    """
    url = "https://api.kucoin.com/api/v1/market/candles"
    params: dict[str, Any] = {
        "symbol": symbol,
        "type": interval,
        "startAt": start_ts,
        "limit": limit,
    }
    # Perform GET request
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    # Parse JSON response; data is list of lists: [time, open, close, high, low, volume, turnover]
    data = response.json().get("data", [])

    # Define column names as per KuCoin API spec
    columns = ["time", "open", "close", "high", "low", "volume", "turnover"]
    df = pd.DataFrame(data, columns=columns)

    # Ensure correct data types
    df = df.astype({
        "time": int,
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float,
    })

    # Return only the required columns in the desired order
    return df[["time", "open", "high", "low", "close", "volume"]]