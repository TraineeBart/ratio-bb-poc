# ║ File: tests/test_bb_strategy.py
# ║ Module: strategies (test)
# ║ Doel: Test de BB-ratio-strategie op correcte signaalgeneratie
# ║ Auteur: QualityEngineerGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
import pytest
from strategies.bb_ratio_strategy import apply_strategy

def test_bb_ratio_signalen():
    # Simuleer koersdata met een stijgende en dalende beweging, incl. uitschieters
    close_prices = [100 + (i % 10) for i in range(60)]
    close_prices[10] = 130  # uitschieter omhoog
    close_prices[40] = 70   # uitschieter omlaag
    df = pd.DataFrame({
        "timestamp": pd.date_range("2025-01-01", periods=len(close_prices), freq="5min"),
        "close": close_prices
    })

    result = apply_strategy(df)

    # Controleer dat kolommen aanwezig zijn
    assert "signal" in result.columns
    assert "ratio_lower" in result.columns
    assert "ratio_upper" in result.columns

    # Controleer dat er signalen zijn gegenereerd (niet allemaal NO_SWAP)
    unique_signals = result["signal"].unique()
    assert len(unique_signals) >= 2  # verwacht minimaal één SWAP-signaal

    # Controleer dat alle signalen valide waarden bevatten
    valid_signals = {"NO_SWAP", "SWAP_TFUEL_TO_THETA", "SWAP_THETA_TO_TFUEL"}
    assert set(unique_signals).issubset(valid_signals)
