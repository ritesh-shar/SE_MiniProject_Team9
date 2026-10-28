"""
Views for recording blood donations and viewing donation history.

# BBMS-F-010: Staff record a donation.
# BBMS-F-011: 90-day donor eligibility check.
# BBMS-F-012: Automatic inventory increase.
# BBMS-SR-002: RBAC enforced on endpoints.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from accounts.permissions import IsStaffOrAdmin, IsDonorOwnerOrStaffAdmin
from .models import Donation
from .serializers import RecordDonationSerializer, DonationSerializer
from .services import check_eligibility, record_donation

User = get_user_model()


class DonationRecordView(APIView):
    """
    POST /api/donations

    Record a new blood donation.
    Accessible only to Staff and Admin.
    Validates donor eligibility (at least 90 days since last donation).
    Atomically updates inventory stock with row-level locking.
    """
    permission_classes = [IsStaffOrAdmin]

    # BBMS-F-010, BBMS-F-011, BBMS-F-012
    def post(self, request):
        serializer = RecordDonationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors, 'code': 'VALIDATION_ERROR'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        donor_id = serializer.validated_data['resolved_donor_id']
        blood_group = serializer.validated_data['resolved_blood_group']
        component = serializer.validated_data['component']
        quantity = serializer.validated_data['quantity']
        donation_date = serializer.validated_data['resolved_donation_date']

        # Find donor
        try:
            donor = User.objects.get(id=donor_id)
        except User.DoesNotExist:
            return Response(
                {'error': f"Donor with id {donor_id} not found.", 'code': 'DONOR_NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # BBMS-F-011: 90-day eligibility check
        is_eligible, message = check_eligibility(donor, donation_date)
        if not is_eligible:
            return Response(
                {'error': message, 'code': 'DONOR_NOT_ELIGIBLE'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # BBMS-F-010, BBMS-F-012: record donation and update inventory atomically
        donation, updated_stock = record_donation(
            donor=donor,
            blood_group=blood_group,
            component=component,
            quantity=quantity,
            donation_date=donation_date,
        )

        return Response(
            {
                'status': 'success',
                'donationId': donation.id,
                'updatedStock': updated_stock,
            },
            status=status.HTTP_201_CREATED,
        )


class DonationHistoryView(APIView):
    """
    GET /api/donations/history

    Donors view their own history.
    Staff and Admin view all donation history.
    """
    permission_classes = [IsDonorOwnerOrStaffAdmin]

    def get(self, request):
        if request.user.role in ('staff', 'admin'):
            donations = Donation.objects.all()
        else:
            donations = Donation.objects.filter(donor=request.user)

        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
