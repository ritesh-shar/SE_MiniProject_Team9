"""
Staff blood request issuance view.

# BBMS-F-041: Decrement inventory stock when an approved request is issued.
"""

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from inventory.services import decrease_stock
from .models import BloodRequest
from .serializers import BloodRequestSerializer


# BBMS-F-041
class BloodRequestIssueView(APIView):
    """
    POST /api/requests/<int:pk>/issue
    Staff and Admin issue approved blood units, decrementing stock under atomic row locking.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # BBMS-SR-002: Only staff and admin can issue blood requests
        if request.user.role not in ('staff', 'admin'):
            return Response(
                {'error': 'Only staff and administrators can issue blood requests.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            blood_request = BloodRequest.objects.get(pk=pk)
        except BloodRequest.DoesNotExist:
            return Response(
                {'error': f'Blood request #{pk} not found.', 'code': 'NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if blood_request.status != 'approved':
            return Response(
                {
                    'error': f'Only approved requests can be issued. Current status: "{blood_request.status}".',
                    'code': 'INVALID_STATUS',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # BBMS-F-041: Decrement stock using row-level locking
        try:
            remaining_stock = decrease_stock(
                blood_group=blood_request.blood_group,
                component=blood_request.component,
                quantity=blood_request.quantity,
            )
        except ValueError as exc:
            return Response(
                {'error': str(exc), 'code': 'INSUFFICIENT_STOCK'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        blood_request.status = 'issued'
        blood_request.issued_by = request.user
        blood_request.issued_at = timezone.now()
        blood_request.save()

        return Response(
            {
                'message': f'Blood request #{pk} issued successfully. Stock updated.',
                'remaining_stock': remaining_stock,
                'request': BloodRequestSerializer(blood_request).data,
            },
            status=status.HTTP_200_OK,
        )
