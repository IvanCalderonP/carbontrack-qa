# Application notes — edit before use

Replace every bracketed field with truthful personal information. Do not claim employment experience from this project alone.

## Personal fields

- Name: [YOUR NAME]
- University: [YOUR UNIVERSITY]
- Degree: [YOUR DEGREE]
- Current semester: [YOUR CURRENT SEMESTER]
- Python experience: [YOUR PYTHON EXPERIENCE]
- Availability: [YOUR AVAILABILITY]

## Short GitHub description

Independent QA automation portfolio: FastAPI, PostgreSQL, React, pytest, Vitest, and CI for a fictional carbon accounting product portfolio with Excel imports and educational emissions calculations.

## English application introduction

I am [YOUR NAME], a [YOUR CURRENT SEMESTER] student in [YOUR DEGREE] at [YOUR UNIVERSITY]. I am interested in the Software Engineer & QA Automation internship at GeoKapti B.V. To demonstrate my current skills, I built CarbonTrack QA, an independent educational portfolio project focused on API testing, validation, Excel ingestion, simplified emissions calculations, and React interaction testing. I would welcome the chance to learn from your team and contribute careful, well-documented test automation. My availability is [YOUR AVAILABILITY].

## Short cover letter paragraph

The internship's emphasis on backend QA and practical software engineering matches the work I explored in CarbonTrack QA. I implemented a typed Python API, wrote isolated pytest unit and API tests for business rules and edge cases, and tested a React UI with Vitest and React Testing Library. I also added migrations and CI to make the project repeatable. This is my own educational sample using fictional data and simplified formulas, not an official CBAM or GeoKapti implementation.

## CV bullets — use after understanding the code

- Built an independent educational QA portfolio using FastAPI, SQLAlchemy, PostgreSQL, React, and TypeScript.
- Automated unit, API, migration, and UI interaction tests with pytest, Vitest, and React Testing Library.
- Validated `.xlsx` product imports with row-level errors, duplicate checks, size limits, and fictional sample workbooks.
- Implemented owner/admin authorization, JWT authentication, product CRUD, pagination, filters, and dashboard aggregation.
- Added Decimal-based educational emissions calculations, a replaceable price provider, Alembic migration, Docker Compose, and GitHub Actions CI.

## Code sample shortlist

| File | Why show it |
| --- | --- |
| `backend/app/services/emissions.py` | Small, readable business rules with explicit boundary behavior. |
| `backend/tests/unit/test_emissions.py` | Exact Decimal expectations and useful parametrization. |
| `backend/app/services/excel_import.py` | Parsing, row-level validation, and error reporting. |
| `backend/tests/unit/test_excel_import.py` | Real workbooks and negative cases. |
| `backend/tests/conftest.py` | Test isolation and dependency replacement. |
| `backend/tests/api/test_products.py` | CRUD, ownership, filtering, and status assertions. |
| `backend/tests/integration/test_migrations.py` | Migration check in a temporary database. |
| `frontend/tests/Products.test.tsx` | User interactions with mocked HTTP. |
| `.github/workflows/ci.yml` | Repeatable quality gates. |

## Presenting it to GeoKapti

Open with the independence disclaimer and the project's testing purpose. In a short walkthrough, run a parameterized emissions test, show a mixed Excel result, explain a cross-owner 403 case, and point to the CI checks. Be ready to explain tradeoffs: SQLite test speed versus PostgreSQL fidelity, local storage as a demo session choice, and educational formulas versus actual regulatory methodology. Show that you understand the code and can discuss improvements rather than presenting it as production software.
