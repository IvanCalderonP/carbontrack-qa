from datetime import timedelta

from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.db.session import get_db
from app.main import app


def test_register_success_and_duplicate_email(client):
    payload = {"email": "New@Example.test", "password": "Password123"}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "new@example.test"
    assert "password" not in response.json()
    duplicate = client.post("/api/v1/auth/register", json=payload)
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "EMAIL_EXISTS"


def test_register_rejects_invalid_email_and_weak_password(client):
    for payload in (
        {"email": "bad", "password": "Password123"},
        {"email": "good@example.test", "password": "weak"},
    ):
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_login_and_me(client, test_user):
    login = client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "Password123"})
    assert login.status_code == 200
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {login.json()['access_token']}"})
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id


def test_login_wrong_password_or_unknown_user(client, test_user):
    for email, password in ((test_user.email, "Wrong123"), ("nobody@example.test", "Password123")):
        response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_auth_rejects_missing_invalid_and_expired_tokens(client, test_user):
    tokens = (
        None,
        "garbage",
        create_access_token(test_user.id, expires_delta=timedelta(seconds=-1)),
        create_access_token(test_user.id, expires_delta=timedelta(0)),
    )
    for token in tokens:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401


def test_inactive_user_cannot_log_in_or_use_existing_token(client, test_user, db_session):
    token = create_access_token(test_user.id)
    test_user.is_active = False
    db_session.commit()
    assert (
        client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "Password123"}).status_code == 401
    )
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_local_frontend_origins_are_allowed(client):
    for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin


def test_unknown_route_uses_consistent_error_envelope(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "HTTP_ERROR"


def test_unexpected_server_error_is_sanitized(db_session, test_user, monkeypatch):
    def override_db():
        yield db_session

    def broken_query(*args, **kwargs):
        raise RuntimeError("sensitive internal detail")

    app.dependency_overrides[get_db] = override_db
    monkeypatch.setattr(db_session, "execute", broken_query)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            token = create_access_token(test_user.id)
            response = client.get("/api/v1/dashboard/summary", headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 500
    assert response.json() == {"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}}
