"""
Tests for audit URL routing (with and without trailing slash).

# BBMS-SR-004: Audit trail URL resolution.
Acceptance Test ID: TC-Sec-04
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from audit.models import AuditLog
from audit.services import log_event

User = get_user_model()


class AuditURLTests(TestCase):
    """Test suite verifying /api/audit and /api/audit/ URL routing and role security (TC-Sec-04)."""

    def setUp(self):
        self.client = APIClient()
        self.url_no_slash = '/api/audit'
        self.url_with_slash = '/api/audit/'

        self.admin = User.objects.create_user(
            username='admin_audit_tester',
            email='admin_audit@bbms.org',
            password='AdminPass123!',
            role='admin',
            is_staff=True,
        )

        self.donor = User.objects.create_user(
            username='donor_audit_tester',
            email='donor_audit@bbms.org',
            password='DonorPass123!',
            role='donor',
        )

        self.staff = User.objects.create_user(
            username='staff_audit_tester',
            email='staff_audit@bbms.org',
            password='StaffPass123!',
            role='staff',
        )

        # Create sample audit log
        log_event(
            event_type='ADMIN_ACTION',
            user=self.admin,
            description='Test audit event',
        )

    def test_TC_Sec_04_admin_get_without_trailing_slash_returns_200(self):
        """Admin GET request to /api/audit (no trailing slash) returns HTTP 200."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url_no_slash)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) >= 1)

    def test_TC_Sec_04_admin_get_with_trailing_slash_returns_200(self):
        """Admin GET request to /api/audit/ (with trailing slash) returns HTTP 200."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url_with_slash)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) >= 1)

    def test_TC_Sec_04_non_admin_get_without_trailing_slash_returns_403(self):
        """Non-admin (donor/staff) GET request to /api/audit returns HTTP 403."""
        self.client.force_authenticate(user=self.donor)
        response = self.client.get(self.url_no_slash)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.staff)
        response_staff = self.client.get(self.url_no_slash)
        self.assertEqual(response_staff.status_code, status.HTTP_403_FORBIDDEN)

    def test_TC_Sec_04_non_admin_get_with_trailing_slash_returns_403(self):
        """Non-admin (donor/staff) GET request to /api/audit/ returns HTTP 403."""
        self.client.force_authenticate(user=self.donor)
        response = self.client.get(self.url_with_slash)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.staff)
        response_staff = self.client.get(self.url_with_slash)
        self.assertEqual(response_staff.status_code, status.HTTP_403_FORBIDDEN)
