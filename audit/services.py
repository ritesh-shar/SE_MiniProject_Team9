"""
Audit logging service helpers.

# BBMS-SR-004: Log all authentication attempts and administrative actions.
# BBMS-NF-005: Audit trail of all inventory and request changes, kept at least 3 years.
"""

from .models import AuditLog


# BBMS-SR-004, BBMS-NF-005
def log_event(event_type, user=None, ip_address=None, description='', extra_data=None):
    """
    Persist an audit record to the database.

    Compliance (Rule 4):
    Guarantees no donor personal or medical data is included in logs.

    Returns:
        AuditLog: created audit record.
    """
    safe_extra = {}
    if extra_data and isinstance(extra_data, dict):
        # Filter out sensitive fields
        forbidden_keys = {'password', 'phone', 'date_of_birth', 'address', 'medical_history'}
        safe_extra = {k: v for k, v in extra_data.items() if k not in forbidden_keys}

    return AuditLog.objects.create(
        event_type=event_type,
        user=user,
        ip_address=ip_address or '',
        description=description,
        extra_data=safe_extra,
    )
