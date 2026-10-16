from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import func, select

from app.api.dependencies import CurrentUser, Db
from app.models import Product
from app.schemas.contracts import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary, summary="Summarize own portfolio")
def summary(db: Db, user: CurrentUser) -> DashboardSummary:
    count, quantity, direct, indirect, cost = db.execute(
        select(
            func.count(Product.id),
            func.sum(Product.quantity),
            func.sum(Product.direct_emissions),
            func.sum(Product.indirect_emissions),
            func.sum((Product.direct_emissions + Product.indirect_emissions) * Product.carbon_price),
        ).where(Product.owner_id == user.id)
    ).one()
    zero = Decimal("0")
    return DashboardSummary(
        total_products=count,
        total_quantity=quantity or zero,
        total_direct_emissions=direct or zero,
        total_indirect_emissions=indirect or zero,
        total_emissions=(direct or zero) + (indirect or zero),
        estimated_carbon_cost=cost or zero,
    )
