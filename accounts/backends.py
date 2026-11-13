"""
Authentication backend enforcing account lockout policies.

# BBMS-F-003: Lock an account after 5 consecutive failed logins. An admin can unlock it.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import AuthenticationFailed

from .lockout import record_failed_attempt, reset_failed_attempts

User = get_user_model()


# BBMS-F-003
class LockoutBackend(ModelBackend):
    """
    Custom authentication backend that enforces account lockout rules:
    - Checks whether an account is locked before testing password.
    - Increments failed attempts on bad passwords; locks account permanently on 5th attempt.
    - Resets failed attempts on successful password verification.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if not username or password is None:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Run default password hasher to protect against timing attacks
            User().set_password(password)
            return None

        # Check existing lock state
        if user.is_locked:
            raise AuthenticationFailed(
                "Account locked: 5 consecutive failed login attempts. Contact an administrator to unlock.",
                code="account_locked",
            )

        if user.check_password(password) and self.user_can_authenticate(user):
            reset_failed_attempts(user)
            # Dispatch user_logged_in signal for JWT and session authentication auditing (SR-004)
            from django.contrib.auth.signals import user_logged_in
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            return user
        else:
            is_now_locked = record_failed_attempt(user)
            if is_now_locked:
                raise AuthenticationFailed(
                    "Account locked: 5 consecutive failed login attempts. Contact an administrator to unlock.",
                    code="account_locked",
                )
            return None
