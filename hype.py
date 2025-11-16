# Get funding rates from Hyperliquid public API

import requests
from decimal import Decimal

URL = "https://api.hyperliquid.xyz/info"

START_TIME = 1731715200000   # your start timestamp (ms)
END_TIME   = 1763272103000   # your end timestamp (ms)

def get_funding_history(coin: str, start_ms: int, end_ms: int):
    payload = {
        "type": "fundingHistory",
        "coin": coin,
        "startTime": start_ms,
        "endTime": end_ms,
    }

    resp = requests.post(URL, json=payload)
    resp.raise_for_status()

    data = resp.json()  # should be a list of entries

    total_funding = Decimal("0")
    total_premium = Decimal("0")

    for entry in data:
        funding_rate = Decimal(entry["fundingRate"])
        premium = Decimal(entry["premium"])

        print(
            f"time={entry['time']} | rate={funding_rate} | premium={premium}"
        )

        total_funding += funding_rate
        total_premium += premium

    print("\n🟢 Total fundingRate:", total_funding)
    print("🟣 Total premium:", total_premium)


if __name__ == "__main__":
    get_funding_history("ETH", START_TIME, END_TIME)