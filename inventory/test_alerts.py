"""
Unit tests for inventory stock expiry and low-stock alerts.

# BBMS-F-021: Flag blood units expiring within 5 days (alert list).
# BBMS-F-022: Low-stock alert when a blood group falls below a threshold configurable per blood group.
Acceptance Test IDs: TC-Inv-02, TC-Inv-03
Owner: Ritesh Babu Reddy (PR #4)
"""

from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from donations.models import Donation
from inventory.models import BloodStock, StockThreshold

User = get_user_model()


class InventoryAlertsTests(TestCase):
    """Test suite for BBMS-F-021 (TC-Inv-02) and BBMS-F-022 (TC-Inv-03)."""

    def setUp(self):
        self.client = APIClient()
        self.expiry_url = '/api/inventory/alerts/expiry'
        self.low_stock_url = '/api/inventory/alerts/low-stock'

        self.staff = User.objects.create_user(
            username='staff_alert_tester',
            email='staff@bbms.org',
            password='StaffPass123!',
            role='staff',
        )

        self.donor = User.objects.create_user(
            username='donor_dan',
            email='dan@bbms.org',
            password='DonorPass123!',
            role='donor',
        )

        today = date.today()

        # F-021: Whole blood shelf life is 35 days
        # Unit 1: Donated 32 days ago -> Expires in 3 days (within 5-day alert window)
        self.expiring_donation = Donation.objects.create(
            donor=self.donor,
            blood_group='O+',
            component='whole_blood',
            quantity=1,
            donation_date=today - timedelta(days=32),
        )

        # Unit 2: Donated 10 days ago -> Expires in 25 days (outside 5-day alert window)
        self.fresh_donation = Donation.objects.create(
            donor=self.donor,
            blood_group='A+',
            component='whole_blood',
            quantity=1,
            donation_date=today - timedelta(days=10),
        )

        # F-022: Stock setup
        # O+ has 25 units (above default threshold 10)
        BloodStock.objects.create(blood_group='O+', component='whole_blood', units_available=25)

        # AB- has only 2 units (below default threshold 10)
        BloodStock.objects.create(blood_group='AB-', component='whole_blood', units_available=2)

        # B+ has 12 units, but custom threshold is set to 15 (below custom threshold)
        BloodStock.objects.create(blood_group='B+', component='whole_blood', units_available=12)
        StockThreshold.objects.create(blood_group='B+', min_units=15)

    # BBMS-F-021 / TC-Inv-02
    def test_TC_Inv_02_flag_units_expiring_within_5_days(self):
        """Donation unit expiring in 3 days is flagged; fresh donation expiring in 25 days is omitted."""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.expiry_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alerts = response.data.get('alerts', [])
        flagged_ids = [a['donation_id'] for a in alerts]

        self.assertIn(self.expiring_donation.id, flagged_ids)
        self.assertNotIn(self.fresh_donation.id, flagged_ids)

    # BBMS-F-022 / TC-Inv-03
    def test_TC_Inv_03_low_stock_alert_below_threshold(self):
        """Blood groups falling below default or configured thresholds are flagged."""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.low_stock_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alerts = response.data.get('alerts', [])
        flagged_groups = [a['blood_group'] for a in alerts]

        # AB- has 2 units < default 10 -> flagged
        self.assertIn('AB-', flagged_groups)

        # B+ has 12 units < custom threshold 15 -> flagged
        self.assertIn('B+', flagged_groups)

        # O+ has 25 units >= 10 -> NOT flagged
        self.assertNotIn('O+', flagged_groups)

    # BBMS-SR-002 / TC-Inv-02, TC-Inv-03 (Fail case: Donor cannot view alerts)
    def test_TC_Inv_02_donor_forbidden_from_alerts(self):
        """Donors are forbidden from viewing inventory alert endpoints."""
        self.client.force_authenticate(user=self.donor)
        res_exp = self.client.get(self.expiry_url)
        res_low = self.client.get(self.low_stock_url)

        self.assertEqual(res_exp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_low.status_code, status.HTTP_403_FORBIDDEN)
