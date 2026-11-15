"""
API views for inventory stock alerts and expiry warnings.

# BBMS-F-021: Flag blood units expiring within 5 days (alert list).
# BBMS-F-022: Low-stock alert when a blood group falls below a threshold configurable per blood group.
Owner: Ritesh Babu Reddy (PR #4)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .alerts import get_expiring_units, get_low_stock_groups


# BBMS-F-021
class ExpiryAlertView(APIView):
    """
    GET /api/inventory/alerts/expiry
    Retrieve list of blood units expiring within 5 days.
    Accessible to staff, admin, and hospital roles.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ('staff', 'admin', 'hospital'):
            return Response(
                {'error': 'Permission denied. Staff, admin, or hospital role required.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        days_param = request.query_params.get('days', 5)
        try:
            days = int(days_param)
        except ValueError:
            days = 5

        alerts = get_expiring_units(within_days=days)
        return Response(
            {
                'expiring_units_count': len(alerts),
                'threshold_days': days,
                'alerts': alerts,
            },
            status=status.HTTP_200_OK,
        )


# BBMS-F-022
class LowStockAlertView(APIView):
    """
    GET /api/inventory/alerts/low-stock
    Retrieve list of blood groups below minimum configurable stock thresholds.
    Accessible to staff, admin, and hospital roles.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ('staff', 'admin', 'hospital'):
            return Response(
                {'error': 'Permission denied. Staff, admin, or hospital role required.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        alerts = get_low_stock_groups()
        return Response(
            {
                'low_stock_groups_count': len(alerts),
                'alerts': alerts,
            },
            status=status.HTTP_200_OK,
        )
