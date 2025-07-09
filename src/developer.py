# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/developer.py                                      │
# │ Module: developer                                           │
# │ Doel: Centraal laden van configuratie uit YAML en omgeving  │
# │ Auteur: DeveloperGPT                                       │
# │ Laatste wijziging: 2025-07-04                              │
# │ Status: stable                                             │
# ╰──────────────────────────────────────────────────────────────╯

import yaml
import os

def load_config(config_path=None):
    if config_path is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
    with open(config_path) as f:
        config = yaml.safe_load(f)
    # 🔹 Override credentials from environment if provided
    for env_var, key in [
        ("KUCOIN_API_KEY", "kucoin_api_key"),
        ("KUCOIN_API_SECRET", "kucoin_api_secret"),
        ("KUCOIN_PASSPHRASE", "kucoin_passphrase")
    ]:
        val = os.getenv(env_var)
        if val:
            config[key] = val
    # 🔹 Ensure webhook_url
    if os.getenv("WEBHOOK_URL"):
        config["webhook_url"] = os.getenv("WEBHOOK_URL")
    return config
