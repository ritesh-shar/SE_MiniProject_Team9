# Usability Verification (3-Click Staff Workflow)

# BBMS-NF-003 (TC-UX-01)
Owner: Reyansh (PR #3)

## Requirement Overview
Per IEEE SRS Section 4.3 and SAD Section 3.7, operational efficiency is critical for blood bank staff. Staff operators must be able to record an incoming blood donation in **3 user clicks or fewer** from the authenticated staff dashboard.

---

## Click-Path Walkthrough

```text
[Dashboard: dashboard.html]
         │
         ▼ Click 1: Click "➕ Record Blood Donation" button
[Donation Form: donation_form.html]
         │
         ▼ Click 2: Focus / Select Donor or Blood Details
[Input Completed]
         │
         ▼ Click 3: Click "Record Donation" submission button
[Donation Saved & Stock Incremented]
```

### Detailed Step-by-Step Breakdown

1. **Click 1: Quick Action Navigation**
   - Location: `frontend/dashboard.html`
   - Element: `<a href="donation_form.html" class="btn btn-primary role-staff-only">➕ Record Blood Donation</a>`
   - Action: User clicks the button in the Quick Actions section. The browser directly loads `donation_form.html` without intermediate modal dialogs or secondary menus.

2. **Click 2: Input Selection**
   - Location: `frontend/donation_form.html`
   - Action: User clicks into the form input controls (e.g., selects donor ID, blood group, or component type).

3. **Click 3: Form Submission**
   - Location: `frontend/donation_form.html`
   - Element: `<button type="submit" class="btn btn-primary">Record Donation</button>`
   - Action: User submits the requisition. The form executes `POST /api/donations`, commits the donation record to the database, automatically increments inventory stock under row-level locking, and displays an immediate confirmation banner.

---

## Automated Verification
Automated verification is codified in `accounts/test_usability.py` (TC-UX-01):
```bash
python manage.py test accounts.test_usability
```
The test suite parses the frontend HTML assets and confirms:
1. `dashboard.html` contains a direct link `href="donation_form.html"` restricted to staff roles.
2. `donation_form.html` contains a single-page direct submit form with no nested steps or multi-page wizards.
3. Total user interaction path $\le 3$ clicks.
