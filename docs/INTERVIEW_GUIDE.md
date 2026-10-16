# Interview guide

## Explain the project in 30 seconds

“CarbonTrack QA is my independent educational QA portfolio project. I built a FastAPI and PostgreSQL product portfolio with authentication, owner authorization, simplified Decimal emissions calculations, and validated Excel imports. I added isolated pytest API and unit tests, a React interface with Vitest interaction tests, Alembic migrations, Docker Compose, and CI. The data and formulas are fictional and are not an official CBAM implementation.”

## Explain the project in two minutes

“I built it to practice the mix of backend testing, frontend testing, and test infrastructure expected in a software engineering and QA automation internship. The backend has typed Pydantic contracts, SQLAlchemy models, a repository for filtering and pagination, and separate services for emissions and Excel parsing. Authentication uses hashed passwords and JWT; individual product access checks owner or admin. The Excel endpoint validates the file and each row, imports valid rows, and reports detailed errors for invalid ones. I kept all calculations educational: total is direct plus indirect emissions, intensity divides by quantity, and estimated cost multiplies total by a fictional price.

“For QA, I focused on risk: invalid quantities, decimal precision, duplicate rows, authorization, expired tokens, and HTTP status codes. pytest fixtures replace the database with a fresh SQLite schema per test, so tests cannot affect my development PostgreSQL database. An Alembic migration has its own temporary-database test. React Testing Library tests visible loading, empty, error, form, filter, pagination, and upload behavior with mocked HTTP responses. CI runs lint, format, tests, coverage, typecheck, and build. The next step would be a PostgreSQL CI integration job and browser end-to-end checks.”

## Technical questions and short answers

1. **Why use `Decimal`?** Binary floats can introduce rounding artifacts; decimal arithmetic suits money and measured values with defined precision.
2. **What does `Numeric(28,10)` mean?** Up to 28 total decimal digits, with 10 after the decimal point in the database column.
3. **Why reject quantity zero?** Intensity divides by quantity, so zero has no valid value in this simplified model.
4. **What are the formulas?** Total is direct plus indirect; intensity is total divided by quantity; estimated cost is total times price.
5. **Are these CBAM formulas?** No. They are explicitly simplified educational calculations.
6. **Why separate the emissions service?** It keeps math independently testable and routes focused on HTTP concerns.
7. **What does Pydantic validate?** Request shape, strings, numeric bounds, precision, password rules, and response contracts.
8. **Why use Argon2?** It is a password hashing algorithm designed to be expensive for attackers; plaintext passwords are never stored.
9. **What is in the JWT?** A user ID subject and expiry; the server signs and verifies it with a configured secret.
10. **Authentication versus authorization?** Authentication identifies the user; authorization decides whether that user may access a specific product.
11. **How is an expired token tested?** Create a token with a past expiry and call `/auth/me`; expect 401.
12. **Why scope list queries by owner?** It prevents one user's portfolio from leaking through listing or dashboard endpoints.
13. **Why does an admin still see only their own list?** This small example grants admin access to individual product operations only; list/summary stay owner scoped by design.
14. **Why return 409 for duplicates?** The request conflicts with an existing identity and cannot create another copy.
15. **Why return 422 for invalid fields?** The request is syntactically valid JSON but violates the API schema.
16. **What is a fixture?** pytest setup that supplies controlled dependencies/data, such as a fresh session or auth header.
17. **How are database tests isolated?** Each test creates and disposes its own in-memory SQLite engine and overrides `get_db`.
18. **Why not run routine tests on the developer database?** Tests must be repeatable and must never mutate personal data.
19. **What is a migration?** A versioned schema change; Alembic's initial revision creates users/products tables and indexes.
20. **What can SQLite tests miss?** PostgreSQL-specific SQL, numeric behavior, locking, and concurrent transaction behavior.
21. **Why parameterize tests?** A single behavior can be checked across meaningful boundary inputs without duplicating test structure.
22. **What is a fake provider?** A local implementation replacing a dependency, here returning a predictable carbon price.
23. **What does a mock assert?** Besides giving a response, it can verify that a call happened with expected arguments.
24. **Why use real in-memory `.xlsx` files in tests?** They exercise openpyxl parsing and workbook structure rather than only mocking a parser.
25. **How are partial imports represented?** Valid rows are inserted and invalid rows are reported with row and field; counts reconcile to the input.
26. **Why limit upload size and rows?** It bounds memory, parsing work, and request duration for this small service.
27. **Why use stable sorting?** An ID tie-breaker keeps paginated results deterministic when primary sort values match.
28. **What is the testing pyramid here?** Many fast unit tests, fewer API/integration tests, and focused UI interaction tests.
29. **Why test visible UI behavior?** It checks what a user can observe and is less brittle than inspecting internal state.
30. **Why use `findByRole` or `findByText`?** They wait for asynchronous rendering and encourage accessible markup.
31. **What does CI run?** Backend lint, format, pytest and coverage; frontend lint, TypeScript, Vitest, and production build.
32. **What does coverage miss?** It cannot prove the assertions are meaningful or that all important scenarios were chosen.
33. **What would you improve next?** Add PostgreSQL CI tests, browser end-to-end coverage, and a more robust production session design.
34. **How would you investigate a flaky test?** Reproduce it repeatedly, inspect shared state/timing, reduce the test to a stable user-observable assertion, and keep it isolated.

## Simple explanation in Spanish

Puedo presentar el proyecto como una muestra de habilidades de ingeniería y QA: construí una API, una interfaz y pruebas que verifican reglas, errores y permisos. La parte más importante para explicar es cómo aislé la base de datos de pruebas y por qué probé casos límite de números y Excel. Debo decir claramente que los datos y las fórmulas son ficticios y educativos.
