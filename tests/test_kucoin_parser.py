import pytest
import os, sys
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