"""
Unit tests for data export functionality (CSV and PDF).

# BBMS-F-052: Admins export donation and inventory reports as CSV and PDF, matching on-screen data.
Acceptance Test ID: TC-Adm-03
Owner: Rithish P M (PR #1)
"""

from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from inventory.models import BloodStock
from donations.models import Donation

User = get_user_model()


class ExportReportsTests(TestCase):
    """Test suite for BBMS-F-052 (TC-Adm-03)."""

    def setUp(self):
        self.client = APIClient()
        self.donations_export_url = '/api/requests/export/donations'
        self.inventory_export_url = '/api/requests/export/inventory'

        self.admin = User.objects.create_user(
            username='admin_exporter',
            email='export@bbms.org',
            password='AdminPass123!',
            role='admin',
        )

        self.donor = User.objects.create_user(
            username='donor_sam',
            email='sam@donor.org',
            password='DonorPass123!',
            role='donor',
        )

        # Seed data
        BloodStock.objects.create(blood_group='O+', component='whole_blood', units_available=10)
        Donation.objects.create(
            donor=self.donor,
            blood_group='O+',
            component='whole_blood',
            quantity=1,
            donation_date=date.today(),
        )

    # BBMS-F-052 / TC-Adm-03 (Pass case: Donations CSV)
    def test_TC_Adm_03_export_donations_csv(self):
        """Admin successfully exports donations as CSV matching on-screen data."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.donations_export_url}?format=csv")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="donations_report.csv"', response['Content-Disposition'])

        content = response.content.decode('utf-8')
        self.assertIn('Donor Username', content)
        self.assertIn('donor_sam', content)
        self.assertIn('O+', content)

    # BBMS-F-052 / TC-Adm-03 (Pass case: Donations PDF)
    def test_TC_Adm_03_export_donations_pdf(self):
        """Admin successfully exports donations as PDF matching on-screen data."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.donations_export_url}?format=pdf")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="donations_report.pdf"', response['Content-Disposition'])
        self.assertTrue(response.content.startswith(b'%PDF'))

    # BBMS-F-052 / TC-Adm-03 (Pass case: Inventory CSV)
    def test_TC_Adm_03_export_inventory_csv(self):
        """Admin successfully exports inventory as CSV matching on-screen stock."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.inventory_export_url}?format=csv")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Blood Group', content)
        self.assertIn('10', content)

    # BBMS-F-052 / TC-Adm-03 (Pass case: Inventory PDF)
    def test_TC_Adm_03_export_inventory_pdf(self):
        """Admin successfully exports inventory as PDF."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.inventory_export_url}?format=pdf")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))

    # BBMS-SR-002 / TC-Adm-03 (Fail case: Donor forbidden)
    def test_TC_Adm_03_donor_forbidden_from_export(self):
        """Donors must be forbidden from exporting data."""
        self.client.force_authenticate(user=self.donor)
        response = self.client.get(f"{self.donations_export_url}?format=csv")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
