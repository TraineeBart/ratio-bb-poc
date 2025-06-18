from developer import load_config
from kucoin_client import get_kucoin_client
from executor import Execution

def main():
    # Load configuration
    cfg = load_config()
    symbols = cfg.get('symbols', [])
    tick_amount = cfg.get('tick_amount', 1.0)

    # Initialize clients
    client = get_kucoin_client()
    executor = Execution(cfg)

    # Process one tick per symbol and exit
    for sym in symbols:
        data = client.get_ticker(sym)
        price = float(data['price'])
        price_slip, amt_after_fee = executor.simulate_order(price, tick_amount)
        print(f"✔ Simulated order for {sym}: price after slippage {price_slip}, amount after fee {amt_after_fee}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print("❌ Error in run_once:", str(e))
        traceback.print_exc()
        # Exit with non-zero code
        import sys
        sys.exit(1)