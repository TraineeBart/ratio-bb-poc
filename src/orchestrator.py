import logging
from logging.handlers import RotatingFileHandler
import os
import pandas as pd
import csv
import requests
from developer import load_config
from strategy import Strategy
from executor import Execution
from src.ws_client import WSClient

class Orchestrator:
    def __init__(self, config):
        self.config = config
        # Ensure logs directory exists
        log_file = config.get('log_file', 'logs/app.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Set up root logger
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, config.get('log_level', 'WARNING')))

        # Rotating handler: max 5 MB, keep 3 backups
        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Module-specific logger for orchestrator
        self.logger = logging.getLogger('Orchestrator')
        self.logger.setLevel(logging.INFO)

    def run(self):
        data_path = self.config.get('data_path')
        df = pd.read_csv(data_path)
        strat = Strategy(df, self.config)
        df_out = strat.run()
        exec_mod = Execution(self.config)
        for _, row in df_out.iterrows():
            price = row['price']
            volume = row.get('volume', 1)
            price_slip, amt_after_fee = exec_mod.simulate_order(price, volume)
            self.logger.info(f"Order simulated at price {price_slip}, amount {amt_after_fee}")
        print("Orchestration complete")

    def on_signal(self, payload: dict) -> None:
        """
        Callback to handle signals: write to CSV and post to webhook.
        """
        csv_file = self.config.get('backtest_output_csv', 'tmp/output.csv')
        # Ensure directory exists
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        webhook_url = os.getenv('WEBHOOK_URL')
        # Ensure CSV has headers
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "timestamp", "signal", "price", "amount"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(payload)
        # Post to webhook if configured
        if webhook_url:
            try:
                requests.post(webhook_url, json=payload, timeout=5).raise_for_status()
            except Exception as e:
                self.logger.error(f"Failed posting signal to webhook: {e}")

    def run_live(self) -> None:
        """
        Start live WebSocket client and attach signal callback.
        """
        ws = WSClient(self.config)
        ws.set_signal_callback(self.on_signal)
        self.logger.info("Starting WSClient for live signals...")
        ws.run_forever()

if __name__ == '__main__':
    config = load_config()
    orch = Orchestrator(config)
    # For backtest:
    orch.run()
    # For live signals:
    orch.run_live()
