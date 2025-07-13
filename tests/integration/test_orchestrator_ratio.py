# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_orchestrator_ratio.py                       │
# │ Module: orchestrator_ratio_tests                             │
# │ Doel: Unit-tests voor src/orchestrator_ratio.py              │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: actief                                               │
# ╰──────────────────────────────────────────────────────────────╯
import pandas as pd
import pytest
from src.orchestrator_ratio import run_once

def test_run_once_ratio_happy(tmp_path, monkeypatch):
    """
    🧪 Test: test_run_once_ratio_happy
    Test de 'happy path' van run_once in orchestrator_ratio met een geldige DataFrame en save_signals_csv aanroep.
    ▶️ Arrange: Dummy DataFrame en monkeypatch van afhankelijkheden.
    ⏺ Assert: calls dict bevat verwachte df en pad.
    """
    # Arrange
    in_csv = tmp_path / "ratio.csv"
    in_csv.write_text("ratio\n0.5")

    dummy_enriched = pd.DataFrame({"signal": ["HOLD"]})
    calls = {}

    monkeypatch.setattr("src.orchestrator_ratio.pd.read_csv", lambda p: pd.DataFrame({"ratio": [0.5]}))
    monkeypatch.setattr("src.orchestrator_ratio.enrich_dataframe", lambda df: dummy_enriched)
    monkeypatch.setattr("src.orchestrator_ratio.apply_strategy", lambda df: dummy_enriched)
    monkeypatch.setattr("src.orchestrator_ratio.save_signals_csv",
                        lambda df, path: calls.update({"df": df, "path": path}))

    # Act
    out_file = tmp_path/"ratio_out.csv"
    run_once(str(in_csv), str(out_file))

    # Assert
    assert calls["df"] is dummy_enriched
    assert calls["path"] == str(out_file)

def test_run_once_ratio_missing_column(tmp_path, monkeypatch):
    """
    🧪 Test: test_run_once_ratio_missing_column
    Test dat run_once KeyError werpt bij ontbrekende 'ratio' kolom.
    ▶️ Arrange: pandas.read_csv retourneert DataFrame zonder 'ratio'.
    ⏺ Act & Assert: verwacht KeyError.
    """
    # Arrange: read_csv returns DataFrame without "ratio"
    monkeypatch.setattr("src.orchestrator_ratio.pd.read_csv", lambda p: pd.DataFrame({"foo": [1]}))
    # Act & Assert: KeyError when renaming or later
    with pytest.raises(KeyError):
        run_once(str(tmp_path/"dummy.csv"), str(tmp_path/"out.csv"))