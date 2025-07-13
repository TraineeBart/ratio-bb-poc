# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_orchestrator_tfuel.py                       │
# │ Module: orchestrator_tfuel_tests                             │
# │ Doel: Unit-tests voor src/orchestrator.py                    │
# │ Auteur: DeveloperGPT                                         │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: actief en stabiel                                    │
# ╰──────────────────────────────────────────────────────────────╯
import pandas as pd
import pytest
from src.orchestrator_tfuel import run_once

def test_run_once_happy_path(tmp_path, monkeypatch):
    """
    🧪 Test: test_run_once_happy_path
    Test de 'happy path' van run_once in orchestrator voor TFUEL, waarmee een dummy DataFrame wordt verwerkt en save_signals_csv wordt aangeroepen.
    ▶️ Arrange: Dummy DataFrame en monkeypatch van afhankelijkheden.
    ⏺ Assert: calls dict bevat verwachte df en pad.
    """
    # Arrange
    input_csv = tmp_path / "in.csv"
    input_csv.write_text("dummy,data\n1,2")

    dummy_df = pd.DataFrame({"signal": ["BUY", "HOLD"]})
    calls = {}

    # Stub pandas.read_csv → lege DataFrame
    monkeypatch.setattr("src.orchestrator_tfuel.pd.read_csv", lambda path: pd.DataFrame())

    # Stub enrich_dataframe → geeft dummy_df terug
    monkeypatch.setattr("src.orchestrator_tfuel.enrich_dataframe",
                        lambda df: dummy_df)

    # Stub apply_strategy → controle dat enriched DataFrame binnenkomt
    def fake_strategy(df):
        assert df is dummy_df
        return dummy_df
    monkeypatch.setattr("src.orchestrator_tfuel.apply_strategy", fake_strategy)

    # Stub save_signals_csv → registreer args
    def fake_save(df, path):
        calls["df"] = df
        calls["path"] = path
    monkeypatch.setattr("src.orchestrator_tfuel.save_signals_csv", fake_save)

    # Act
    out_path = str(tmp_path / "out.csv")
    run_once(str(input_csv), out_path)

    # Assert
    assert calls["df"] is dummy_df
    assert calls["path"] == out_path

def test_run_once_csv_write_error(tmp_path, monkeypatch):
    """
    🧪 Test: test_run_once_csv_write_error
    Test dat run_once een IOError werpt bij een fout in save_signals_csv (bijv. disk full).
    ▶️ Arrange: save_signals_csv gemockt om IOError te gooien.
    ⏺ Act & Assert: verwacht IOError met correcte message.
    """
    # Arrange
    input_csv = tmp_path / "in.csv"
    input_csv.write_text("x,y\n1,2")

    # Stub everything up to save_signals_csv
    monkeypatch.setattr("src.orchestrator_tfuel.pd.read_csv", lambda p: pd.DataFrame())
    monkeypatch.setattr("src.orchestrator_tfuel.enrich_dataframe", lambda df: df)
    # Stub apply_strategy to return an empty DataFrame with a 'signal' column, to satisfy value_counts()
    monkeypatch.setattr("src.orchestrator_tfuel.apply_strategy", lambda df: pd.DataFrame({"signal": []}))

    # save_signals_csv raise IOError
    def fake_save(df, path):
        raise IOError("disk full")
    monkeypatch.setattr("src.orchestrator_tfuel.save_signals_csv", fake_save)

    # Act & Assert
    with pytest.raises(IOError) as exc:
        run_once(str(input_csv), str(tmp_path/"out.csv"))
    assert "disk full" in str(exc.value)