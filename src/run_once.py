import pandas as pd
from developer import load_config
from strategy import Strategy

def main():
    # 1) Config inladen
    cfg = load_config()

    # 2) Historische data inlezen
    hist_path = cfg.get('historical_csv_path')
    df = pd.read_csv(hist_path)

    # 3) Strategy initialiseren
    strat = Strategy(df, cfg)

    # 4) Strategy runnen (bereken filters en EMA’s)
    df_res = strat.run()

    # 5) Laatste tick als dict en signaal genereren
    last_tick = df_res.iloc[-1].to_dict()
    signal = strat.generate_signal(last_tick)

    # 6) Print alleen het signaal
    print(signal)

if __name__ == '__main__':
    main()