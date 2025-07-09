# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_orchestrator_theta.py                        │
# │ Module: orchestrator_theta_tests                              │
# │ Doel: Unit-tests voor src/orchestrator_theta.py               │
# │ Auteur: DeveloperGPT                                          │
# │ Laatste wijziging: 2025-07-08                                 │
# │ Status: draft                                                 │
# ╰──────────────────────────────────────────────────────────────╯
import pandas as pd
import pytest
from src.orchestrator_theta import run_once

def test_run_once_theta_happy(tmp_path, monkeypatch):
    """
    🧪 Test: test_run_once_theta_happy
    Test de 'happy path' van run_once in orchestrator_theta welke een geldige DataFrame genereert en save_signals_csv aanroept.
    ▶️ Arrange: Dummy DataFrame en monkeypatch van dependencies.
    ⏺ Assert: calls dict bevat verwachte df en pad.
    """
    # Arrange
    in_csv = tmp_path / "theta.csv"
    in_csv.write_text("c,d\n3,4")

    dummy_df = pd.DataFrame({"signal": ["SELL"]})
    calls = {}

    monkeypatch.setattr("src.orchestrator_theta.pd.read_csv", lambda p: pd.DataFrame())
    monkeypatch.setattr("src.orchestrator_theta.enrich_dataframe", lambda df: dummy_df)
    monkeypatch.setattr("src.orchestrator_theta.apply_strategy",
                        lambda df: dummy_df)
    monkeypatch.setattr("src.orchestrator_theta.save_signals_csv",
                        lambda df, path: calls.update({"df": df, "path": path}))

    # Act
    out = tmp_path / "theta_out.csv"
    run_once(str(in_csv), str(out))

    # Assert
    assert calls["df"] is dummy_df
    assert calls["path"] == str(out)

def test_run_once_theta_read_error(tmp_path, monkeypatch):
    """
    🧪 Test: test_run_once_theta_read_error
    Test dat run_once FileNotFoundError werpt wanneer de inputbestand ontbreekt.
    ▶️ Arrange: pandas.read_csv gemockt om FileNotFoundError te werpen.
    ⏺ Act & Assert: verwacht FileNotFoundError.
    """
    # Arrange
    bad_path = tmp_path / "nope.csv"
    # pd.read_csv throws FileNotFoundError
    monkeypatch.setattr("src.orchestrator_theta.pd.read_csv",
                        lambda p: (_ for _ in ()).throw(FileNotFoundError("not found")))

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        run_once(str(bad_path), str(tmp_path/"out.csv"))