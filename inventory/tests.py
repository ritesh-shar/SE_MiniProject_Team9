"""
Unit and integration tests for inventory stock view.

# BBMS-F-020: Real-time stock count per blood group and component (TC-Inv-01).
Owner: Ritesh Kumar Sharma (PES2UG24CS404)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from inventory.models import BloodStock

User = get_user_model()


class InventoryStockTests(TestCase):
    """Test suite for BBMS-F-020 (TC-Inv-01)."""

    def setUp(self):
        self.client = APIClient()

        self.staff = User.objects.create_user(
            username='inventory_staff',
            password='Password123!',
            role='staff',
        )
        token = AccessToken.for_user(self.staff)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

    # BBMS-F-020 / TC-Inv-01
    def test_TC_Inv_01_stock_reflects_latest_donations(self):
        """GET /api/inventory returns accurate, real-time stock counts."""
        BloodStock.objects.create(blood_group='B+', component='red_cells', units_available=14)
        BloodStock.objects.create(blood_group='O-', component='platelets', units_available=2)

        response = self.client.get('/api/inventory')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stock_map = {(item['blood_group'], item['component']): item['units_available'] for item in response.data}

        self.assertEqual(stock_map.get(('B+', 'red_cells')), 14)
        self.assertEqual(stock_map.get(('O-', 'platelets')), 2)
