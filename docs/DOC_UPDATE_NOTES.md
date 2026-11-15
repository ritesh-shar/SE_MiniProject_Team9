# Documentation Update Specifications (SRS, SAD, and Test Plan)

**Document Reference:** `docs/DOC_UPDATE_NOTES.md`  
**Purpose:** Precise section-by-section update guidance for IEEE SRS, SAD, and Test Plan documents reflecting Sprint 2 deliverables.

---

## 1. Software Requirements Specification (SRS) Updates

### Section 3.2: System Features & Functional Requirements
- **Feature BBMS-F-031 (Hospital Blood Requisition):**
  - *Location:* Append subsection 3.2.5 "Hospital Requisition Management".
  - *Text to add:*  
    > "3.2.5 Hospital Requisition Submission: Authorized hospital accounts (`hospital` role) shall submit formal requisitions via `POST /api/requests` specifying blood group, component type (Whole Blood, Red Cells, Platelets, Plasma), requested quantity in units, and urgency level (Normal, Urgent, Critical). Each requisition is assigned a unique tracking identifier and initialized with status `pending`."
- **Feature BBMS-F-032 (Stock Availability Validation):**
  - *Text to add:*  
    > "3.2.6 Inventory Stock Pre-Validation: The system shall validate hospital requests against on-hand available stock in `BloodStock`. Any requisition exceeding current stock shall be rejected with HTTP 400 Bad Request and an explicit diagnostic error message indicating requested vs. available quantities."
- **Feature BBMS-F-040 (Staff Requisition Review):**
  - *Text to add:*  
    > "3.2.7 Staff Requisition Review: Blood bank staff or administrators shall review pending requisitions via `POST /api/requests/{id}/review` to approve or reject with decision notes. The status becomes visible to the requesting hospital."
- **Feature BBMS-F-041 (Inventory Decrement on Issuance):**
  - *Text to add:*  
    > "3.2.8 Inventory Stock Decrement: When staff issues an approved request via `POST /api/requests/{id}/issue`, the system shall atomically decrement inventory units using `select_for_update()` row-level locks. If requested units exceed stock at time of issuance, the transaction aborts with a zero-floor exception."
- **Feature BBMS-F-042 (Dispatch Chain-of-Custody Manifest):**
  - *Text to add:*  
    > "3.2.9 Dispatch Record Tracking: Upon successful issuance, a decoupled signal creates an immutable `DispatchRecord` containing timestamp, issuing staff ID, recipient hospital ID, and manifest details, retrievable via `GET /api/dispatch/{request_id}`."
- **Feature BBMS-F-003 (Account Lockout Policy):**
  - *Location:* Update Section 4.1 "Security Requirements - Authentication".
  - *Text to add:*  
    > "4.1.2 Account Lockout: To mitigate brute-force password attacks, the authentication backend shall track consecutive failed login attempts. On the 5th consecutive failure, the user account is locked (`is_locked = True`). The account remains locked indefinitely until an administrator explicitly unlocks it via the Django administration interface. There is no automatic expiration timer."
- **Feature BBMS-F-021 & BBMS-F-022 (Inventory Alerts):**
  - *Location:* Section 3.2.10 "Inventory Alerts and Monitoring".
  - *Text to add:*  
    > "3.2.10.1 Expiry Surveillance: Blood unit expiration dates are dynamically derived from donation date plus biological shelf life: Whole Blood (35 days), Red Cells (42 days), Platelets (5 days), Plasma (365 days). Units expiring within 5 days are surfaced at `GET /api/inventory/alerts/expiry`."  
    > "3.2.10.2 Low-Stock Thresholds: Configurable minimum thresholds per blood group (`StockThreshold` model) trigger low-stock alerts at `GET /api/inventory/alerts/low-stock` whenever total on-hand units fall below threshold."
- **Feature BBMS-F-050, BBMS-F-051, BBMS-F-052 (Admin Operations & Reporting):**
  - *Location:* Section 3.2.11 "Administrative Operations".
  - *Text to add:*  
    > "3.2.11.1 Operations Dashboard: Aggregates real-time inventory counts, pending request queues, and recent donations (`GET /api/admin/dashboard`)."  
    > "3.2.11.2 Donor Notification Microservice: An asynchronous Node.js Express service (`notification-service/`) handles donor reminder notifications. Django queries donors eligible for donation (90+ days since last donation) and dispatches reminders non-blockingly via HTTP."  
    > "3.2.11.3 Data Export: Administrative exports for donations and inventory stock are available in CSV and PDF formats (ReportLab), matching on-screen tables."

### Section 4.2 & 4.3: Non-Functional Requirements
- **BBMS-SR-004 / BBMS-NF-005 (Audit Trail & 3-Year Retention):**  
  > "All authentication events (success, failure, lockout), administrative changes, and inventory movements are logged in an immutable `AuditLog` table. Management purge operations strictly enforce a 3-year statutory medical retention period, refusing deletion of younger records."
- **BBMS-SR-001 (Transport Layer Security):**  
  > "TLS 1.2+ is mandatory in production deployments via `SECURE_SSL_REDIRECT=True` and reverse-proxy HTTPS termination."
- **BBMS-NF-001 & BBMS-NF-004 (Performance & Concurrency):**  
  > "95% of search and dashboard queries respond within 2.0 s ($p_{95} \le 20\text{ ms}$ verified). The system sustains 200 concurrent user sessions with zero packet drops."
- **BBMS-NF-003 (Usability):**  
  > "Staff record incoming donations in 3 clicks or fewer from the dashboard."

---

## 2. Software Architecture and Design (SAD) Updates

### Section 2: Architectural Overview & Component Decomposition
- **New Microservice:** Add the Node.js Donor Notification Microservice (`notification-service/`) to the architectural diagram:
  ```text
  [Django REST Backend] ──(HTTP JSON / Urllib)──► [Node.js Express (Port 3000)]
                                                            │
                                                     [Outbox Log]
  ```
- **New Django Applications:**
  - `bloodrequests`: Requisition lifecycle (`BloodRequest` model, submit, review, issue, dashboard, exports).
  - `audit`: Security event logging and immutable audit trail (`AuditLog` model).
  - `dispatch`: Requisition fulfillment manifests (`DispatchRecord` model, decoupled post-save signal, audit hooks).

### Section 3.7: Concurrency & Transaction Management
- Update row-level locking table to include `decrease_stock`:
  - `decrease_stock(blood_group, component, quantity)` executes inside `transaction.atomic()` with `BloodStock.objects.select_for_update()`.
  - Ensures atomic decrement with zero lower-bound validation.

---

## 3. Software Test Plan (STP) Updates

Update the Test Plan matrix to record all executed acceptance tests for Sprint 2:

| Test ID | Requirement | Target Module / Endpoint | Verified Behavior | Status |
|---|---|---|---|:---:|
| **TC-Req-02** | BBMS-F-031 | `POST /api/requests` | Hospital submits valid requisition; unique ID and pending status assigned. | **PASS** |
| **TC-Req-03** | BBMS-F-032 | `POST /api/requests` | Over-stock requests rejected with 400 Bad Request and error message. | **PASS** |
| **TC-Iss-01** | BBMS-F-040 | `POST /api/requests/{id}/review` | Staff approves or rejects pending request with reviewer notes. | **PASS** |
| **TC-Iss-02** | BBMS-F-041 | `POST /api/requests/{id}/issue` | Approved request issued; inventory stock decremented atomically; zero-floor guard enforced. | **PASS** |
| **TC-Iss-03** | BBMS-F-042 | `GET /api/dispatch/{request_id}` | Dispatch record created via signal and retrievable by request ID. | **PASS** |
| **TC-Auth-02** | BBMS-F-003 | `POST /api/auth/login` | 4 failures allow login; 5th failure locks account; admin unlocks account. | **PASS** |
| **TC-Sec-04** | BBMS-SR-004 | `GET /api/audit` | Login successes, failures, and admin actions logged in audit table. | **PASS** |
| **TC-Ops-01** | BBMS-NF-005 | `purge_audit_logs` | Inventory/request changes logged; purge command refuses records under 3 years old. | **PASS** |
| **TC-Inv-02** | BBMS-F-021 | `GET /api/inventory/alerts/expiry` | Units expiring within 5 days flagged based on component shelf life. | **PASS** |
| **TC-Inv-03** | BBMS-F-022 | `GET /api/inventory/alerts/low-stock`| Blood groups below configurable threshold flagged in red. | **PASS** |
| **TC-Adm-01** | BBMS-F-050 | `GET /api/admin/dashboard` | Live summary for stock, pending requests, and recent donations. | **PASS** |
| **TC-Adm-02** | BBMS-F-051 | `POST /api/requests/reminders/send` | Dispatches reminders to eligible donors (90+ days) via Node.js service non-blockingly. | **PASS** |
| **TC-Adm-03** | BBMS-F-052 | `GET /api/requests/export/*` | Donations and stock exported as CSV and PDF matching on-screen tables. | **PASS** |
| **TC-Sec-01** | BBMS-SR-001 | `SecurityMiddleware` | `SECURE_SSL_REDIRECT` forces HTTPS redirection. | **PASS** |
| **TC-Perf-01** | BBMS-NF-001 | 100 queries | 95th-percentile response latency measured under 20 ms (< 2.0 s threshold). | **PASS** |
| **TC-Perf-02** | BBMS-NF-004 | `scripts/load_test.py` | 200 concurrent users sustained with 0% error rate. | **PASS** |
| **TC-UX-01** | BBMS-NF-003 | `dashboard.html` $\rightarrow$ `donation_form.html` | Staff records donation in $\le 3$ clicks. | **PASS** |
| **TC-Uptime-01**| BBMS-NF-002 | `GET /api/health` | Health probe validates DB connectivity. | **PASS** |
