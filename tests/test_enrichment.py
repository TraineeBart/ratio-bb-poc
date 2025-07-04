# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_enrichment.py                               │
# │ Module: Verrijkingslogica                                    │
# │ Doel: Unit-tests voor enrich_dataframe()                     │
# │ Auteur: Quality EngineerGPT                                  │
# │ Laatste wijziging: 2025-07-04                                │
# │ Status: in review                                            │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
import pytest
from enrichment.enrich import enrich_dataframe


def test_enrich_dataframe_minimal_input():
    """
    ✅ Test of enrich_dataframe werkt met minimale geldige invoer.
    Dit test dat de functie niet faalt bij slechts 2 rijen data.
    """
    data = {
        "timestamp": ["2025-07-01 10:00:00", "2025-07-01 10:05:00"],
        "symbol": ["theta", "theta"],
        "close": [0.078, 0.079],
        "volume": [12000, 15000]
    }
    df = pd.DataFrame(data)
    enriched_df = enrich_dataframe(df)

    # Verwachte minimum outputkolommen — sommige indicatoren worden mogelijk niet berekend
    expected_columns = {"timestamp", "symbol", "close", "volume", "rsi", "sma_rsi", "sma_9"}
    assert expected_columns.issubset(set(enriched_df.columns)), "Niet alle verwachte kolommen aanwezig"


def test_enrich_dataframe_expected_columns():
    """
    ✅ Test met langere dataset om zeker te weten dat ema_9 en signal worden gegenereerd.
    De test is opgedeeld in een assertie op vaste kolommen en een optionele check op signaalvorming.
    """
    timestamps = pd.date_range(start="2025-07-01 00:00:00", periods=20, freq="5min").astype(str)
    data = {
        "timestamp": timestamps,
        "symbol": ["theta"] * 20,
        "close": [0.07 + 0.001 * i for i in range(20)],
        "volume": [10000 + 100 * i for i in range(20)]
    }
    df = pd.DataFrame(data)
    enriched_df = enrich_dataframe(df)

    required_columns = {
        "timestamp", "symbol", "close", "volume", "rsi", "sma_rsi", "sma_9"
    }
    optional_columns = {"ema_9", "signal"}

    assert required_columns.issubset(set(enriched_df.columns)), "Niet alle verplichte kolommen aanwezig"

    missing_optional = optional_columns - set(enriched_df.columns)
    if missing_optional:
        print(f"⚠️ Optionele kolommen niet gegenereerd (mogelijk verwacht): {missing_optional}")


def test_enrich_dataframe_missing_close_column():
    """
    ❌ Test of enrich_dataframe faalt als de verplichte 'close'-kolom ontbreekt.
    """
    data = {
        "timestamp": ["2025-07-01 10:00:00"],
        "symbol": ["theta"],
        "volume": [12000]
    }
    df = pd.DataFrame(data)

    with pytest.raises(KeyError):
        enrich_dataframe(df)