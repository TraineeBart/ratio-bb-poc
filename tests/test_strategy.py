import pandas as pd
import pytest
from strategy import Strategy

@pytest.fixture
def config():
    return {
        'nk_threshold': 0.0,
        'volume_threshold': 0,
        'short_ema_span': 3
    }

def make_sample_df():
    return pd.DataFrame({
        'timestamp': ['2025-06-17T12:00:00'],
        'price': [100.0],
        'volume': [50],
        'nk': [0.5]
    })

def test_apply_filters(config):
    df = make_sample_df()
    strat = Strategy(df, config)
    filtered = strat.apply_filters()
    assert not filtered.empty

def test_compute_ema(config):
    df = make_sample_df()
    strat = Strategy(df, config)
    ema = strat.compute_ema(config['short_ema_span'])
    assert isinstance(ema, pd.Series)
    assert ema.iloc[-1] == 100.0
