import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
from developer import load_config

async def handle_msg(msg):
    # Filter voor ticker-updates
    if msg.get("topic", "").startswith("/market/ticker"):
        data = msg.get("data", {})
        symbol = data.get("symbol")
        price = data.get("price")
        print(f"✔ Tick {symbol} @ {price}")

async def main():
    cfg = load_config()
    client = Client(cfg['kucoin_api_key'],
                    cfg['kucoin_api_secret'],
                    cfg['kucoin_passphrase'])
    # Initialiseer socket manager
    ksm = await KucoinSocketManager.create(asyncio.get_event_loop(), client, handle_msg)
    # Subscribe op één test-topic
    await ksm.subscribe("/market/ticker:THETA-USDT")
    print("✅ Subscribed, awaiting ticks…")
    # Houd de loop levend
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())