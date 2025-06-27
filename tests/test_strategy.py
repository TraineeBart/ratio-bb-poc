import pandas as pd
import pytest
from src.strategy import compute_bbands, detect_signal

@pytest.mark.parametrize(
    "data, expected_ratio_lower, expected_ratio_upper",
    [
        (
            pd.Series([1, 2, 3, 4, 5, 6, 7]),
            pd.Series([float('nan')] * 6 + [3.5]),
            pd.Series([float('nan')] * 6 + [pytest.approx(1.1666667)]),
        ),
    ],
)
def test_compute_bbands(data, expected_ratio_lower, expected_ratio_upper):
    df_input = pd.DataFrame({'price': data})
    bb = compute_bbands(df_input, window=len(data), stddev=1.0)
    # Only the last value should be defined and equal to expected
    assert bb['ratio_lower'].iloc[-1] == expected_ratio_lower.iloc[-1]
    assert bb['ratio_upper'].iloc[-1] == expected_ratio_upper.iloc[-1]

@pytest.mark.parametrize(
    "latest_row, expected_signal",
    [
        ({'ratio_lower': 0.9, 'ratio_upper': 1.1}, 'SWAP_TFUEL_TO_THETA'),
        ({'ratio_lower': 1.1, 'ratio_upper': 1.1}, 'SWAP_THETA_TO_TFUEL'),
        ({'ratio_lower': 1.0, 'ratio_upper': 1.0}, 'NO_SWAP'),
    ],
)
def test_detect_signal(latest_row, expected_signal):
    signal = detect_signal(latest_row)
    assert signal == expected_signal
