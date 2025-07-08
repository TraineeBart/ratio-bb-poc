# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/orchestrator_tfuel.py                             │
# │ Module: orchestrator_tfuel                                  │
# │ Doel: Uitvoeren van een volledige analyse-run (load → enrich → strategy → output) │
# │ Auteur: ArchitectGPT                                        │
# │ Laatste wijziging: 2025-07-08                               │
# │ Status: draft                                               │
# ╰──────────────────────────────────────────────────────────────╯
import pandas as pd
from enrichment.enrich import enrich_dataframe
from strategies.bb_ratio_strategy import apply_strategy
from outputs.output_writer import save_signals_csv

def run_once(input_path: str, output_path: str):
    """
    🧠 Functie: run_once
    Laadt een dataset, verrijkt deze, voert een strategie uit en toont output.

    ▶️ In:
        - input_path (str): pad naar CSV-bestand met raw of verrijkte candles
        - output_path (str): pad om output naar weg te schrijven
    ⏺ Out:
        - None (print en opslaan)
    """
    print(f"📥 Inlezen van dataset: {input_path}")
    df = pd.read_csv(input_path)

    print("🧠 Verrijken met RSI/SMA...")
    enriched = enrich_dataframe(df)

    print("📊 Toepassen van BB-ratio-strategie...")
    result = apply_strategy(enriched)

    print("🔢 Aantal gegenereerde signalen:")
    print(result["signal"].value_counts())

    save_signals_csv(result, output_path)

if __name__ == "__main__":
    # Aangepaste paden naar tfuel-data op de VPS
    INPUT = "/opt/tradingbot/data/tfuel/5m/tfuel-5m-recent.csv"
    OUTPUT = "/opt/ratio-bb-poc/data/signals_bb_tfuel_5m.csv"
    run_once(INPUT, OUTPUT)