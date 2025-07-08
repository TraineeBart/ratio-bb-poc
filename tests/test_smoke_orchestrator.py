# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_smoke_orchestrator.py                       │
# │ Module: smoke_orchestrator_tests                             │
# │ Doel: Smoke-test van run_once (end-to-end CSV I/O zonder mocks) │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: integration                                          │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
import pytest
from src.orchestrator_tfuel import run_once

@pytest.mark.integration
def test_run_once_creates_output(tmp_path):
    # Maak dummy input CSV
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    df = pd.DataFrame({
        "timestamp": pd.date_range("2025-01-01", periods=30, freq="5min"),
        "close": [100 + (i % 10) for i in range(30)]
    })
    df.to_csv(input_path, index=False)

    # Run de orchestrator
    run_once(str(input_path), str(output_path))

    # Controleer dat outputbestand bestaat
    assert output_path.exists()

    # Controleer dat er signalen zijn
    result_df = pd.read_csv(output_path)
    assert "signal" in result_df.columns
    assert not result_df.empty
    # Controleer dat signal-waarden geldig zijn
    valid_signals = {"BUY", "HOLD", "SELL", "NO_SWAP"}
    assert set(result_df["signal"].unique()).issubset(valid_signals)
