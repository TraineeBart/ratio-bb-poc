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