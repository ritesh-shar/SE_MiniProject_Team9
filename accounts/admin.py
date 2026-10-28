"""Django admin configuration for the accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin view for the custom User model with role and blood group fields."""

    list_display = ['username', 'email', 'role', 'blood_group', 'is_active']
    list_filter = ['role', 'blood_group', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('BBMS Fields', {'fields': ('role', 'blood_group', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('BBMS Fields', {'fields': ('role', 'blood_group', 'phone')}),
    )
