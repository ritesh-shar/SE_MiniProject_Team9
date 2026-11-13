"""
Unit tests for audit trail functionality.

# BBMS-SR-004: Log all authentication attempts and administrative actions.
Acceptance Test ID: TC-Sec-04
Owner: Reyansh (PR #3)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from audit.models import AuditLog
from audit.services import log_event

User = get_user_model()


class AuditLoggingTests(TestCase):
    """Test suite for BBMS-SR-004 (TC-Sec-04)."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login'
        self.audit_url = '/api/audit/'

        self.admin = User.objects.create_user(
            username='admin_auditor',
            email='auditor@bbms.org',
            password='AdminPass123!',
            role='admin',
            is_staff=True,
        )

        self.donor = User.objects.create_user(
            username='donor_test',
            email='test@donor.org',
            password='DonorPass123!',
            role='donor',
        )

    # BBMS-SR-004 / TC-Sec-04 (Pass case: Successful login logged)
    def test_TC_Sec_04_successful_login_logged(self):
        """Successful user authentication generates an audit log entry."""
        payload = {'username': 'donor_test', 'password': 'DonorPass123!'}
        response = self.client.post(self.login_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log = AuditLog.objects.filter(event_type='LOGIN_SUCCESS', user=self.donor).first()
        self.assertIsNotNone(log)
        self.assertIn('donor_test', log.description)

    # BBMS-SR-004 / TC-Sec-04 (Pass case: Failed login logged)
    def test_TC_Sec_04_failed_login_logged(self):
        """Failed user authentication generates LOGIN_FAILED audit log entry."""
        payload = {'username': 'donor_test', 'password': 'WrongPassword999!'}
        response = self.client.post(self.login_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        log = AuditLog.objects.filter(event_type='LOGIN_FAILED').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.extra_data.get('attempted_username'), 'donor_test')

    # BBMS-SR-004 / TC-Sec-04 (Pass case: Admin queries audit logs)
    def test_TC_Sec_04_admin_can_view_audit_logs(self):
        """Admin successfully retrieves list of audit records."""
        log_event(event_type='ADMIN_ACTION', user=self.admin, description='Admin updated configuration')

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.audit_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    # BBMS-SR-002 / TC-Sec-04 (Fail case: Donor cannot view audit logs)
    def test_TC_Sec_04_donor_forbidden_from_audit_logs(self):
        """Donors are forbidden from accessing audit trail endpoint."""
        self.client.force_authenticate(user=self.donor)
        response = self.client.get(self.audit_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
