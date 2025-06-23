import sys
import os
import csv
from datetime import datetime
import requests
import logging
from logging.handlers import RotatingFileHandler

def on_signal(payload: dict):
    webhook_url = os.getenv('WEBHOOK_URL')
    # 1) Write to CSV
    output_csv = os.path.join('tmp', 'output.csv')
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    file_exists = os.path.isfile(output_csv)
    with open(output_csv, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "symbol", "price", "signal"])
        if not file_exists:
            writer.writeheader()
        # ensure timestamp is ISO format
        payload["timestamp"] = datetime.utcnow().isoformat()
        writer.writerow(payload)

    # 2) Post to webhook and log result
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'webhook.log')
    if webhook_url:
        try:
            resp = requests.post(webhook_url, json=payload, timeout=5)
            resp.raise_for_status()
            with open(log_file, mode='a') as logf:
                logf.write(f"{datetime.utcnow().isoformat()} POST {payload}\n")
        except Exception as e:
            with open(log_file, mode='a') as logf:
                logf.write(f"{datetime.utcnow().isoformat()} ERROR {e}\n")

# Logging configuration: rotate logs and set levels before importing ws_client
log_file_path = os.getenv('LOG_FILE', 'logs/app.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    filename=log_file_path,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s'))

# Console handler: duplicate logs to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s'))
root_logger.addHandler(console_handler)
root_logger.addHandler(handler)  # write logs to file as well

# Allow ws_client module to log at INFO (for BUY/SELL events)
logging.getLogger('ws_client').setLevel(logging.INFO)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ws_client import WSClient

def main():
    print("▶️ In main(): starting WebSocket client")
    symbols = os.getenv('SYMBOLS', 'THETA-USDT,TFUEL-USDT').split(',')
    ws = WSClient(symbols)
    ws.set_signal_callback(on_signal)
    ws.run()

if __name__ == '__main__':
    main()
