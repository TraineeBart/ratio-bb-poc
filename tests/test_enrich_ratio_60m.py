

# ╭────────────────────────────────────────────────────────────────────────────╮
# │ File: tests/test_enrich_ratio_60m.py                                       │
# │ Module: Enrichment Testing (60m)                                           │
# │ Doel: Basisvalidatie van verrijkte RATIO 60m dataset                      │
# │ Auteur: Quality EngineerGPT                                                │
# │ Laatste wijziging: 2025-07-01                                              │
# │ Status: draft                                                              │
# ╰────────────────────────────────────────────────────────────────────────────╯

import pandas as pd
import numpy as np
from pathlib import Path
import pytest; pytest.skip("Nog niet actief: dataset wordt (nog) niet gegenereerd door Ratio BB POC pipeline", allow_module_level=True)

def test_enrich_ratio_60m_structure_and_quality():
    """
    🧪 Controleert of de verrijkte 60m RATIO dataset valide is:
    - Kolomnamen kloppen
    - Geen NaN- of inf-waarden
    - Dataset bevat voldoende rijen
    """
    file_path = Path("/opt/tradingbot/data/enriched/ratio/60m/ratio-60m-enriched.csv")
    df = pd.read_csv(file_path)

    expected_columns = [
        "timestamp", "close", "rsi", "sma_rsi", "sma_9", "sma",
        "upper_band", "lower_band", "ratio_lower", "ratio_upper", "signal"
    ]

    assert list(df.columns) == expected_columns, "❌ Kolomnamen komen niet overeen met verwachting"
    assert not df.isnull().values.any(), "❌ Dataset bevat NaN-waarden"
    assert not np.isinf(df.values).any(), "❌ Dataset bevat inf-waarden"
    assert len(df) > 50, "❌ Dataset bevat te weinig rijen"