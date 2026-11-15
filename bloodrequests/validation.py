"""
Stock validation logic for blood requests.

# BBMS-F-032: Reject a request whose quantity exceeds available stock for that group, with a message.
Owner: Ritesh Babu Reddy (PR #4)
"""

from inventory.models import BloodStock


# BBMS-F-032
def validate_request_stock(blood_group, component, quantity):
    """
    Validate that sufficient inventory stock exists for the requested blood group and component.

    Queries BloodStock to verify units_available >= quantity.
    Rejects exceeding requests with a clear, descriptive message.

    Returns:
        tuple (is_valid: bool, error_message: str or None)
    """
    stock = BloodStock.objects.filter(
        blood_group=blood_group,
        component=component,
    ).first()

    available = stock.units_available if stock else 0

    if available < quantity:
        return (
            False,
            f"Requested quantity ({quantity} unit(s)) exceeds available inventory stock ({available} unit(s)) for {blood_group} {component}.",
        )

    return True, None
