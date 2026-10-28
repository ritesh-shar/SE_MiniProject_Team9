"""
Service logic for blood stock inventory management.

# BBMS-F-012: Transactional stock update with row-level locking.
"""

from django.db import transaction
from .models import BloodStock


# BBMS-F-012
def increase_stock(blood_group, component, quantity):
    """
    Atomically increase inventory stock for the specified blood group and component.

    Uses select_for_update() for row-level locking to prevent race conditions
    during concurrent donations/issues, per SAD section 3.7 risk mitigation table.

    Returns:
        int: updated units_available count.
    """
    with transaction.atomic():
        # Acquire row lock or create the row under transaction
        stock, created = BloodStock.objects.select_for_update().get_or_create(
            blood_group=blood_group,
            component=component,
            defaults={'units_available': 0}
        )
        stock.units_available += quantity
        stock.save(update_fields=['units_available', 'last_updated'])
        return stock.units_available
