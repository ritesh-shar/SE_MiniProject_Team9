# Architecture and Specification Deviations (Sprint 1 & Sprint 2)

This document records all deviations from the initial Software Architecture and Design (SAD), Software Requirements Specification (SRS), and Software Test Plan (STP) for the Blood Bank Management System (Team 9).

| # | Item / Specification | Original SAD / SRS / STP Baseline | Sprint Implementation | Reason & Rationale |
|---|----------------------|-----------------------------------|-----------------------|---------------------|
| 1 | **Database Engine (Local Dev)** | PostgreSQL / MySQL specified as primary DB | SQLite default for local development with environment variable switch (`DB_ENGINE`) | Required for zero-configuration local setup; production deployments remain driven by `.env` for PostgreSQL. |
| 2 | **Password Hashing Algorithm** | SRS Section 4.1 listed bcrypt as candidate | Django default PBKDF2 with SHA-256 (`PBKDF2PasswordHasher`) | Approved PBKDF2 hashing for BBMS-SR-003. Avoids compiled C dependencies on student Windows machines. |
| 3 | **Account Lockout (BBMS-F-003)** | SRS Section 4.1 specifies 5 failed attempts lock | Implemented in Sprint 2: Permanent lock on 5 failures until admin unlock (no auto-expiry timer) | Adheres strictly to IEEE SRS Section 4.1 requirement that only an administrator can unlock the account. |
| 4 | **Notification Service (BBMS-F-051)** | Node.js asynchronous notification worker | Implemented in Sprint 2: Express microservice on port 3000 with mock outbox file | Lightweight standalone microservice with non-blocking `urllib` integration from Django; avoids heavy message broker (RabbitMQ/Kafka) setup on student laptops. |
| 5 | **Hospital Blood Request / Issue Tracking** | BBMS-F-031, F-040, F-041, F-042 | Implemented in Sprint 2: Endpoints at `/api/requests`, `/api/requests/<id>/review`, `/api/requests/<id>/issue`, `/api/dispatch/<id>` | Full request requisition and dispatch pipeline delivered in Sprint 2. |
| 6 | **Frontend Architecture** | Generic responsive web client | Pure vanilla JavaScript (HTML5/CSS3/Fetch API) without framework build tools | Plain HTML/CSS/JS in `frontend/` so students can explain every line without React/Webpack complexity. |
| 7 | **TLS 1.2+ Transport Security (BBMS-SR-001)** | Mandatory in SAD Section 3.6 | Implemented in Sprint 2: Env-driven (`DJANGO_SECURE_SSL_REDIRECT`), documented in `docs/TLS.md`, verified via test | HTTP permitted in local development (`127.0.0.1:8000`); TLS enforced via reverse proxy and env flags in production. |
| 8 | **Blood Unit Tracking via Barcode/QR** | SRS Section 3.2 mentions optional barcode scanners | Direct unit counting by blood group & component | Hardware integration is outside software prototype scope. |
| 9 | **Biological Expiry Calculation (BBMS-F-021)** | Static expiry date field | Computed dynamically from donation date plus component shelf life table | Prevents redundant database schema changes; uses standard hematological shelf lives: Whole Blood (35d), Red Cells (42d), Platelets (5d), Plasma (365d). |

