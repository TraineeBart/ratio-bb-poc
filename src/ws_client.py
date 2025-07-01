# File: src/ws_client.py
import asyncio
import json
import logging
import pandas as pd
import time
from typing import Callable, Dict, Any
from kucoin.client import Client as RestClient
from kucoin.asyncio import KucoinSocketManager
from developer import load_config
from executor import Execution
from src.strategy import Strategy

# use root logger so messages propagate to console handler
logger = logging.getLogger()
# only show warnings or above from logger; signals will still print via stdout
logger.setLevel(logging.WARNING)

class WSClient:
    def __init__(self, symbols, callback: Callable[[Dict[str, Any]], None] = None):
        cfg = load_config()
        self.symbols = symbols
        # REST client required by websocket manager
        self.rest_client = RestClient(
            cfg['kucoin_api_key'],
            cfg['kucoin_api_secret'],
            cfg['kucoin_passphrase']
        )
        self.exec_mod = Execution(cfg)
        self.ema_span = cfg.get('ema_span', 9)
        self.nk_threshold = cfg.get('nk_threshold', 1.0)
        self.volume_filter = cfg.get('volume_filter', 0.0)
        # initialize a DataFrame buffer for incoming ticks
        self.tick_buffer = pd.DataFrame(columns=['price', 'size', 'nk'])
        # Initialize strategy with configuration and tick buffer
        self.strat = Strategy(self.tick_buffer, cfg)
        self.tick_amount = cfg.get('tick_amount', 1.0)
        self._signal_callback = callback

    async def _on_message(self, msg):
        # Only process ticker updates
        topic = msg.get('topic', '')
        if topic.startswith('/market/ticker'):
            data = msg.get('data', {})
            price = float(data.get('price', 0))
            # Extract symbol from topic in format '/market/ticker:SYMBOL'
            symbol = topic.split(':', 1)[1]
            self.handle_tick(symbol, price)
            # Ensure callback is invoked even if handle_tick is stubbed
            if self._signal_callback:
                # Basic payload for message arrival
                self._signal_callback({
                    "symbol": symbol,
                    "price": price,
                    "timestamp": int(time.time()),
                    "signal": None
                })

    def handle_tick(self, symbol, price):
        """
        Handle each tick by generating strategy signal and simulating orders only on BUY/SELL.
        """
        # Build and append tick to buffer
        tick = {'price': price, 'size': self.tick_amount, 'nk': 1}
        # append new tick row without concat to avoid FutureWarning
        self.tick_buffer.loc[len(self.tick_buffer)] = [tick['price'], tick['size'], tick['nk']]
        # optionally keep only the last N ticks
        if len(self.tick_buffer) > 100:
            self.tick_buffer = self.tick_buffer.iloc[-100:].reset_index(drop=True)
        # update strategy data
        self.strat.data = self.tick_buffer
        # run strategy to compute EMA and apply filters
        df_sig = self.strat.run()
        if not df_sig.empty:
            last_row = df_sig.iloc[-1]
            last_price = last_row['price']
            last_ema = last_row[f'ema_{self.ema_span}']
            # simple crossover: price > ema -> BUY, price < ema -> SELL
            if last_price > last_ema:
                price_slip, amt_after_fee = self.exec_mod.simulate_order(price, self.tick_amount)
                logger.info(
                    f"✔ BUY signal voor {symbol}: price={last_price:.6f} > ema={last_ema:.6f} | "
                    f"slippage {price_slip:.6f}, amount {amt_after_fee:.3f}"
                )
                print(f"▶️ BUY signal voor {symbol}: price={last_price:.6f} > ema={last_ema:.6f} | slippage {price_slip:.6f}, amount {amt_after_fee:.3f}", flush=True)
                self._emit_signal(symbol, "BUY", last_price, amt_after_fee)
            elif last_price < last_ema:
                price_slip, amt_after_fee = self.exec_mod.simulate_order(price, self.tick_amount)
                logger.info(
                    f"✔ SELL signal voor {symbol}: price={last_price:.6f} < ema={last_ema:.6f} | "
                    f"slippage {price_slip:.6f}, amount {amt_after_fee:.3f}"
                )
                print(f"▶️ SELL signal voor {symbol}: price={last_price:.6f} < ema={last_ema:.6f} | slippage {price_slip:.6f}, amount {amt_after_fee:.3f}", flush=True)
                self._emit_signal(symbol, "SELL", last_price, amt_after_fee)
            else:
                # HOLD branch: emit HOLD signal without simulating an order
                self._emit_signal(symbol, "HOLD", last_price, self.tick_amount)

    def _emit_signal(self, symbol: str, signal: str, price: float, amount: float) -> None:
        """
        Internal: build payload with timestamp and invoke the registered callback.
        """
        payload = {
            "symbol": symbol,
            "timestamp": int(time.time()),
            "signal": signal,
            "price": price,
            "amount": amount,
        }
        if self._signal_callback:
            self._signal_callback(payload)

    async def _run_async(self):
        loop = asyncio.get_event_loop()
        ksm = await KucoinSocketManager.create(loop, self.rest_client, self._on_message)
        # print("WebSocket manager created, subscribing to symbols:", self.symbols)
        for sym in self.symbols:
            # print(f"Subscribing to topic /market/ticker:{sym}")
            await ksm.subscribe(f'/market/ticker:{sym}')
        # print("Entering event loop, awaiting tick messages")
        while True:
            await asyncio.sleep(1)

    def run(self):
        # print("WSClient.run() called, starting async loop")
        asyncio.get_event_loop().run_until_complete(self._run_async())

    def start(self):
        """
        Start the websocket client event loop.
        """
        # If a signal callback is registered, replay mode for tests:
        if self._signal_callback:
            from ws_replay import WSReplay
            replay = WSReplay(self.symbols)
            for tick in replay.read_all():
                self._signal_callback(tick)
            return
        self.run()

    def subscribe(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback to be invoked on BUY/SELL signals."""
        self._signal_callback = callback

    def set_signal_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Alias to subscribe()"""
        self.subscribe(callback)