from __future__ import annotations

from decimal import Decimal
from typing import Any, Sequence

import requests

from FundingRateClient import FundingRateClient


class HyperliquidFundingRateClient(FundingRateClient):
    """Funding rate client backed by Hyperliquid's public API."""

    _URL = "https://api.hyperliquid.xyz/info"

    def __init__(
        self,
        session: requests.Session | None = None,
        *,
        request_timeout: float = 10.0,
    ) -> None:
        self._session = session or requests.Session()
        self._request_timeout = request_timeout

    @property
    def exchange(self) -> str:
        return "hyperliquid"

    def get_total_funding_rate(
        self,
        instrument: str,
        start_timestamp_ms: int,
        end_timestamp_ms: int,
    ) -> float:
        payload = {
            "type": "fundingHistory",
            "coin": instrument,
            "startTime": start_timestamp_ms,
            "endTime": end_timestamp_ms,
        }

        response = self._session.post(
            self._URL,
            json=payload,
            timeout=self._request_timeout,
        )
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, Sequence):
            raise ValueError("Hyperliquid funding history response must be a list")

        total_funding = Decimal("0")
        for entry in data:
            funding_rate = self._parse_decimal(entry, "fundingRate")
            total_funding += funding_rate

        return float(total_funding)

    @staticmethod
    def _parse_decimal(entry: Any, key: str) -> Decimal:
        try:
            value = entry[key]
        except (TypeError, KeyError) as err:
            raise ValueError(f"Missing {key} in Hyperliquid response entry: {entry}") from err

        try:
            return Decimal(str(value))
        except Exception as err:  # Decimal raises several exception types
            raise ValueError(
                f"Hyperliquid response value for {key} is not numeric: {value}"
            ) from err


if __name__ == "__main__":
    client = HyperliquidFundingRateClient()
    total = client.get_total_funding_rate("ETH", 1731715200000, 1763272103000)
    print(f"Aggregated funding for ETH: {total}")
