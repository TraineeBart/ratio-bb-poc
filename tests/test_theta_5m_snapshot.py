# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_theta_5m_snapshot.py                        │
# │ Module: Snapshot Testing                                     │
# │ Doel: Snapshot-validatie van verrijkte theta 5m dataset      │
# │ Auteur: Quality EngineerGPT                                  │
# │ Laatste wijziging: 2025-07-01                                │
# │ Status: stable                                               │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
from pathlib import Path

def test_theta_5m_column_headers_snapshot(snapshot):
    """
    🧠 Functie: test_theta_5m_column_headers_snapshot
    Verifieert of de kolomstructuur van de verrijkte theta 5m CSV overeenkomt met de opgeslagen snapshot.

    ▶️ In:
        - snapshot: Syrupy snapshot fixture

    ⏺ Out:
        - Assertion tegen bekende kolomlijst
    """
    file_path = Path("/opt/ratio-bb-poc/data/signals_bb_theta_5m.csv")
    df = pd.read_csv(file_path)
    actual_columns = list(df.columns)

    assert actual_columns == snapshot