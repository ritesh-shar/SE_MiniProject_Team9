# BBMS Sprint 2 Demo Walkthrough Script (2-Minute Video)

**Team 9:** Ritesh Kumar Sharma (Lead/Accounts/Donations), Reyansh (Security/Audit/Reports), Ritesh Babu Reddy (Search/Dispatch/Alerts), Rithish P M (Architecture/Requests/CI)  
**Total Target Duration:** 2 Minutes (120 Seconds)

---

## Demo Preparation Checklist (Before Recording)
```bash
# 1. Reset database and run migrations
python manage.py migrate

# 2. Seed Sprint 2 demo data
python manage.py seed_demo_s2

# 3. Start Node.js notification service (Terminal 1)
cd notification-service && npm start

# 4. Start Django development server (Terminal 2)
python manage.py runserver
```

---

## Timed Video Script

### [0:00 - 0:15] Introduction & Sprint 2 Overview
- **Speaker:** "Hello everyone. Today Team 9 presents Sprint 2 of the Blood Bank Management System. In Sprint 2, we built the hospital requisition pipeline, staff review and atomic stock decrement, account security lockout, audit trails, real-time alerts, and automated donor notification microservices."

### [0:15 - 0:40] Hospital Blood Request Workflow (BBMS-F-031, BBMS-F-032)
- **Action:** Open `http://127.0.0.1:8000/frontend/index.html`. Log in as `demo_hospital` (password: `HospitalPassword123!`).
- **Action:** Navigate to **Blood Requests** (`hospital_requests.html`). Show existing requests.
- **Action:** Submit a new requisition: `O+`, `Whole Blood`, `2 units`, `Urgent`.
- **Narration:** "Here the hospital submits a requisition for 2 units of O+ blood. The system logs it with a unique ID and marks it Pending."
- **Action:** Try to submit 999 units $\rightarrow$ system rejects with insufficient stock warning (BBMS-F-032). Log out.

### [0:40 - 1:05] Staff Approval, Atomic Issuance & Dispatch (BBMS-F-040, BBMS-F-041, BBMS-F-042)
- **Action:** Log in as `demo_staff` (password: `StaffPassword123!`).
- **Action:** Click **⚡ Review & Issue Requests** (`staff_requests.html`).
- **Action:** Click **Approve** on the pending request with a short note ("Approved for surgical wing").
- **Action:** Scroll to **Approved Requests Ready for Issue** and click **📦 Issue Blood**.
- **Narration:** "Staff reviews and approves the request. When issued, our backend executes a transactional `select_for_update` row-lock that decrements inventory stock atomically, and automatically dispatches a tracking record."

### [1:05 - 1:25] Account Lockout Policy & Admin Unlock (BBMS-F-003, BBMS-SR-004)
- **Action:** Log out. Return to login page. Enter username `demo_donor` with a wrong password 5 consecutive times.
- **Narration:** "To demonstrate security (BBMS-F-003), an adversary enters wrong passwords. On the 5th attempt, the account is permanently locked with a clear diagnostic message."
- **Action:** Log in as `demo_admin` (password: `AdminPassword123!`). Navigate to `/admin/accounts/user/`, select `demo_donor`, choose action **Unlock selected user accounts**, and click Go.
- **Narration:** "An administrator reviews the locked account and unlocks it. Every attempt is permanently recorded in our immutable audit trail."

### [1:25 - 1:45] Operational Dashboard, Data Export & Node Reminders (BBMS-F-050, BBMS-F-051, BBMS-F-052)
- **Action:** Open **Admin Operations** (`admin_dashboard.html`).
- **Narration:** "The administrator dashboard summarizes live stock, pending queues, and recent donations."
- **Action:** Click **📄 Export Donations (CSV)** and **📑 Export Donations (PDF)**. Show the generated PDF file.
- **Action:** Click **🔔 Send Donor Reminders**.
- **Narration:** "With one click, BBMS queries all eligible donors who haven't donated in 90 days and dispatches asynchronous notifications to our Node.js microservice."

### [1:45 - 2:00] Inventory Expiry & Low-Stock Alerts (BBMS-F-021, BBMS-F-022) & Conclusion
- **Action:** Open **Stock Alerts** (`alerts.html`).
- **Narration:** "Finally, our alerts dashboard flags units expiring within 5 days based on biological component shelf lives, and highlights blood groups falling below configurable threshold limits in bright red."
- **Closing:** "All 18 sprint issues are fully verified with 100% passing tests. Thank you!"
