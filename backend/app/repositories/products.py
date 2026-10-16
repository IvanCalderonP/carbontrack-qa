from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Product


def duplicate_exists(db: Session, owner_id: int, name: str, cn_code: str, country: str, exclude_id: int = 0) -> bool:
    query = select(Product.id).where(
        Product.owner_id == owner_id,
        Product.name == name,
        Product.cn_code == cn_code,
        Product.country_of_origin == country,
        Product.id != exclude_id,
    )
    return db.scalar(query.limit(1)) is not None


def list_products(
    db: Session,
    owner_id: int,
    page: int,
    page_size: int,
    country: str | None,
    cn_code: str | None,
    search: str | None,
    min_emissions: Decimal | None,
    max_emissions: Decimal | None,
    sort_by: str,
    sort_order: str,
) -> tuple[list[Product], int]:
    query = select(Product).where(Product.owner_id == owner_id)
    if country:
        query = query.where(Product.country_of_origin == country)
    if cn_code:
        query = query.where(Product.cn_code == cn_code)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    total_expression = Product.direct_emissions + Product.indirect_emissions
    if min_emissions is not None:
        query = query.where(total_expression >= min_emissions)
    if max_emissions is not None:
        query = query.where(total_expression <= max_emissions)
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    columns = {
        "name": Product.name,
        "created_at": Product.created_at,
        "quantity": Product.quantity,
        "total_emissions": total_expression,
    }
    order_column = columns[sort_by]
    query = query.order_by(order_column.desc() if sort_order == "desc" else order_column.asc(), Product.id.asc())
    return list(db.scalars(query.offset((page - 1) * page_size).limit(page_size))), total


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)
