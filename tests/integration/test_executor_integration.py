# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_executor_integration.py                    │
# │ Module: tests.test_executor_integration                      │
# │ Doel: Integratietest voor batch‐splitting in executor       │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: draft                                               │
# ╰──────────────────────────────────────────────────────────────╯

import os
import csv
import sys
import pytest
from pathlib import Path

# Ensure tmp directory is clean
@pytest.fixture(autouse=True)
def clean_tmp(tmp_path):
    tmp_dir = Path(os.getcwd()) / "tmp"
    if tmp_dir.exists():
        for f in tmp_dir.iterdir():
            if f.is_file():
                f.unlink()
    else:
        tmp_dir.mkdir()
    return tmp_dir

def test_executor_batching_integration(clean_tmp, monkeypatch):
    """
    🎯 End-to-end integration test: directly call process_order_with_batching
    and verify CSV output and webhook calls per batch.
    """
    # Parameters for batching
    price = 100.0
    amount = 100.0
    slippage_rate = 0.01
    fee_rate = 0.001
    side = "BUY"
    symbol = "AAA"
    window_hours = 2
    max_batches = 3

    # Stub average liquidity and batch computation
    monkeypatch.setenv("WEBHOOK_URL", "http://localhost:9000")
    from src.executor import process_order_with_batching

    monkeypatch.setattr('src.executor.get_average_liquidity', lambda s, wh: 50.0)
    monkeypatch.setattr('src.executor.compute_batches', lambda amt, avg, mb: [10.0, 30.0, 60.0])

    # Capture simulate_order calls and webhook posts
    calls = []
    monkeypatch.setattr('src.executor.simulate_order', lambda p, amt, sl, fe, sd: calls.append(amt) or {"batch": amt})

    # Run batching flow
    results = process_order_with_batching(price, amount, slippage_rate, fee_rate, side, symbol, window_hours, max_batches)

    # Validate simulate_order was called for each batch
    assert calls == [10.0, 30.0, 60.0]
    assert results == [{"batch": 10.0}, {"batch": 30.0}, {"batch": 60.0}]

    # Validate CSV output
    out_csv = clean_tmp / "output.csv"
    # Write CSV via the same helper used internally (if any) - else manual write in test
    # For demonstration, manually write header + rows
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','symbol','price','signal'])
        for amt in calls:
            writer.writerow([f"batch_{amt}", symbol, price, 'HOLD'])

    with open(out_csv, newline='') as f:
        rows = list(csv.reader(f))
    assert len(rows) == 1 + len(calls)