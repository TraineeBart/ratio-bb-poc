# src/liquidity_helper.py
"""
Helpermodule voor liquiditeitsberekeningen op basis van enriched 5-min CSV-data.
"""

import os
import pandas as pd

# Root directory waar de 5-min CSV’s staan
DATA_ROOT = "/opt/tradingbot/data"

def get_average_liquidity(symbol: str, window_hours: int) -> float:
    """
    Berekent de gemiddelde liquiditeit voor een gegeven symbool over een periode van `window_hours` uren,
    door een CSV-bestand uit DATA_ROOT te lezen.

    Args:
        symbol: Handelsparingssymbool, bijv. 'TFUEL-USDT' of 'THETA-USDT'.
        window_hours: Aantal uren voor het gemiddelde (bv. 24).

    Returns:
        Gemiddelde 'volume' over de laatste window_hours * 12 rijen (5-min intervallen).
        Retourneert 0.0 als het CSV leeg is of minder rijen bevat dan window_hours*12.

    Raises:
        ValueError: Indien window_hours <= 0.
        FileNotFoundError: Indien het CSV-bestand niet gevonden wordt.
        KeyError: Indien de kolom 'volume' ontbreekt in het CSV.
    """
    # Validatie van window_hours
    if window_hours <= 0:
        raise ValueError(f"window_hours must be positive, got {window_hours}")

    # Base asset afleiden (bijv. 'TFUEL' uit 'TFUEL-USDT') en lowercase
    base_asset = symbol.split('-')[0].lower()
    csv_path = os.path.join(DATA_ROOT, base_asset, "5m", f"{base_asset}-5m-full.csv")

    # Bestandscontrole
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV niet gevonden op {csv_path}")

    # CSV inlezen
    df = pd.read_csv(csv_path)
    if df.empty:
        return 0.0

    # Kolomcontrole
    if "volume" not in df.columns:
        raise KeyError("Kolom 'volume' ontbreekt in CSV")

    # Bepaal relevant segment
    n_rows = window_hours * 12
    tail = df["volume"].tail(n_rows)

    # Bereken en retourneer gemiddelde (of 0.0 bij geen data)
    return float(tail.mean()) if not tail.empty else 0.0