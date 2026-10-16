from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import get_settings

hasher = PasswordHasher()
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return hasher.verify(hashed, password)
    except VerifyMismatchError:
        return False


def create_access_token(user_id: int, *, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    expiry = datetime.now(UTC) + (
        expires_delta if expires_delta is not None else timedelta(minutes=settings.access_token_expire_minutes)
    )
    return jwt.encode({"sub": str(user_id), "exp": expiry}, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, get_settings().secret_key, algorithms=[ALGORITHM])
    return int(payload["sub"])
