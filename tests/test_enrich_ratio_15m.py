# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_enrich_ratio_15m.py                         │
# │ Module: Enrichment Test (Ratio 15m)                          │
# │ Doel: Validatie van verrijkte ratio-data op 15m interval     │
# │ Auteur: Quality EngineerGPT                                  │
# │ Laatste wijziging: 2025-07-01                                │
# │ Status: draft                                                │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
import numpy as np
from pathlib import Path
import pytest; pytest.skip("Nog niet actief: dataset wordt (nog) niet gegenereerd door Ratio BB POC pipeline", allow_module_level=True)

def test_ratio_15m_enriched_structure():
    """
    ✅ Verifieert de kolomstructuur van de verrijkte 15m ratio dataset.
    """
    file_path = Path("/opt/tradingbot/data/enriched/ratio/15m/ratio-15m-enriched.csv")
    df = pd.read_csv(file_path)
    expected_columns = [
        "timestamp", "close", "rsi", "sma_rsi", "sma_9", "sma",
        "upper_band", "lower_band", "ratio_lower", "ratio_upper", "signal"
    ]
    assert list(df.columns) == expected_columns, "Kolomnamen of volgorde wijkt af"

def test_ratio_15m_enriched_no_nans_or_infs():
    """
    ✅ Controleert op aanwezigheid van NaN of inf-waarden in de dataset.
    """
    file_path = Path("/opt/tradingbot/data/enriched/ratio/15m/ratio-15m-enriched.csv")
    df = pd.read_csv(file_path)
    assert not df.isnull().values.any(), "Dataset bevat NaN-waarden"
    assert not np.isinf(df.select_dtypes(include=[np.number])).values.any(), "Dataset bevat inf-waarden"

def test_ratio_15m_enriched_min_length():
    """
    ✅ Verifieert dat de dataset een minimale lengte heeft (bijv. > 100 rijen).
    """
    file_path = Path("/opt/tradingbot/data/enriched/ratio/15m/ratio-15m-enriched.csv")
    df = pd.read_csv(file_path)
    assert len(df) > 100, "Te weinig rijen in de verrijkte dataset"
