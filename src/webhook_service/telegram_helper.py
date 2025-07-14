# ╭───────────────────────────────────────────────────────────╮
# │ File: src/webhook_service/telegram_helper.py              │
# │ Module: webhook_service                                   │
# │ Doel: Versturen van Telegram-meldingen via Bot API        │
# │ Auteur: DeveloperGPT                                     │
# │ Laatste wijziging: 2025-07-14                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯

import os
import requests
import logging

def send_telegram_message(text: str):
    """
    🧠 Functie: send_telegram_message
    Verstuur een bericht naar Telegram via de Bot API.

    ▶ In:
        - text (str): Het bericht dat verstuurd wordt

    💡 Gebruikt:
        - TELEGRAM_TOKEN en TELEGRAM_CHAT_ID uit omgevingsvariabelen of .env
    """
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logging.error("Telegram token of chat_id ontbreekt in omgevingsvariabelen.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Fout bij verzenden Telegram bericht: {e}")