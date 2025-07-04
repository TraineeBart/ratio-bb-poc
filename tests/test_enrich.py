# ║ File: tests/test_enrich.py
# ║ Module: enrichment (test)
# ║ Doel: Test de enrich_dataframe-functie op correcte output en kolommen
# ║ Auteur: QualityEngineerGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
import pytest
from enrichment.enrich import enrich_dataframe

def test_enrich_dataframe_output():
    # Voorbeelddata (kunstmatig, met oplopende close-prijzen)
    data = {
        "timestamp": pd.date_range("2025-01-01", periods=30, freq="5min"),
        "close": [100 + i for i in range(30)]
    }
    df = pd.DataFrame(data)

    enriched = enrich_dataframe(df)

    # Controleer dat de output kolommen bevat
    assert "rsi" in enriched.columns
    assert "sma_rsi" in enriched.columns
    assert "sma_9" in enriched.columns

    # Controleer dat er geen NaN-waarden overblijven (na dropna)
    assert not enriched.isnull().values.any()

    # Controleer dat het resultaat een DataFrame is met minder rijen (door rolling windows)
    assert len(enriched) < len(df)