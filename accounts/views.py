"""
API views for user registration and authentication.

# BBMS-F-001: POST /api/auth/register — donor self-registration.
# BBMS-F-002: POST /api/auth/login — JWT authentication (via simplejwt).
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterView(APIView):
    """
    POST /api/auth/register

    Allows a new donor to register with personal details, blood group,
    and contact information.  Returns the new user's ID on success.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    # BBMS-F-001
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'Donor registered successfully.',
                    'userId': user.id,
                    'username': user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'error': serializer.errors, 'code': 'VALIDATION_ERROR'},
            status=status.HTTP_400_BAD_REQUEST,
        )
