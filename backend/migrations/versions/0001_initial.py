"""Initial users and products schema.

Revision ID: 0001_initial
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=10), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("cn_code", sa.String(length=12), nullable=False),
        sa.Column("country_of_origin", sa.String(length=2), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("unit", sa.String(length=20), nullable=False),
        sa.Column("direct_emissions", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("indirect_emissions", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("carbon_price", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("owner_id", "name", "cn_code", "country_of_origin"),
    )
    op.create_index("ix_products_owner_id", "products", ["owner_id"])
    op.create_index("ix_products_cn_code", "products", ["cn_code"])
    op.create_index("ix_products_country_of_origin", "products", ["country_of_origin"])


def downgrade() -> None:
    op.drop_table("products")
    op.drop_table("users")
