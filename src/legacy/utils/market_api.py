# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/utils/market_api.py                               │
# │ Module: market_api                                          │
# │ Doel: Ophalen en filteren van recente trades van KuCoin    │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-05                                │
# │ Status: stable                                              │
# ╰──────────────────────────────────────────────────────────────╯

import os
import requests
from datetime import datetime
from typing import List, Dict

Tick = Dict[str, any]

def fetch_recent_trades(symbol: str, since: datetime) -> List[Tick]:
    """
    Fetch recent trades for the given symbol from KuCoin REST API since the given timestamp.
    Returns a list of ticks with keys: 'timestamp', 'price', 'volume'.
    """
    url = "https://api.kucoin.com/api/v1/market/histories"
    params = {"symbol": symbol}
    headers = {}

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    resp_json = resp.json()

    if isinstance(resp_json, dict) and "data" in resp_json:
        entries = resp_json["data"]
    elif isinstance(resp_json, list):
        entries = resp_json
    else:
        entries = []

    ticks: List[Tick] = []
    for entry in entries:
        # time in API is nanoseconds since epoch
        entry_ns = int(entry["time"])
        ts = datetime.fromtimestamp(entry_ns / 1e9)
        if ts <= since:
            continue
        ticks.append({
            "timestamp": ts,
            "price": float(entry["price"]),
            "volume": float(entry["size"]),
        })

    return ticks
