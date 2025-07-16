import asyncio
import json
import websockets
from client.kucoin_client import get_bullet_public

async def test_ws():
    auth = get_bullet_public()
    url = f"{auth['endpoint']}?token={auth['token']}"
    symbols = ["THETA-USDT", "TFUEL-USDT"]

    async with websockets.connect(url) as ws:
        for symbol in symbols:
            msg = {
                "id": f"sub-{symbol}",
                "type": "subscribe",
                "topic": f"/market/ticker:{symbol}",
                "privateChannel": False,
                "response": True
            }
            await ws.send(json.dumps(msg))

        while True:
            message = await ws.recv()
            print(message)

asyncio.run(test_ws())