# File: src/client/kucoin_client.py

import os
from typing import Any
import requests

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
        session: requests.Session = None
    ):
        self.api_key = api_key or os.getenv("KUCOIN_API_KEY")
        self.api_secret = api_secret or os.getenv("KUCOIN_API_SECRET")
        self.api_passphrase = api_passphrase or os.getenv("KUCOIN_API_PASSPHRASE")

        self.session = session or requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

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
        url = f"{self.BASE_URL}/api/v1/market/candles"
        params = {
            "symbol": symbol,
            "type": interval,
            "startAt": start_ts,
            "limit": limit
        }
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("data", [])