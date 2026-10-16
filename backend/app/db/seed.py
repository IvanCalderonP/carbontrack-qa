"""Populate clearly fictional examples in a locally configured development database."""

from decimal import Decimal

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models import Product, User


def seed() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        email = "demo@example.test"
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, hashed_password=hash_password("DemoPass123"))
            db.add(user)
            db.flush()
        if not db.scalar(select(Product.id).where(Product.owner_id == user.id).limit(1)):
            for name, cn, country, quantity, direct, indirect, price in (
                ("Sample steel coil", "720810", "TR", "125", "43.5", "12.4", "42"),
                ("Sample aluminium billet", "760120", "IN", "80", "24.2", "8.1", "42"),
                ("Sample cement clinker", "252310", "MA", "230", "72.9", "16.3", "42"),
                ("Sample fertilizer", "310210", "EG", "65", "18.5", "5.6", "42"),
            ):
                db.add(
                    Product(
                        owner_id=user.id,
                        name=name,
                        cn_code=cn,
                        country_of_origin=country,
                        quantity=Decimal(quantity),
                        unit="tonnes",
                        direct_emissions=Decimal(direct),
                        indirect_emissions=Decimal(indirect),
                        carbon_price=Decimal(price),
                    )
                )
        db.commit()
    print("Fictional demo data ready. Login: demo@example.test / DemoPass123")


if __name__ == "__main__":
    seed()
