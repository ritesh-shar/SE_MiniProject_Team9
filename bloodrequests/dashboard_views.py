"""
Admin dashboard views.

# BBMS-F-050: Admin dashboard: current stock, pending requests, recent donations.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Sum
from inventory.models import BloodStock
from donations.models import Donation
from donations.serializers import DonationSerializer
from .models import BloodRequest
from .serializers import BloodRequestSerializer


# BBMS-F-050
class AdminDashboardView(APIView):
    """
    GET /api/admin/dashboard

    Aggregated operational view for administrators:
    - Current blood stock totals and breakdown
    - Pending blood requests
    - Recent donations
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ('admin', 'staff'):
            return Response(
                {'error': 'Administrator or staff access required.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 1. Current stock
        stocks = BloodStock.objects.all().order_by('blood_group', 'component')
        total_units = stocks.aggregate(total=Sum('units_available'))['total'] or 0
        stock_list = [
            {
                'blood_group': s.blood_group,
                'component': s.component,
                'units_available': s.units_available,
                'last_updated': s.last_updated.isoformat() if s.last_updated else None,
            }
            for s in stocks
        ]

        # 2. Pending requests
        pending_requests = BloodRequest.objects.filter(status='pending').order_by('-created_at')
        pending_count = pending_requests.count()
        pending_data = BloodRequestSerializer(pending_requests[:10], many=True).data

        # 3. Recent donations
        recent_donations = Donation.objects.all().order_by('-created_at')[:10]
        recent_count = Donation.objects.count()
        recent_data = DonationSerializer(recent_donations, many=True).data

        return Response(
            {
                'summary': {
                    'total_stock_units': total_units,
                    'pending_requests_count': pending_count,
                    'total_donations_count': recent_count,
                },
                'stock': stock_list,
                'pending_requests': pending_data,
                'recent_donations': recent_data,
            },
            status=status.HTTP_200_OK,
        )
