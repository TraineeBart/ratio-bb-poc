# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/outputs/webhook.py                                │
# │ Module: outputs.webhook                                     │
# │ Doel: Helper voor het dispatchen van webhooks met JSON      │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-08                                │
# │ Status: draft                                               │
# ╰──────────────────────────────────────────────────────────────╯
"""
src/outputs/webhook.py

Helper module for dispatching webhooks with JSON payloads.
"""

import os
import requests

def dispatch_webhook(payload: dict, timeout: int = 10) -> None:
    """
    Send a JSON payload to the configured WEBHOOK_URL via HTTP POST.

    Args:
        payload (dict): The JSON-serializable payload to send.
        timeout (int): Request timeout in seconds (default: 10).

    Raises:
        EnvironmentError: if WEBHOOK_URL is not set.
        requests.RequestException: if the HTTP request fails.
    """
    url = os.getenv("WEBHOOK_URL")
    if not url:
        raise EnvironmentError("WEBHOOK_URL environment variable not set")

    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
