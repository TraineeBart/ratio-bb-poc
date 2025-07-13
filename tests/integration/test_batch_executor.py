# ╭───────────────────────────────────────────────────────────╮
# │ File: tests/integration/test_batch_executor.py            │
# │ Module: tests/integration                                │
# │ Doel: Integratietest BatchBuilder en Executor pipeline   │
# │ Auteur: Quality EngineerGPT                             │
# │ Laatste wijziging: 2025-07-13                           │
# │ Status: test draft                                      │
# ╰───────────────────────────────────────────────────────────╯

import pytest
from batching.batch_builder import BatchBuilder
from executor.execute_batch import Executor

def test_batch_executor_pipeline():
    # 🔹 Setup: Simuleer 5 signalen
    signals = []
    for i in range(5):
        signals.append({
            'timestamp': '2025-07-13T12:00:00',
            'signal': 'BUY',
            'from_asset': 'USDT',
            'to_asset': 'THETA',
            'amount': 10000,
            'price': 1.0 + i * 0.1
        })

    # 🔹 Bouwen van batches (max 3 per batch default)
    batches = BatchBuilder.build_batch(signals)

    assert len(batches) == 2  # 5 signalen → 2 batches (3+2)

    # 🔹 Verwerken van elke batch via executor
    for batch in batches:
        result = Executor.execute_batch(batch)

        assert 'batch_size' in result
        assert result['batch_size'] == len(batch['signals'])
        assert 'results' in result
        for r in result['results']:
            assert r['status'] == 'executed'
            assert 'executed_price' in r