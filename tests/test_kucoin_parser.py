import pytest
import os, sys
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser.kucoin_parser import parse_klines
from src.models.kucoin_models import Candle

def test_parse_klines_empty():
    assert parse_klines([]) == []

def test_parse_klines_standard():
    data = [
        ["1620000000", "1.0", "2.0", "0.5", "1.5", "100.0", "0"]
    ]
    candles = parse_klines(data)
    assert len(candles) == 1
    c = candles[0]
    assert isinstance(c, Candle)
    assert c.time == 1620000000
    assert c.open == 1.0
    assert c.high == 2.0
    assert c.low == 0.5
    assert c.close == 1.5
    assert c.volume == 100.0


def test_parse_klines_missing_fields():
    # Each row must have 6 elements; missing fields should raise ValueError
    malformed = [
        ["1620000000", "1.0", "2.0", "0.5", "1.5"]  # only 5 fields
    ]
    with pytest.raises(ValueError):
        parse_klines(malformed)


def test_parse_klines_extra_fields():
    # Extra fields should be ignored and first six mapped
    data = [
        ["1620000000", "1.0", "2.0", "0.5", "1.5", "100.0", "XTRA", "Y"]
    ]
    candles = parse_klines(data)
    assert len(candles) == 1
    c = candles[0]
    # Extra columns beyond the sixth should not affect parsing
    assert c.time == 1620000000 and c.open == 1.0 and c.high == 2.0
    assert c.low == 0.5 and c.close == 1.5 and c.volume == 100.0


import pytest

@pytest.mark.parametrize("field, bad_value", [
    ("timestamp", "not_an_int"),
    ("open",      "bad_float"),
    ("high",      None),
    ("low",       "1.two"),
    ("close",     {}),
    ("volume",    "NaN"),
])
def test_parse_klines_wrong_type(field, bad_value):
    # Create a valid row and then inject a bad value
    base = ["1620000000", "1.0", "2.0", "0.5", "1.5", "100.0"]
    mapping = {
        "timestamp": 0, "open": 1, "high": 2,
        "low": 3, "close": 4, "volume": 5
    }
    row = list(base)
    row[mapping[field]] = bad_value
    if field == "volume" and bad_value == "NaN":
        # float("NaN") yields nan, so parse_klines should succeed, volume is nan
        candles = parse_klines([row])
        assert len(candles) == 1
        assert math.isnan(candles[0].volume)
    else:
        with pytest.raises((ValueError, TypeError)):
            parse_klines([row])