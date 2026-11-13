"""
Staff review view for approving or rejecting pending blood requests.

# BBMS-F-040: Staff approve or reject a pending request. Status is visible to the requester.
"""

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import BloodRequest
from .serializers import BloodRequestSerializer


# BBMS-F-040
class BloodRequestReviewView(APIView):
    """
    POST /api/requests/<int:pk>/review
    Staff and Admin review pending blood requisitions (approve or reject with notes).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # BBMS-SR-002: Only staff and admin can review requests
        if request.user.role not in ('staff', 'admin'):
            return Response(
                {'error': 'Only staff and administrators can review blood requests.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            blood_request = BloodRequest.objects.get(pk=pk)
        except BloodRequest.DoesNotExist:
            return Response(
                {'error': f'Blood request #{pk} not found.', 'code': 'NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if blood_request.status != 'pending':
            return Response(
                {'error': f'Cannot review request #{pk}: status is already "{blood_request.status}".', 'code': 'INVALID_STATUS'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        decision = request.data.get('decision') or request.data.get('status')
        if decision not in ('approved', 'rejected'):
            return Response(
                {'error': 'Decision must be either "approved" or "rejected".', 'code': 'INVALID_DECISION'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        decision_note = request.data.get('decision_note', '').strip()

        blood_request.status = decision
        blood_request.reviewed_by = request.user
        blood_request.reviewed_at = timezone.now()
        blood_request.decision_note = decision_note
        blood_request.save()

        return Response(
            {
                'message': f'Blood request #{pk} has been {decision}.',
                'request': BloodRequestSerializer(blood_request).data,
            },
            status=status.HTTP_200_OK,
        )
