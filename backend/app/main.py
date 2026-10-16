import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.api import auth, dashboard, imports, products
from app.core.config import get_settings
from app.core.errors import AppError

app = FastAPI(
    title="CarbonTrack QA API",
    description="Independent educational carbon accounting QA portfolio; not official CBAM methodology.",
    version="1.0.0",
)
logger = logging.getLogger(__name__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "HTTP_ERROR", "message": str(exc.detail)}},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    issues = [
        {"field": ".".join(str(part) for part in issue["loc"]), "message": issue["msg"]} for issue in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid request", "issues": issues}},
    )


@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled API error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}},
    )


@app.get("/health", tags=["Health"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok"}


for router in (auth.router, products.router, imports.router, dashboard.router):
    app.include_router(router, prefix="/api/v1")
