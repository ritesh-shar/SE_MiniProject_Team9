"""
Stock validation helper for BloodRequest creation.
BBMS-F-032: Stub in PR 1 (RPM), real implementation in PR 4 (RBR).
"""


def validate_request_stock(blood_group, component, quantity):
    """
    Validates if sufficient stock exists for the requested blood group and component.
    Stub implementation for PR 1; real inventory check implemented in PR 4.
    Returns (is_valid: bool, error_message: str | None).
    """
    if quantity <= 0:
        return False, "Requested quantity must be at least 1 unit."
    return True, None
