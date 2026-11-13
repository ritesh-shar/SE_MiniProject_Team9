"""
Unit tests for account lockout and admin unlock functionality.

# BBMS-F-003: Lock an account after 5 consecutive failed logins. An admin can unlock it.
Acceptance Test ID: TC-Auth-02
Owner: Reyansh (PR #3)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from accounts.lockout import unlock_user

User = get_user_model()


class AccountLockoutTests(TestCase):
    """Test suite for BBMS-F-003 (TC-Auth-02)."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login'

        self.user = User.objects.create_user(
            username='lockout_victim',
            email='victim@bbms.org',
            password='ValidPassword123!',
            role='donor',
        )

        self.admin = User.objects.create_user(
            username='admin_hero',
            email='hero@bbms.org',
            password='AdminPassword123!',
            role='admin',
            is_staff=True,
        )

    # BBMS-F-003 / TC-Auth-02
    def test_TC_Auth_02_four_failed_logins_do_not_lock_account(self):
        """Four consecutive failed login attempts do not trigger account lockout."""
        payload = {'username': 'lockout_victim', 'password': 'WrongPassword!'}

        for _ in range(4):
            response = self.client.post(self.login_url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 4)
        self.assertFalse(self.user.is_locked)

    # BBMS-F-003 / TC-Auth-02
    def test_TC_Auth_02_fifth_failed_login_locks_account_permanently(self):
        """Fifth consecutive failed attempt locks the account and rejects subsequent valid logins."""
        wrong_payload = {'username': 'lockout_victim', 'password': 'WrongPassword!'}
        valid_payload = {'username': 'lockout_victim', 'password': 'ValidPassword123!'}

        # 5 failed attempts
        for i in range(5):
            response = self.client.post(self.login_url, wrong_payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 5)
        self.assertTrue(self.user.is_locked)

        # 6th attempt with CORRECT password must now be rejected due to lock
        locked_response = self.client.post(self.login_url, valid_payload, format='json')
        self.assertEqual(locked_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('locked', str(locked_response.data).lower())

    # BBMS-F-003 / TC-Auth-02
    def test_TC_Auth_02_admin_unlocks_locked_account(self):
        """Admin unlocks a locked account, allowing successful login thereafter."""
        # Manually lock user
        self.user.is_locked = True
        self.user.failed_login_attempts = 5
        self.user.save()

        # Admin executes unlock
        unlock_user(self.user)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_locked)
        self.assertEqual(self.user.failed_login_attempts, 0)

        # User logs in with valid credentials successfully
        valid_payload = {'username': 'lockout_victim', 'password': 'ValidPassword123!'}
        response = self.client.post(self.login_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    # BBMS-F-003 / TC-Auth-02
    def test_TC_Auth_02_successful_login_resets_failed_counter(self):
        """A successful login prior to reaching 5 failures resets the failed attempts counter."""
        wrong_payload = {'username': 'lockout_victim', 'password': 'WrongPassword!'}
        valid_payload = {'username': 'lockout_victim', 'password': 'ValidPassword123!'}

        # 3 failed attempts
        for _ in range(3):
            self.client.post(self.login_url, wrong_payload, format='json')

        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 3)

        # 4th attempt is successful
        success_response = self.client.post(self.login_url, valid_payload, format='json')
        self.assertEqual(success_response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)
        self.assertFalse(self.user.is_locked)
