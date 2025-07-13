

# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_executor_batching.py                        │
# │ Module: tests.test_executor_batching                         │
# │ Doel: Unit-tests voor batching-logic in executor             │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: draft                                               │
# ╰──────────────────────────────────────────────────────────────╯

import pytest
from src.executor import process_order_with_batching

def test_process_order_with_batching_happy(monkeypatch):
    """
    🧪 Test: Happy path with multiple batches.
    Verifieert dat simulate_order voor elke batch wordt aangeroepen.
    """
    # Arrange
    price = 100.0
    amount = 50.0
    slippage_rate = 0.01
    fee_rate = 0.001
    side = "BUY"
    symbol = "AAA"
    window_hours = 2
    max_batches = 3

    # Stub get_average_liquidity (unused in compute_batches stub)
    monkeypatch.setattr('src.executor.get_average_liquidity', lambda sym, wh: 123.0)
    # Stub compute_batches to return three batch amounts
    monkeypatch.setattr('src.executor.compute_batches', lambda amt, avg, mb: [10.0, 15.0, 25.0])

    calls = []
    def fake_simulate_order(p, amt, sl, fr, sd):
        calls.append((p, amt, sl, fr, sd))
        return {"batch": amt}
    monkeypatch.setattr('src.executor.simulate_order', fake_simulate_order)

    # Act
    results = process_order_with_batching(price, amount, slippage_rate, fee_rate, side, symbol, window_hours, max_batches)

    # Assert
    assert calls == [
        (price, 10.0, slippage_rate, fee_rate, side),
        (price, 15.0, slippage_rate, fee_rate, side),
        (price, 25.0, slippage_rate, fee_rate, side),
    ]
    assert results == [{"batch": 10.0}, {"batch": 15.0}, {"batch": 25.0}]

def test_process_order_with_batching_fallback(monkeypatch):
    """
    🧪 Test: Fallback when compute_batches returns empty list.
    Verifieert dat er één batch met het volledige amount wordt uitgevoerd en een warning gelogd.
    """
    # Arrange
    price = 200.0
    amount = 60.0
    slippage_rate = 0.02
    fee_rate = 0.002
    side = "SELL"
    symbol = "BBB"
    window_hours = 1
    max_batches = 5

    monkeypatch.setattr('src.executor.get_average_liquidity', lambda sym, wh: 50.0)
    monkeypatch.setattr('src.executor.compute_batches', lambda amt, avg, mb: [])

    calls = []
    def fake_simulate_order(p, amt, sl, fr, sd):
        calls.append((p, amt, sl, fr, sd))
        return {"batch": amt}
    monkeypatch.setattr('src.executor.simulate_order', fake_simulate_order)

    # Act
    results = process_order_with_batching(price, amount, slippage_rate, fee_rate, side, symbol, window_hours, max_batches)

    # Assert
    assert calls == [
        (price, amount, slippage_rate, fee_rate, side),
    ]
    assert results == [{"batch": amount}]