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


# ---------------------------------------------------------------------------
# Stock Decrement Logic (Ritesh Kumar Sharma — PR #2)
# ---------------------------------------------------------------------------
# BBMS-F-041
def decrease_stock(blood_group, component, quantity):
    """
    Atomically decrease inventory stock for the specified blood group and component.

    Uses select_for_update() for row-level locking to prevent race conditions.
    Ensures units_available cannot drop below zero.

    Raises:
        ValueError: If requested quantity exceeds units_available.

    Returns:
        int: updated units_available count.
    """
    with transaction.atomic():
        stock = BloodStock.objects.select_for_update().filter(
            blood_group=blood_group,
            component=component,
        ).first()

        if not stock or stock.units_available < quantity:
            available = stock.units_available if stock else 0
            raise ValueError(
                f"Insufficient stock for {blood_group} {component}. Available: {available}, requested: {quantity}."
            )

        stock.units_available -= quantity
        stock.save(update_fields=['units_available', 'last_updated'])
        return stock.units_available

