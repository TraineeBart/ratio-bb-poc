# ║ File: src/orchestrator_ratio.py
# ║ Module: orchestrator_ratio
# ║ Doel: Verrijken en signaleren op basis van RATIO (THETA/TFUEL)
# ║ Auteur: ArchitectGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import pandas as pd
from outputs.output_writer import save_signals_csv
from enrichment.enrich import enrich_dataframe
from strategies.bb_ratio_strategy import apply_strategy

def run_once(input_path: str, output_path: str):
    print(f"📥 Inlezen van dataset: {input_path}")
    df = pd.read_csv(input_path)
    df = df.rename(columns={"ratio": "close"})
    print("🧠 Verrijken met RSI/SMA...")
    enriched = enrich_dataframe(df)
    print("📊 Toepassen van BB-ratio-strategie...")
    result = apply_strategy(enriched)
    print("🔢 Aantal gegenereerde signalen:")
    print(result["signal"].value_counts())
    save_signals_csv(result, output_path)

if __name__ == "__main__":
    INPUT = "/opt/tradingbot/data/ratio/5m/ratio-5m-recent.csv"
    OUTPUT = "/opt/ratio-bb-poc/data/signals_bb_ratio_5m.csv"
    run_once(INPUT, OUTPUT)