import threading
import time
import http.server
import socketserver
import json
import pytest

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    """
    HTTP request handler that captures POST payloads in a class-level list.
    """
    calls = []

    @staticmethod
    def record(url, json=None, **kwargs):
        print(f"[MOCK] Capturing payload via record(): {json}")
        WebhookHandler.calls.append(json)
        class MockResponse:
            status_code = 200
        return MockResponse()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = body.decode('utf-8')
        print(f"[WEBHOOK] Captured payload: {payload}")
        WebhookHandler.calls.append(payload)
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        return

@pytest.fixture
def http_server():
    """
    Starts a local HTTP server to capture webhook POSTs.
    Yields the base URL (e.g. http://localhost:port) and
    resets WebhookHandler.calls on setup/teardown.
    """
    handler = WebhookHandler
    # Create server on an ephemeral port
    httpd = socketserver.TCPServer(("localhost", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    WebhookHandler.calls.clear()
    yield f"http://localhost:{port}"
    httpd.shutdown()
    thread.join()
    # Clear captured calls
    WebhookHandler.calls.clear()


# DummyWSClient for emitting test ticks (emits ticks for both THETA and TFUEL)
class DummyWSClient:
    def __init__(self, symbols, on_tick, max_ticks=5, interval=1):
        self.symbols = symbols
        self.on_tick = on_tick
        self.max_ticks = max_ticks
        self.interval = interval
        self.thread = None

    def start(self):
        def emit_ticks():
            print("[TEST] DummyWSClient emit_ticks started")
            for i in range(self.max_ticks):
                for symbol in self.symbols:
                    tick = {
                        "type": "message",
                        "topic": f"/market/ticker:{symbol}",
                        "data": {
                            "price": float(i),
                            "size": 1.0,
                        }
                    }
                    print(f"[TEST] Sending tick {i+1}/{self.max_ticks} for {symbol}")
                    self.on_tick(tick)

                print(f"[TEST] Waiting {self.interval}s for next tick...")
                time.sleep(self.interval)
                print(f"[TEST] Slept {self.interval}s after tick {i+1}")

            # Emit one synthetic candle for each symbol at the end
            for symbol in self.symbols:
                candle = {
                    "type": "candle",
                    "symbol": symbol,
                    "interval": "1T",
                    "open": 0.0,
                    "close": float(self.max_ticks - 1),
                    "high": float(self.max_ticks - 1),
                    "low": 0.0,
                    "volume": float(self.max_ticks),
                }
                print(f"[TEST] Sending final candle for {symbol}")
                self.on_tick(candle)

        self.thread = threading.Thread(target=emit_ticks, daemon=True)
        self.thread.start()

import csv
from pathlib import Path

def load_csv_as_dicts(path):
    """
    Load CSV rows as a list of dictionaries from a given file path.
    """
    path = Path(path)
    with path.open() as f:
        return list(csv.DictReader(f))