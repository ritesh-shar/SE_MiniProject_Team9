"""
Inventory alert computations for blood unit expiry and low-stock thresholds.

# BBMS-F-021: Flag blood units expiring within 5 days (alert list).
# BBMS-F-022: Low-stock alert when a blood group falls below a threshold configurable per blood group.
Owner: Ritesh Babu Reddy (PR #4)
"""

from datetime import date, timedelta
from django.conf import settings
from django.db.models import Sum

from donations.models import Donation
from .models import BloodStock, StockThreshold

# Standard biological shelf life per component (in days)
# Recorded in docs/DEVIATIONS.md per prompt rule #5
SHELF_LIFE_DAYS = {
    'whole_blood': 35,
    'red_cells': 42,
    'platelets': 5,
    'plasma': 365,
}


# BBMS-F-021
def get_expiring_units(within_days=5, reference_date=None):
    """
    Compute blood unit expiry dates based on donation date plus component shelf life.
    Flags units expiring within `within_days` days from reference_date.

    Returns:
        list of dicts containing donation ID, blood group, component, expiry date, days left.
    """
    if reference_date is None:
        reference_date = date.today()

    expiring_list = []
    donations = Donation.objects.all().order_by('donation_date')

    for d in donations:
        shelf_life = SHELF_LIFE_DAYS.get(d.component, 35)
        expiry_date = d.donation_date + timedelta(days=shelf_life)
        days_left = (expiry_date - reference_date).days

        # Flag if expiring within window (0 <= days_left <= within_days) or already expired
        if days_left <= within_days:
            expiring_list.append({
                'donation_id': d.id,
                'donor_username': d.donor.username,
                'blood_group': d.blood_group,
                'component': d.component,
                'quantity': d.quantity,
                'donation_date': d.donation_date.isoformat(),
                'expiry_date': expiry_date.isoformat(),
                'days_until_expiry': days_left,
                'is_expired': days_left < 0,
            })

    return expiring_list


# BBMS-F-022
def get_low_stock_groups(default_threshold=None):
    """
    Evaluate total on-hand blood stock per blood group against configurable thresholds.
    Flags blood groups falling below minimum unit thresholds.

    Returns:
        list of dicts containing blood group, current stock, threshold, and deficit.
    """
    if default_threshold is None:
        default_threshold = getattr(settings, 'DEFAULT_STOCK_THRESHOLD', 10)

    # Pre-load custom thresholds from database
    thresholds = {
        st.blood_group: st.min_units
        for st in StockThreshold.objects.all()
    }

    all_groups = [g[0] for g in BloodStock.BLOOD_GROUP_CHOICES]
    low_stock_list = []

    for bg in all_groups:
        total = (
            BloodStock.objects.filter(blood_group=bg)
            .aggregate(total=Sum('units_available'))['total']
            or 0
        )
        threshold = thresholds.get(bg, default_threshold)

        if total < threshold:
            low_stock_list.append({
                'blood_group': bg,
                'current_units': total,
                'threshold_units': threshold,
                'deficit': threshold - total,
                'severity': 'critical' if total == 0 else 'warning',
            })

    return low_stock_list
