import logging
import pandas as pd
from developer import load_config
from strategy import Strategy
from executor import Execution

class Orchestrator:
    def __init__(self, config):
        self.config = config
        log_file = config.get('log_file', 'logs/app.log')
        logging.basicConfig(filename=log_file, level=getattr(logging, config.get('log_level', 'INFO')))
        self.logger = logging.getLogger('Orchestrator')

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
