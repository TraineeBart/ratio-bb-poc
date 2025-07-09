# ║ File: src/orchestrator_theta.py
# ║ Module: orchestrator_theta
# ║ Doel: Verrijken en signaleren op basis van THETA
# ║ Auteur: ArchitectGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import pandas as pd
from enrichment.enrich import enrich_dataframe
from strategies.bb_ratio_strategy import apply_strategy
from outputs.output_writer import save_signals_csv

def run_once(input_path: str, output_path: str):
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
    INPUT = "/opt/tradingbot/data/theta/5m/theta-5m-recent.csv"
    OUTPUT = "/opt/ratio-bb-poc/data/signals_bb_theta_5m.csv"
    run_once(INPUT, OUTPUT)