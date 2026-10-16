from decimal import Decimal


def calculate_emissions(
    quantity: Decimal, direct: Decimal, indirect: Decimal, carbon_price: Decimal
) -> tuple[Decimal, Decimal, Decimal]:
    """Return simplified educational total, intensity, and cost; not official CBAM math."""
    if quantity <= 0 or min(direct, indirect, carbon_price) < 0:
        raise ValueError("Quantity must be positive and emissions and price cannot be negative")
    total = direct + indirect
    return total, total / quantity, total * carbon_price
