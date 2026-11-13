"""
Signal receivers for authentication auditing.

# BBMS-SR-004: Log all authentication attempts and administrative actions.
"""

from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .services import log_event


def get_client_ip(request):
    if not request:
        return ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


# BBMS-SR-004
@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """Log successful login event."""
    ip = get_client_ip(request)
    log_event(
        event_type='LOGIN_SUCCESS',
        user=user,
        ip_address=ip,
        description=f"User '{user.username}' logged in successfully.",
        extra_data={'role': getattr(user, 'role', 'unknown')},
    )


# BBMS-SR-004
@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    """Log failed login attempt without recording password."""
    ip = get_client_ip(request)
    username = credentials.get('username') if credentials else 'unknown'
    log_event(
        event_type='LOGIN_FAILED',
        user=None,
        ip_address=ip,
        description=f"Failed login attempt for username '{username}'.",
        extra_data={'attempted_username': username},
    )
