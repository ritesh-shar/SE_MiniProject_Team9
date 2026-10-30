"""
Role-based access control (RBAC) tests.

# BBMS-SR-002: Role-based access control enforced at the API layer.
Acceptance Test ID: TC-Sec-02
Owner: Ritesh Babu Reddy (PES2UG24CS403)
"""

from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class RBACTests(TestCase):
    """Test suite for BBMS-SR-002 (TC-Sec-02)."""

    def setUp(self):
        self.client = APIClient()

        # Create users with different roles
        self.donor = User.objects.create_user(
            username='donor_user',
            password='Password123!',
            role='donor',
            blood_group='O+',
        )
        self.staff = User.objects.create_user(
            username='staff_user',
            password='Password123!',
            role='staff',
        )
        self.hospital = User.objects.create_user(
            username='hospital_user',
            password='Password123!',
            role='hospital',
        )
        self.admin = User.objects.create_user(
            username='admin_user',
            password='Password123!',
            role='admin',
        )

    def auth_as(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

    # BBMS-SR-002 / TC-Sec-02 (Negative check: Donor blocked from recording donation)
    def test_TC_Sec_02_donor_cannot_access_staff_endpoints(self):
        """Donors must NOT be allowed to record a blood donation (403 Forbidden)."""
        self.auth_as(self.donor)
        payload = {
            'donorId': self.donor.id,
            'bloodGroup': 'O+',
            'component': 'whole_blood',
            'quantity': 1,
            'donationDate': str(date.today()),
        }
        response = self.client.post('/api/donations', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # BBMS-SR-002 / TC-Sec-02 (Negative check: Donor blocked from viewing stock)
    def test_TC_Sec_02_donor_cannot_view_stock(self):
        """Donors must NOT be allowed to view blood inventory (403 Forbidden)."""
        self.auth_as(self.donor)
        response = self.client.get('/api/inventory')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # BBMS-SR-002 / TC-Sec-02 (Positive check: Staff can record donation)
    def test_TC_Sec_02_staff_can_record_donation(self):
        """Staff members are authorized to record donations (201 Created)."""
        self.auth_as(self.staff)
        payload = {
            'donorId': self.donor.id,
            'bloodGroup': 'O+',
            'component': 'whole_blood',
            'quantity': 1,
            'donationDate': str(date.today()),
        }
        response = self.client.post('/api/donations', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # BBMS-SR-002 / TC-Sec-02 (Positive check: Hospital can view inventory)
    def test_TC_Sec_02_hospital_can_view_stock(self):
        """Hospital users are authorized to view stock levels (200 OK)."""
        self.auth_as(self.hospital)
        response = self.client.get('/api/inventory')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
