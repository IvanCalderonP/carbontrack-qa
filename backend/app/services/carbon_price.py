from decimal import Decimal
from typing import Protocol


class CarbonPriceProvider(Protocol):
    def reference_price(self) -> Decimal: ...


class LocalCarbonPriceProvider:
    """Fixed fictional price to demonstrate a replaceable external dependency."""

    def reference_price(self) -> Decimal:
        return Decimal("42.00")
