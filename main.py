"""Entrypoint for aggregating Hyperliquid and Deribit funding rates."""

from __future__ import annotations

from DeribitFundingRateClient import DeribitFundingRateClient
from HyperliquidFundingRateClient import HyperliquidFundingRateClient

# Update these constants before running the script.
START_TIMESTAMP_MS = 1763658645000
END_TIMESTAMP_MS = 1764303045000
HYPERLIQUID_INSTRUMENT = "NEAR"
DERIBIT_INSTRUMENT = "NEAR_USDC-PERPETUAL"


def main() -> None:
    hyperliquid_client = HyperliquidFundingRateClient()
    deribit_client = DeribitFundingRateClient()

    hyperliquid_total = hyperliquid_client.get_total_funding_rate(
        HYPERLIQUID_INSTRUMENT,
        START_TIMESTAMP_MS,
        END_TIMESTAMP_MS,
    )
    print(
        f"Aggregated funding for {HYPERLIQUID_INSTRUMENT} on Hyperliquid: "
        f"{hyperliquid_total}"
    )

    deribit_total = deribit_client.get_total_funding_rate(
        DERIBIT_INSTRUMENT,
        START_TIMESTAMP_MS,
        END_TIMESTAMP_MS,
    )
    print(
        f"Aggregated funding for {DERIBIT_INSTRUMENT} on Deribit: {deribit_total}"
    )


if __name__ == "__main__":
    main()
