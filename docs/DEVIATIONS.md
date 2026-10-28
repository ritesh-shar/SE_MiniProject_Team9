# Architecture and Specification Deviations (Sprint 1)

This document records all deviations from the initial Software Architecture and Design (SAD), Software Requirements Specification (SRS), and Software Test Plan (STP) for the Blood Bank Management System (Team 9).

| # | Item / Specification | Original SAD / SRS / STP Baseline | Sprint 1 Implementation | Reason & Rationale |
|---|----------------------|-----------------------------------|-------------------------|---------------------|
| 1 | **Database Engine (Local Dev)** | PostgreSQL / MySQL specified as primary DB | SQLite default for local development with environment variable switch (`DB_ENGINE`) | Required by PROMPT.md for zero-configuration local setup; production deployments remain driven by `.env` for PostgreSQL. |
| 2 | **Password Hashing Algorithm** | SRS Section 4.1 listed bcrypt as candidate | Django default PBKDF2 with SHA-256 (`PBKDF2PasswordHasher`) | PROMPT.md explicitly approved Django default PBKDF2 hashing as sufficient for BBMS-SR-003. Avoids compiled C dependencies on student Windows machines. |
| 3 | **Account Lockout (BBMS-F-003)** | SRS Section 4.1 specifies 5 failed attempts lock | Out of scope for Sprint 1 | PROMPT.md defines Sprint 1 scope strictly as F-001, F-002, SR-003, SR-005, SR-002, F-010, F-011, F-012, F-020, F-030, and SETUP-001. |
| 4 | **Notification Service** | Node.js asynchronous notification worker | Deferred to Sprint 2 | Explicitly marked as Sprint 2 scope in PROMPT.md hard rule #2. |
| 5 | **Hospital Blood Request / Issue Tracking** | BBMS-F-031, F-040, F-041, F-042 | Deferred to Sprint 2 | Core request dispatch workflow is scheduled for Sprint 2. Sprint 1 provides blood search (F-030). |
| 6 | **Frontend Architecture** | Generic responsive web client | Pure vanilla JavaScript (HTML5/CSS3/Fetch API) without framework build tools | PROMPT.md specified plain HTML/CSS/JS in `frontend/` so students can explain every line without React/Webpack complexity. |
| 7 | **TLS 1.2+ Transport Security** | Mandatory in SAD Section 3.6 | HTTP in local dev (`127.0.0.1:8000`) | TLS/SSL termination is a reverse-proxy/cloud infrastructure concern for deployment; local student testing runs HTTP. |
| 8 | **Blood Unit Tracking via Barcode/QR** | SRS Section 3.2 mentions optional barcode scanners | Direct unit counting by blood group & component | Hardware integration is outside the software prototype scope for Sprint 1. |
