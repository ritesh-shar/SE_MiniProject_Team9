"""
Unit tests for user authentication and JWT issuance.

# BBMS-F-002: Authenticate with username and password, returning JWT.
Acceptance Test ID: TC-Auth-01
Owner: Ritesh Kumar Sharma (PES2UG24CS404)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthenticationTests(TestCase):
    """Test suite for BBMS-F-002 (TC-Auth-01)."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login'
        self.user = User.objects.create_user(
            username='authuser',
            email='auth@example.com',
            password='CorrectPassword123!',
            role='donor',
        )

    # BBMS-F-002 / TC-Auth-01 (Pass case)
    def test_TC_Auth_01_correct_credentials_return_jwt(self):
        """Correct credentials must return JWT access and refresh tokens."""
        payload = {
            'username': 'authuser',
            'password': 'CorrectPassword123!',
        }
        response = self.client.post(self.login_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # BBMS-F-002 / TC-Auth-01 (Fail case)
    def test_TC_Auth_01_wrong_credentials_rejected(self):
        """Incorrect credentials must be rejected with 401 Unauthorized."""
        payload = {
            'username': 'authuser',
            'password': 'WrongPassword999!',
        }
        response = self.client.post(self.login_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # BBMS-F-002 / Public Endpoint Auth Header Robustness (Added by RKS — Sprint 2 Health Check)
    def test_TC_Auth_01_login_with_expired_or_garbage_auth_header_succeeds(self):
        """
        Public login endpoint must ignore old or invalid Authorization headers.
        Login succeeds and returns JWT tokens even when browser passes expired header.
        """
        payload = {
            'username': 'authuser',
            'password': 'CorrectPassword123!',
        }
        response = self.client.post(
            self.login_url,
            payload,
            format='json',
            HTTP_AUTHORIZATION='Bearer expired_or_garbage_jwt_token_from_prior_session',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

