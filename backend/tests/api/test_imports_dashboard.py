from decimal import Decimal
from io import BytesIO

from tests.conftest import workbook_bytes


def upload(client, headers, filename, content):
    return client.post("/api/v1/imports/products", files={"file": (filename, BytesIO(content))}, headers=headers)


def test_import_valid_file_and_dashboard(client, auth_headers, valid_excel_file):
    result = upload(client, auth_headers, "products.xlsx", valid_excel_file)
    assert result.status_code == 200
    assert result.json()["imported"] == 2
    summary = client.get("/api/v1/dashboard/summary", headers=auth_headers)
    assert summary.status_code == 200
    assert summary.json()["total_products"] == 2
    assert summary.json()["total_emissions"] == "8.0000000000"
    assert Decimal(summary.json()["estimated_carbon_cost"]) == Decimal("325")


def test_dashboard_empty_and_owner_scoped(client, auth_headers, admin_headers, sample_product):
    assert client.get("/api/v1/dashboard/summary", headers=auth_headers).json()["total_products"] == 0
    client.post("/api/v1/products", json=sample_product, headers=auth_headers)
    assert client.get("/api/v1/dashboard/summary", headers=admin_headers).json()["total_products"] == 0


def test_import_mixed_rows_and_existing_duplicate(client, auth_headers, invalid_excel_file):
    result = upload(client, auth_headers, "products.xlsx", invalid_excel_file)
    assert result.status_code == 200
    assert result.json()["invalid_rows"] == 1
    assert result.json()["imported"] == 1
    repeated = upload(client, auth_headers, "products.xlsx", invalid_excel_file)
    assert repeated.json()["invalid_rows"] == 2
    assert repeated.json()["imported"] == 0


def test_import_rejects_extension_corruption_and_empty(client, auth_headers):
    assert upload(client, auth_headers, "products.csv", b"a,b").status_code == 400
    assert upload(client, auth_headers, "products.xlsx", b"corrupt").status_code == 400
    assert upload(client, auth_headers, "products.xlsx", workbook_bytes([])).status_code == 422


def test_import_rejects_large_file(client, auth_headers):
    assert upload(client, auth_headers, "products.xlsx", b"a" * (2 * 1024 * 1024 + 1)).status_code == 413


def test_import_requires_authentication(client, valid_excel_file):
    assert upload(client, {}, "products.xlsx", valid_excel_file).status_code == 401
