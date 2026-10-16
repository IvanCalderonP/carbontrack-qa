# Final QA review — 14 October 2026

## Findings fixed during the build-test-review cycle

- A malformed ZIP with an `.xlsx` suffix raised an uncaught parser exception. It now returns a sanitized 400 error, and the workbook closes after parsing.
- Decimal response strings carried database scale; tests now compare numeric values instead of brittle serialization formatting.
- A frontend filter test assumed one request per user action. It now responds to each keystroke, matching actual interaction behavior.
- A stored expired token left the app on “Checking your session…”. A new session test reproduced it; the app now clears both token and loading state.
- Unknown routes returned a different 404 body. A generic Starlette HTTP handler now uses the same error envelope, and unexpected 500 responses hide internal details.
- npm audit found advisories in older React Router/Vitest dependencies. Both were upgraded; the final audit reports zero vulnerabilities.

## Final checks

| Check | Result |
| --- | --- |
| Backend Ruff lint and format | Passed |
| Backend pytest | 67 passed |
| Backend coverage | 97.14% total; 85% gate passed |
| Frontend ESLint and TypeScript | Passed |
| Frontend Vitest | 19 passed |
| Frontend coverage | 97.26% statements; 82.81% branches |
| Frontend production build | Passed |
| Fresh `npm ci` and npm audit | Passed; zero audit advisories |
| Compose and GitHub Actions YAML | Parsed; expected services/jobs present |
| Live UI | API health and Vite responded; real dashboard, product, and import screenshots captured |
| Docker containers | Not run: Docker is not installed on this machine |

## Remaining limitations

One upstream FastAPI/Starlette deprecation warning appears in pytest; it does not fail tests. PostgreSQL behavior and Docker container startup were not exercised here because Docker/PostgreSQL are unavailable. Routine tests use isolated SQLite, and the migration was exercised on a temporary SQLite database. The educational formulas have no regulatory validity. No known critical application or test failure remains from this review.
