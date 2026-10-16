from decimal import Decimal

import pytest


def test_create_read_update_delete_product(client, auth_headers, sample_product):
    created = client.post("/api/v1/products", json=sample_product, headers=auth_headers)
    assert created.status_code == 201
    product = created.json()
    assert product["total_emissions"] == "4.5000000000"
    product_id = product["id"]
    assert client.get(f"/api/v1/products/{product_id}", headers=auth_headers).json()["name"] == sample_product["name"]
    updated = client.put(
        f"/api/v1/products/{product_id}", json={**sample_product, "name": "Updated steel"}, headers=auth_headers
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Updated steel"
    assert client.delete(f"/api/v1/products/{product_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/api/v1/products/{product_id}", headers=auth_headers).status_code == 404


def test_create_uses_replaceable_carbon_price_provider(
    client, auth_headers, sample_product, mock_carbon_price_provider
):
    data = {key: value for key, value in sample_product.items() if key != "carbon_price"}
    response = client.post("/api/v1/products", json=data, headers=auth_headers)
    assert response.status_code == 201
    assert Decimal(response.json()["carbon_price"]) == Decimal("99.99")


def test_create_rejects_duplicate_and_invalid_product(client, auth_headers, sample_product):
    assert client.post("/api/v1/products", json=sample_product, headers=auth_headers).status_code == 201
    duplicate = client.post("/api/v1/products", json=sample_product, headers=auth_headers)
    assert duplicate.status_code == 409
    invalid = client.post("/api/v1/products", json={**sample_product, "quantity": 0}, headers=auth_headers)
    assert invalid.status_code == 422


def test_list_pagination_search_filter_sort(client, auth_headers, sample_products):
    response = client.get("/api/v1/products?page=2&page_size=1&sort_by=name&sort_order=asc", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 3
    assert response.json()["pages"] == 3
    assert response.json()["items"][0]["name"] == "Fictional product 1"
    filtered = client.get(
        "/api/v1/products?country_of_origin=TR&cn_code=720810&search=product%202&min_emissions=4&max_emissions=5",
        headers=auth_headers,
    )
    assert [item["id"] for item in filtered.json()["items"]] == [sample_products[2]["id"]]
    assert client.get("/api/v1/products?country_of_origin=IN", headers=auth_headers).json()["total"] == 0


@pytest.mark.parametrize(
    "query,status",
    [
        ("page=0", 422),
        ("page_size=101", 422),
        ("sort_by=secret", 422),
        ("min_emissions=5&max_emissions=1", 400),
    ],
)
def test_list_rejects_invalid_query(client, auth_headers, query, status):
    assert client.get(f"/api/v1/products?{query}", headers=auth_headers).status_code == status


def test_owner_cannot_access_other_product_but_admin_can(client, auth_headers, admin_headers, sample_product):
    created = client.post("/api/v1/products", json=sample_product, headers=auth_headers).json()
    product_url = f"/api/v1/products/{created['id']}"
    assert client.get(product_url, headers=admin_headers).status_code == 200
    other = client.post("/api/v1/auth/register", json={"email": "other@example.test", "password": "Password123"})
    assert other.status_code == 201
    token = client.post("/api/v1/auth/login", json={"email": "other@example.test", "password": "Password123"}).json()[
        "access_token"
    ]
    other_headers = {"Authorization": f"Bearer {token}"}
    assert client.get(product_url, headers=other_headers).status_code == 403
    assert client.put(product_url, json=sample_product, headers=other_headers).status_code == 403
    assert client.delete(product_url, headers=other_headers).status_code == 403
    assert client.get("/api/v1/products", headers=other_headers).json()["total"] == 0
    assert client.delete(product_url, headers=admin_headers).status_code == 204


def test_update_duplicate_returns_conflict(client, auth_headers, sample_products, sample_product):
    first = sample_products[0]
    second = sample_products[1]
    response = client.put(
        f"/api/v1/products/{second['id']}", json={**sample_product, "name": first["name"]}, headers=auth_headers
    )
    assert response.status_code == 409


def test_missing_product_and_unauthenticated_request(client, auth_headers):
    assert client.get("/api/v1/products/999", headers=auth_headers).status_code == 404
    assert client.get("/api/v1/products").status_code == 401
