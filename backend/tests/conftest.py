import os
from collections.abc import Iterator
from decimal import Decimal
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["SECRET_KEY"] = "test-only-secret-key-with-enough-length-123456"

from app.api.dependencies import get_carbon_price_provider  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.db.session import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import User  # noqa: E402
from app.services.excel_import import HEADERS  # noqa: E402


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine, expire_on_commit=False)() as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    def override_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    user = User(email="student@example.test", hashed_password=hash_password("Password123"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session: Session) -> User:
    user = User(email="admin@example.test", hashed_password=hash_password("Password123"), role="admin")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "Password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def admin_headers(client: TestClient, admin_user: User) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": admin_user.email, "password": "Password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def sample_product() -> dict[str, str]:
    return {
        "name": "Fictional steel coil",
        "cn_code": "720810",
        "country_of_origin": "TR",
        "quantity": "10.25",
        "unit": "tonnes",
        "direct_emissions": "3.125",
        "indirect_emissions": "1.375",
        "carbon_price": "40.50",
    }


@pytest.fixture
def sample_products(client: TestClient, auth_headers: dict[str, str], sample_product: dict[str, str]) -> list[dict]:
    result = []
    for index in range(3):
        data = {**sample_product, "name": f"Fictional product {index}"}
        result.append(client.post("/api/v1/products", json=data, headers=auth_headers).json())
    return result


def workbook_bytes(rows: list[list[object]], headers: tuple[str, ...] = HEADERS) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


@pytest.fixture
def valid_excel_file() -> bytes:
    return workbook_bytes(
        [
            ["Fictional steel", "720810", "TR", Decimal("10.25"), "tonnes", 2, 1, 40],
            ["Fictional aluminium", "760120", "IN", 8, "tonnes", 3, 2, 41],
        ]
    )


@pytest.fixture
def invalid_excel_file() -> bytes:
    return workbook_bytes(
        [
            ["Fictional steel", "720810", "TR", -1, "tonnes", 2, 1, 40],
            ["Fictional aluminium", "760120", "IN", 8, "tonnes", 3, 2, 41],
        ]
    )


@pytest.fixture
def mock_carbon_price_provider(client: TestClient) -> Iterator[object]:
    class FakeProvider:
        def reference_price(self) -> Decimal:
            return Decimal("99.99")

    provider = FakeProvider()
    app.dependency_overrides[get_carbon_price_provider] = lambda: provider
    yield provider
    app.dependency_overrides.pop(get_carbon_price_provider, None)
