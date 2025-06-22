# File: src/client/kucoin_client.py

import os
from typing import Any
import requests
import re

def _interval_to_seconds(interval: str) -> int:
    """
    Convert interval string (e.g., "5m", "1h", "2d") to seconds.
    Valid formats: digits followed by 'm', 'h', or 'd'.
    """
    match = re.fullmatch(r"(\d+)([mhd])", interval)
    if not match:
        raise ValueError(f"Unknown interval: {interval}")
    value, unit = match.groups()
    value = int(value)
    if unit == 'm':
        return value * 60
    if unit == 'h':
        return value * 3600
    if unit == 'd':
        return value * 86400
    # Fallback
    raise ValueError(f"Unknown interval: {interval}")

class KucoinClient:
    """
    KuCoin REST API client voor market-data.
    """
    BASE_URL = "https://api.kucoin.com"

    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        api_passphrase: str = None,
    ):
        self.api_key = api_key or os.getenv("KUCOIN_API_KEY")
        self.api_secret = api_secret or os.getenv("KUCOIN_API_SECRET")
        self.api_passphrase = api_passphrase or os.getenv("KUCOIN_API_PASSPHRASE")

    def get_candles(
        self,
        symbol: str,
        interval: str,
        start_ts: int,
        limit: int = 1000
    ) -> Any:
        """
        Haal ruwe kline-data (candles) op als JSON-list.
        """
        granularity = _interval_to_seconds(interval)
        url = f"{self.BASE_URL}/api/v1/market/candles"
        params = {
            "symbol": symbol,
            "granularity": granularity,
            "startAt": start_ts,
            "limit": limit
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("data", [])