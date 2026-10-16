from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.contracts import ProductInput, UserCreate


@pytest.mark.parametrize("password", ["short1", "abcdefgh", "12345678"])
def test_registration_rejects_weak_passwords(password):
    with pytest.raises(ValidationError):
        UserCreate(email="student@example.test", password=password)


@pytest.mark.parametrize("email", ["missing-at", "a@b", "a b@example.test"])
def test_registration_rejects_invalid_email(email):
    with pytest.raises(ValidationError):
        UserCreate(email=email, password="Password123")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("quantity", "0"),
        ("quantity", "-1"),
        ("direct_emissions", "-0.1"),
        ("indirect_emissions", "-1"),
        ("carbon_price", "-1"),
        ("quantity", "oops"),
        ("country_of_origin", "tur"),
        ("name", "   "),
    ],
)
def test_product_rejects_invalid_fields(field, value):
    data = dict(
        name="Sample",
        cn_code="720810",
        country_of_origin="TR",
        quantity=Decimal("1"),
        unit="tonnes",
        direct_emissions=Decimal("1"),
        indirect_emissions=Decimal("0"),
        carbon_price=Decimal("1"),
    )
    data[field] = value
    with pytest.raises(ValidationError):
        ProductInput.model_validate(data)
