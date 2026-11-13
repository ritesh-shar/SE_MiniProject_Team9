"""
Unit tests for administrator dashboard metrics.

# BBMS-F-050: Admin dashboard: current stock, pending requests, recent donations.
Acceptance Test ID: TC-Adm-01
Owner: Rithish P M (PR #1)
"""

from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from inventory.models import BloodStock
from donations.models import Donation
from bloodrequests.models import BloodRequest

User = get_user_model()


class AdminDashboardTests(TestCase):
    """Test suite for BBMS-F-050 (TC-Adm-01)."""

    def setUp(self):
        self.client = APIClient()
        self.endpoint = '/api/admin/dashboard'

        self.admin = User.objects.create_user(
            username='admin_boss',
            email='admin@bbms.org',
            password='AdminPassword123!',
            role='admin',
            is_staff=True,
        )

        self.staff = User.objects.create_user(
            username='staff_worker',
            email='staff@bbms.org',
            password='StaffPassword123!',
            role='staff',
        )

        self.donor = User.objects.create_user(
            username='donor_dan',
            email='dan@donor.org',
            password='DonorPassword123!',
            role='donor',
        )

        self.hospital = User.objects.create_user(
            username='general_hospital',
            email='general@hospital.org',
            password='HospitalPassword123!',
            role='hospital',
        )

        # Seed some data
        BloodStock.objects.create(blood_group='A+', component='whole_blood', units_available=15)
        BloodStock.objects.create(blood_group='O-', component='red_cells', units_available=8)

        Donation.objects.create(
            donor=self.donor,
            blood_group='A+',
            component='whole_blood',
            quantity=1,
            donation_date=date.today(),
        )

        BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='A+',
            component='whole_blood',
            quantity=2,
            urgency='urgent',
            status='pending',
        )

    # BBMS-F-050 / TC-Adm-01 (Pass case)
    def test_TC_Adm_01_admin_dashboard_metrics(self):
        """Admin views dashboard with accurate aggregate stock, pending requests, and recent donations."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)
        summary = response.data['summary']

        self.assertEqual(summary['total_stock_units'], 23)
        self.assertEqual(summary['pending_requests_count'], 1)
        self.assertEqual(summary['total_donations_count'], 1)

        self.assertIn('stock', response.data)
        self.assertIn('pending_requests', response.data)
        self.assertIn('recent_donations', response.data)

    # BBMS-F-050 / TC-Adm-01 (Pass case: Staff can also view)
    def test_TC_Adm_01_staff_can_view_dashboard(self):
        """Staff members are authorized to view operational dashboard."""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # BBMS-SR-002 / TC-Adm-01 (Fail case: Donor forbidden)
    def test_TC_Adm_01_donor_forbidden_from_dashboard(self):
        """Donor role must be forbidden from administrative dashboard."""
        self.client.force_authenticate(user=self.donor)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
