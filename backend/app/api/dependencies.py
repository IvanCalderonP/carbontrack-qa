from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models import User
from app.services.carbon_price import CarbonPriceProvider, LocalCarbonPriceProvider

Db = Annotated[Session, Depends(get_db)]
bearer = HTTPBearer(auto_error=False)


def get_current_user(db: Db, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> User:
    if credentials is None:
        raise AppError(401, "UNAUTHORIZED", "Authentication required")
    try:
        user_id = decode_access_token(credentials.credentials)
    except (jwt.PyJWTError, ValueError, KeyError):
        raise AppError(401, "INVALID_TOKEN", "Invalid or expired token") from None
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise AppError(401, "INVALID_TOKEN", "Invalid or expired token")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_carbon_price_provider() -> CarbonPriceProvider:
    return LocalCarbonPriceProvider()


PriceProvider = Annotated[CarbonPriceProvider, Depends(get_carbon_price_provider)]
