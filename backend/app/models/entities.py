from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(10), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    products: Mapped[list["Product"]] = relationship(back_populates="owner")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (UniqueConstraint("owner_id", "name", "cn_code", "country_of_origin"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    cn_code: Mapped[str] = mapped_column(String(12), index=True)
    country_of_origin: Mapped[str] = mapped_column(String(2), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    unit: Mapped[str] = mapped_column(String(20))
    direct_emissions: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    indirect_emissions: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    carbon_price: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    owner: Mapped[User] = relationship(back_populates="products")
