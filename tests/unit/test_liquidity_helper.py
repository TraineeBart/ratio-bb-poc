# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_liquidity_helper.py                        │
# │ Module: test_liquidity_helper                                │
# │ Doel: Unit tests for get_average_liquidity                   │
# │ Auteur: Data-EngineerGPT                                     │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: stable                                               │
# ╰──────────────────────────────────────────────────────────────╯

import pytest
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.liquidity_helper import get_average_liquidity, DATA_ROOT

from src.liquidity_helper import get_average_liquidity, DATA_ROOT

def create_dummy_csv(tmp_path, base_asset, rows):
    """
    Helper to create a dummy 5m-full.csv file with given rows.
    Each row is a tuple: (timestamp_ms, volume)
    """
    asset_dir = tmp_path / base_asset / "5m"
    asset_dir.mkdir(parents=True, exist_ok=True)
    csv_path = asset_dir / f"{base_asset}-5m-full.csv"
    df = pd.DataFrame({
        "timestamp": [ts for ts, _ in rows],
        "open": 1.0,
        "high": 1.0,
        "low": 1.0,
        "close": 1.0,
        "volume": [vol for _, vol in rows],
    })
    df.to_csv(csv_path, index=False)
    return csv_path

@pytest.fixture(autouse=True)
def patch_data_root(tmp_path, monkeypatch):
    # Redirect DATA_ROOT to temporary directory
    monkeypatch.setattr("src.liquidity_helper.DATA_ROOT", str(tmp_path))

def test_happy_path(tmp_path):
    base = "theta"
    now = datetime.now(timezone.utc)
    # Create two points: one within window, one outside
    rows = [
        (int((now - timedelta(hours=1)).timestamp() * 1000), 100),
        (int((now - timedelta(hours=25)).timestamp() * 1000), 200),
    ]
    create_dummy_csv(tmp_path, base, rows)

    avg = get_average_liquidity("THETA-USDT", window_hours=24)
    # only the first row counts
    assert avg == pytest.approx(100.0)

def test_empty_after_filter(tmp_path):
    base = "tfuel"
    now = datetime.now(timezone.utc)
    # volumes <= 0 or old timestamps
    rows = [
        (int((now - timedelta(hours=1)).timestamp() * 1000), 0),
        (int((now - timedelta(hours=25)).timestamp() * 1000), 50),
    ]
    create_dummy_csv(tmp_path, base, rows)

    avg = get_average_liquidity("TFUEL-USDT", window_hours=24)
    assert avg == 0.0

def test_missing_file(tmp_path):
    # No CSV created
    with pytest.raises(ValueError) as exc:
        get_average_liquidity("FOO-USDT", window_hours=1)
    assert "Data file not found for symbol" in str(exc.value)

def test_missing_columns(tmp_path):
    base = "bar"
    # Create CSV without 'volume' column
    asset_dir = tmp_path / base / "5m"
    asset_dir.mkdir(parents=True)
    pd.DataFrame({
        "timestamp": [int(datetime.now(timezone.utc).timestamp() * 1000)],
        "open": [1.0],
    }).to_csv(asset_dir / f"{base}-5m-full.csv", index=False)

    with pytest.raises(ValueError) as exc:
        get_average_liquidity("BAR-USDT", window_hours=1)
    assert "must contain 'timestamp' and 'volume'" in str(exc.value)

def test_negative_window_hours(tmp_path):
    base = "theta"
    create_dummy_csv(tmp_path, base, [
        (int(datetime.now(timezone.utc).timestamp() * 1000), 100)
    ])
    with pytest.raises(ValueError) as exc:
        get_average_liquidity("THETA-USDT", window_hours=-5)
    assert "window_hours must be a positive integer" in str(exc.value)


def test_zero_window_hours(tmp_path):
    base = "theta"
    # Create a valid dummy CSV
    rows = [
        (int(datetime.now(timezone.utc).timestamp() * 1000), 100)
    ]
    create_dummy_csv(tmp_path, base, rows)
    with pytest.raises(ValueError) as exc:
        get_average_liquidity("THETA-USDT", window_hours=0)
    assert "window_hours must be a positive integer" in str(exc.value)