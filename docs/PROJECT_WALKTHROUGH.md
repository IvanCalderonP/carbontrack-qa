# Project walkthrough

Read this guide after running the tests once. Start with one request, then follow it through validation, services, persistence, and the UI.

## Backend modules

| File or group | Responsibility | Connection and useful tests |
| --- | --- | --- |
| `app/main.py` | Builds FastAPI, CORS, health, error envelope, OpenAPI. | Includes route modules; `tests/api/test_auth.py` checks health/errors. |
| `app/core/config.py` | Reads env-based database URL, secret, token lifetime, origins. | Imported by database/security; tests set a test secret before importing app. |
| `app/core/security.py` | Argon2 hashing and JWT creation/validation. | Auth routes and current-user dependency; auth API tests cover wrong/expired tokens. |
| `app/core/errors.py` | Typed expected HTTP errors. | Routes raise it; main serializes a consistent error body. |
| `app/db/session.py` | Engine, session factory, injectable `get_db`. | Tests override this dependency with isolated SQLite. |
| `app/models/entities.py` | User/Product SQLAlchemy tables, ownership, numeric columns. | Migration mirrors schema; API tests inspect behavior through HTTP. |
| `app/schemas/contracts.py` | Pydantic request/response contracts. | Used by routes and parser; `tests/unit/test_validation.py` probes boundaries. |
| `app/api/dependencies.py` | Database, token-to-user, and price-provider injection. | `tests/conftest.py` replaces database/provider. |
| `app/api/auth.py` | Register, login, current user. | `tests/api/test_auth.py`. |
| `app/api/products.py` | CRUD endpoints, status codes, ownership, calculated response. | Calls repository/services; `tests/api/test_products.py`. |
| `app/repositories/products.py` | Count, filters, stable order, pagination, duplicate check. | Exercised through API list tests. |
| `app/services/emissions.py` | Exact `Decimal` educational formulas. | `tests/unit/test_emissions.py` uses meaningful parametrization. |
| `app/services/carbon_price.py` | Local fictional default price behind a protocol. | Fake injected in a product API test. |
| `app/services/excel_import.py` | Header, row, duplicate, and numeric workbook validation. | `tests/unit/test_excel_import.py`. |
| `app/api/imports.py` | Upload limits, owner duplicate check, partial import response. | `tests/api/test_imports_dashboard.py`. |
| `app/api/dashboard.py` | One aggregate query over owned products. | Summary API tests. |
| `app/db/seed.py` | Optional fictional local data. | Only run against a chosen development database. |
| `migrations/` | Alembic initial schema. | `tests/integration/test_migrations.py` uses a temporary database file. |
| `tests/conftest.py` | Fresh schema/session per test, users, headers, workbooks, fake provider. | Central test isolation; no configured developer DB is touched. |

## Frontend modules

| File or group | Responsibility | Connection and useful tests |
| --- | --- | --- |
| `src/App.tsx` | Session check, navigation, protected pages. | Uses auth API and routes. |
| `src/api/client.ts` | Shared fetch, bearer header, network and HTTP errors, 204 handling. | Exercised by all component tests with mocked `fetch`. |
| `src/api/auth.ts`, `products.ts`, `dashboard.ts`, `imports.ts` | Small typed endpoint clients. | Pages call one client each. |
| `src/types/index.ts` | Shared API shape definitions. | Keeps page contracts explicit. |
| `src/pages/Login.tsx` | Form validation, loading, and login errors. | `tests/Login.test.tsx`. |
| `src/pages/Dashboard.tsx` | Summary cards, loading/error/empty states. | `tests/Dashboard.test.tsx`. |
| `src/pages/Products.tsx` | Search, country filter, pagination, creation, deletion. | `tests/Products.test.tsx`. |
| `src/pages/ImportExcel.tsx` | File picker, upload, result counts and row errors. | `tests/ImportExcel.test.tsx`. |
| `src/styles.css` | Responsive SaaS-style presentation. | Manual narrow-viewport case in `TEST_CASES.md`. |

## Suggested study exercise

Trace a workbook row through `parse_products_workbook`, `import_products`, the `Product` model, dashboard aggregation, and the React import result. Then change a boundary (for example zero quantity), write the expected unit/API assertions, and run both suites. This connects the architecture to observable behavior.

## Explicación breve en español

El proyecto simula un portafolio de productos con datos ficticios. El backend valida usuarios, productos y archivos Excel; guarda datos en PostgreSQL y calcula emisiones con fórmulas educativas. El frontend permite iniciar sesión, consultar el resumen, gestionar productos e importar un libro. Las pruebas unitarias revisan reglas pequeñas; las pruebas API revisan el flujo completo con una base aislada; Vitest revisa lo que ve y hace el usuario. Ninguna fórmula pretende ser oficial de CBAM.
