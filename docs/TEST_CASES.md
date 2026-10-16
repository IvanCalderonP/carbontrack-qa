# Manual test cases

These complement automation. Use a local seeded account unless a case says otherwise. "Own product" means a product created by the signed-in user. Each case is independent; reset demo data as needed.

| ID | Feature | Scenario | Preconditions | Steps | Expected result | Priority | Type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-01 | Health | Service responds | API running | GET `/health` | 200 with `status: ok` | High | Positive |
| TC-02 | Auth | Register valid account | New email | POST valid email/password | 201, no password in response | High | Positive |
| TC-03 | Auth | Duplicate registration | Existing email | Register same email again | 409 EMAIL_EXISTS | High | Negative |
| TC-04 | Auth | Invalid email | None | Register `bad-email` | 422 validation error | High | Negative |
| TC-05 | Auth | Weak password | None | Register short password | 422 validation error | High | Boundary |
| TC-06 | Auth | Correct login | Existing user | Sign in with valid credentials | Token returned and dashboard shown | High | Positive |
| TC-07 | Auth | Wrong password | Existing user | Enter wrong password | 401 and clear UI error | High | Negative |
| TC-08 | Auth | Missing token | None | GET `/auth/me` without header | 401 | High | Security |
| TC-09 | Auth | Expired token | Expired token | GET `/auth/me` | 401 | High | Security |
| TC-10 | Auth | Sign out | Signed in | Click Sign out | Login screen shown; token removed | Medium | Usability |
| TC-11 | Product | Create valid record | Signed in | Complete product form and save | 201; row appears | High | Positive |
| TC-12 | Product | Zero quantity | Signed in | POST quantity 0 | 422; no row created | High | Boundary |
| TC-13 | Product | Negative emissions | Signed in | POST negative direct emissions | 422; no row created | High | Boundary |
| TC-14 | Product | Invalid CN code | Signed in | POST letters in CN code | 422 | Medium | Negative |
| TC-15 | Product | Duplicate identity | Own product exists | POST same name/code/country | 409; count unchanged | High | Negative |
| TC-16 | Product | Read missing ID | Signed in | GET nonexistent ID | 404 PRODUCT_NOT_FOUND | Medium | Negative |
| TC-17 | Product | Update record | Own product exists | PUT changed name | 200; subsequent GET shows change | High | Positive |
| TC-18 | Product | Delete record | Own product exists | DELETE ID | 204; GET returns 404 | High | Positive |
| TC-19 | Authorization | Other owner reads | Two users; one product | Other user GETs ID | 403 | High | Security |
| TC-20 | Authorization | Other owner deletes | Two users; one product | Other user DELETEs ID | 403; record remains | High | Security |
| TC-21 | Authorization | Admin deletes | Admin and other user's product | Admin DELETEs ID | 204 | Medium | Security |
| TC-22 | List | Pagination | More than 8 records | Open Products; click Next | Next page, stable row set and metadata | Medium | Positive |
| TC-23 | List | Search and country | Several records | Enter name and country | Matching rows only | Medium | Positive |
| TC-24 | List | Invalid range | Signed in | min emissions > max | 400 INVALID_RANGE | Medium | Negative |
| TC-25 | Dashboard | Empty portfolio | New user | Open dashboard | Empty message and zero totals | Medium | Usability |
| TC-26 | Dashboard | Correct sums | Known own products | Open dashboard | Count/emissions/cost match manual arithmetic | High | Positive |
| TC-27 | Excel | Valid workbook | Signed in | Upload `valid_products.xlsx` | All rows imported; no errors | High | Positive |
| TC-28 | Excel | Mixed workbook | Signed in | Upload `invalid_products.xlsx` | Valid rows imported; bad rows show row/field errors | High | Negative |
| TC-29 | Excel | Wrong extension | Signed in | Upload `.csv` | UI/API rejects file | Medium | Negative |
| TC-30 | Excel | Corrupted workbook | Signed in | Upload broken `.xlsx` | 400; no records imported | High | Security |
| TC-31 | Excel | Extra header | Signed in | Add ninth column and upload | 422 INVALID_HEADERS | Medium | Negative |
| TC-32 | Excel | Oversize file | Signed in | Upload over 2 MiB | 413; no records imported | High | Boundary |
| TC-33 | UI | Narrow viewport | App running | Resize to mobile width; visit all pages | Navigation, forms, and tables remain usable | Medium | Usability |
| TC-34 | UI | API unavailable | Backend stopped | Attempt login or open protected page | Clear error state; no misleading success | Medium | Negative |
