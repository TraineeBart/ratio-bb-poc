import asyncio
import json
import logging
from kucoin.client import Client as RestClient
from kucoin.asyncio import KucoinSocketManager
from developer import load_config
from executor import Execution
from src.strategy import Strategy

logger = logging.getLogger(__name__)

class WSClient:
    def __init__(self, symbols):
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
        # Initialize strategy with configuration
        self.strat = Strategy(cfg)
        self.tick_amount = cfg.get('tick_amount', 1.0)

    async def _on_message(self, msg):
        # Only process ticker updates
        topic = msg.get('topic', '')
        if topic.startswith('/market/ticker'):
            data = msg.get('data', {})
            price = float(data.get('price', 0))
            # Extract symbol from topic in format '/market/ticker:SYMBOL'
            symbol = topic.split(':', 1)[1]
            self.handle_tick(symbol, price)

    def handle_tick(self, symbol, price):
        """
        Handle each tick by generating strategy signal and simulating orders only on BUY/SELL.
        """
        # Build a minimal tick dict for strategy
        tick = {
            'price': price,
            'size': self.tick_amount,
            'nk': 1,
            f'ema_{self.ema_span}': price
        }
        signal = self.strat.generate_signal(tick)
        if signal in ("BUY", "SELL"):
            price_slip, amt_after_fee = self.exec_mod.simulate_order(price, self.tick_amount)
            logger.info(f"✔ Simulated order for {symbol}: price after slippage {price_slip}, amount after fee {amt_after_fee}")
        else:
            # Skip logging for HOLD signals
            pass

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