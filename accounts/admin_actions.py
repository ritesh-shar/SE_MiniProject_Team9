"""
Django admin actions for user account management.

# BBMS-F-003: Lock an account after 5 consecutive failed logins. An admin can unlock it.
"""

from django.contrib import admin
from .lockout import unlock_user


# BBMS-F-003
@admin.action(description='Unlock selected user accounts')
def unlock_user_accounts(modeladmin, request, queryset):
    """Admin action to unlock selected locked user accounts and reset failure counters."""
    unlocked_count = 0
    for user in queryset:
        unlock_user(user)
        unlocked_count += 1

    modeladmin.message_user(
        request,
        f"Successfully unlocked {unlocked_count} user account(s).",
    )
