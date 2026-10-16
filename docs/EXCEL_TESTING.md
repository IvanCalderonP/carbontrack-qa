# Excel ingestion testing

## File and schema validation

Only `.xlsx` is accepted. The route reads at most 2 MiB plus one byte before rejecting an oversized upload. The parser requires a ZIP-backed workbook with one active sheet and the eight documented headers in exact order. Missing, extra, or reordered headers fail the entire file with 422. Empty data fails with 422. Corrupted files return 400 without leaking parser exceptions. The workbook is read-only, formulas are not executed, links are not followed, and the parser closes the file.

## Row validation

Required cells cannot be empty. Quantity must exceed zero; direct/indirect emissions and carbon price cannot be negative. CN code remains text to preserve leading zeros. Country uses two uppercase letters. Decimal fields allow at most 28 digits and 10 decimal places. Interior blank rows, invalid numeric types, and repeated `(name, CN code, country)` identities are reported by row/field. Existing products for the current owner also produce row errors. Valid rows can import alongside invalid ones, with one database commit for the accepted set.

## Test inventory

Unit tests create genuine in-memory openpyxl files for valid multirow/decimal data, header errors, empty workbooks, damaged ZIPs, missing cells, bad types, negative numbers, duplicates, and blank rows. API tests cover extension, size, authentication, mixed rows, duplicate imports, summary effects, and a valid upload. `sample-data/` contains persistent real `.xlsx` examples for manual review.

The 1,000-row cap is a pragmatic resource limit. A production parser would add deeper ZIP expansion limits, content scanning, streaming/storage design, and documented formula handling. These safeguards are outside this educational sample.
