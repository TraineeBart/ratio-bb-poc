import os
import sys
import pytest
import pandas as pd

# Voeg de src-folder toe aan sys.path zodat Python de helper-module kan vinden
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from liquidity_helper import get_average_liquidity
from unittest.mock import patch

def test_invalid_window_hours():
    with pytest.raises(ValueError):
        get_average_liquidity("TFUEL-USDT", 0)

@patch("os.path.isfile", return_value=False)
def test_csv_not_found(mock_isfile):
    with pytest.raises(FileNotFoundError):
        get_average_liquidity("TFUEL-USDT", 1)

@patch("os.path.isfile", return_value=True)
@patch("pandas.read_csv", return_value=pd.DataFrame())
def test_empty_csv(mock_read_csv, mock_isfile):
    result = get_average_liquidity("TFUEL-USDT", 1)
    assert result == 0.0

@patch("os.path.isfile", return_value=True)
@patch("pandas.read_csv", return_value=pd.DataFrame({'other': [1, 2, 3]}))
def test_missing_volume_column(mock_read_csv, mock_isfile):
    with pytest.raises(KeyError):
        get_average_liquidity("TFUEL-USDT", 1)

@patch("os.path.isfile", return_value=True)
@patch("pandas.read_csv", return_value=pd.DataFrame({'volume': [5, 15, 25, 35]}))
def test_happy_path(mock_read_csv, mock_isfile):
    expected = pd.DataFrame({'volume': [5, 15, 25, 35]})["volume"].mean()
    result = get_average_liquidity("TFUEL-USDT", 1)
    assert result == pytest.approx(expected)