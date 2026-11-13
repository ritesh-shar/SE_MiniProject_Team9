"""
Unit tests for blood request submission and tracking.

# BBMS-F-031: A hospital submits a blood request: group, component, quantity, urgency.
#             Logged with a unique request ID.
Acceptance Test ID: TC-Req-02
Owner: Rithish P M (PR #1)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from bloodrequests.models import BloodRequest

User = get_user_model()


class BloodRequestSubmissionTests(TestCase):
    """Test suite for BBMS-F-031 (TC-Req-02)."""

    def setUp(self):
        self.client = APIClient()
        self.endpoint_slash = '/api/requests/'
        self.endpoint_noslash = '/api/requests'

        # Hospital user
        self.hospital = User.objects.create_user(
            username='city_hospital',
            email='hospital@citymed.org',
            password='HospitalPass123!',
            role='hospital',
        )

        # Other hospital user
        self.other_hospital = User.objects.create_user(
            username='metro_hospital',
            email='metro@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        # Staff user
        self.staff = User.objects.create_user(
            username='staff_john',
            email='staff@bbms.local',
            password='StaffPass123!',
            role='staff',
        )

        # Donor user
        self.donor = User.objects.create_user(
            username='regular_donor',
            email='donor@gmail.com',
            password='DonorPass123!',
            role='donor',
        )

        # Seed initial inventory stock for requisitions
        from inventory.models import BloodStock
        BloodStock.objects.create(blood_group='O+', component='whole_blood', units_available=20)
        BloodStock.objects.create(blood_group='A-', component='platelets', units_available=20)
        BloodStock.objects.create(blood_group='B+', component='red_cells', units_available=20)
        BloodStock.objects.create(blood_group='AB-', component='plasma', units_available=20)

    # BBMS-F-031 / TC-Req-02 (Pass case with trailing slash)
    def test_TC_Req_02_hospital_submits_valid_blood_request(self):
        """Hospital submits a valid blood request with group, component, quantity, urgency."""
        self.client.force_authenticate(user=self.hospital)
        payload = {
            'blood_group': 'O+',
            'component': 'whole_blood',
            'quantity': 2,
            'urgency': 'urgent',
        }
        response = self.client.post(self.endpoint_slash, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('requestId', response.data)
        request_id = response.data['requestId']

        # Verify database record
        req = BloodRequest.objects.get(id=request_id)
        self.assertEqual(req.hospital, self.hospital)
        self.assertEqual(req.blood_group, 'O+')
        self.assertEqual(req.component, 'whole_blood')
        self.assertEqual(req.quantity, 2)
        self.assertEqual(req.urgency, 'urgent')
        self.assertEqual(req.status, 'pending')

    # BBMS-F-031 / TC-Req-02 (Pass case without trailing slash)
    def test_TC_Req_02_hospital_submits_request_without_trailing_slash(self):
        """Hospital submits request to exact path /api/requests without trailing slash."""
        self.client.force_authenticate(user=self.hospital)
        payload = {
            'blood_group': 'A-',
            'component': 'platelets',
            'quantity': 1,
            'urgency': 'critical',
        }
        response = self.client.post(self.endpoint_noslash, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('requestId', response.data)
        req = BloodRequest.objects.get(id=response.data['requestId'])
        self.assertEqual(req.urgency, 'critical')

    # BBMS-F-031 / TC-Req-02 (Fail case: validation error for missing field)
    def test_TC_Req_02_missing_field_rejected(self):
        """Submission missing required quantity must be rejected with 400 Bad Request."""
        self.client.force_authenticate(user=self.hospital)
        payload = {
            'blood_group': 'B+',
            'component': 'red_cells',
            # missing quantity
        }
        response = self.client.post(self.endpoint_slash, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('code'), 'VALIDATION_ERROR')

    # BBMS-SR-002 / TC-Req-02 (Fail case: Donor cannot submit request)
    def test_TC_Req_02_donor_cannot_submit_request(self):
        """Donor role must be forbidden from submitting blood requests."""
        self.client.force_authenticate(user=self.donor)
        payload = {
            'blood_group': 'O+',
            'component': 'whole_blood',
            'quantity': 1,
        }
        response = self.client.post(self.endpoint_slash, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # BBMS-F-031 / TC-Req-02 (List visibility: hospital sees only own requests)
    def test_TC_Req_02_hospital_sees_only_own_requests(self):
        """Hospital listing /api/requests sees only requests submitted by their own hospital."""
        BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='O+',
            component='whole_blood',
            quantity=2,
            urgency='normal',
        )
        BloodRequest.objects.create(
            hospital=self.other_hospital,
            blood_group='AB-',
            component='plasma',
            quantity=5,
            urgency='urgent',
        )

        self.client.force_authenticate(user=self.hospital)
        response = self.client.get(self.endpoint_noslash)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['hospital_name'], 'city_hospital')

    # BBMS-F-031 / TC-Req-02 (List visibility: staff sees all requests)
    def test_TC_Req_02_staff_sees_all_requests(self):
        """Staff listing /api/requests sees requests from all hospitals."""
        BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='O+',
            component='whole_blood',
            quantity=2,
            urgency='normal',
        )
        BloodRequest.objects.create(
            hospital=self.other_hospital,
            blood_group='AB-',
            component='plasma',
            quantity=5,
            urgency='urgent',
        )

        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.endpoint_noslash)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
