# BBMS 60-Second Video Demo Script (Team 9)

This script guides the team through recording the 1-minute video demonstration required for the evaluation.

---

## Pre-Demo Setup (Do this before pressing record)

1. Ensure the development server is running:
   ```bash
   python manage.py migrate
   python manage.py seed_demo
   python manage.py runserver
   ```
2. Open modern browser to: `file:///path/to/frontend/index.html` (or serve via simple HTTP server).
3. Have your browser split-screened or ready with two tabs:
   - Tab A: `index.html` (Login & Registration)
   - Tab B: API tool / Curl terminal (optional, or stick purely to the UI)

---

## 60-Second Video Script Timeline

### 00:00 - 00:10 | 1. Introduction & Donor Self-Registration (BBMS-F-001)
* **Action:** Click "Register as Donor". Fill form:
  - Username: `alice_donor`
  - Email: `alice@example.com`
  - Password: `Password123!`
  - Blood Group: `O+`
  - Phone: `+91-9876543210`
  - Click **Register**.
* **Spoken commentary:** *"Welcome to Blood Bank Management System, Team 9. We start by registering a new donor profile with blood group and contact information."*

### 00:10 - 00:20 | 2. Authentication & Donor Dashboard (BBMS-F-002, SR-003, SR-005)
* **Action:** Log in with `alice_donor` / `Password123!`.
* **Visual:** Dashboard shows "Welcome, alice_donor [DONOR]" with empty donation history.
* **Spoken commentary:** *"The donor logs in via JWT authentication with salted PBKDF2 hashing. Notice that donors can view only their personal history, and cannot view or alter blood inventory."*

### 00:20 - 00:35 | 3. Staff Login & Record Donation with Real-Time Stock Increment (BBMS-F-010, F-012, F-020)
* **Action:** Log out and log in as `demo_staff` / `StaffPassword123!`.
  - Click **"Record Blood Donation"**.
  - Fill: Donor ID: `1`, Blood Group: `O+`, Component: `whole_blood`, Quantity: `2`, Date: today.
  - Click **Submit Donation**.
  - Note success alert showing: *"Updated Inventory Stock: 17 units"*.
  - Click **"View Blood Stock"**.
  - Show `O+ Whole Blood` at 17 units, and point out colour-coded low stock badges (e.g. `O-` or `AB-` highlighted in red for <= 3 units).
* **Spoken commentary:** *"Next, blood bank staff record a new whole blood donation for donor #1. An atomic transaction locks the row and increments stock in real time. Our stock board highlights units in red when stock falls below 3 units."*

### 00:35 - 00:45 | 4. Search Available Blood Units (BBMS-F-030)
* **Action:** Click **"Search Blood Stock"**.
  - Select Blood Group: `O+`, Component: `whole_blood`.
  - Click **Search Units**.
  - Show instant matching result: `O+ - Whole Blood: 17 units`.
* **Spoken commentary:** *"Hospitals and staff can filter units instantly by group and component to fulfill critical requests."*

### 00:45 - 01:00 | 5. Blocked Unauthorized Action & 90-Day Eligibility Rejection (BBMS-SR-002, BBMS-F-011)
* **Action:**
  - Attempt to submit a second donation for Donor ID `1` on today's date:
  - Error alert pops up: **"Donor is not eligible to donate. Only 0 days since last donation. Minimum 90 days required."**
  - Briefly demonstrate RBAC: Donor token attempting to access `/api/inventory` is rejected with `403 Forbidden`.
* **Spoken commentary:** *"Finally, safety and security: if staff try to record another donation for the same donor within 90 days, the system blocks it. Role-based access control strictly enforces that donors cannot view stock or unauthorized endpoints. All 18 automated tests pass."*

---

## Demo Check-Off Checklist

- [ ] Donor registered (profile created in DB)
- [ ] JWT tokens issued upon login
- [ ] Donation recorded with valid donor ID
- [ ] Stock count updated atomically
- [ ] Low-stock units displayed in red
- [ ] Blood search filters accurately
- [ ] 90-day eligibility rule actively blocks donation
- [ ] RBAC blocks unauthorized role access
