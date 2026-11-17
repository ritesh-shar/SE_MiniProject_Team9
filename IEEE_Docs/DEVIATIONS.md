# Deviations from the SRS, SAD and Test Plan (Sprint 1 and Sprint 2)

This register lists every difference between the submitted documents (version 1.0) and the system as built at the end of Sprint 2. The updated documents (version 1.1) contain the same items.

| # | Item | Baseline in the documents | As built | Reason |
|---|------|---------------------------|----------|--------|
| D1 | Database for local development | PostgreSQL or MySQL (SRS 2.4, SAD 3.6) | SQLite by default; PostgreSQL or MySQL selected with the DB_ENGINE environment variable | Zero-setup development and fast in-memory test runs |
| D2 | Frontend technology | JavaScript-based responsive web client (SAD 3.6) | Plain HTML, CSS and vanilla JavaScript in frontend/, served by Django in debug mode, no framework | Simple enough for every team member to explain |
| D3 | Blood request API contract | SAD 4.3: request body carries hospitalId; insufficient stock returns HTTP 402 | Hospital is taken from the authenticated user; insufficient stock returns HTTP 400 with a JSON error and a message with requested and available units | Prevents a client from claiming another hospital; 402 is a payment status code |
| D4 | Expiry tracking | Units tracked by group, component and expiry (SRS 4.3) | Expiry computed from donation date plus component shelf life: whole blood 35 days, red cells 42, platelets 5, plasma 365 | Avoids storing a separate expiry per unit in this release |
| D5 | Search by location | SRS 2.2 lists search by group, location and component | Search by blood group and component only, as required by BBMS-F-030 | Single blood bank; location not needed for F-030 |
| D6 | Barcode/QR scanner | Optional scanner (SRS 3.2) | Not implemented; units counted by blood group and component | Optional hardware, outside the software prototype |
| D7 | Email/SMS notifications | Email or SMS gateway (SRS 3.3, F-051) | Node.js service writes messages to a mock outbox; no live gateway | No external gateway account; delivery is outside the test scope |
| D8 | TLS in local development | TLS 1.2+ for all connections (SR-001) | Enforced by settings and a reverse proxy in production; local development over HTTP | The development server has no TLS support |
| D9 | Uptime verification (NF-002) | Monthly uptime monitoring | Health endpoint GET /api/health and design review; monthly uptime not measured | The project timeline is shorter than a month |
| D10 | Performance measurement (NF-001, NF-004) | Load testing with JMeter | Timed test of 100 requests and a Python threaded script for 200 users, on one machine with SQLite | Simple, repeatable and runs in CI and on laptops |
| D11 | Test tools | Selenium, JMeter, Jira (Test Plan 6) | Django test runner, coverage.py, node:test, Playwright for browser checks, GitHub Actions, GitHub Issues | Tools matched to the stack and the course repository |
| D12 | Fuzzing and penetration testing | Planned in Test Plan 5.1 | Not executed; input validation covered by API tests; planned as future work | Time limit of the sprints |
| D13 | API rate limiting | Rate limiting on API endpoints (SAD 3.9, STRIDE) | Not implemented; account lockout limits password guessing on login | Out of scope for this release |

## Items that match the documents (not deviations)

- **Account lockout (BBMS-F-003):** the account is locked after 5 consecutive failures and stays locked until an administrator unlocks it, as the SRS requires.
- **Password hashing (BBMS-SR-003):** the SRS allows PBKDF2 or bcrypt (Section 5.1.2), so PBKDF2 with SHA-256 follows the SRS.
- **Notification service (BBMS-F-051):** the SAD already specifies a Node.js notification service; only the live gateway is replaced by a mock outbox (D7).
- **Request, review, issue and dispatch features (BBMS-F-031, F-040, F-041, F-042):** implemented as specified; the only change is the API contract in D3.

## Defects found by testing and fixed

- D-01: Registration failed when the browser held an old login token. Public endpoints now ignore Authorization headers.
- D-02: The audit log page returned 404 because the frontend called /api/audit without a trailing slash. A slash-less route and 4 tests were added.
