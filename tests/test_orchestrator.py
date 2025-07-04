# ║ File: tests/test_orchestrator.py
# ║ Module: orchestrator (test)
# ║ Doel: Test de run_once-functie op correcte verwerking en outputbestand
# ║ Auteur: QualityEngineerGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from orchestrator import run_once

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
