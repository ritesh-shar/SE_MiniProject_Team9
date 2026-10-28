"""
Views for blood inventory stock tracking.

# BBMS-F-020: Real-time stock count per blood group and component.
# BBMS-SR-002: RBAC enforced (Staff, Hospital, Admin allowed; Donor blocked).
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsHospitalOrStaffOrAdmin
from .models import BloodStock
from .serializers import BloodStockSerializer


class InventoryListView(APIView):
    """
    GET /api/inventory

    Returns the real-time stock count per blood group and component.
    Accessible to Staff, Hospital, and Admin users.
    Blocked for Donors (403 Forbidden).
    """
    # BBMS-SR-002
    permission_classes = [IsHospitalOrStaffOrAdmin]

    # BBMS-F-020
    def get(self, request):
        stocks = BloodStock.objects.all().order_by('blood_group', 'component')
        serializer = BloodStockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
