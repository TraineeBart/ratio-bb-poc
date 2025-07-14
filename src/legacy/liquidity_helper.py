# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/liquidity_helper.py                                │
# │ Module: liquidity_helper                                     │
# │ Doel: Provides functions to calculate average trading volume │
# │       (liquidity) for a given symbol over a time window.     │
# │ Auteur: Data-EngineerGPT                                     │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: stable                                               │
# ╰──────────────────────────────────────────────────────────────╯
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
liquidity_helper module

Provides functions to calculate average trading volume (liquidity) for a given symbol
over a specified time window using enriched 5-minute CSV data.

Functions:
    get_average_liquidity(symbol: str, window_hours: int = 24) -> float
        Calculate the average positive volume for the past `window_hours`.
"""

import os
import pandas as pd
from datetime import datetime, timezone, timedelta

# Root directory waar de 5-min CSV’s staan
DATA_ROOT = "/opt/tradingbot/data"


def get_average_liquidity(symbol: str, window_hours: int = 24) -> float:
    """
    Berekent de gemiddelde liquiditeit voor een gegeven symbool over een periode van `window_hours` uren,
    door een CSV-bestand uit DATA_ROOT te lezen.

    Args:
        symbol: Handelsparingssymbool, bijv. 'TFUEL-USDT' of 'THETA-USDT'.
        window_hours: int, optional, number of hours for the average (default 24).

    Returns:
        Gemiddelde 'volume' over de laatste window_hours (5-min intervallen).
        Retourneert 0.0 als er geen data binnen het tijdvenster is.

    Raises:
        ValueError: For invalid window_hours, missing file, missing columns, or parsing errors.
    """
    # Validatie van window_hours
    if not isinstance(window_hours, int) or window_hours <= 0:
        raise ValueError(f"window_hours must be a positive integer, got {window_hours}")

    # Base asset afleiden (bijv. 'TFUEL' uit 'TFUEL-USDT') en lowercase
    base_asset = symbol.split('-')[0].lower()
    csv_path = os.path.join(DATA_ROOT, base_asset, "5m", f"{base_asset}-5m-full.csv")

    # Bestandscontrole
    if not os.path.isfile(csv_path):
        raise ValueError(f"Data file not found for symbol {symbol}: {csv_path}")

    # CSV inlezen
    df = pd.read_csv(csv_path)

    # Validate required columns
    if 'timestamp' not in df.columns or 'volume' not in df.columns:
        raise ValueError("CSV must contain 'timestamp' and 'volume' columns")

    # Convert timestamp (ms) to UTC datetime
    try:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    except Exception as e:
        raise ValueError(f"Failed to parse timestamps: {e}")

    # Compute cutoff time
    now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=window_hours)

    # Filter rows: within time window and positive volume
    df_window = df.loc[(df['datetime'] >= cutoff) & (df['volume'] > 0)]

    # Return the average volume, or 0.0 if no data in window
    if df_window.empty:
        return 0.0
    return float(df_window['volume'].mean())
