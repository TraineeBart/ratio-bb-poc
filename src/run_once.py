# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/run_once.py                                        │
# │ Module: run_once                                            │
# │ Doel: Entry-point voor replay- en live-mode uitvoering      │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-04                               │
# │ Status: stable                                             │
# ╰──────────────────────────────────────────────────────────────╯

import pandas as pd
from datetime import datetime, timezone
from src.developer import load_config
from src.strategy import Strategy
from src.utils.timezone import format_cet_ts
from src.utils.candles import CandleAggregator
from src.outputs.webhook import dispatch_webhook
import os
import csv
import json
import argparse
import sys
import time
import threading
from datetime import timedelta
import requests
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

def start_health_server(port=8000):
    srv = HTTPServer(('0.0.0.0', port), HealthHandler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    print(f"[LIVE] health endpoint listening on http://0.0.0.0:{port}/health")

def main():
    # 0) CLI argument parsing
    parser = argparse.ArgumentParser(description="Run strategy on historical CSV or replay JSON ticks")
    parser.add_argument('--replay', type=str, help='Path to JSON file with ticks to replay')
    args = parser.parse_args()
    print("[DEBUG] Entering main()")
    print(f"[DEBUG] Args: replay={args.replay!r}, MODE={os.getenv('MODE')!r}")

    # 1) Config inladen
    cfg = load_config()

    # —— Replay smoke-test override ——
    print("[DEBUG] → Entering replay branch")
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
        # 8) Send webhook callback via helper
        try:
            dispatch_webhook(output, timeout=5)
        except Exception as e:
            print(f"⚠️ Webhook POST failed: {e}", file=sys.stderr)
        # Print and exit
        print(json.dumps(output))
        print("[DEBUG] ← Exiting replay branch")
        return
    # —— End replay override ——

    # —— Live-mode override ——
    print("[DEBUG] → Entering live branch")
    if os.getenv('MODE') == 'live':
        print("ENTERED LIVE MODE OVERRIDE")
        # Start health endpoint
        start_health_server(port=8000)
        print("[DEBUG] After start_health_server()")
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        logging.basicConfig(level=log_level, format='[LIVE] %(asctime)s %(levelname)s %(message)s')
        # Enable verbose websocket-client tracing
        import websocket
        websocket.enableTrace(True)
        # Enable DEBUG-level logs from websocket-client library
        logging.getLogger("websocket").setLevel(logging.DEBUG)
        logging.getLogger("src.ws_client").setLevel(logging.INFO)
        logging.getLogger("websocket").propagate = True
        os.makedirs('tmp', exist_ok=True)
        out_path = os.path.join('tmp', 'output.csv')
        # Always write header row to output.csv (overwrite)
        with open(out_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp','symbol','price','signal'])
        # 🔹 Emit a JSON summary with signal on stdout
        # Use current UTC time converted to CET format (pass float timestamp)
        hist_path = cfg.get('historical_csv_path')
        ts = format_cet_ts(datetime.now(timezone.utc).timestamp())
        symbols = cfg.get('symbols', [])
        if isinstance(symbols, list) and symbols:
            summary_symbol = symbols[0]
        else:
            summary_symbol = symbols if isinstance(symbols, str) else ''
        # No last row copying to output.csv; just print summary
        last_price = None
        signal = 'HOLD'
        output = {'timestamp': ts, 'symbol': summary_symbol, 'price': last_price, 'signal': signal}
        print(json.dumps(output))
        # ▶️ Write summary to CSV before starting live aggregation
        with open(out_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([output['timestamp'], output['symbol'], output['price'], output['signal']])

        # Live-mode: per-symbol candle aggregation smoke test
        symbols = cfg.get('symbols') or []
        if isinstance(symbols, str):
            symbols = symbols.split(',')

        # Track last tick arrival per symbol for gap detection
        last_tick = {symbol: datetime.now(timezone.utc) for symbol in symbols}

        from src.ws_client import WSClient

        # 🔹 Setup per-symbol CandleAggregators with separate logs
        period = os.getenv('CANDLE_PERIOD', '5T')
        aggregators = {}
        os.makedirs(os.path.join(os.getcwd(), 'tmp'), exist_ok=True)
        webhook_url = cfg.get('webhook_url') or os.getenv('WEBHOOK_URL')
        for symbol in symbols:
            log_path = os.path.join(os.getcwd(), 'tmp', f'candles_{symbol}.log')
            def make_on_candle(sym, path):
                def on_candle(candle):
                    # 🔹 Debug: direct console feedback on candle closure
                    print(f"CANDLE for {sym}: {candle}")
                    # 🔹 TFUEL-specific debug when TFUEL candle closes
                    if sym == 'TFUEL-USDT':
                        print(">>> TFUEL callback entered!")
                    entry = {
                        'symbol': sym,
                        'start_ts': candle['start_ts'].isoformat(),
                        'open': candle['open'],
                        'high': candle['high'],
                        'low': candle['low'],
                        'close': candle['close'],
                        'volume': candle['volume']
                    }
                    try:
                        with open(path, 'a') as f:
                            f.write(json.dumps(entry) + "\n")
                    except Exception as e:
                        print(f"Failed to write candle log for {sym}: {e}")
                    # Append live signal entry to tmp/output.csv
                    out_csv = os.path.join(os.getcwd(), 'tmp', 'output.csv')
                    write_header = not os.path.isfile(out_csv)
                    output = {
                        'timestamp': candle['start_ts'].isoformat(),
                        'symbol': sym,
                        'price': candle['close'],
                        'signal': 'HOLD'
                    }
                    try:
                        with open(out_csv, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            if write_header:
                                writer.writerow(['timestamp', 'symbol', 'price', 'signal'])
                            writer.writerow([output['timestamp'], output['symbol'], output['price'], output['signal']])
                    except Exception as e:
                        print(f"Failed to write live signal to output.csv for {sym}: {e}")
                    # Send webhook POST
                    if webhook_url:
                        try:
                            requests.post(webhook_url, json=output, timeout=5)
                        except Exception as e:
                            print(f"⚠️ Webhook POST failed for {sym}: {e}", file=sys.stderr)
                    # Print JSON payload to stdout
                    print(json.dumps(output))
                return on_candle
            aggregators[symbol] = CandleAggregator(period=period, on_candle=make_on_candle(symbol, log_path))

        # Callback: route each tick to the correct aggregator by symbol
        def on_tick(tick):
            print(f"DEBUG on_tick type={tick.get('type')}: {tick}")
            """
            Callback for each raw tick: route by symbol to its CandleAggregator.
            """
            # 🔹 Skip non-message events (welcome/ack)
            if tick.get('type') != 'message':
                return
            # 🔹 Print raw tick
            print(json.dumps(tick))
            topic = tick.get('topic', '')
            parts = topic.split(':', 1)
            if len(parts) != 2:
                return
            sym = parts[1]
            data = tick.get('data', {})
            try:
                # 🔹 Gebruik actuele UTC-arrivaltijd i.p.v. data['time'] voor aggregatie
                ts = datetime.now(timezone.utc)
                last_tick[sym] = ts
                price = float(data.get('price', 0))
                volume = float(data.get('size', 0))
            except Exception as e:
                print(f"Failed to parse tick for aggregation: {e}")
                return
            tick_struct = {'timestamp': ts, 'price': price, 'volume': volume}
            if sym in aggregators:
                aggregators[sym].on_tick(tick_struct)
            else:
                print(f"No aggregator for symbol {sym}")

        # 🔧 Debug: before creating WSClient
        print("[DEBUG] Before creating WSClient")
        client = WSClient(symbols, on_tick)
        print(f"[DEBUG] WSClient created for symbols: {symbols}")
        print("WSClient: Initialized, about to start")
        for sym in symbols:
            print(f"WSClient: Sent subscribe for topic /market/ticker:{sym}")

        # Start heartbeat logging
        def heartbeat():
            while True:
                print(f"[LIVE][HEARTBEAT] {datetime.now(timezone.utc).isoformat()}")
                time.sleep(60)
        threading.Thread(target=heartbeat, daemon=True).start()

        print("[DEBUG] Before client.start()")
        print("WSClient: Starting WebSocket client")
        client.start()
        print("[DEBUG] After client.start()")

        # Start background thread to detect data gaps
        def gap_checker():
            while True:
                for sym, last in last_tick.items():
                    if datetime.now(timezone.utc) - last > timedelta(seconds=60):
                        print(f"⚠️ Gap detected for {sym}, last tick at {last.isoformat()}")
                time.sleep(30)

        threading.Thread(target=gap_checker, daemon=True).start()

        
        print("[DEBUG] Entering main processing loop")
        # Keep running to collect candles; stop after a fixed time or CTRL+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            client.stop()
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

        # Send webhook callback via helper
        try:
            dispatch_webhook(output, timeout=5)
        except Exception as e:
            print(f"⚠️ Webhook POST failed: {e}", file=sys.stderr)
        print(json.dumps(output))

if __name__ == '__main__':
    main()