import sys, os
import csv
import time
import argparse

# Ensure src modules are on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ws_client import WSClient
from developer import load_config


def replay(symbol, input_csv, delay):
    """
    Replay historical ticks from a CSV file by calling handle_tick for each row.

    :param symbol: Ticker symbol, e.g. 'THETA-USDT'
    :param input_csv: Path to CSV file with columns timestamp,price,volume,nk
    :param delay: Seconds to wait between ticks (0 for no delay)
    """
    # Instantiate WSClient to use handle_tick logic
    ws = WSClient([symbol])

    # Read CSV and replay ticks
    with open(input_csv, newline='') as f:
        rows = list(csv.DictReader(f))
        for idx, row in enumerate(rows):
            # Determine price: prefer non-empty 'close', otherwise use 'price'
            close_val = row.get('close')
            if close_val is not None and close_val != '':
                price = float(close_val)
            else:
                price = float(row.get('price', 0))
            ws.handle_tick(symbol, price)
            # Sleep only between ticks, not after the last one
            if delay and delay > 0 and idx < len(rows) - 1:
                time.sleep(delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replay historical ticks for strategy testing')
    parser.add_argument('--symbol', default='THETA-USDT', help='Ticker symbol to replay')
    parser.add_argument('--file', default='data/historical.csv', help='Path to historical CSV file')
    parser.add_argument('--delay', type=float, default=0, help='Seconds to wait between ticks')
    args = parser.parse_args()

    # Load config to ensure environment is set
    _ = load_config()
    print(f"Replaying ticks for {args.symbol} from {args.file} (delay={args.delay}s)")
    replay(args.symbol, args.file, args.delay)