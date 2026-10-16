from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def strong_enough(cls, value: str) -> str:
        if not any(ch.isalpha() for ch in value) or not any(ch.isdigit() for ch in value):
            raise ValueError("Password must include a letter and a number")
        return value


class LoginRequest(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProductInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    cn_code: str = Field(min_length=4, max_length=12, pattern=r"^\d+$")
    country_of_origin: str = Field(min_length=2, max_length=2, pattern=r"^[A-Z]{2}$")
    quantity: Decimal = Field(gt=0, max_digits=28, decimal_places=10)
    unit: str = Field(min_length=1, max_length=20)
    direct_emissions: Decimal = Field(ge=0, max_digits=28, decimal_places=10)
    indirect_emissions: Decimal = Field(ge=0, max_digits=28, decimal_places=10)
    carbon_price: Decimal | None = Field(default=None, ge=0, max_digits=28, decimal_places=10)

    @field_validator("name", "unit")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Must not be blank")
        return value


class ProductRead(ProductInput):
    id: int
    owner_id: int
    carbon_price: Decimal
    total_emissions: Decimal
    emission_intensity: Decimal
    estimated_carbon_cost: Decimal
    created_at: datetime
    updated_at: datetime


class ProductPage(BaseModel):
    items: list[ProductRead]
    total: int
    page: int
    page_size: int
    pages: int


class ImportErrorRow(BaseModel):
    row: int
    field: str
    message: str


class ImportResult(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    imported: int
    errors: list[ImportErrorRow]


class DashboardSummary(BaseModel):
    total_products: int
    total_quantity: Decimal
    total_direct_emissions: Decimal
    total_indirect_emissions: Decimal
    total_emissions: Decimal
    estimated_carbon_cost: Decimal
