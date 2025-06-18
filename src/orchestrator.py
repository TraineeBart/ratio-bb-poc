import logging
from logging.handlers import RotatingFileHandler
import os
import pandas as pd
from developer import load_config
from strategy import Strategy
from executor import Execution

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

if __name__ == '__main__':
    config = load_config()
    orch = Orchestrator(config)
    orch.run()
