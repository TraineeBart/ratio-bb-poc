# File: tests/test_strategy.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import pytest
from src.strategy import Strategy

@pytest.fixture
def config():
    return {
        'nk_threshold': 0.0,
        'volume_threshold': 0,
        'short_ema_span': 3
    }

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'price': [10, 12, 14, 16, 18],
        'nk':    [1,   0,  2,  1,  3],
        'volume':[100, 50, 200, 25, 300]
    })

def test_apply_filters(sample_data, config):
    strat = Strategy(sample_data.copy(), config)
    df_filtered = strat.apply_filters()
    # Rows where nk>=0.0 AND volume>=0: all rows
    assert list(df_filtered.index) == [0,1,2,3,4]

@pytest.mark.parametrize("span,expected_first,expected_second", [
    (3, 10.0, pytest.approx((12 * (2/4) + 10 * (1 - 2/4)))),
    (5, 10.0, pytest.approx((12 * (2/6) + 10 * (1 - 2/6))))
])
def test_compute_ema(sample_data, config, span, expected_first, expected_second):
    strat = Strategy(sample_data.copy(), config)
    ema = strat.compute_ema(span)
    assert isinstance(ema, pd.Series)
    assert ema.iloc[0] == expected_first
    assert ema.iloc[1] == expected_second

def test_run_adds_ema_and_filters(sample_data, config):
    strat = Strategy(sample_data.copy(), config)
    df_run = strat.run()
    # Should have ema column
    assert f"ema_{config['short_ema_span']}" in df_run.columns
    # apply_filters with config nk>=0.0, volume>=0 keeps all rows
    assert len(df_run) == len(sample_data)

@pytest.mark.parametrize("tick,expected_signal", [
    ({'price': 5, 'ema_3': 3}, 'BUY'),
    ({'price': 2, 'ema_3': 4}, 'SELL'),
    ({'price': 3, 'ema_3': 3}, 'HOLD'),
    ({'price': None, 'ema_3': 3}, 'HOLD'),
    ({'price': 5, 'ema_3': None}, 'HOLD'),
    ({}, 'HOLD'),
])
def test_generate_signal(sample_data, config, tick, expected_signal):
    strat = Strategy(sample_data.copy(), config)
    sig = strat.generate_signal(tick)
    assert sig == expected_signal
