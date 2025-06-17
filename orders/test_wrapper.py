import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from executor import Execution
from developer import load_config
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test order wrapper')
    parser.add_argument('--price', type=float, default=100.0, help='Price')
    parser.add_argument('--amount', type=float, default=10.0, help='Amount')
    args = parser.parse_args()

    config = load_config()
    exec_mod = Execution(config)
    price_slip, amt_after_fee = exec_mod.simulate_order(args.price, args.amount)
    print(f"Test order: price after slippage {price_slip}, amount after fee {amt_after_fee}")
