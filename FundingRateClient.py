from __future__ import annotations

from abc import ABC, abstractmethod


class FundingRateClient(ABC):
    """
    Interface for any exchange funding-rate client (Deribit, Hyperliquid, Binance, etc).
    Implementations must return a single aggregated funding rate value for an instrument
    between the given timestamps.
    """

    @property
    @abstractmethod
    def exchange(self) -> str:
        """
        Short identifier of the exchange, e.g. "deribit", "hyperliquid", "binance".
        """
        raise NotImplementedError

    @abstractmethod
    def get_total_funding_rate(
        self,
        instrument: str,
        start_timestamp_ms: int,
        end_timestamp_ms: int,
    ) -> float:
        """
        Return the aggregated funding rate for `instrument` between the given times,
        normalized to a decimal fractional rate.

        Example:
        - 0.0003   →  0.03% total funding
        - -0.0011  → -0.11% total funding

        Implementations may:
        - call REST or websocket
        - paginate under the hood
        - handle exchange-specific schemas
        - sum funding periods correctly
        """
        raise NotImplementedError
