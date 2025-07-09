# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_enrich_tfuel_60m.py                         │
# │ Module: Enrichment Test                                      │
# │ Doel: Basisvalidatie van de verrijkte 60m TFUEL dataset     │
# │ Auteur: Quality EngineerGPT                                  │
# │ Laatste wijziging: 2025-07-01                                │
# │ Status: draft                                                │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
import numpy as np
from pathlib import Path
import pytest; pytest.skip("Nog niet actief: dataset wordt (nog) niet gegenereerd door Ratio BB POC pipeline", allow_module_level=True)

def test_tfuel_60m_column_structure():
    """
    ✅ Verifieert de kolomstructuur van de verrijkte 60m TFUEL dataset.
    """
    file_path = Path("/opt/tradingbot/data/enriched/tfuel/60m/tfuel-60m-enriched.csv")
    df = pd.read_csv(file_path)
    expected_columns = [
        "timestamp", "close", "rsi", "sma_rsi", "sma_9", "sma",
        "upper_band", "lower_band", "ratio_lower", "ratio_upper", "signal"
    ]
    assert list(df.columns) == expected_columns, "Kolomnamen of volgorde wijkt af"

def test_tfuel_60m_no_nans_or_infs():
    """
    ✅ Controleert op aanwezigheid van NaN of inf-waarden in de dataset.
    """
    file_path = Path("/opt/tradingbot/data/enriched/tfuel/60m/tfuel-60m-enriched.csv")
    df = pd.read_csv(file_path)
    assert not df.isnull().values.any(), "Dataset bevat NaN-waarden"
    assert not np.isinf(df.select_dtypes(include=[np.number])).values.any(), "Dataset bevat inf-waarden"

def test_tfuel_60m_min_length():
    """
    ✅ Verifieert dat de dataset een minimale lengte heeft (bijv. > 100 rijen).
    """
    file_path = Path("/opt/tradingbot/data/enriched/tfuel/60m/tfuel-60m-enriched.csv")
    df = pd.read_csv(file_path)
    assert len(df) > 100, "Te weinig rijen in de verrijkte dataset"
