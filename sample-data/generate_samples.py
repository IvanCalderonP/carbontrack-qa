"""Regenerate the two genuine, entirely fictional Excel workbooks."""

from pathlib import Path

from openpyxl import Workbook

HEADERS = [
    "product_name",
    "cn_code",
    "country_of_origin",
    "quantity",
    "unit",
    "direct_emissions",
    "indirect_emissions",
    "carbon_price",
]
ROOT = Path(__file__).resolve().parent


def write(name: str, rows: list[list[object]]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Products"
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    sheet.freeze_panes = "A2"
    for column, width in {"A": 28, "B": 15, "C": 22, "D": 15, "E": 14, "F": 21, "G": 21, "H": 17}.items():
        sheet.column_dimensions[column].width = width
    workbook.save(ROOT / name)


write(
    "valid_products.xlsx",
    [
        ["Fictional steel coil", "720810", "TR", 125.25, "tonnes", 43.5, 12.4, 42],
        ["Fictional aluminium billet", "760120", "IN", 80, "tonnes", 24.2, 8.1, 42],
        ["Fictional cement clinker", "252310", "MA", 230.75, "tonnes", 72.9, 16.3, 42],
        ["Fictional fertilizer", "310210", "EG", 65.125, "tonnes", 18.5, 5.6, 42],
    ],
)
write(
    "invalid_products.xlsx",
    [
        ["Valid fictional steel", "720810", "TR", 10, "tonnes", 3, 1, 42],
        ["Negative quantity", "720810", "TR", -2, "tonnes", 1, 1, 42],
        ["Missing price", "760120", "IN", 5, "tonnes", 2, 1, None],
        ["Invalid number", "252310", "MA", "many", "tonnes", 2, 1, 42],
        ["Valid fictional cement", "252310", "MA", 8.25, "tonnes", 3, 2, 42],
        ["Valid fictional cement", "252310", "MA", 8.25, "tonnes", 3, 2, 42],
    ],
)
print("Generated genuine .xlsx sample workbooks")
