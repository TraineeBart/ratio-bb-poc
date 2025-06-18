from developer import load_config
from kucoin_client import get_kucoin_client
from executor import Execution
from strategy import Strategy  # Ensure correct import path

def main():
    # Load configuration
    cfg = load_config()
    symbols       = cfg.get('symbols', [])
    tick_amount   = cfg.get('tick_amount', 1.0)
    ema_span      = cfg.get('ema_span', 9)
    nk_threshold  = cfg.get('nk_threshold', 1.0)
    volume_filter = cfg.get('volume_filter', 0.0)

    # Initialize clients and modules
    client   = get_kucoin_client()
    executor = Execution(cfg)
    strat    = Strategy(nk_threshold=nk_threshold,
                        volume_filter=volume_filter,
                        ema_span=ema_span)

    # Process one tick per symbol and exit
    for sym in symbols:
        data = client.get_ticker(sym)
        price = float(data['price'])
        signal = strat.generate_signal(data)

        if signal in ("BUY", "SELL"):
            price_slip, amt_after_fee = executor.simulate_order(price, tick_amount)
            print(f"{signal} {sym} @ price after slippage {price_slip}, amount after fee {amt_after_fee}")
        else:
            # For HOLD, just log the current price
            print(f"HOLD {sym} @ {price}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print("❌ Error in run_once:", str(e))
        traceback.print_exc()
        import sys
        sys.exit(1)