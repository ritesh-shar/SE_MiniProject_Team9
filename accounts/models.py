"""
User model with role-based access for the Blood Bank Management System.

# BBMS-F-001: Donor registration with personal details, blood group, and contact info.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that adds a role field and blood-bank-specific fields.

    Roles: donor, staff, hospital, admin.
    Self-registration (POST /api/auth/register) always creates a 'donor'.
    Staff, Hospital, and Admin accounts are created via Django admin or seed_demo.
    """

    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('staff', 'Staff'),
        ('hospital', 'Hospital'),
        ('admin', 'Admin'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # BBMS-F-001
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='donor',
        help_text='User role: donor, staff, hospital, or admin.',
    )
    blood_group = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True,
        help_text='Blood group (required for donors).',
    )
    phone = models.CharField(
        max_length=15, blank=True,
        help_text='Contact phone number.',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
