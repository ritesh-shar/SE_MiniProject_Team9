"""
DispatchRecord model for tracking blood unit handoff to recipient hospitals.

# BBMS-F-042: Dispatch record with timestamp, staff ID and recipient details,
#             retrievable by request ID.
"""

from django.db import models
from django.conf import settings


# BBMS-F-042
class DispatchRecord(models.Model):
    """
    Official dispatch documentation generated upon blood issuance.
    Contains timestamp, dispatching staff ID, and recipient hospital metadata.
    """

    request = models.OneToOneField(
        'bloodrequests.BloodRequest',
        on_delete=models.CASCADE,
        related_name='dispatch_record',
        help_text='Blood requisition fulfilled by this dispatch.',
    )
    dispatched_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when blood units were officially dispatched.',
    )
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dispatches_issued',
        help_text='Staff member executing the physical dispatch.',
    )
    recipient_hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dispatches_received',
        help_text='Hospital user receiving the blood units.',
    )
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text='Manifest details (blood group, component, quantity, notes).',
    )

    class Meta:
        ordering = ['-dispatched_at']

    def __str__(self):
        return f"Dispatch #{self.id} for Request #{self.request_id} -> {self.recipient_hospital.username} ({self.dispatched_at.strftime('%Y-%m-%d %H:%M')})"
