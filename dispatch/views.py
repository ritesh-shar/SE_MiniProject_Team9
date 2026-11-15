"""
API views for dispatch record tracking.

# BBMS-F-042: Dispatch record with timestamp, staff ID and recipient details,
#             retrievable by request ID.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import DispatchRecord


# BBMS-F-042
class DispatchDetailView(APIView):
    """
    GET /api/dispatch/<int:request_id>
    Retrieve the dispatch record for a fulfilled blood request by its request ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        record = DispatchRecord.objects.filter(request_id=request_id).first()
        if not record:
            return Response(
                {'error': f'Dispatch record for blood request #{request_id} not found.', 'code': 'NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # RBAC: Hospital can only retrieve its own dispatches; staff and admin see all
        if request.user.role == 'hospital' and record.recipient_hospital != request.user:
            return Response(
                {'error': 'Unauthorized to view dispatches intended for other hospitals.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                'dispatch_id': record.id,
                'request_id': record.request_id,
                'dispatched_at': record.dispatched_at.isoformat(),
                'issued_by_id': record.issued_by_id,
                'issued_by_name': record.issued_by.username if record.issued_by else None,
                'recipient_hospital_id': record.recipient_hospital_id,
                'recipient_hospital_name': record.recipient_hospital.username,
                'details': record.details,
            },
            status=status.HTTP_200_OK,
        )
