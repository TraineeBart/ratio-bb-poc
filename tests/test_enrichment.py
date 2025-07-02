# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_enrichment.py                               │
# │ Module: Verrijkingslogica                                    │
# │ Doel: Unit-tests voor enrich_dataframe()                     │
# │ Auteur: Quality EngineerGPT                                  │
# │ Laatste wijziging: 2025-07-01                                │
# │ Status: draft                                                │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
import pytest
from enrichment.enrich import enrich_dataframe


def test_enrich_dataframe_adds_columns():
    """
    🧠 Functie: test_enrich_dataframe_adds_columns
    Test of enrich_dataframe de verwachte verrijkte kolommen toevoegt aan een geldig DataFrame met een 'close' kolom.

    ▶️ In:
        - df: minimaal geldige DataFrame met close- en volumedata

    ⏺ Out:
        - verrijkt DataFrame met o.a. 'ema_9', 'sma_rsi', 'rsi', 'signal'

    💡 Gebruikt:
        - enrich_dataframe uit enrichment.enrich
    """
    data = {
        "timestamp": ["2025-07-01 10:00:00", "2025-07-01 10:05:00"],
        "symbol": ["theta", "theta"],
        "close": [0.078, 0.079],
        "volume": [12000, 15000]
    }
    df = pd.DataFrame(data)
    enriched_df = enrich_dataframe(df)

    expected_columns = {"timestamp", "symbol", "close", "volume", "ema_9", "sma_rsi", "rsi", "signal"}
    assert expected_columns.issubset(set(enriched_df.columns))


def test_enrich_dataframe_missing_price_column():
    """
    🧠 Functie: test_enrich_dataframe_missing_price_column
    Verifieert dat enrich_dataframe faalt als verplichte kolom 'close' ontbreekt.

    ▶️ In:
        - df: DataFrame zonder 'close'-kolom

    ⏺ Out:
        - verwacht een KeyError

    💡 Gebruikt:
        - pytest.raises
    """
    data = {
        "timestamp": ["2025-07-01 10:00:00"],
        "symbol": ["theta"],
        "volume": [12000]
    }
    df = pd.DataFrame(data)

    with pytest.raises(KeyError):
        enrich_dataframe(df)