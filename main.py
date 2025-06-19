import sys, os
import requests
import logging
from logging.handlers import RotatingFileHandler

# Logging configuration: rotate logs and set levels before importing ws_client
log_file_path = os.getenv('LOG_FILE', 'logs/app.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)
handler = RotatingFileHandler(
    filename=log_file_path,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s'))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s'))
root_logger.addHandler(console_handler)
root_logger.addHandler(handler)

# Allow ws_client module to log at INFO (for BUY/SELL events)
logging.getLogger('ws_client').setLevel(logging.INFO)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from developer import load_config
from ws_client import WSClient

def main():
    print("▶️ In main(): starting WebSocket client")
    cfg = load_config()
    webhook_url = cfg.get('webhook_url')
    # Determine which symbols to subscribe to
    symbols = cfg.get('symbols', ['THETA-USDT', 'TFUEL-USDT'])
    ws = WSClient(symbols)

    def on_signal(payload: dict):
        # Log every incoming signal payload
        logging.getLogger(__name__).info(f"on_signal payload: {payload}")
        if webhook_url:
            try:
                requests.post(webhook_url, json=payload, timeout=5)
            except Exception as e:
                logging.getLogger(__name__).error(f"Webhook POST failed: {e}")

    ws.set_signal_callback(on_signal)
    ws.run()

if __name__ == '__main__':
    main()
