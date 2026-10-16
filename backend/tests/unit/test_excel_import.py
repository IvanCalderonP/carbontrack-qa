from io import BytesIO

import pytest
from openpyxl import Workbook

from app.core.errors import AppError
from app.services.excel_import import HEADERS, parse_products_workbook
from tests.conftest import workbook_bytes


def test_parser_accepts_multiple_valid_rows_and_decimals(valid_excel_file):
    result = parse_products_workbook(valid_excel_file)
    assert result.total_rows == 2
    assert len(result.products) == 2
    assert str(result.products[0][1].quantity) == "10.25"
    assert result.errors == []


@pytest.mark.parametrize(
    ("content", "code"),
    [
        (b"not excel", "INVALID_WORKBOOK"),
        (workbook_bytes([], HEADERS), "EMPTY_WORKBOOK"),
        (workbook_bytes([["X"]], HEADERS[:-1]), "INVALID_HEADERS"),
        (workbook_bytes([["X"]], HEADERS + ("extra",)), "INVALID_HEADERS"),
    ],
    ids=["not-zip", "headers-only", "missing-header", "extra-header"],
)
def test_parser_rejects_invalid_workbook_or_headers(content, code):
    with pytest.raises(AppError) as error:
        parse_products_workbook(content)
    assert error.value.detail["code"] == code


def test_parser_rejects_valid_zip_that_is_not_workbook():
    with pytest.raises(AppError) as error:
        parse_products_workbook(b"PKbroken")
    assert error.value.detail["code"] == "INVALID_WORKBOOK"


@pytest.mark.parametrize(
    ("row", "field"),
    [
        (["Steel", "720810", "TR", None, "tonnes", 1, 1, 40], "quantity"),
        (["Steel", "720810", "TR", "bad", "tonnes", 1, 1, 40], "quantity"),
        (["Steel", "720810", "TR", -1, "tonnes", 1, 1, 40], "quantity"),
        (["Steel", "720810", "TR", 1, "tonnes", -1, 1, 40], "direct_emissions"),
        (["Steel", "720810", "TR", 1, "tonnes", 1, 1, -1], "carbon_price"),
    ],
)
def test_parser_reports_row_and_field_errors(row, field):
    result = parse_products_workbook(workbook_bytes([row]))
    assert len(result.products) == 0
    assert any(error.row == 2 and error.field == field for error in result.errors)


def test_parser_reports_duplicate_and_mixed_rows():
    row = ["Steel", "720810", "TR", 1, "tonnes", 1, 1, 40]
    result = parse_products_workbook(workbook_bytes([row, row, ["Bad", "720810", "TR", -1, "tonnes", 1, 1, 40]]))
    assert result.total_rows == 3
    assert len(result.products) == 1
    assert {error.row for error in result.errors} == {3, 4}


def test_parser_reports_interior_empty_row():
    row = ["Steel", "720810", "TR", 1, "tonnes", 1, 1, 40]
    result = parse_products_workbook(workbook_bytes([row, [None] * 8, row]))
    assert any(error.row == 3 and error.field == "row" for error in result.errors)


def test_parser_rejects_workbook_without_header():
    workbook = Workbook()
    output = BytesIO()
    workbook.save(output)
    with pytest.raises(AppError):
        parse_products_workbook(output.getvalue())


def test_parser_rejects_more_than_1000_data_rows():
    row = ["Steel", "720810", "TR", 1, "tonnes", 1, 1, 40]
    with pytest.raises(AppError) as error:
        parse_products_workbook(workbook_bytes([row] * 1001))
    assert error.value.detail["code"] == "TOO_MANY_ROWS"
