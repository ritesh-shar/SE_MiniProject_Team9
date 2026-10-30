"""
Unit tests for blood inventory search.

# BBMS-F-030: Search available blood units by blood group and component (TC-Req-01).
Owner: Ritesh Babu Reddy (PES2UG24CS403)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from inventory.models import BloodStock

User = get_user_model()


class InventorySearchTests(TestCase):
    """Test suite for BBMS-F-030 (TC-Req-01)."""

    def setUp(self):
        self.client = APIClient()

        self.hospital_user = User.objects.create_user(
            username='city_hospital',
            password='HospitalPassword123!',
            role='hospital',
        )
        token = AccessToken.for_user(self.hospital_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        BloodStock.objects.create(blood_group='AB+', component='platelets', units_available=9)
        BloodStock.objects.create(blood_group='O+', component='whole_blood', units_available=15)
        BloodStock.objects.create(blood_group='O+', component='red_cells', units_available=7)

    # BBMS-F-030 / TC-Req-01 (Match case)
    def test_TC_Req_01_search_returns_matching_stock(self):
        """Search by blood group and component returns accurate matching stock."""
        response = self.client.get('/api/inventory/search?bloodGroup=AB%2B&component=platelets')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['blood_group'], 'AB+')
        self.assertEqual(response.data[0]['component'], 'platelets')
        self.assertEqual(response.data[0]['units_available'], 9)

    # BBMS-F-030 / TC-Req-01 (No match case)
    def test_TC_Req_01_search_no_match_returns_empty(self):
        """Search with criteria matching no records returns an empty list."""
        response = self.client.get('/api/inventory/search?bloodGroup=B-&component=platelets')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
