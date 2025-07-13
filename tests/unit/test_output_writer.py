import pandas as pd
import pytest
from src.outputs.output_writer import save_signals_csv

def test_save_signals_csv_happy(tmp_path):
    # Arrange: DataFrame en pad
    df = pd.DataFrame({
        "timestamp": ["2025-07-01T00:00:00+00:00"],
        "symbol": ["AAA"],
        "price": [1.23],
        "signal": ["BUY"]
    })
    out_file = tmp_path / "out.csv"

    # Act
    save_signals_csv(df, str(out_file))

    # Assert: bestand bestaat en inhoud klopt
    result = pd.read_csv(out_file)
    assert list(result.columns) == ["timestamp", "symbol", "price", "signal"]
    pd.testing.assert_frame_equal(result, df, check_dtype=False)

def test_save_signals_csv_ioerror(monkeypatch, tmp_path):
    # Arrange: dummy DataFrame en pad
    df = pd.DataFrame({"x":[1]})
    out_file = tmp_path / "bad.csv"

    # Stub to_csv om IOError te gooien
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda self, path, index: (_ for _ in ()).throw(IOError("disk full")))

    # Act & Assert
    with pytest.raises(IOError) as exc:
        save_signals_csv(df, str(out_file))
    assert "disk full" in str(exc.value)