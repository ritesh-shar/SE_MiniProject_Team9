"""
Unit tests for donor registration.

# BBMS-F-001: Donor registration with personal details, blood group, contact information.
Acceptance Test ID: TC-Reg-01
Owner: Ritesh Kumar Sharma (PES2UG24CS404)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class DonorRegistrationTests(TestCase):
    """Test suite for BBMS-F-001 (TC-Reg-01)."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register'

    # BBMS-F-001 / TC-Reg-01 (Pass case)
    def test_TC_Reg_01_valid_registration_creates_donor(self):
        """A new donor registers with valid personal details, blood group, and contact info."""
        payload = {
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'SecurePassword123!',
            'blood_group': 'O+',
            'phone': '+91-9876543210',
        }
        response = self.client.post(self.register_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('userId', response.data)
        self.assertEqual(response.data['username'], 'johndoe')

        # Verify database record
        user = User.objects.get(username='johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')
        self.assertEqual(user.blood_group, 'O+')
        self.assertEqual(user.phone, '+91-9876543210')
        self.assertEqual(user.role, 'donor')  # Self-registration defaults to donor

    # BBMS-F-001 / TC-Reg-01 (Fail case)
    def test_TC_Reg_01_duplicate_registration_rejected(self):
        """Registration with an already existing username must be rejected."""
        User.objects.create_user(
            username='existingdonor',
            email='existing@example.com',
            password='Password123!',
            role='donor',
        )

        payload = {
            'username': 'existingdonor',
            'email': 'another@example.com',
            'password': 'Password456!',
            'blood_group': 'A+',
            'phone': '+91-9876543219',
        }
        response = self.client.post(self.register_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('code'), 'VALIDATION_ERROR')

    # BBMS-F-001 / Public Endpoint Auth Header Robustness
    def test_TC_Reg_01_registration_with_expired_or_garbage_auth_header_succeeds(self):
        """
        Public registration must ignore Authorization headers.
        Registration succeeds even when an expired or garbage Authorization header is sent.
        """
        payload = {
            'username': 'headerdonor',
            'email': 'headerdonor@example.com',
            'password': 'SecurePassword123!',
            'blood_group': 'B+',
            'phone': '+91-9123456780',
        }
        response = self.client.post(
            self.register_url,
            payload,
            format='json',
            HTTP_AUTHORIZATION='Bearer expired_or_garbage_jwt_token',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('userId', response.data)
        self.assertEqual(response.data['username'], 'headerdonor')

        # Verify database record
        user = User.objects.get(username='headerdonor')
        self.assertEqual(user.email, 'headerdonor@example.com')
        self.assertEqual(user.blood_group, 'B+')
        self.assertEqual(user.role, 'donor')
