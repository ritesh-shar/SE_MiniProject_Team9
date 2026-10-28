"""
Security and JWT token validation tests.

# BBMS-SR-003: Salted password hashing in database.
# BBMS-SR-005: JWT tokens with expiry enforcement.
Acceptance Test IDs: TC-Sec-03, TC-Sec-05
Owner: Reyansh (PES2UG24CS401)
"""

from datetime import datetime, timezone, timedelta
import jwt
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class SecurityAndJWTTests(TestCase):
    """Test suite for BBMS-SR-003 (TC-Sec-03) and BBMS-SR-005 (TC-Sec-05)."""

    def setUp(self):
        self.client = APIClient()
        self.raw_password = 'SuperSecretPassword123!'
        self.user = User.objects.create_user(
            username='securityuser',
            email='sec@bbms.local',
            password=self.raw_password,
            role='donor',
        )

    # BBMS-SR-003 / TC-Sec-03
    def test_TC_Sec_03_password_is_hashed(self):
        """Database stores salted hash; plaintext password must NEVER appear in DB."""
        fresh_user = User.objects.get(id=self.user.id)
        # Verify it's not plaintext
        self.assertNotEqual(fresh_user.password, self.raw_password)
        # Verify it uses Django's PBKDF2 hasher
        self.assertTrue(
            fresh_user.password.startswith('pbkdf2_sha256$'),
            f"Expected PBKDF2 hash, found: {fresh_user.password[:20]}"
        )
        # Verify password check functions correctly
        self.assertTrue(fresh_user.check_password(self.raw_password))
        self.assertFalse(fresh_user.check_password('WrongPassword'))

    # BBMS-SR-005 / TC-Sec-05 (Fail case: expired token)
    def test_TC_Sec_05_expired_token_rejected(self):
        """An expired JWT token must be rejected with 401 Unauthorized."""
        # Craft a token whose expiry is 10 minutes in the past
        past_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        payload = {
            'user_id': self.user.id,
            'exp': past_time,
            'token_type': 'access',
            'jti': 'test_expired_jti_123',
        }
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get('/api/donations/history')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # BBMS-SR-005 / TC-Sec-05 (Pass case: valid token)
    def test_TC_Sec_05_valid_token_accepted(self):
        """A valid, unexpired JWT access token must grant access to authorized endpoints."""
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.get('/api/donations/history')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
