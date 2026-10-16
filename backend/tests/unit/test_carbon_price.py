from decimal import Decimal

from app.services.carbon_price import LocalCarbonPriceProvider


def test_local_carbon_price_is_a_fictional_fixed_decimal():
    assert LocalCarbonPriceProvider().reference_price() == Decimal("42.00")
