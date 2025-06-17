import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from developer import load_config
from ws_client import WSClient
import logging

def main():
    print("▶️ In main(): starting WebSocket client")
    cfg = load_config()
    # Configure logging as specified in config.yaml
    logging.basicConfig(
        filename=cfg.get('log_file', 'logs/app.log'),
        level=getattr(logging, cfg.get('log_level', 'INFO'))
    )
    # Determine which symbols to subscribe to
    symbols = cfg.get('symbols', ['THETA-USDT', 'TFUEL-USDT'])
    ws = WSClient(symbols)
    ws.run()

if __name__ == '__main__':
    main()
