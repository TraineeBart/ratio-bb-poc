# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_candles.py                                  │
# │ Module: test_candles                                         │
# │ Doel: Unit-tests voor CandleAggregator                       │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-04                                │
# │ Status: draft                                              │
# ╰──────────────────────────────────────────────────────────────╯

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import pandas as pd
import pytest
from utils.candles import CandleAggregator

def test_single_candle_emission():
    emitted = []
    def callback(candle):
        emitted.append(candle)

    aggregator = CandleAggregator(period='5T', on_candle=callback)

    # Feed ticks within one 5-minute bucket
    aggregator.on_tick({'timestamp': '2025-07-04T00:00:10', 'price': 100, 'volume': 10})
    aggregator.on_tick({'timestamp': '2025-07-04T00:04:59', 'price': 105, 'volume': 5})

    # Feed one tick in next bucket to trigger emission of first candle
    aggregator.on_tick({'timestamp': '2025-07-04T00:05:00', 'price': 102, 'volume': 7})

    # There should be exactly one candle emitted
    assert len(emitted) == 1
    candle = emitted[0]

    # Check candle fields
    assert candle['open'] == 100
    assert candle['high'] == 105
    assert candle['low'] == 100
    assert candle['close'] == 105
    assert candle['volume'] == 15
    assert candle['start_ts'] == pd.Timestamp('2025-07-04T00:00:00')

def test_multiple_candles_emission():
    emitted = []
    def callback(candle):
        emitted.append(candle)

    aggregator = CandleAggregator(period='5T', on_candle=callback)

    # Feed ticks spanning three buckets
    # Bucket 1: 00:00:00 - 00:04:59
    aggregator.on_tick({'timestamp': '2025-07-04T00:00:10', 'price': 100, 'volume': 10})
    aggregator.on_tick({'timestamp': '2025-07-04T00:04:59', 'price': 105, 'volume': 5})

    # Bucket 2: 00:05:00 - 00:09:59
    aggregator.on_tick({'timestamp': '2025-07-04T00:05:00', 'price': 102, 'volume': 7})
    aggregator.on_tick({'timestamp': '2025-07-04T00:09:30', 'price': 108, 'volume': 3})

    # Bucket 3: 00:10:00 - 00:14:59
    aggregator.on_tick({'timestamp': '2025-07-04T00:10:00', 'price': 107, 'volume': 8})

    # Feeding a tick in bucket 4 to trigger emission of bucket 3 candle
    aggregator.on_tick({'timestamp': '2025-07-04T00:15:00', 'price': 110, 'volume': 2})

    # There should be exactly three candles emitted
    assert len(emitted) == 3

    # Check start_ts order and correctness
    expected_starts = [
        pd.Timestamp('2025-07-04T00:00:00'),
        pd.Timestamp('2025-07-04T00:05:00'),
        pd.Timestamp('2025-07-04T00:10:00'),
    ]
    for candle, expected_start in zip(emitted, expected_starts):
        assert candle['start_ts'] == expected_start

    # Additional checks for candle contents can be added if desired
    # For example, check first candle
    c1 = emitted[0]
    assert c1['open'] == 100
    assert c1['high'] == 105
    assert c1['low'] == 100
    assert c1['close'] == 105
    assert c1['volume'] == 15

    # Second candle
    c2 = emitted[1]
    assert c2['open'] == 102
    assert c2['high'] == 108
    assert c2['low'] == 102
    assert c2['close'] == 108
    assert c2['volume'] == 10

    # Third candle
    c3 = emitted[2]
    assert c3['open'] == 107
    assert c3['high'] == 107
    assert c3['low'] == 107
    assert c3['close'] == 107
    assert c3['volume'] == 8
