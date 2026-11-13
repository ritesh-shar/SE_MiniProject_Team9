"""
Unit tests for staff blood request review (approval and rejection).

# BBMS-F-040: Staff approve or reject a pending request. Status is visible to the requester.
Acceptance Test ID: TC-Iss-01
Owner: Ritesh Kumar Sharma (PR #2)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from bloodrequests.models import BloodRequest

User = get_user_model()


class BloodRequestReviewTests(TestCase):
    """Test suite for BBMS-F-040 (TC-Iss-01)."""

    def setUp(self):
        self.client = APIClient()

        self.hospital = User.objects.create_user(
            username='general_hospital',
            email='general@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        self.staff = User.objects.create_user(
            username='staff_mary',
            email='mary@bbms.org',
            password='StaffPass123!',
            role='staff',
        )

        self.donor = User.objects.create_user(
            username='donor_dave',
            email='dave@donor.org',
            password='DonorPass123!',
            role='donor',
        )

        # Pending request for testing
        self.pending_request = BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='O+',
            component='whole_blood',
            quantity=2,
            urgency='urgent',
            status='pending',
        )

    # BBMS-F-040 / TC-Iss-01 (Pass case: Staff approves request)
    def test_TC_Iss_01_staff_approve_pending_request(self):
        """Staff member successfully approves a pending blood request."""
        self.client.force_authenticate(user=self.staff)
        url = f"/api/requests/{self.pending_request.id}/review"
        payload = {
            'decision': 'approved',
            'decision_note': 'Approved for trauma patient.',
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pending_request.refresh_from_db()
        self.assertEqual(self.pending_request.status, 'approved')
        self.assertEqual(self.pending_request.reviewed_by, self.staff)
        self.assertEqual(self.pending_request.decision_note, 'Approved for trauma patient.')
        self.assertIsNotNone(self.pending_request.reviewed_at)

    # BBMS-F-040 / TC-Iss-01 (Pass case: Staff rejects request with reason)
    def test_TC_Iss_01_staff_reject_pending_request(self):
        """Staff member successfully rejects a pending blood request with notes."""
        self.client.force_authenticate(user=self.staff)
        url = f"/api/requests/{self.pending_request.id}/review"
        payload = {
            'decision': 'rejected',
            'decision_note': 'Unavailable units for requested type.',
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pending_request.refresh_from_db()
        self.assertEqual(self.pending_request.status, 'rejected')
        self.assertEqual(self.pending_request.decision_note, 'Unavailable units for requested type.')

    # BBMS-F-040 / TC-Iss-01 (Fail case: Cannot review non-pending request)
    def test_TC_Iss_01_cannot_review_already_approved_request(self):
        """Cannot re-review a request that is already approved or rejected."""
        self.pending_request.status = 'approved'
        self.pending_request.save()

        self.client.force_authenticate(user=self.staff)
        url = f"/api/requests/{self.pending_request.id}/review"
        payload = {'decision': 'rejected'}
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('code'), 'INVALID_STATUS')

    # BBMS-SR-002 / TC-Iss-01 (Fail case: Donor cannot review)
    def test_TC_Iss_01_donor_forbidden_from_review(self):
        """Donors are forbidden from approving or rejecting blood requests."""
        self.client.force_authenticate(user=self.donor)
        url = f"/api/requests/{self.pending_request.id}/review"
        payload = {'decision': 'approved'}
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
