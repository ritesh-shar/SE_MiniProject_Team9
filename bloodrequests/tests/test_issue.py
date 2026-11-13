"""
Unit tests for blood request issuance and stock decrement.

# BBMS-F-041: Decrement inventory stock when an approved request is issued.
Acceptance Test ID: TC-Iss-02
Owner: Ritesh Kumar Sharma (PR #2)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from inventory.models import BloodStock
from bloodrequests.models import BloodRequest

User = get_user_model()


class BloodRequestIssueTests(TestCase):
    """Test suite for BBMS-F-041 (TC-Iss-02)."""

    def setUp(self):
        self.client = APIClient()

        self.hospital = User.objects.create_user(
            username='metro_hospital',
            email='metro@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        self.staff = User.objects.create_user(
            username='staff_alex',
            email='alex@bbms.org',
            password='StaffPass123!',
            role='staff',
        )

        self.donor = User.objects.create_user(
            username='donor_dan',
            email='dan@donor.org',
            password='DonorPass123!',
            role='donor',
        )

        # Seed initial inventory stock: 10 units of A+ Whole Blood
        self.stock = BloodStock.objects.create(
            blood_group='A+',
            component='whole_blood',
            units_available=10,
        )

        # Approved blood request for 3 units
        self.approved_request = BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='A+',
            component='whole_blood',
            quantity=3,
            urgency='urgent',
            status='approved',
            reviewed_by=self.staff,
        )

    # BBMS-F-041 / TC-Iss-02 (Pass case: Issue decrements stock)
    def test_TC_Iss_02_issue_request_decrements_inventory_stock(self):
        """Issuing an approved blood request atomically decrements available inventory stock."""
        self.client.force_authenticate(user=self.staff)
        url = f"/api/requests/{self.approved_request.id}/issue"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['remaining_stock'], 7)

        # Verify database record
        self.approved_request.refresh_from_db()
        self.assertEqual(self.approved_request.status, 'issued')
        self.assertEqual(self.approved_request.issued_by, self.staff)
        self.assertIsNotNone(self.approved_request.issued_at)

        # Verify stock in DB decreased from 10 to 7
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.units_available, 7)

    # BBMS-F-041 / TC-Iss-02 (Fail case: Cannot drop stock below zero)
    def test_TC_Iss_02_issue_cannot_drop_stock_below_zero(self):
        """Issuance fails with 400 Bad Request if requested volume exceeds current inventory."""
        self.stock.units_available = 2  # Only 2 units in stock, but request needs 3
        self.stock.save()

        self.client.force_authenticate(user=self.staff)
        url = f"/api/requests/{self.approved_request.id}/issue"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('code'), 'INSUFFICIENT_STOCK')

        # Stock unchanged
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.units_available, 2)

        # Request status remains approved
        self.approved_request.refresh_from_db()
        self.assertEqual(self.approved_request.status, 'approved')

    # BBMS-F-041 / TC-Iss-02 (Fail case: Cannot issue pending request)
    def test_TC_Iss_02_cannot_issue_unapproved_request(self):
        """Cannot issue a request whose status is 'pending'."""
        self.approved_request.status = 'pending'
        self.approved_request.save()

        self.client.force_authenticate(user=self.staff)
        url = f"/api/requests/{self.approved_request.id}/issue"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('code'), 'INVALID_STATUS')

    # BBMS-SR-002 / TC-Iss-02 (Fail case: Hospital cannot issue)
    def test_TC_Iss_02_hospital_forbidden_from_issuing(self):
        """Hospital role is forbidden from issuing blood requests."""
        self.client.force_authenticate(user=self.hospital)
        url = f"/api/requests/{self.approved_request.id}/issue"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
