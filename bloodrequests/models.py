"""
BloodRequest model for hospital blood requests.

# BBMS-F-031: A hospital submits a blood request: group, component, quantity, urgency.
#             Logged with a unique request ID.
"""

from django.db import models
from django.conf import settings


# BBMS-F-031
class BloodRequest(models.Model):
    """
    Hospital blood request record.

    Contains all fields required across Sprint 2:
    submission, staff review, and dispatch issuance.
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

    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('issued', 'Issued'),
    ]

    hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blood_requests',
        help_text='Hospital user submitting the request.'
    )
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        help_text='Requested blood group.'
    )
    component = models.CharField(
        max_length=20,
        choices=COMPONENT_CHOICES,
        help_text='Requested blood component.'
    )
    quantity = models.PositiveIntegerField(
        help_text='Quantity requested in units.'
    )
    urgency = models.CharField(
        max_length=10,
        choices=URGENCY_CHOICES,
        default='normal',
        help_text='Urgency level (normal, urgent, critical).'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Request workflow status.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the request was submitted.'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_requests',
        help_text='Staff member who approved or rejected the request.'
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the review occurred.'
    )
    decision_note = models.TextField(
        blank=True,
        default='',
        help_text='Reviewer notes or reason for approval/rejection.'
    )
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issued_requests',
        help_text='Staff member who issued the blood units.'
    )
    issued_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when blood units were issued.'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.id} - {self.hospital.username} - {self.blood_group} {self.component} ({self.quantity} units) [{self.status}]"
