import pandas as pd
from developer import load_config
from strategy import Strategy


def main():
    # Load configuration
    cfg = load_config()

    # Read historical CSV path from config
    hist_path = cfg.get('historical_csv_path')
    df = pd.read_csv(hist_path)

    # Take the latest tick
    last_tick = df.iloc[-1].to_dict()
    df_tick = pd.DataFrame([last_tick])

    # Initialize strategy with DataFrame and config
    strat = Strategy(df_tick, cfg)

    # Generate and output signal
    signal = strat.generate_signal(last_tick)
    print(signal)


if __name__ == '__main__':
    main()