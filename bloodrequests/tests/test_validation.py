"""
Unit tests for request stock availability validation.

# BBMS-F-032: Reject a request whose quantity exceeds available stock for that group, with a message.
Acceptance Test ID: TC-Req-03
Owner: Ritesh Babu Reddy (PR #4)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from inventory.models import BloodStock

User = get_user_model()


class StockValidationTests(TestCase):
    """Test suite for BBMS-F-032 (TC-Req-03)."""

    def setUp(self):
        self.client = APIClient()
        self.requests_url = '/api/requests'

        self.hospital = User.objects.create_user(
            username='st_jude_hospital',
            email='stjude@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        # Seed exact stock: 4 units of B+ Platelets
        BloodStock.objects.create(
            blood_group='B+',
            component='platelets',
            units_available=4,
        )

    # BBMS-F-032 / TC-Req-03 (Pass case: Quantity within available stock)
    def test_TC_Req_03_request_within_available_stock_accepted(self):
        """Hospital requisition within current inventory stock is accepted."""
        self.client.force_authenticate(user=self.hospital)
        payload = {
            'blood_group': 'B+',
            'component': 'platelets',
            'quantity': 3,
            'urgency': 'normal',
        }
        response = self.client.post(self.requests_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('requestId', response.data)

    # BBMS-F-032 / TC-Req-03 (Fail case: Quantity exceeds stock)
    def test_TC_Req_03_request_exceeding_stock_rejected(self):
        """Requisition exceeding available inventory is rejected with 400 and explanatory message."""
        self.client.force_authenticate(user=self.hospital)
        payload = {
            'blood_group': 'B+',
            'component': 'platelets',
            'quantity': 10,  # Available is only 4
            'urgency': 'critical',
        }
        response = self.client.post(self.requests_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_detail = str(response.data.get('error', ''))
        self.assertIn('exceeds available inventory stock', error_detail)

    # BBMS-F-032 / TC-Req-03 (Fail case: Zero stock available)
    def test_TC_Req_03_request_with_zero_stock_rejected(self):
        """Requisition for group/component with 0 stock is rejected."""
        self.client.force_authenticate(user=self.hospital)
        payload = {
            'blood_group': 'AB-',
            'component': 'plasma',
            'quantity': 1,
            'urgency': 'normal',
        }
        response = self.client.post(self.requests_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_detail = str(response.data.get('error', ''))
        self.assertIn('exceeds available inventory stock', error_detail)
