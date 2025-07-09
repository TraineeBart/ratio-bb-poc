import sys, os
import csv
import time
import argparse
from datetime import datetime

# Ensure src modules are on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ws_client import WSClient
from developer import load_config


class WSReplay:
    def __init__(self, symbols):
        self.symbols = symbols
        config = load_config()
        self.historical_csv_path = config.get('historical_csv_path', 'data/historical.csv')

    def read_all(self):
        with open(self.historical_csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts_str = row['timestamp']
                try:
                    ts = int(ts_str)
                except ValueError:
                    ts = int(datetime.fromisoformat(ts_str).timestamp())
                yield {
                    'timestamp': ts,
                    'symbol': row.get('symbol'),
                    'price': float(row['price']),
                    'volume': float(row.get('volume', 0.0)),
                    'nk': float(row.get('nk', 0.0))
                }


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
            try:
                # Determine price: prefer non-empty 'close', otherwise use 'price'
                close_val = row.get('close')
                if close_val is not None and close_val != '':
                    price = float(close_val)
                else:
                    price = float(row.get('price', 0))
            except (TypeError, ValueError):
                # Skip rows with invalid numeric values
                continue
            ws.handle_tick(symbol, price)
            # Sleep only between ticks, not after the last one
            if delay and delay > 0 and idx < len(rows) - 1:
                time.sleep(delay)


if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(description='Replay historical ticks for strategy testing')
    parser.add_argument('--symbol', default='THETA-USDT', help='Ticker symbol to replay')
    parser.add_argument('--file', default='data/historical.csv', help='Path to historical CSV file')
    parser.add_argument('--delay', type=float, default=0, help='Seconds to wait between ticks')
    args = parser.parse_args()

    # Load config to ensure environment is set
    _ = load_config()
    print(f"Replaying ticks for {args.symbol} from {args.file} (delay={args.delay}s)")
    replay(args.symbol, args.file, args.delay)
# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/ws_replay.py                                       │
# │ Module: ws_replay                                           │
# │ Doel: Replay client module voor historische tickdata        │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-04                               │
# │ Status: stable                                              │
# ╰──────────────────────────────────────────────────────────────╯

import threading
import time
from typing import Callable, Dict
import pandas as pd

class WSReplay:
    """
    Replay client for historical tick data.
    """

    def __init__(self, csv_path: str, callback: Callable[[Dict], None], speed: float = 1.0):
        """
        🧠 Functie: __init__
        Initialiseer de replay client met CSV-pad, callback en snelheid.

        ▶️ In:
            - self (WSReplay): instantie
            - csv_path (str): pad naar CSV-bestand met kolom 'timestamp'
            - callback (Callable[[Dict], None]): functie voor verwerking van elke tick
            - speed (float): factor voor vertraging (1.0 = realtime)
        ⏺ Out:
            - None

        💡 Gebruikt:
            - pandas voor inlezen en sorteren van CSV
            - threading voor achtergrond-executie
        """
        self.csv_path = csv_path
        self.callback = callback
        self.speed = speed
        self._thread = None
        self._running = False

    def _run(self):
        """
        🧠 Functie: _run
        Speelt ticks af uit het CSV-bestand in timestamp-volgorde.

        ▶️ In:
            - self (WSReplay): instantie
        ⏺ Out:
            - None

        💡 Gebruikt:
            - pandas DataFrame iteratie
            - time.sleep voor vertraging
        """
        df = pd.read_csv(self.csv_path, parse_dates=['timestamp'])
        df = df.sort_values('timestamp')
        prev_ts = None
        for _, row in df.iterrows():
            if not self._running:
                break
            ts = row['timestamp']
            if prev_ts is not None:
                # 🔹 Bereken delay op basis van snelheid
                delay = (ts - prev_ts).total_seconds() / self.speed
                time.sleep(delay)
            # Roep callback aan met tickdata
            self.callback(row.to_dict())
            prev_ts = ts

    def start(self):
        """
        🧠 Functie: start
        Start de replay in een aparte thread.

        ▶️ In:
            - self (WSReplay): instantie
        ⏺ Out:
            - None

        💡 Gebruikt:
            - threading.Thread voor achtergrond-executie
        """
        # 🔹 Start alleen als niet al lopend
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """
        🧠 Functie: stop
        Stop de replay en wacht op thread beëindiging.

        ▶️ In:
            - self (WSReplay): instantie
        ⏺ Out:
            - None

        💡 Gebruikt:
            - thread.join om te wachten tot stop compleet is
        """
        self._running = False
        if self._thread:
            self._thread.join()