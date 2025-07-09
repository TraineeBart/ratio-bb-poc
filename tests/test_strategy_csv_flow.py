

# 📄 tests/test_strategy_csv_flow.py
# 🔍 Strategie Output Test via CSV
#
# ✅ Vergelijkt tick + candle input uit CSV-bestanden met verwachte output
# 👤 Auteur: DeveloperGPT
# 🗓 Laatst gewijzigd: 2025-07-09
# 📌 Status: draft


import pandas as pd
import pytest
from src.strategy import process_tick_with_candle
from tests.helpers import load_csv_as_dicts

# Assert that process_tick_with_candle is successfully imported and callable
assert callable(process_tick_with_candle)

@pytest.fixture
def tick_data():
    return load_csv_as_dicts("tests/data/test_ticks.csv")

@pytest.fixture
def candle_data_theta():
    return load_csv_as_dicts("tests/data/test_candles_theta.csv")

@pytest.fixture
def candle_data_tfuel():
    return load_csv_as_dicts("tests/data/test_candles_tfuel.csv")

@pytest.fixture
def expected_output():
    return pd.read_csv("tests/data/test_ticks.csv")

def test_strategy_output_matches_expected(tick_data, candle_data_theta, candle_data_tfuel, expected_output):
    actual_rows = []

    for tick in tick_data:
        symbol = tick["symbol"]
        if symbol == "THETA-USDT":
            candles = candle_data_theta
        elif symbol == "TFUEL-USDT":
            candles = candle_data_tfuel
        else:
            continue

        candle = next((c for c in candles if c["timestamp"] == tick["timestamp"]), None)
        if not candle:
            continue

        row = process_tick_with_candle(tick, candle)
        actual_rows.append(row)

    columns = ["timestamp", "symbol", "price", "signal"]
    actual_df = pd.DataFrame(actual_rows)[columns]
    expected_df = expected_output[columns]
    actual_df["price"] = actual_df["price"].astype(float)
    expected_df["price"] = expected_df["price"].astype(float)
    pd.testing.assert_frame_equal(actual_df.reset_index(drop=True), expected_df.reset_index(drop=True))