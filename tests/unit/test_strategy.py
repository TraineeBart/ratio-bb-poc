import os
import sys
# Ensure project root is on sys.path for src imports
sys.path.insert(0, os.getcwd())
import pandas as pd
import pytest
from src.strategy import compute_bbands, detect_signal, Strategy

@pytest.fixture
def sample_df():
    # Eenvoudige prijsreeks en kolommen voor filters
    prices = [1.0, 2.0, 3.0, 4.0, 5.0]
    return pd.DataFrame({
        'price': prices,
        'nk':      [1,    2,    3,    4,    5   ],
        'volume': [10,   20,   30,   40,   50  ]
    })

# Unit tests voor compute_bbands
def test_compute_bbands_basic(sample_df):
    # Window=3, stddev=1 → voor het derde element (index 2):
    # sma = (1+2+3)/3 = 2.0
    # sigma = sqrt(((1-2)^2+(2-2)^2+(3-2)^2)/3) = sqrt(2/3) ≈ 0.8165
    df_b = compute_bbands(sample_df, window=3, stddev=1.0)
    assert df_b.loc[2, 'sma'] == pytest.approx(2.0, rel=1e-3)
    assert df_b.loc[2, 'upper'] == pytest.approx(2.0 + (2/3)**0.5, rel=1e-3)
    assert df_b.loc[2, 'lower'] == pytest.approx(2.0 - (2/3)**0.5, rel=1e-3)
    # Ratio’s: price 3.0 ten opzichte van bands
    assert df_b.loc[2, 'ratio_upper'] == pytest.approx(3.0 / df_b.loc[2, 'upper'], rel=1e-3)
    assert df_b.loc[2, 'ratio_lower'] == pytest.approx(3.0 / df_b.loc[2, 'lower'], rel=1e-3)

# Tests voor detect_signal
def test_detect_signal_branches():
    # Onder de lower band => SWAP_TFUEL_TO_THETA
    s = pd.Series({'ratio_lower': 0.9, 'ratio_upper': 1.1})
    assert detect_signal(s) == 'SWAP_TFUEL_TO_THETA'
    # Boven de upper band => SWAP_THETA_TO_TFUEL
    s = pd.Series({'ratio_lower': 1.1, 'ratio_upper': 1.2})
    assert detect_signal(s) == 'SWAP_THETA_TO_TFUEL'
    # Tussen de banden => NO_SWAP
    s = pd.Series({'ratio_lower': 1.0, 'ratio_upper': 1.0})
    assert detect_signal(s) == 'NO_SWAP'
    # Missing values => NO_SWAP
    s = pd.Series({'ratio_lower': None, 'ratio_upper': None})
    assert detect_signal(s) == 'NO_SWAP'

# Tests voor Strategy-klassen
def test_strategy_filters_and_run(sample_df):
    config = {'nk_threshold': 3, 'volume_threshold': 30, 'short_ema_span': 2}
    strat = Strategy(sample_df, config)
    df_filtered = strat.apply_filters()
    # Nk>=3 en volume>=30 → alleen index 2,3,4
    assert list(df_filtered.index) == [2, 3, 4]

    ema_series = strat.compute_ema(span=2)
    assert ema_series.iloc[0] == sample_df['price'].iloc[0]
    df_run = strat.run()
    assert f"ema_{config['short_ema_span']}" in df_run.columns
    alpha = 2 / (config['short_ema_span'] + 1)
    expected_ema1 = sample_df['price'].iloc[1] * alpha + sample_df['price'].iloc[0] * (1 - alpha)
    # EMA_2[2] should follow EMA smoothing: new = prev*(1-alpha) + price*alpha
    expected_ema2 = expected_ema1 * (1 - alpha) + sample_df['price'].iloc[2] * alpha
    assert df_run.loc[2, 'ema_2'] == pytest.approx(expected_ema2, rel=1e-3)

def test_generate_signal():
    config = {'short_ema_span': 3}
    strat = Strategy(pd.DataFrame(), config)
    # No ema/key → HOLD
    assert strat.generate_signal({'price': None, 'ema_3': None}) == 'HOLD'
    # price > ema → BUY
    assert strat.generate_signal({'price': 5.0, 'ema_3': 4.0}) == 'BUY'
    # price < ema → SELL
    assert strat.generate_signal({'price': 3.0, 'ema_3': 4.0}) == 'SELL'
    # price == ema → HOLD
    assert strat.generate_signal({'price': 4.0, 'ema_3': 4.0}) == 'HOLD'
