# Test strategy

## Objective and scope

The objective is confidence in the sample's validation, ownership boundaries, deterministic calculations, ingestion behavior, and visible UI flows. Scope includes backend services, API contracts and database effects, the initial migration, and React user interactions. Official CBAM correctness, third-party integrations, and production security certification are out of scope.

## Risk-based priorities

| Risk | Priority | Evidence |
| --- | --- | --- |
| Wrong decimal calculations | High | Parameterized zero, precision, large number, and invalid-input unit tests |
| Unauthorized portfolio access | High | Authentication and cross-owner/admin API tests |
| Bad Excel rows polluting data | High | Parser and import API tests with mixed rows and duplicates |
| Incorrect HTTP contract | High | API status, response, filtering, and pagination tests |
| Broken UI feedback | Medium | Loading, empty, error, form, filter, pagination, and upload tests |
| Database schema drift | Medium | Temporary-database Alembic migration test |
| Read endpoint latency | Medium | Optional local Locust scenario; no performance claim |

## Testing pyramid

Many unit cases exercise pure calculations, Pydantic validation, and workbook parsing. A smaller API layer checks realistic request-to-database flows. A migration integration test checks the schema. UI tests cover user-visible flows with mocked HTTP responses; no full browser end-to-end suite is included. This mix gives fast feedback while preserving confidence where layers meet.

## Test data and isolation

`backend/tests/conftest.py` supplies a fresh SQLite schema and session for each test, overrides FastAPI's database dependency, and clears overrides afterward. Fixtures create users, auth headers, fictional product data, and real in-memory workbooks. Parametrization groups meaningful boundary families. The fake `CarbonPriceProvider` returns a controlled value to verify the optional-price path without any network call. A **fake** is a working local replacement; a **stub** supplies fixed answers; a **mock** additionally checks interactions. Here the fake provider and HTTP mocks each serve a distinct purpose.

Frontend tests intercept `fetch` and assert accessible, visible behavior. They do not inspect internal component state. Regular tests must work offline and in any order.

## Coverage and regression

The backend gate is 85% statement/branch coverage with `pytest-cov`; the measured local result should be read from a fresh run, not assumed from this document. Coverage is a signal, not a substitute for assertions about ownership, HTTP codes, and database effects. Vitest coverage is available via `npm run coverage`. CI runs all checks on push and pull request. A defect should first receive a reproducing test at the narrowest useful layer, then a fix, followed by the full affected suite.

## Performance and limitations

`backend/tests/performance/locustfile.py` exercises authenticated product listing and dashboard summary. It is an opt-in local smoke load with controlled credentials and request rates; no throughput threshold or load result is claimed. SQLite tests cannot prove PostgreSQL dialect correctness or concurrent transaction behavior. There is no browser end-to-end, accessibility audit, or official regulation validation.
