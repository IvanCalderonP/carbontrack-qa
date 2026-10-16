from decimal import Decimal
from math import ceil
from typing import Literal

from fastapi import APIRouter, Query
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, Db, PriceProvider
from app.core.errors import AppError
from app.models import Product
from app.repositories.products import duplicate_exists, get_product, list_products
from app.schemas.contracts import ProductInput, ProductPage, ProductRead
from app.services.emissions import calculate_emissions

router = APIRouter(prefix="/products", tags=["Products"])


def product_read(product: Product) -> ProductRead:
    total, intensity, cost = calculate_emissions(
        product.quantity, product.direct_emissions, product.indirect_emissions, product.carbon_price
    )
    return ProductRead.model_validate(
        {
            **{field: getattr(product, field) for field in ProductInput.model_fields},
            "id": product.id,
            "owner_id": product.owner_id,
            "total_emissions": total,
            "emission_intensity": intensity,
            "estimated_carbon_cost": cost,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }
    )


def visible_product(db: Db, user: CurrentUser, product_id: int) -> Product:
    product = get_product(db, product_id)
    if product is None:
        raise AppError(404, "PRODUCT_NOT_FOUND", "Product not found")
    if product.owner_id != user.id and user.role != "admin":
        raise AppError(403, "FORBIDDEN", "You cannot access this product")
    return product


@router.post("", response_model=ProductRead, status_code=201, summary="Create product")
def create_product(data: ProductInput, db: Db, user: CurrentUser, provider: PriceProvider) -> ProductRead:
    if duplicate_exists(db, user.id, data.name, data.cn_code, data.country_of_origin):
        raise AppError(409, "PRODUCT_EXISTS", "Product already exists")
    product = Product(
        **data.model_dump(exclude={"carbon_price"}),
        carbon_price=data.carbon_price if data.carbon_price is not None else provider.reference_price(),
        owner_id=user.id,
    )
    db.add(product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "PRODUCT_EXISTS", "Product already exists") from None
    db.refresh(product)
    return product_read(product)


@router.get("", response_model=ProductPage, summary="Search and paginate products")
def products(
    db: Db,
    user: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    country_of_origin: str | None = None,
    cn_code: str | None = None,
    search: str | None = None,
    min_emissions: Decimal | None = Query(None, ge=0),
    max_emissions: Decimal | None = Query(None, ge=0),
    sort_by: Literal["name", "created_at", "quantity", "total_emissions"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> ProductPage:
    if min_emissions is not None and max_emissions is not None and min_emissions > max_emissions:
        raise AppError(400, "INVALID_RANGE", "Minimum emissions exceeds maximum")
    items, total = list_products(
        db,
        user.id,
        page,
        page_size,
        country_of_origin,
        cn_code,
        search,
        min_emissions,
        max_emissions,
        sort_by,
        sort_order,
    )
    return ProductPage(
        items=[product_read(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=ceil(total / page_size),
    )


@router.get("/{product_id}", response_model=ProductRead, summary="Get product")
def read_product(product_id: int, db: Db, user: CurrentUser) -> ProductRead:
    return product_read(visible_product(db, user, product_id))


@router.put("/{product_id}", response_model=ProductRead, summary="Replace product")
def update_product(
    product_id: int, data: ProductInput, db: Db, user: CurrentUser, provider: PriceProvider
) -> ProductRead:
    product = visible_product(db, user, product_id)
    if duplicate_exists(db, product.owner_id, data.name, data.cn_code, data.country_of_origin, product_id):
        raise AppError(409, "PRODUCT_EXISTS", "Product already exists")
    for field, value in data.model_dump(exclude={"carbon_price"}).items():
        setattr(product, field, value)
    product.carbon_price = data.carbon_price if data.carbon_price is not None else provider.reference_price()
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "PRODUCT_EXISTS", "Product already exists") from None
    db.refresh(product)
    return product_read(product)


@router.delete("/{product_id}", status_code=204, summary="Delete own product or administer one")
def delete_product(product_id: int, db: Db, user: CurrentUser) -> None:
    product = visible_product(db, user, product_id)
    db.delete(product)
    db.commit()
