import pandas as pd
from src.developer import load_config
from src.strategy import Strategy
from src.utils.timezone import format_cet_ts
import os
import csv
import json
import argparse
import sys
import importlib

def main():
    # 0) CLI argument parsing
    parser = argparse.ArgumentParser(description="Run strategy on historical CSV or replay JSON ticks")
    parser.add_argument('--replay', type=str, help='Path to JSON file with ticks to replay')
    args = parser.parse_args()

    # 1) Config inladen
    cfg = load_config()

    # —— Replay smoke-test override ——
    if args.replay:
        # Load tick data from JSON replay file
        if not os.path.isfile(args.replay):
            raise FileNotFoundError(f"Replay file niet gevonden: {args.replay}")
        with open(args.replay, 'r') as f:
            ticks = json.load(f)
        # Determine simple signal based on first vs. last price
        first_price = ticks[0]['price']
        last_price  = ticks[-1]['price']
        if last_price > first_price:
            signal = 'BUY'
        elif last_price < first_price:
            signal = 'SELL'
        else:
            signal = 'HOLD'
        # 🔹 Gebruik helper voor ISO CET-timestamp met offset
        ts = format_cet_ts(ticks[-1]['timestamp'])
        # Determine default symbol from config
        cfg_symbols = cfg.get('symbols', [])
        if isinstance(cfg_symbols, str):
            default_symbol = cfg_symbols.split(',')[0]
        elif isinstance(cfg_symbols, list) and cfg_symbols:
            default_symbol = cfg_symbols[0]
        else:
            default_symbol = ''
        symbol = ticks[-1].get('symbol', default_symbol)
        output = {'timestamp': ts, 'symbol': symbol, 'price': last_price, 'signal': signal}
        # Write to tmp/output.csv
        os.makedirs('tmp', exist_ok=True)
        out_path = os.path.join('tmp', 'output.csv')
        write_header = not os.path.isfile(out_path)
        with open(out_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(['timestamp','symbol','price','signal'])
            writer.writerow([output['timestamp'], output['symbol'], output['price'], output['signal']])
        # 8) Send webhook callback
        webhook_url = cfg.get('webhook_url') or os.getenv('WEBHOOK_URL')
        try:
            req = importlib.import_module('requests')
            req.post(webhook_url, json=output, timeout=5)
        except Exception as e:
            print(f"⚠️ Webhook POST failed: {e}", file=sys.stderr)
        # Print and exit
        print(json.dumps(output))
        return
    # —— End replay override ——

    # —— Live-mode override ——
    if os.getenv('MODE') == 'live':
        # Collect only the final tick from the WSClient stub
        symbols = cfg.get('symbols') or []
        if isinstance(symbols, str):
            symbols = symbols.split(',')

        last_tick = {}
        def collect_last(tick):
            nonlocal last_tick
            last_tick = tick

        from src.ws_client import WSClient
        client = WSClient(symbols, collect_last)
        client.start()

        # 🔹 Gebruik helper voor ISO CET-timestamp met offset
        ts = format_cet_ts(last_tick['timestamp'])

        # Build single-line output dict matching replay flow
        output = {
            'timestamp': ts,
            'symbol': '',
            'price': last_tick['price'],
            'signal': 'HOLD'
        }

        # Write to tmp/output.csv
        os.makedirs('tmp', exist_ok=True)
        out_path = os.path.join('tmp', 'output.csv')
        write_header = not os.path.isfile(out_path)
        with open(out_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(['timestamp','symbol','price','signal'])
            writer.writerow([output['timestamp'], output['symbol'], output['price'], output['signal']])

        # Send webhook callback
        webhook_url = cfg.get('webhook_url') or os.getenv('WEBHOOK_URL')
        try:
            req = importlib.import_module('requests')
            req.post(webhook_url, json=output, timeout=5)
        except Exception:
            pass

        # Print and exit
        print(json.dumps(output))
        return
    # —— End live override ——

    # 2) Data inlezen: historische CSV (replay is handled above)
    hist_path = cfg.get('historical_csv_path', 'data/historical.csv')
    if not os.path.isfile(hist_path):
        raise FileNotFoundError(f"Kan historische data niet vinden: {hist_path}")
    df = pd.read_csv(hist_path)

    # 3) Strategy initialiseren
    strat = Strategy(df, cfg)

    # 4) Strategy runnen (bereken filters en EMA’s)
    df_res = strat.run()

    # 5) Laatste tick als dict en signaal genereren
    last_tick = df_res.iloc[-1].to_dict()
    signal = strat.generate_signal(last_tick)

    # 6) Print alleen het signaal
    output = last_tick.copy()
    output['signal'] = signal

    # 7) Write output to tmp/output.csv
    os.makedirs('tmp', exist_ok=True)
    out_path = os.path.join('tmp', 'output.csv')
    write_header = not os.path.isfile(out_path)
    with open(out_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(['timestamp', 'symbol', 'price', 'signal'])
        writer.writerow([output.get('timestamp'), output.get('symbol'), output.get('price'), output.get('signal')])

        # Send webhook callback (live mode)
        webhook_url = cfg.get('webhook_url') or os.getenv('WEBHOOK_URL')
        try:
            req = importlib.import_module('requests')
            req.post(webhook_url, json=output, timeout=5)
        except Exception as e:
            print(f"⚠️ Webhook POST failed: {e}", file=sys.stderr)
        print(json.dumps(output))

if __name__ == '__main__':
    main()