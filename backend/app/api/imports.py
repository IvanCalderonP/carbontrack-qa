from fastapi import APIRouter, UploadFile
from sqlalchemy import select, tuple_
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, Db
from app.core.errors import AppError
from app.models import Product
from app.schemas.contracts import ImportErrorRow, ImportResult
from app.services.excel_import import MAX_UPLOAD_BYTES, parse_products_workbook

router = APIRouter(prefix="/imports", tags=["Imports"])


@router.post("/products", response_model=ImportResult, summary="Import validated Excel products")
async def import_products(file: UploadFile, db: Db, user: CurrentUser) -> ImportResult:
    if not file.filename or not file.filename.lower().endswith(".xlsx"):
        raise AppError(400, "UNSUPPORTED_FILE", "Only .xlsx files are supported")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise AppError(413, "FILE_TOO_LARGE", "Maximum upload size is 2 MiB")
    parsed = parse_products_workbook(content)
    identities = [(item.name, item.cn_code, item.country_of_origin) for _, item in parsed.products]
    existing = set()
    if identities:
        existing = set(
            db.execute(
                select(Product.name, Product.cn_code, Product.country_of_origin).where(
                    Product.owner_id == user.id,
                    tuple_(Product.name, Product.cn_code, Product.country_of_origin).in_(identities),
                )
            ).all()
        )
    imported = 0
    for row_number, data in parsed.products:
        key = (data.name, data.cn_code, data.country_of_origin)
        if key in existing:
            parsed.errors.append(ImportErrorRow(row=row_number, field="product_name", message="Product already exists"))
            continue
        db.add(Product(**data.model_dump(), owner_id=user.id))
        existing.add(key)
        imported += 1
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "IMPORT_CONFLICT", "Import conflicts with existing products") from None
    invalid_rows = len({error.row for error in parsed.errors})
    return ImportResult(
        total_rows=parsed.total_rows,
        valid_rows=parsed.total_rows - invalid_rows,
        invalid_rows=invalid_rows,
        imported=imported,
        errors=sorted(parsed.errors, key=lambda e: e.row),
    )
