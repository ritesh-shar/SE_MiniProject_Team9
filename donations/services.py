"""
Service functions for donations: eligibility checks and stock coordination.

# BBMS-F-011: 90-day eligibility check before accepting a donation.
# BBMS-F-012: Increase stock on successful donation.
"""

from datetime import date
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Donation
from inventory.services import increase_stock

User = get_user_model()


# BBMS-F-011
def check_eligibility(donor, donation_date=None):
    """
    Check if a donor is eligible to donate blood.

    Rule: At least 90 days must have passed since their last donation.
    If donation_date is not provided, defaults to today.

    Returns:
        tuple (is_eligible: bool, message: str)
    """
    if donation_date is None:
        donation_date = date.today()

    # Find the most recent donation prior to or on the candidate donation date
    last_donation = (
        Donation.objects.filter(donor=donor, donation_date__lte=donation_date)
        .order_by('-donation_date', '-created_at')
        .first()
    )

    if last_donation:
        delta = (donation_date - last_donation.donation_date).days
        if delta < 90:
            return (
                False,
                f"Donor is not eligible to donate. Only {delta} days since last donation on {last_donation.donation_date}. Minimum 90 days required."
            )

    return True, "Donor is eligible to donate."


# BBMS-F-010, BBMS-F-012
def record_donation(donor, blood_group, component, quantity, donation_date):
    """
    Record a blood donation and atomically increase blood stock.

    Executes within an atomic transaction with row-level locking on inventory.
    """
    with transaction.atomic():
        donation = Donation.objects.create(
            donor=donor,
            blood_group=blood_group,
            component=component,
            quantity=quantity,
            donation_date=donation_date,
        )
        updated_stock = increase_stock(blood_group, component, quantity)
        return donation, updated_stock
