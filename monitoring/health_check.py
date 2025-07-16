# Health check script voor Ratio-BB-POC
# Controleert de outbox file en Telegram bereikbaarheid

import os
import time
import requests

OUTBOX_PATH = '/opt/ratio-bb-poc/outbox/events.jsonl'
TELEGRAM_API = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/getMe"

def check_outbox():
    if not os.path.exists(OUTBOX_PATH):
        return "[✖] Outbox events.jsonl bestaat niet"
    mtime = time.time() - os.path.getmtime(OUTBOX_PATH)
    if mtime > 60:
        return f"[!] Outbox: geen updates sinds {int(mtime)} seconden"
    return "[✔] Outbox events.jsonl OK"

def check_telegram():
    try:
        resp = requests.get(TELEGRAM_API, timeout=3)
        if resp.status_code == 200:
            return "[✔] Telegram bot OK"
        return f"[!] Telegram API status {resp.status_code}"
    except Exception as e:
        return f"[✖] Telegram fout: {e}"

if __name__ == "__main__":
    print(check_outbox())
    print(check_telegram())