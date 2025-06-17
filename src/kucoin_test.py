from kucoin_client import get_kucoin_client

if __name__ == '__main__':
    client = get_kucoin_client()
    # Haal de huidige ticker op voor THETA-USDT
    ticker = client.get_ticker('THETA-USDT')
    print('THETA-USDT prijs:', ticker['price'])