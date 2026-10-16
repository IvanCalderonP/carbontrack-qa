# Test plan

| Item | Plan |
| --- | --- |
| Objective | Verify the educational portfolio's behavior and make failures easy to diagnose. |
| Features under test | Auth, ownership, product CRUD/search/pagination, simplified emissions, Excel import, dashboard, UI feedback, migration. |
| Features outside scope | Official CBAM compliance, external price feeds, production-scale load, third-party identity. |
| Environment | Python 3.11+ and Node 22+; isolated SQLite for routine API tests; optional PostgreSQL via Compose. |
| Entry criteria | Dependencies installed, a runnable API and frontend build, documented request contracts. |
| Exit criteria | Backend and frontend suites pass; lint, format, typecheck, and build pass; backend coverage meets 85%; no known critical issue. |
| Test types | Unit, API/integration, migration, UI interaction, optional smoke load, manual exploratory cases. |
| Deliverables | pytest/Vitest suites, CI workflow, coverage output, sample workbooks, manual case inventory. |

## Execution order

Run backend unit tests first, then the full API/migration suite and coverage. Run frontend lint, typecheck, Vitest, and build. Review the CI commands against local commands. If Docker is available, build and run Compose, apply the migration, use the seed, and verify UI and `/health`. Record environment-dependent checks honestly.

## Defect handling

For a failure, record the input, expected and actual results, status/stack trace, and the smallest reproduction. Prioritize data corruption and authorization defects first, then broken core flows, then presentation issues. Add a regression test before or alongside the fix. Rerun the affected suite and final gates.

## Main risks and mitigations

- Decimal precision: service tests with exact `Decimal` expectations; PostgreSQL uses `Numeric(28,10)`.
- Input shape: Pydantic constraints and invalid-file cases.
- Isolation: one test database per case, no configured developer database connection.
- Flaky UI timing: use role-based queries and `findBy`/`waitFor` for asynchronous behavior.
- Environment drift: lock frontend dependencies and run the same scripts in CI.
