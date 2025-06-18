import sys, os
import logging
from logging.handlers import RotatingFileHandler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from developer import load_config
from ws_client import WSClient

def main():
    print("▶️ In main(): starting WebSocket client")
    cfg = load_config()
    # Ensure logs directory exists
    log_file_path = cfg.get('log_file', 'logs/app.log')
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, cfg.get('log_level', 'WARNING')))

    # Rotating file handler: max 5 MB per file, keep 3 backups
    handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Allow ws_client module to log at INFO (for BUY/SELL events)
    logging.getLogger('ws_client').setLevel(logging.INFO)

    # Determine which symbols to subscribe to
    symbols = cfg.get('symbols', ['THETA-USDT', 'TFUEL-USDT'])
    ws = WSClient(symbols)
    ws.run()

if __name__ == '__main__':
    main()
