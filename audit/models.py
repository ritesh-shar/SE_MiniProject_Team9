"""
AuditLog model for recording security events, authentication attempts, and operational changes.

# BBMS-SR-004: Log all authentication attempts and administrative actions.
# BBMS-NF-005: Audit trail of all inventory and request changes, kept at least 3 years.
"""

from django.db import models
from django.conf import settings


# BBMS-SR-004, BBMS-NF-005
class AuditLog(models.Model):
    """
    Immutable audit trail record.
    Stores authentication attempts, administrative operations, and inventory/request transitions.
    """

    EVENT_TYPES = [
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_FAILED', 'Login Failed'),
        ('ACCOUNT_LOCKED', 'Account Locked'),
        ('ADMIN_ACTION', 'Admin Action'),
        ('STOCK_CHANGE', 'Inventory Stock Change'),
        ('REQUEST_CHANGE', 'Blood Request Transition'),
    ]

    event_type = models.CharField(
        max_length=40,
        choices=EVENT_TYPES,
        help_text='Category of the audited event.',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        help_text='User associated with this event (if authenticated).',
    )
    ip_address = models.CharField(
        max_length=45,
        blank=True,
        default='',
        help_text='Client IP address.',
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='Exact timestamp when event occurred.',
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Human-readable description of the audited event.',
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional contextual metadata (JSON).',
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        user_repr = self.user.username if self.user else 'Anonymous'
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.event_type} - {user_repr}: {self.description[:50]}"
