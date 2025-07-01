import os
import sys
import runpy
import pandas as pd
import pytest
from pathlib import Path

def test_strategy_main_writes_output(tmp_path, monkeypatch, capsys):
    # 1) Maak een kleine CSV-input
    input_df = pd.DataFrame({
        'price': [1.0, 2.0, 3.0],
        'nk': [1, 2, 3],
        'volume': [10, 20, 30]
    })
    csv_in = tmp_path / 'input.csv'
    input_df.to_csv(csv_in, index=False)

    # 2) Bepaal output-pad
    csv_out = tmp_path / 'output.csv'

    # 3) Stub load_config zodat de script een bekende config gebruikt
    import developer
    monkeypatch.setattr(developer, 'load_config', lambda: {
        'nk_threshold': 0,
        'volume_threshold': 0,
        'short_ema_span': 2
    })

    # 4) Stel sys.argv in voor het script
    monkeypatch.setattr(sys, 'argv', [
        'src/strategy.py',
        '--data', str(csv_in),
        '--output', str(csv_out)
    ])

    # 5) Run de module als script (cover __main__-block)
    sys.modules.pop('src.strategy', None)
    runpy.run_module('src.strategy', run_name='__main__')

    # 6) Controleer stdout JSON-output
    captured = capsys.readouterr()
    # De script output bevat een JSON-string met minimaal het signaal
    assert '"signal"' in captured.out

    # 7) Controleer dat de output-CSV bestaat en de EMA-kolom bevat
    assert csv_out.exists(), "Output CSV niet aangemaakt"
    out_df = pd.read_csv(csv_out)
    assert 'ema_2' in out_df.columns

    # 8) Verifieer dat de EMA-waarden kloppen
    expected_ema = input_df['price'].ewm(span=2, adjust=False).mean()
    pd.testing.assert_series_equal(
        out_df['ema_2'].reset_index(drop=True),
        expected_ema.reset_index(drop=True),
        check_names=False
    )