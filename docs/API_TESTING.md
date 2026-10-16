# API testing

The API is rooted at `/api/v1`; `/health` is outside that prefix. Swagger at `/docs` exposes request and response schemas. Authenticate with `POST /auth/login`, then send `Authorization: Bearer <token>`. The suite creates its own users and avoids a shared developer database.

## Contract checks

| Operation | Expected path and status | Negative cases |
| --- | --- | --- |
| Register | `POST /auth/register` → 201 | 409 duplicate; 422 invalid email/password |
| Login | `POST /auth/login` → 200 | 401 unknown/wrong credentials |
| Current user | `GET /auth/me` → 200 | 401 missing/invalid/expired token |
| Products | `POST /products` → 201, `GET` → 200 | 409 duplicate, 422 invalid input |
| Product detail | `GET/PUT /products/{id}` → 200 | 403 other owner, 404 absent |
| Delete | `DELETE /products/{id}` → 204 | 403 other owner, 404 absent |
| Import | `POST /imports/products` → 200 | 400 wrong extension/corrupt, 413 oversize, 422 headers/empty |
| Summary | `GET /dashboard/summary` → 200 | 401 missing token |

The envelope for expected errors is `{"error":{"code":"...","message":"..."}}`; request validation also includes `issues`. Tests assert status, semantic content, and database effects where meaningful. The product list checks page metadata, filters, minimum/maximum emissions, sorting, and owner scope. The dashboard checks aggregate numbers and empty results.

## Example

```sh
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.test","password":"DemoPass123"}'
```

Use the returned token with `curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/products`. The demo account exists only after running the optional seed command. The backend suite tests the same flow with FastAPI TestClient and an isolated SQLite session.
