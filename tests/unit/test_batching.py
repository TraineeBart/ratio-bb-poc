# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_batching.py                                │
# │ Module: test_batching                                        │
# │ Doel: Unit tests for compute_batches                         │
# │ Auteur: Data-EngineerGPT                                     │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: stable                                               │
# ╰──────────────────────────────────────────────────────────────╯

import pytest

from src.batching import compute_batches

def test_equal_split_within_liquidity():
    amount = 100.0
    avg_liquidity = 20.0
    # per batch = 100/10 = 10 <= liquidity
    batches = compute_batches(amount, avg_liquidity, max_batches=10)
    assert len(batches) == 10
    assert all(batch == pytest.approx(10.0) for batch in batches)
    assert sum(batches) == pytest.approx(amount)

def test_min_batches_when_exceeds_liquidity():
    amount = 95.0
    avg_liquidity = 20.0
    # amount/liquidity = 4.75 → needed batches = 5
    batches = compute_batches(amount, avg_liquidity, max_batches=10)
    assert len(batches) == 5
    assert all(batch == pytest.approx(95.0/5) for batch in batches)
    assert sum(batches) == pytest.approx(amount)

def test_cap_batches_at_max_batches():
    amount = 300.0
    avg_liquidity = 20.0
    # amount/liquidity = 15 → needed=15 but capped to max_batches=10
    batches = compute_batches(amount, avg_liquidity, max_batches=10)
    assert len(batches) == 10
    assert all(batch == pytest.approx(300.0/10) for batch in batches)
    assert sum(batches) == pytest.approx(amount)

def test_amount_non_positive_returns_empty():
    assert compute_batches(0.0, 100.0) == []
    assert compute_batches(-10.0, 100.0) == []

def test_liquidity_non_positive_returns_empty():
    assert compute_batches(100.0, 0.0) == []
    assert compute_batches(100.0, -5.0) == []

def test_invalid_max_batches_raises():
    with pytest.raises(ValueError):
        compute_batches(100.0, 10.0, max_batches=0)
    with pytest.raises(ValueError):
        compute_batches(100.0, 10.0, max_batches=-3)

def test_default_max_batches():
    # default max_batches should be 10
    amount = 50.0
    avg_liquidity = 10.0
    batches = compute_batches(amount, avg_liquidity)
    assert len(batches) == 10
    assert sum(batches) == pytest.approx(amount)
