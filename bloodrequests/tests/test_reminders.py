"""
Unit tests for eligible donor reminders dispatching.

# BBMS-F-051: Reminders to eligible donors through a Node.js notification service.
Acceptance Test ID: TC-Adm-02
Owner: Rithish P M (PR #1)
"""

from datetime import date, timedelta
from unittest.mock import patch
import urllib.error
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from donations.models import Donation

User = get_user_model()


class DonorRemindersTests(TestCase):
    """Test suite for BBMS-F-051 (TC-Adm-02)."""

    def setUp(self):
        self.client = APIClient()
        self.endpoint = '/api/requests/reminders/send'

        self.admin = User.objects.create_user(
            username='admin_remind',
            email='admin@bbms.org',
            password='AdminPass123!',
            role='admin',
        )

        self.eligible_donor = User.objects.create_user(
            username='eligible_donor',
            email='eligible@donor.org',
            password='DonorPass123!',
            role='donor',
        )

        self.ineligible_donor = User.objects.create_user(
            username='recent_donor',
            email='recent@donor.org',
            password='DonorPass123!',
            role='donor',
        )

        # Eligible: donated 95 days ago
        Donation.objects.create(
            donor=self.eligible_donor,
            blood_group='O+',
            component='whole_blood',
            quantity=1,
            donation_date=date.today() - timedelta(days=95),
        )

        # Ineligible: donated 20 days ago
        Donation.objects.create(
            donor=self.ineligible_donor,
            blood_group='A+',
            component='whole_blood',
            quantity=1,
            donation_date=date.today() - timedelta(days=20),
        )

    # BBMS-F-051 / TC-Adm-02 (Pass case: successful notification dispatch)
    @patch('urllib.request.urlopen')
    def test_TC_Adm_02_send_reminders_to_eligible_donors(self, mock_urlopen):
        """Eligible donors (>=90 days) receive reminders via mocked notification service."""
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.status = 200

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible_count'], 1)
        self.assertEqual(response.data['sent_count'], 1)
        self.assertEqual(response.data['failed_count'], 0)
        self.assertTrue(mock_urlopen.called)

    # BBMS-F-051 / TC-Adm-02 (Pass case: Non-blocking on service failure)
    @patch('urllib.request.urlopen')
    def test_TC_Adm_02_notification_service_failure_is_non_blocking(self, mock_urlopen):
        """Notification service network failure is non-blocking and does not fail HTTP request."""
        mock_urlopen.side_effect = urllib.error.URLError('Connection refused')

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.endpoint)

        # Still returns HTTP 200 with failed count recorded
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible_count'], 1)
        self.assertEqual(response.data['sent_count'], 0)
        self.assertEqual(response.data['failed_count'], 1)

    # BBMS-SR-002 / TC-Adm-02 (Fail case: Donor cannot trigger reminders)
    def test_TC_Adm_02_donor_forbidden_from_triggering_reminders(self):
        """Donors are forbidden from accessing admin reminder endpoints."""
        self.client.force_authenticate(user=self.eligible_donor)
        response = self.client.post(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
