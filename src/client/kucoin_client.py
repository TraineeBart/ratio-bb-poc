# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/client/kucoin_client.py                           │
# │ Module: kucoin_client                                       │
# │ Doel: KuCoin REST API-client met retry-logica               │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-04                               │
# │ Status: stable                                              │
# ╰──────────────────────────────────────────────────────────────╯
"""
KucoinClient module with built-in retry logic for resilient HTTP calls.
Uses exponential back-off (1s, 2s, 4s) and custom KucoinClientError.
"""
# File: src/client/kucoin_client.py
# Path: /opt/ratio-bb-poc/src/client/kucoin_client.py

import os
from typing import Any
import requests
import re
import time
import logging

# Custom exception for retry failures
class KucoinClientError(Exception):
    """Raised when API retries have been exhausted or an unrecoverable error occurs."""
    pass

def retry_request(func):
    """
    Decorator implementing retry logic with exponential back-off.
    Retries up to 3 times on rate limit or network errors.
    """
    def wrapper(*args, **kwargs):
        backoff = 1
        for attempt in range(1, 4):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 429:
                    logging.warning(f"Rate limit hit, retrying in {backoff}s (attempt {attempt})")
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    # Non-rate-limit HTTP errors should not be retried
                    raise
            except requests.exceptions.RequestException as e:
                logging.warning(f"Network error, retrying in {backoff}s (attempt {attempt}): {e}")
                time.sleep(backoff)
                backoff *= 2
        raise KucoinClientError("API retries exhausted after 3 attempts")
    return wrapper

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
        # 🔹 Config validity check
        if not all([self.api_key, self.api_secret, self.api_passphrase]):
            logging.error("Missing one or more KuCoin credentials in environment variables")

    @retry_request
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


# Helper: get_bullet_public
def get_bullet_public() -> dict:
    """
    🧠 Functie: get_bullet_public
    Haalt een publieke bullet token en WebSocket endpoint op van KuCoin.

    ▶️ In:
        - geen
    ⏺ Out:
        - dict: {
            'endpoint': str,  # WebSocket endpoint URL
            'token': str      # bullet-public token
        }

    💡 Gebruikt:
        - requests voor REST-call
    """
    base_url = os.getenv("KUCOIN_API_URL", "https://api.kucoin.com")
    url = f"{base_url}/api/v1/bullet-public"
    response = requests.post(url, timeout=10)
    response.raise_for_status()
    data = response.json().get("data", {})
    # Kies de eerste instanceServer
    servers = data.get("instanceServers", [])
    if not servers:
        raise KucoinClientError("No instanceServers returned from bullet-public")
    server = servers[0]
    return {
        "endpoint": server.get("endpoint"),
        "token": data.get("token"),
        "pingInterval": server.get("pingInterval")
    }