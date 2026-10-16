from decimal import Decimal

import pytest

from app.services.emissions import calculate_emissions


@pytest.mark.parametrize(
    ("quantity", "direct", "indirect", "price", "expected"),
    [
        ("10", "2", "3", "40", ("5", "0.5", "200")),
        ("2", "0", "0", "0", ("0", "0", "0")),
        ("0.1", "0.01", "0.02", "0.03", ("0.03", "0.3", "0.0009")),
        ("100000000000", "10000000000", "10000000000", "5", ("20000000000", "0.2", "100000000000")),
    ],
)
def test_calculate_emissions_preserves_decimal_precision(quantity, direct, indirect, price, expected):
    result = calculate_emissions(*(Decimal(value) for value in (quantity, direct, indirect, price)))
    assert result == tuple(Decimal(value) for value in expected)


@pytest.mark.parametrize(
    "values",
    [("0", "1", "1", "1"), ("-1", "1", "1", "1"), ("1", "-1", "1", "1"), ("1", "1", "-1", "1"), ("1", "1", "1", "-1")],
)
def test_calculate_emissions_rejects_invalid_values(values):
    with pytest.raises(ValueError):
        calculate_emissions(*(Decimal(value) for value in values))
