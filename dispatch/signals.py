"""
Signal receivers for decoupled dispatch record generation.

# BBMS-F-042: Dispatch record with timestamp, staff ID and recipient details,
#             retrievable by request ID.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DispatchRecord


# BBMS-F-042
@receiver(post_save, sender='bloodrequests.BloodRequest')
def create_dispatch_on_issue(sender, instance, created, **kwargs):
    """
    Automatically generate an immutable DispatchRecord whenever a BloodRequest
    transitions to 'issued' status.

    Decouples RKS's issuance logic from RBR's dispatch persistence.
    """
    if instance.status == 'issued':
        # Avoid duplicate creation if already dispatched
        if not DispatchRecord.objects.filter(request=instance).exists():
            manifest = {
                'blood_group': instance.blood_group,
                'component': instance.component,
                'quantity': instance.quantity,
                'urgency': instance.urgency,
                'decision_note': instance.decision_note,
            }
            DispatchRecord.objects.create(
                request=instance,
                issued_by=instance.issued_by,
                recipient_hospital=instance.hospital,
                details=manifest,
            )
