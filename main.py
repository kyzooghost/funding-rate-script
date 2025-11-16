# Get funding rates from Deribit public API

import asyncio
import websockets
import json
from decimal import Decimal

msg = \
{"id":7617,"jsonrpc":"2.0","method":"public/get_funding_rate_history","params":{"end_timestamp":1763272103000,"instrument_name":"SOL_USDC-PERPETUAL","start_timestamp":1731715200000}}

async def call_api(msg: str):
    async with websockets.connect("wss://test.deribit.com/ws/api/v2") as websocket:
        await websocket.send(msg)

        # receive raw JSON text
        raw = await websocket.recv()
        # parse into Python dict
        response = json.loads(raw)

        total_interest_8h = Decimal("0")
        total_interest_1h = Decimal("0")
        for item in response["result"]:
            total_interest_8h += Decimal(str(item["interest_8h"]))
            total_interest_1h += Decimal(str(item["interest_1h"]))
        
        print("Total interest_8h:", total_interest_8h)
        print("Total interest_1h:", total_interest_1h)

if __name__ == "__main__":
    asyncio.run(call_api(json.dumps(msg)))