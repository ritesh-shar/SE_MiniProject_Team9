"""
Unit tests for dispatch record generation and retrieval.

# BBMS-F-042: Dispatch record with timestamp, staff ID and recipient details, retrievable by request ID.
Acceptance Test ID: TC-Iss-03
Owner: Ritesh Babu Reddy (PR #4)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from inventory.models import BloodStock
from bloodrequests.models import BloodRequest
from dispatch.models import DispatchRecord

User = get_user_model()


class DispatchTrackingTests(TestCase):
    """Test suite for BBMS-F-042 (TC-Iss-03)."""

    def setUp(self):
        self.client = APIClient()

        self.hospital = User.objects.create_user(
            username='apollo_hospital',
            email='apollo@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        self.other_hospital = User.objects.create_user(
            username='fortis_hospital',
            email='fortis@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        self.staff = User.objects.create_user(
            username='staff_dispatcher',
            email='dispatch@bbms.org',
            password='StaffPass123!',
            role='staff',
        )

        BloodStock.objects.create(blood_group='O+', component='whole_blood', units_available=20)

        self.approved_request = BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='O+',
            component='whole_blood',
            quantity=2,
            urgency='urgent',
            status='approved',
            reviewed_by=self.staff,
        )

    # BBMS-F-042 / TC-Iss-03 (Pass case: Signal creates dispatch record on issue)
    def test_TC_Iss_03_dispatch_record_created_on_issue_retrievable_by_id(self):
        """Issuing an approved request triggers signal to create DispatchRecord, retrievable by request ID."""
        self.client.force_authenticate(user=self.staff)

        # Issue the blood request
        issue_response = self.client.post(f"/api/requests/{self.approved_request.id}/issue")
        self.assertEqual(issue_response.status_code, status.HTTP_200_OK)

        # Verify dispatch record automatically created by signal
        dispatch = DispatchRecord.objects.filter(request=self.approved_request).first()
        self.assertIsNotNone(dispatch)
        self.assertEqual(dispatch.recipient_hospital, self.hospital)
        self.assertEqual(dispatch.issued_by, self.staff)

        # Retrieve record via GET /api/dispatch/<request_id>
        get_response = self.client.get(f"/api/dispatch/{self.approved_request.id}")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['request_id'], self.approved_request.id)
        self.assertEqual(get_response.data['issued_by_name'], 'staff_dispatcher')
        self.assertEqual(get_response.data['recipient_hospital_name'], 'apollo_hospital')
        self.assertEqual(get_response.data['details']['blood_group'], 'O+')

    # BBMS-F-042 / TC-Iss-03 (Fail case: Unfulfilled request has no dispatch record)
    def test_TC_Iss_03_unfulfilled_request_returns_404(self):
        """Querying dispatch for an unissued blood request returns 404 Not Found."""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(f"/api/dispatch/{self.approved_request.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # BBMS-SR-002 / TC-Iss-03 (Fail case: Hospital cannot view other hospital dispatches)
    def test_TC_Iss_03_hospital_cannot_view_other_hospital_dispatch(self):
        """Hospital role is forbidden from retrieving dispatches destined for other hospitals."""
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/requests/{self.approved_request.id}/issue")

        # Other hospital tries to view Apollo's dispatch
        self.client.force_authenticate(user=self.other_hospital)
        response = self.client.get(f"/api/dispatch/{self.approved_request.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
