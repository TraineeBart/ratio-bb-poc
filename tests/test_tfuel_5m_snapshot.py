#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_tfuel_5m_snapshot.py                        │
# │ Module: Snapshot Testing                                     │
# │ Doel: Snapshot-validatie van verrijkte tfuel 5m dataset      │
# │ Auteur: Quality EngineerGPT                                  │
# │ Laatste wijziging: 2025-07-01                                │
# │ Status: stable                                               │
# ╰──────────────────────────────────────────────────────────────╯

import pytest
import pandas as pd
from pathlib import Path


@pytest.mark.skip(reason="⏭️ Skipped in CI: test vereist lokale TFUEL-signaaldata die niet in GitHub aanwezig is.")
def test_tfuel_5m_column_headers_snapshot(snapshot):
    """
    🧠 Functie: test_tfuel_5m_column_headers_snapshot
    Verifieert of de kolomstructuur van het TFUEL 5m signaalbestand (gegenereerd door de strategy) overeenkomt met de opgeslagen snapshot.

    ▶️ In:
        - snapshot: Syrupy snapshot fixture

    ⏺ Out:
        - Assertion tegen bekende kolomlijst
    """
    file_path = Path("/opt/ratio-bb-poc/data/signals_bb_tfuel_5m.csv")
    df = pd.read_csv(file_path)
    actual_columns = list(df.columns)

    assert actual_columns == snapshot