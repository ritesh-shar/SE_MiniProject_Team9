"""
API views for blood request submission and tracking.

# BBMS-F-031: A hospital submits a blood request: group, component, quantity, urgency.
#             Logged with a unique request ID.
#             Status is visible to the requester.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import BloodRequest
from .serializers import BloodRequestCreateSerializer, BloodRequestSerializer


# BBMS-F-031
class BloodRequestView(APIView):
    """
    Handles hospital blood request submission (POST) and request listing (GET).
    Served at both /api/requests and /api/requests/.

    - POST: Hospital submits a blood request (group, component, quantity, urgency).
    - GET: Hospital sees their own requests; staff and admin see all requests.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # BBMS-SR-002: Donors cannot submit hospital blood requests
        if request.user.role not in ('hospital', 'staff', 'admin'):
            return Response(
                {'error': 'Only hospitals can submit blood requests.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BloodRequestCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors, 'code': 'VALIDATION_ERROR'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated = serializer.validated_data
        blood_request = BloodRequest.objects.create(
            hospital=request.user,
            blood_group=validated['resolved_blood_group'],
            component=validated['component'],
            quantity=validated['quantity'],
            urgency=validated.get('urgency', 'normal'),
            status='pending',
        )

        return Response(
            {
                'message': 'Blood request submitted successfully.',
                'requestId': blood_request.id,
                'request': BloodRequestSerializer(blood_request).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        # BBMS-SR-002: Donors cannot view blood requests
        if request.user.role not in ('hospital', 'staff', 'admin'):
            return Response(
                {'error': 'Donors cannot view hospital requests.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.role == 'hospital':
            # Hospitals see only their own requests
            queryset = BloodRequest.objects.filter(hospital=request.user)
        else:
            # Staff and admin see all requests
            queryset = BloodRequest.objects.all()

        # Optional query filter by status (e.g. ?status=pending)
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        serializer = BloodRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
