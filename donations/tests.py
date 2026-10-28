"""
Unit and integration tests for blood donation recording and eligibility.

# BBMS-F-010: Staff record a donation (TC-Don-01).
# BBMS-F-011: 90-day donor eligibility rule (TC-Don-02: 89 days blocked, 90 days allowed).
# BBMS-F-012: Automatic stock increment (TC-Don-03).
Owner: Ritesh Kumar Sharma (PES2UG24CS404)
"""

from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from donations.models import Donation
from inventory.models import BloodStock

User = get_user_model()


class DonationTests(TestCase):
    """Test suite for donation recording, eligibility, and stock updates."""

    def setUp(self):
        self.client = APIClient()

        self.donor = User.objects.create_user(
            username='donor_alice',
            password='Password123!',
            role='donor',
            blood_group='A+',
            phone='9876543201',
        )
        self.staff = User.objects.create_user(
            username='staff_bob',
            password='Password123!',
            role='staff',
        )

        token = AccessToken.for_user(self.staff)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

    # BBMS-F-010 / TC-Don-01
    def test_TC_Don_01_staff_records_donation(self):
        """Staff records donation; new donation appears in donor history."""
        payload = {
            'donorId': self.donor.id,
            'bloodGroup': 'A+',
            'component': 'whole_blood',
            'quantity': 2,
            'donationDate': str(date.today()),
        }
        response = self.client.post('/api/donations', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('donationId', response.data)

        # Check that it appears in donor history
        donor_token = AccessToken.for_user(self.donor)
        donor_client = APIClient()
        donor_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(donor_token)}')

        history_resp = donor_client.get('/api/donations/history')
        self.assertEqual(history_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(history_resp.data), 1)
        self.assertEqual(history_resp.data[0]['blood_group'], 'A+')
        self.assertEqual(history_resp.data[0]['quantity'], 2)

    # BBMS-F-011 / TC-Don-02 (Blocked at 89 days)
    def test_TC_Don_02_blocks_donation_at_89_days(self):
        """Donation is BLOCKED if only 89 days have elapsed since previous donation."""
        past_date = date.today() - timedelta(days=89)
        Donation.objects.create(
            donor=self.donor,
            blood_group='A+',
            component='whole_blood',
            quantity=1,
            donation_date=past_date,
        )

        payload = {
            'donorId': self.donor.id,
            'bloodGroup': 'A+',
            'component': 'whole_blood',
            'quantity': 1,
            'donationDate': str(date.today()),
        }
        response = self.client.post('/api/donations', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('code'), 'DONOR_NOT_ELIGIBLE')
        self.assertIn('89 days', response.data.get('error', ''))

    # BBMS-F-011 / TC-Don-02 (Allowed at exactly 90 days)
    def test_TC_Don_02_allows_donation_at_exactly_90_days(self):
        """Donation is ALLOWED when exactly 90 days have elapsed since previous donation."""
        past_date = date.today() - timedelta(days=90)
        Donation.objects.create(
            donor=self.donor,
            blood_group='A+',
            component='whole_blood',
            quantity=1,
            donation_date=past_date,
        )

        payload = {
            'donorId': self.donor.id,
            'bloodGroup': 'A+',
            'component': 'whole_blood',
            'quantity': 1,
            'donationDate': str(date.today()),
        }
        response = self.client.post('/api/donations', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')

    # BBMS-F-012 / TC-Don-03
    def test_TC_Don_03_donation_increases_stock(self):
        """Successful donation automatically increases inventory stock by the donated quantity."""
        # Baseline stock
        stock, _ = BloodStock.objects.get_or_create(
            blood_group='A+',
            component='plasma',
            defaults={'units_available': 5}
        )
        initial_units = stock.units_available

        payload = {
            'donorId': self.donor.id,
            'bloodGroup': 'A+',
            'component': 'plasma',
            'quantity': 3,
            'donationDate': str(date.today()),
        }
        response = self.client.post('/api/donations', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['updatedStock'], initial_units + 3)

        # Confirm from DB directly
        stock.refresh_from_db()
        self.assertEqual(stock.units_available, initial_units + 3)
