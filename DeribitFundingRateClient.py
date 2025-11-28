from __future__ import annotations

import asyncio
import json
from decimal import Decimal
from typing import Any, Dict

import websockets

from FundingRateClient import FundingRateClient


class DeribitFundingRateClient(FundingRateClient):
    """Funding rate client backed by Deribit's websocket API."""

    _WS_URL = "wss://test.deribit.com/ws/api/v2"

    def __init__(self, *, request_timeout: float = 10.0) -> None:
        self._request_timeout = request_timeout

    @property
    def exchange(self) -> str:
        return "deribit"

    def get_total_funding_rate(
        self,
        instrument: str,
        start_timestamp_ms: int,
        end_timestamp_ms: int,
    ) -> float:
        payload: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "public/get_funding_rate_history",
            "params": {
                "instrument_name": instrument,
                "start_timestamp": start_timestamp_ms,
                "end_timestamp": end_timestamp_ms,
            },
        }

        response = asyncio.run(self._call_api(payload))
        result = response.get("result")
        if not isinstance(result, list):
            raise ValueError("Deribit response missing funding history result list")

        total_interest = Decimal("0")
        for item in result:
            total_interest += self._parse_decimal(item, "interest_1h")

        return float(total_interest)

    async def _call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with websockets.connect(self._WS_URL) as websocket:
            await websocket.send(json.dumps(payload))
            raw = await asyncio.wait_for(websocket.recv(), timeout=self._request_timeout)

        data = json.loads(raw)
        if "error" in data:
            raise ValueError(f"Deribit error response: {data['error']}")
        return data

    @staticmethod
    def _parse_decimal(entry: Any, key: str) -> Decimal:
        try:
            value = entry[key]
        except (TypeError, KeyError) as err:
            raise ValueError(f"Missing {key} in Deribit response entry: {entry}") from err

        try:
            return Decimal(str(value))
        except Exception as err:
            raise ValueError(
                f"Deribit response value for {key} is not numeric: {value}"
            ) from err


if __name__ == "__main__":
    client = DeribitFundingRateClient()
    total = client.get_total_funding_rate(
        "SOL_USDC-PERPETUAL",
        1731715200000,
        1763272103000,
    )
    print(f"Aggregated funding for SOL perpetual: {total}")
