"""
Donation model for the Blood Bank Management System.

# BBMS-F-010: Staff record a donation (donor, date, blood group, component type, quantity).
"""

from django.db import models
from django.conf import settings


class Donation(models.Model):
    """
    Blood donation record.

    Stores each donation event linked to a donor user.
    """

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    COMPONENT_CHOICES = [
        ('whole_blood', 'Whole Blood'),
        ('red_cells', 'Red Cells'),
        ('plasma', 'Plasma'),
        ('platelets', 'Platelets'),
    ]

    # BBMS-F-010
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donations',
        help_text='The donor who provided this blood donation.'
    )
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        help_text='Blood group of the donation.'
    )
    component = models.CharField(
        max_length=20,
        choices=COMPONENT_CHOICES,
        help_text='Component type (whole_blood, red_cells, plasma, platelets).'
    )
    quantity = models.PositiveIntegerField(
        help_text='Quantity donated in units.'
    )
    donation_date = models.DateField(
        help_text='Date of the donation.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when this donation record was created.'
    )

    class Meta:
        ordering = ['-donation_date', '-created_at']

    def __str__(self):
        return f"Donation #{self.id} - {self.donor.username} - {self.blood_group} ({self.quantity} units)"
