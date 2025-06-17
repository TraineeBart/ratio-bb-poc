from kucoin.client import Client
from developer import load_config

def get_kucoin_client():
    cfg = load_config()
    api_key = cfg['kucoin_api_key']
    api_secret = cfg['kucoin_api_secret']
    passphrase = cfg['kucoin_passphrase']
    client = Client(api_key, api_secret, passphrase)
    return client