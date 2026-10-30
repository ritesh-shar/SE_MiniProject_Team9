"""
Blood inventory search view.

# BBMS-F-030: Search available blood units by blood group and component.
# BBMS-SR-002: RBAC enforced (Staff, Hospital, Admin allowed; Donor blocked).
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsHospitalOrStaffOrAdmin
from .models import BloodStock
from .serializers import BloodStockSerializer


class BloodSearchView(APIView):
    """
    GET /api/inventory/search?bloodGroup=&component=

    Search available blood units by blood group and component type.
    Accessible to Staff, Hospital, and Admin users.
    Blocked for Donors (403 Forbidden).
    """
    # BBMS-SR-002
    permission_classes = [IsHospitalOrStaffOrAdmin]

    # BBMS-F-030
    def get(self, request):
        blood_group = request.query_params.get('bloodGroup') or request.query_params.get('blood_group')
        component = request.query_params.get('component')

        queryset = BloodStock.objects.all()

        if blood_group:
            queryset = queryset.filter(blood_group=blood_group.strip())
        if component:
            queryset = queryset.filter(component=component.strip())

        queryset = queryset.order_by('blood_group', 'component')
        serializer = BloodStockSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
