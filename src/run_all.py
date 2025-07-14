# ║ File: src/run_all.py
# ║ Module: orchestrator_batch
# ║ Doel: Voert alle orchestrator-scripts uit voor TFUEL, THETA en RATIO
# ║ Auteur: ArchitectGPT
# ║ Laatste wijziging: 2025-07-01
# ║ Status: draft

import subprocess

def run_script(script_name):
    print(f"\n🚀 Start {script_name}...")
    result = subprocess.run(["python", f"src/{script_name}"])
    if result.returncode == 0:
        print(f"✅ {script_name} voltooid.")
    else:
        print(f"❌ {script_name} gaf een foutmelding.")

if __name__ == "__main__":
    run_script("orchestrator.py")         # tfuel
    run_script("orchestrator_theta.py")   # theta
    run_script("orchestrator_ratio.py")   # ratio
# ║ File: src/run_all.py
# ║ Module: orchestrator_batch
# ║ Doel: Continue loop voor live- of sim-mode execution van run_once.py
# ║ Auteur: DeveloperGPT
# ║ Laatste wijziging: 2025-07-13
# ║ Status: stable

import time
import logging
import argparse
import os
from orchestration.run_once import run_once_main

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Run continuous execution loop.")
    parser.add_argument("--mode", type=str, default=os.getenv("MODE", "sim"), help="Execution mode: sim | live | replay")
    parser.add_argument("--interval", type=int, default=300, help="Interval tussen runs in seconden (default: 300)")
    return parser.parse_args()

def run_all():
    args = parse_args()
    logging.info(f"Start run_all loop in {args.mode.upper()} mode. Interval: {args.interval} sec")

    while True:
        try:
            logging.info("🔄 Start nieuwe batchronde")

            run_once_main(mode=args.mode)

            logging.info("✅ Batchronde afgerond. Wacht op volgende run...")
            time.sleep(args.interval)

        except Exception as e:
            logging.error(f"⚠️ Fout tijdens batchronde: {e}")
            logging.info("Wachten 10 seconden voor herstart...")
            time.sleep(10)

if __name__ == "__main__":
    run_all()