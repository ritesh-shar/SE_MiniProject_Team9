"""
Account lockout service logic.

# BBMS-F-003: Lock an account after 5 consecutive failed logins. An admin can unlock it.
"""

from django.conf import settings


# BBMS-F-003
def get_max_failed_attempts():
    """Retrieve maximum allowed consecutive failed attempts before lockout (default: 5)."""
    return getattr(settings, 'MAX_FAILED_LOGIN_ATTEMPTS', 5)


# BBMS-F-003
def record_failed_attempt(user):
    """
    Increment consecutive failed attempts counter.
    Locks the user account permanently once threshold is reached (until unlocked by admin).
    """
    user.failed_login_attempts += 1
    if user.failed_login_attempts >= get_max_failed_attempts():
        user.is_locked = True
    user.save(update_fields=['failed_login_attempts', 'is_locked'])
    return user.is_locked


# BBMS-F-003
def reset_failed_attempts(user):
    """Reset failed login attempts to 0 upon successful authentication."""
    if user.failed_login_attempts > 0:
        user.failed_login_attempts = 0
        user.save(update_fields=['failed_login_attempts'])


# BBMS-F-003
def unlock_user(user):
    """Administrator unlock action: clears locked state and resets attempts counter."""
    user.is_locked = False
    user.failed_login_attempts = 0
    user.save(update_fields=['is_locked', 'failed_login_attempts'])
