# ║ File: src/outputs/output_writer.py
# ║ Module: outputs
# ║ Doel: Schrijven van strategie-output naar CSV-bestand
# ║ Auteur: ArchitectGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import pandas as pd

def save_signals_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    🧠 Functie: save_signals_csv
    Slaat het resultaat van een strategie-analyse op als CSV-bestand.

    ▶️ In:
        - df (pd.DataFrame): resultaat van apply_strategy()
        - output_path (str): pad om CSV op te slaan
    ⏺ Out:
        - None (bestand wordt weggeschreven)
    """
    print(f"💾 Wegschrijven naar: {output_path}")
    df.to_csv(output_path, index=False)