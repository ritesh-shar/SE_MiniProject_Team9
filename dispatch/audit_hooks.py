"""
Audit hooks for tracking inventory stock and requisition changes.

# BBMS-NF-005: Audit trail of all inventory and request changes, kept at least 3 years.
Owner: Ritesh Babu Reddy (PR #4)
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from audit.services import log_event


# BBMS-NF-005
@receiver(post_save, sender='inventory.BloodStock')
def audit_stock_change(sender, instance, created, **kwargs):
    """Log an audit entry whenever blood stock changes."""
    log_event(
        event_type='STOCK_CHANGE',
        user=None,
        description=f"Inventory stock updated: {instance.blood_group} {instance.component} is now {instance.units_available} unit(s).",
        extra_data={
            'blood_group': instance.blood_group,
            'component': instance.component,
            'units_available': instance.units_available,
        },
    )


# BBMS-NF-005
@receiver(post_save, sender='bloodrequests.BloodRequest')
def audit_request_change(sender, instance, created, **kwargs):
    """Log an audit entry whenever a blood request is created or status transitions."""
    action = 'created' if created else f"status changed to '{instance.status}'"
    actor = instance.issued_by or instance.reviewed_by or instance.hospital

    log_event(
        event_type='REQUEST_CHANGE',
        user=actor,
        description=f"Blood requisition #{instance.id} {action} ({instance.blood_group} {instance.component}, {instance.quantity} units).",
        extra_data={
            'request_id': instance.id,
            'status': instance.status,
            'hospital': instance.hospital.username,
            'blood_group': instance.blood_group,
            'component': instance.component,
            'quantity': instance.quantity,
        },
    )
