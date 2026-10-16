from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, Db
from app.core.errors import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.schemas.contracts import LoginRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=201, summary="Register a user")
def register(data: UserCreate, db: Db) -> User:
    user = User(email=data.email.lower(), hashed_password=hash_password(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "EMAIL_EXISTS", "Email is already registered") from None
    db.refresh(user)
    return user


@router.post("/login", response_model=Token, summary="Log in")
def login(data: LoginRequest, db: Db) -> Token:
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    if user is None or not user.is_active or not verify_password(data.password, user.hashed_password):
        raise AppError(401, "INVALID_CREDENTIALS", "Invalid email or password")
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserRead, summary="Get authenticated user")
def me(user: CurrentUser) -> User:
    return user
