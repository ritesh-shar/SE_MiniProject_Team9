# BBMS Unit Test Execution Report

**Execution Date:** 2026-11-15 22:46:16  
**Framework:** Django Test Runner (SQLite in-memory test database)  

## Test Execution Summary Matrix

| Acceptance Test ID | Requirement ID | Feature Area | Automated Test Method(s) | Status | Date Run |
|---|---|---|---|:---:|---|
| **TC-Reg-01** | BBMS-F-001 | Donor Registration | `test_TC_Reg_01_valid_registration_creates_donor, test_TC_Reg_01_duplicate_registration_rejected, test_TC_Reg_01_registration_with_expired_or_garbage_auth_header_succeeds` | **PASS** | 2026-11-15 |
| **TC-Auth-01** | BBMS-F-002 | JWT Authentication | `test_TC_Auth_01_correct_credentials_return_jwt, test_TC_Auth_01_wrong_credentials_rejected, test_TC_Auth_01_login_with_expired_or_garbage_auth_header_succeeds` | **PASS** | 2026-11-15 |
| **TC-Auth-02** | BBMS-F-003 | Account Lockout | `test_TC_Auth_02_four_failed_logins_do_not_lock_account, test_TC_Auth_02_fifth_failed_login_locks_account_permanently, test_TC_Auth_02_admin_unlocks_locked_account, test_TC_Auth_02_successful_login_resets_failed_counter` | **PASS** | 2026-11-15 |
| **TC-Sec-02** | BBMS-SR-002 | RBAC Enforcement | `test_TC_Sec_02_donor_cannot_access_staff_endpoints, test_TC_Sec_02_donor_cannot_view_stock, test_TC_Sec_02_staff_can_record_donation, test_TC_Sec_02_hospital_can_view_stock` | **PASS** | 2026-11-15 |
| **TC-Sec-03** | BBMS-SR-003 | Password Hashing (PBKDF2) | `test_TC_Sec_03_password_is_hashed` | **PASS** | 2026-11-15 |
| **TC-Sec-04** | BBMS-SR-004 | Authentication & Admin Auditing | `test_TC_Sec_04_successful_login_logged, test_TC_Sec_04_failed_login_logged, test_TC_Sec_04_admin_can_view_audit_logs, test_TC_Sec_04_donor_forbidden_from_audit_logs` | **PASS** | 2026-11-15 |
| **TC-Sec-05** | BBMS-SR-005 | JWT Expiry | `test_TC_Sec_05_expired_token_rejected, test_TC_Sec_05_valid_token_accepted` | **PASS** | 2026-11-15 |
| **TC-Sec-01** | BBMS-SR-001 | TLS 1.2+ Enforcement | `test_TC_Sec_01_http_redirects_to_https_when_ssl_redirect_enabled, test_TC_Sec_01_https_request_succeeds` | **PASS** | 2026-11-15 |
| **TC-Don-01** | BBMS-F-010 | Record Blood Donation | `test_TC_Don_01_staff_records_donation` | **PASS** | 2026-11-15 |
| **TC-Don-02** | BBMS-F-011 | 90-Day Donor Eligibility Guard | `test_TC_Don_02_blocks_donation_at_89_days, test_TC_Don_02_allows_donation_at_exactly_90_days` | **PASS** | 2026-11-15 |
| **TC-Don-03** | BBMS-F-012 | Stock Increment on Donation | `test_TC_Don_03_donation_increases_stock` | **PASS** | 2026-11-15 |
| **TC-Inv-01** | BBMS-F-020 | Real-Time Inventory Stock Levels | `test_TC_Inv_01_stock_reflects_latest_donations` | **PASS** | 2026-11-15 |
| **TC-Inv-02** | BBMS-F-021 | Expiry Alerts (<= 5 Days) | `test_TC_Inv_02_flag_units_expiring_within_5_days` | **PASS** | 2026-11-15 |
| **TC-Inv-03** | BBMS-F-022 | Low-Stock Alerts vs Threshold | `test_TC_Inv_03_low_stock_alert_below_threshold` | **PASS** | 2026-11-15 |
| **TC-Req-01** | BBMS-F-030 | Blood Search Querying | `test_TC_Req_01_search_returns_matching_stock, test_TC_Req_01_search_no_match_returns_empty` | **PASS** | 2026-11-15 |
| **TC-Req-02** | BBMS-F-031 | Hospital Requisition Submission | `test_TC_Req_02_hospital_submits_valid_blood_request, test_TC_Req_02_hospital_submits_request_without_trailing_slash, test_TC_Req_02_missing_field_rejected, test_TC_Req_02_donor_cannot_submit_request, test_TC_Req_02_hospital_sees_only_own_requests, test_TC_Req_02_staff_sees_all_requests` | **PASS** | 2026-11-15 |
| **TC-Req-03** | BBMS-F-032 | Rejection Exceeding Available Stock | `test_TC_Req_03_request_exceeding_stock_rejected` | **PASS** | 2026-11-15 |
| **TC-Iss-01** | BBMS-F-040 | Staff Approval/Rejection | `test_TC_Iss_01_staff_approve_pending_request, test_TC_Iss_01_staff_reject_pending_request, test_TC_Iss_01_cannot_review_already_approved_request, test_TC_Iss_01_donor_forbidden_from_review` | **PASS** | 2026-11-15 |
| **TC-Iss-02** | BBMS-F-041 | Stock Decrement on Issue | `test_TC_Iss_02_issue_request_decrements_inventory_stock, test_TC_Iss_02_issue_cannot_drop_stock_below_zero, test_TC_Iss_02_cannot_issue_unapproved_request, test_TC_Iss_02_hospital_forbidden_from_issuing` | **PASS** | 2026-11-15 |
| **TC-Iss-03** | BBMS-F-042 | Dispatch Record Tracking | `test_TC_Iss_03_dispatch_record_created_on_issue_retrievable_by_id` | **PASS** | 2026-11-15 |
| **TC-Adm-01** | BBMS-F-050 | Admin Dashboard Metrics | `test_TC_Adm_01_admin_dashboard_metrics, test_TC_Adm_01_staff_can_view_dashboard, test_TC_Adm_01_donor_forbidden_from_dashboard` | **PASS** | 2026-11-15 |
| **TC-Adm-02** | BBMS-F-051 | Eligible Donor Reminders | `test_TC_Adm_02_send_reminders_to_eligible_donors, test_TC_Adm_02_notification_service_failure_is_non_blocking, test_TC_Adm_02_donor_forbidden_from_triggering_reminders` | **PASS** | 2026-11-15 |
| **TC-Adm-03** | BBMS-F-052 | CSV & PDF Data Export | `test_TC_Adm_03_export_donations_csv, test_TC_Adm_03_export_donations_pdf, test_TC_Adm_03_export_inventory_csv, test_TC_Adm_03_export_inventory_pdf, test_TC_Adm_03_donor_forbidden_from_export` | **PASS** | 2026-11-15 |
| **TC-Ops-01** | BBMS-NF-005 | Audit Trail Retention & Purge | `test_TC_Ops_01_inventory_and_request_changes_logged, test_TC_Ops_01_purge_command_refuses_records_under_3_years` | **PASS** | 2026-11-15 |
| **TC-Perf-01** | BBMS-NF-001 | 95% Latency < 2 s | `test_TC_Perf_01_95th_percentile_under_2s` | **PASS** | 2026-11-15 |
| **TC-UX-01** | BBMS-NF-003 | 3-Click Staff Workflow | `test_TC_UX_01_dashboard_links_directly_to_donation_form, test_TC_UX_01_donation_form_has_direct_submit` | **PASS** | 2026-11-15 |

---

## Verbose Test Runner Raw Output

```text
Found 76 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: accounts, admin, audit, auth, bloodrequests, contenttypes, dispatch, donations, inventory, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying accounts.0001_initial... OK
  Applying accounts.0002_user_failed_login_attempts_user_is_locked... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying audit.0001_initial... OK
  Applying bloodrequests.0001_initial... OK
  Applying dispatch.0001_initial... OK
  Applying donations.0001_initial... OK
  Applying inventory.0001_initial... OK
  Applying inventory.0002_stockthreshold... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
Successfully purged 1 audit record(s) older than 2023-11-16.
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

test_TC_Auth_01_correct_credentials_return_jwt (accounts.test_auth.AuthenticationTests.test_TC_Auth_01_correct_credentials_return_jwt)
Correct credentials must return JWT access and refresh tokens. ... ok
test_TC_Auth_01_login_with_expired_or_garbage_auth_header_succeeds (accounts.test_auth.AuthenticationTests.test_TC_Auth_01_login_with_expired_or_garbage_auth_header_succeeds)
Public login endpoint must ignore old or invalid Authorization headers. ... ok
test_TC_Auth_01_wrong_credentials_rejected (accounts.test_auth.AuthenticationTests.test_TC_Auth_01_wrong_credentials_rejected)
Incorrect credentials must be rejected with 401 Unauthorized. ... ok
test_TC_Auth_02_admin_unlocks_locked_account (accounts.test_lockout.AccountLockoutTests.test_TC_Auth_02_admin_unlocks_locked_account)
Admin unlocks a locked account, allowing successful login thereafter. ... ok
test_TC_Auth_02_fifth_failed_login_locks_account_permanently (accounts.test_lockout.AccountLockoutTests.test_TC_Auth_02_fifth_failed_login_locks_account_permanently)
Fifth consecutive failed attempt locks the account and rejects subsequent valid logins. ... ok
test_TC_Auth_02_four_failed_logins_do_not_lock_account (accounts.test_lockout.AccountLockoutTests.test_TC_Auth_02_four_failed_logins_do_not_lock_account)
Four consecutive failed login attempts do not trigger account lockout. ... ok
test_TC_Auth_02_successful_login_resets_failed_counter (accounts.test_lockout.AccountLockoutTests.test_TC_Auth_02_successful_login_resets_failed_counter)
A successful login prior to reaching 5 failures resets the failed attempts counter. ... ok
test_TC_Perf_01_95th_percentile_under_2s (accounts.test_performance.PerformanceLatencyTests.test_TC_Perf_01_95th_percentile_under_2s)
Execute 100 search and dashboard queries; verify 95th percentile response latency is under 2.0s. ... ok
test_TC_Sec_02_donor_cannot_access_staff_endpoints (accounts.test_rbac.RBACTests.test_TC_Sec_02_donor_cannot_access_staff_endpoints)
Donors must NOT be allowed to record a blood donation (403 Forbidden). ... ok
test_TC_Sec_02_donor_cannot_view_stock (accounts.test_rbac.RBACTests.test_TC_Sec_02_donor_cannot_view_stock)
Donors must NOT be allowed to view blood inventory (403 Forbidden). ... ok
test_TC_Sec_02_hospital_can_view_stock (accounts.test_rbac.RBACTests.test_TC_Sec_02_hospital_can_view_stock)
Hospital users are authorized to view stock levels (200 OK). ... ok
test_TC_Sec_02_staff_can_record_donation (accounts.test_rbac.RBACTests.test_TC_Sec_02_staff_can_record_donation)
Staff members are authorized to record donations (201 Created). ... ok
test_TC_Reg_01_duplicate_registration_rejected (accounts.test_registration.DonorRegistrationTests.test_TC_Reg_01_duplicate_registration_rejected)
Registration with an already existing username must be rejected. ... ok
test_TC_Reg_01_registration_with_expired_or_garbage_auth_header_succeeds (accounts.test_registration.DonorRegistrationTests.test_TC_Reg_01_registration_with_expired_or_garbage_auth_header_succeeds)
Public registration must ignore Authorization headers. ... ok
test_TC_Reg_01_valid_registration_creates_donor (accounts.test_registration.DonorRegistrationTests.test_TC_Reg_01_valid_registration_creates_donor)
A new donor registers with valid personal details, blood group, and contact info. ... ok
test_TC_Sec_03_password_is_hashed (accounts.test_security_jwt.SecurityAndJWTTests.test_TC_Sec_03_password_is_hashed)
Database stores salted hash; plaintext password must NEVER appear in DB. ... ok
test_TC_Sec_05_expired_token_rejected (accounts.test_security_jwt.SecurityAndJWTTests.test_TC_Sec_05_expired_token_rejected)
An expired JWT token must be rejected with 401 Unauthorized. ... ok
test_TC_Sec_05_valid_token_accepted (accounts.test_security_jwt.SecurityAndJWTTests.test_TC_Sec_05_valid_token_accepted)
A valid, unexpired JWT access token must grant access to authorized endpoints. ... ok
test_TC_UX_01_dashboard_links_directly_to_donation_form (accounts.test_usability.UsabilityWorkflowTests.test_TC_UX_01_dashboard_links_directly_to_donation_form)
Dashboard HTML must provide a direct 1-click link to donation form for staff. ... ok
test_TC_UX_01_donation_form_has_direct_submit (accounts.test_usability.UsabilityWorkflowTests.test_TC_UX_01_donation_form_has_direct_submit)
Donation form page must provide immediate form inputs and direct submission button. ... ok
test_TC_Sec_04_admin_get_with_trailing_slash_returns_200 (audit.test_audit_urls.AuditURLTests.test_TC_Sec_04_admin_get_with_trailing_slash_returns_200)
Admin GET request to /api/audit/ (with trailing slash) returns HTTP 200. ... ok
test_TC_Sec_04_admin_get_without_trailing_slash_returns_200 (audit.test_audit_urls.AuditURLTests.test_TC_Sec_04_admin_get_without_trailing_slash_returns_200)
Admin GET request to /api/audit (no trailing slash) returns HTTP 200. ... ok
test_TC_Sec_04_non_admin_get_with_trailing_slash_returns_403 (audit.test_audit_urls.AuditURLTests.test_TC_Sec_04_non_admin_get_with_trailing_slash_returns_403)
Non-admin (donor/staff) GET request to /api/audit/ returns HTTP 403. ... ok
test_TC_Sec_04_non_admin_get_without_trailing_slash_returns_403 (audit.test_audit_urls.AuditURLTests.test_TC_Sec_04_non_admin_get_without_trailing_slash_returns_403)
Non-admin (donor/staff) GET request to /api/audit returns HTTP 403. ... ok
test_TC_Sec_04_admin_can_view_audit_logs (audit.tests.AuditLoggingTests.test_TC_Sec_04_admin_can_view_audit_logs)
Admin successfully retrieves list of audit records. ... ok
test_TC_Sec_04_donor_forbidden_from_audit_logs (audit.tests.AuditLoggingTests.test_TC_Sec_04_donor_forbidden_from_audit_logs)
Donors are forbidden from accessing audit trail endpoint. ... ok
test_TC_Sec_04_failed_login_logged (audit.tests.AuditLoggingTests.test_TC_Sec_04_failed_login_logged)
Failed user authentication generates LOGIN_FAILED audit log entry. ... ok
test_TC_Sec_04_successful_login_logged (audit.tests.AuditLoggingTests.test_TC_Sec_04_successful_login_logged)
Successful user authentication generates an audit log entry. ... ok
test_TC_Ops_01_inventory_changes_logged (audit.tests_audit_ops.AuditTrailOpsTests.test_TC_Ops_01_inventory_changes_logged)
Updating blood stock triggers an audit log entry with details. ... ok
test_TC_Ops_01_purge_command_refuses_records_under_3_years (audit.tests_audit_ops.AuditTrailOpsTests.test_TC_Ops_01_purge_command_refuses_records_under_3_years)
Purge command must refuse execution when requested cutoff is under 3 years old. ... ok
test_TC_Ops_01_purge_deletes_records_older_than_3_years (audit.tests_audit_ops.AuditTrailOpsTests.test_TC_Ops_01_purge_deletes_records_older_than_3_years)
Purge command successfully deletes records older than 3 years. ... ok
test_TC_Ops_01_request_changes_logged (audit.tests_audit_ops.AuditTrailOpsTests.test_TC_Ops_01_request_changes_logged)
Creating and transitioning a blood request logs audit records. ... ok
test_TC_Adm_01_admin_dashboard_metrics (bloodrequests.tests.test_dashboard.AdminDashboardTests.test_TC_Adm_01_admin_dashboard_metrics)
Admin views dashboard with accurate aggregate stock, pending requests, and recent donations. ... ok
test_TC_Adm_01_donor_forbidden_from_dashboard (bloodrequests.tests.test_dashboard.AdminDashboardTests.test_TC_Adm_01_donor_forbidden_from_dashboard)
Donor role must be forbidden from administrative dashboard. ... ok
test_TC_Adm_01_staff_can_view_dashboard (bloodrequests.tests.test_dashboard.AdminDashboardTests.test_TC_Adm_01_staff_can_view_dashboard)
Staff members are authorized to view operational dashboard. ... ok
test_TC_Adm_03_donor_forbidden_from_export (bloodrequests.tests.test_export.ExportReportsTests.test_TC_Adm_03_donor_forbidden_from_export)
Donors must be forbidden from exporting data. ... ok
test_TC_Adm_03_export_donations_csv (bloodrequests.tests.test_export.ExportReportsTests.test_TC_Adm_03_export_donations_csv)
Admin successfully exports donations as CSV matching on-screen data. ... ok
test_TC_Adm_03_export_donations_pdf (bloodrequests.tests.test_export.ExportReportsTests.test_TC_Adm_03_export_donations_pdf)
Admin successfully exports donations as PDF matching on-screen data. ... ok
test_TC_Adm_03_export_inventory_csv (bloodrequests.tests.test_export.ExportReportsTests.test_TC_Adm_03_export_inventory_csv)
Admin successfully exports inventory as CSV matching on-screen stock. ... ok
test_TC_Adm_03_export_inventory_pdf (bloodrequests.tests.test_export.ExportReportsTests.test_TC_Adm_03_export_inventory_pdf)
Admin successfully exports inventory as PDF. ... ok
test_health_check_returns_ok_when_database_connected (bloodrequests.tests.test_health.HealthCheckTests.test_health_check_returns_ok_when_database_connected)
Public health check endpoint returns 200 OK with database connected status. ... ok
test_TC_Iss_02_cannot_issue_unapproved_request (bloodrequests.tests.test_issue.BloodRequestIssueTests.test_TC_Iss_02_cannot_issue_unapproved_request)
Cannot issue a request whose status is 'pending'. ... ok
test_TC_Iss_02_hospital_forbidden_from_issuing (bloodrequests.tests.test_issue.BloodRequestIssueTests.test_TC_Iss_02_hospital_forbidden_from_issuing)
Hospital role is forbidden from issuing blood requests. ... ok
test_TC_Iss_02_issue_cannot_drop_stock_below_zero (bloodrequests.tests.test_issue.BloodRequestIssueTests.test_TC_Iss_02_issue_cannot_drop_stock_below_zero)
Issuance fails with 400 Bad Request if requested volume exceeds current inventory. ... ok
test_TC_Iss_02_issue_request_decrements_inventory_stock (bloodrequests.tests.test_issue.BloodRequestIssueTests.test_TC_Iss_02_issue_request_decrements_inventory_stock)
Issuing an approved blood request atomically decrements available inventory stock. ... ok
test_TC_Adm_02_donor_forbidden_from_triggering_reminders (bloodrequests.tests.test_reminders.DonorRemindersTests.test_TC_Adm_02_donor_forbidden_from_triggering_reminders)
Donors are forbidden from accessing admin reminder endpoints. ... ok
test_TC_Adm_02_notification_service_failure_is_non_blocking (bloodrequests.tests.test_reminders.DonorRemindersTests.test_TC_Adm_02_notification_service_failure_is_non_blocking)
Notification service network failure is non-blocking and does not fail HTTP request. ... Notification service call failed for donor 2: <urlopen error Connection refused>
ok
test_TC_Adm_02_send_reminders_to_eligible_donors (bloodrequests.tests.test_reminders.DonorRemindersTests.test_TC_Adm_02_send_reminders_to_eligible_donors)
Eligible donors (>=90 days) receive reminders via mocked notification service. ... ok
test_TC_Req_02_donor_cannot_submit_request (bloodrequests.tests.test_requests.BloodRequestSubmissionTests.test_TC_Req_02_donor_cannot_submit_request)
Donor role must be forbidden from submitting blood requests. ... ok
test_TC_Req_02_hospital_sees_only_own_requests (bloodrequests.tests.test_requests.BloodRequestSubmissionTests.test_TC_Req_02_hospital_sees_only_own_requests)
Hospital listing /api/requests sees only requests submitted by their own hospital. ... ok
test_TC_Req_02_hospital_submits_request_without_trailing_slash (bloodrequests.tests.test_requests.BloodRequestSubmissionTests.test_TC_Req_02_hospital_submits_request_without_trailing_slash)
Hospital submits request to exact path /api/requests without trailing slash. ... ok
test_TC_Req_02_hospital_submits_valid_blood_request (bloodrequests.tests.test_requests.BloodRequestSubmissionTests.test_TC_Req_02_hospital_submits_valid_blood_request)
Hospital submits a valid blood request with group, component, quantity, urgency. ... ok
test_TC_Req_02_missing_field_rejected (bloodrequests.tests.test_requests.BloodRequestSubmissionTests.test_TC_Req_02_missing_field_rejected)
Submission missing required quantity must be rejected with 400 Bad Request. ... ok
test_TC_Req_02_staff_sees_all_requests (bloodrequests.tests.test_requests.BloodRequestSubmissionTests.test_TC_Req_02_staff_sees_all_requests)
Staff listing /api/requests sees requests from all hospitals. ... ok
test_TC_Iss_01_cannot_review_already_approved_request (bloodrequests.tests.test_review.BloodRequestReviewTests.test_TC_Iss_01_cannot_review_already_approved_request)
Cannot re-review a request that is already approved or rejected. ... ok
test_TC_Iss_01_donor_forbidden_from_review (bloodrequests.tests.test_review.BloodRequestReviewTests.test_TC_Iss_01_donor_forbidden_from_review)
Donors are forbidden from approving or rejecting blood requests. ... ok
test_TC_Iss_01_staff_approve_pending_request (bloodrequests.tests.test_review.BloodRequestReviewTests.test_TC_Iss_01_staff_approve_pending_request)
Staff member successfully approves a pending blood request. ... ok
test_TC_Iss_01_staff_reject_pending_request (bloodrequests.tests.test_review.BloodRequestReviewTests.test_TC_Iss_01_staff_reject_pending_request)
Staff member successfully rejects a pending blood request with notes. ... ok
test_TC_Sec_01_http_redirects_to_https_when_ssl_redirect_enabled (bloodrequests.tests.test_tls.TLSSecurityTests.test_TC_Sec_01_http_redirects_to_https_when_ssl_redirect_enabled)
When SECURE_SSL_REDIRECT is active, standard HTTP requests are redirected to HTTPS. ... ok
test_TC_Sec_01_https_request_succeeds (bloodrequests.tests.test_tls.TLSSecurityTests.test_TC_Sec_01_https_request_succeeds)
Requests over HTTPS succeed directly without redirection. ... ok
test_TC_Req_03_request_exceeding_stock_rejected (bloodrequests.tests.test_validation.StockValidationTests.test_TC_Req_03_request_exceeding_stock_rejected)
Requisition exceeding available inventory is rejected with 400 and explanatory message. ... ok
test_TC_Req_03_request_with_zero_stock_rejected (bloodrequests.tests.test_validation.StockValidationTests.test_TC_Req_03_request_with_zero_stock_rejected)
Requisition for group/component with 0 stock is rejected. ... ok
test_TC_Req_03_request_within_available_stock_accepted (bloodrequests.tests.test_validation.StockValidationTests.test_TC_Req_03_request_within_available_stock_accepted)
Hospital requisition within current inventory stock is accepted. ... ok
test_TC_Iss_03_dispatch_record_created_on_issue_retrievable_by_id (dispatch.tests.DispatchTrackingTests.test_TC_Iss_03_dispatch_record_created_on_issue_retrievable_by_id)
Issuing an approved request triggers signal to create DispatchRecord, retrievable by request ID. ... ok
test_TC_Iss_03_hospital_cannot_view_other_hospital_dispatch (dispatch.tests.DispatchTrackingTests.test_TC_Iss_03_hospital_cannot_view_other_hospital_dispatch)
Hospital role is forbidden from retrieving dispatches destined for other hospitals. ... ok
test_TC_Iss_03_unfulfilled_request_returns_404 (dispatch.tests.DispatchTrackingTests.test_TC_Iss_03_unfulfilled_request_returns_404)
Querying dispatch for an unissued blood request returns 404 Not Found. ... ok
test_TC_Don_01_staff_records_donation (donations.tests.DonationTests.test_TC_Don_01_staff_records_donation)
Staff records donation; new donation appears in donor history. ... ok
test_TC_Don_02_allows_donation_at_exactly_90_days (donations.tests.DonationTests.test_TC_Don_02_allows_donation_at_exactly_90_days)
Donation is ALLOWED when exactly 90 days have elapsed since previous donation. ... ok
test_TC_Don_02_blocks_donation_at_89_days (donations.tests.DonationTests.test_TC_Don_02_blocks_donation_at_89_days)
Donation is BLOCKED if only 89 days have elapsed since previous donation. ... ok
test_TC_Don_03_donation_increases_stock (donations.tests.DonationTests.test_TC_Don_03_donation_increases_stock)
Successful donation automatically increases inventory stock by the donated quantity. ... ok
test_TC_Inv_02_donor_forbidden_from_alerts (inventory.test_alerts.InventoryAlertsTests.test_TC_Inv_02_donor_forbidden_from_alerts)
Donors are forbidden from viewing inventory alert endpoints. ... ok
test_TC_Inv_02_flag_units_expiring_within_5_days (inventory.test_alerts.InventoryAlertsTests.test_TC_Inv_02_flag_units_expiring_within_5_days)
Donation unit expiring in 3 days is flagged; fresh donation expiring in 25 days is omitted. ... ok
test_TC_Inv_03_low_stock_alert_below_threshold (inventory.test_alerts.InventoryAlertsTests.test_TC_Inv_03_low_stock_alert_below_threshold)
Blood groups falling below default or configured thresholds are flagged. ... ok
test_TC_Req_01_search_no_match_returns_empty (inventory.test_search.InventorySearchTests.test_TC_Req_01_search_no_match_returns_empty)
Search with criteria matching no records returns an empty list. ... ok
test_TC_Req_01_search_returns_matching_stock (inventory.test_search.InventorySearchTests.test_TC_Req_01_search_returns_matching_stock)
Search by blood group and component returns accurate matching stock. ... ok
test_TC_Inv_01_stock_reflects_latest_donations (inventory.tests.InventoryStockTests.test_TC_Inv_01_stock_reflects_latest_donations)
GET /api/inventory returns accurate, real-time stock counts. ... ok

----------------------------------------------------------------------
Ran 76 tests in 44.185s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...


```