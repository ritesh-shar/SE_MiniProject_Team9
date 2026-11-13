"""
Health check endpoint for system monitoring.

# BBMS-NF-002: 99.5% uptime (verified by review and a health check).
"""

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


# BBMS-NF-002
class HealthCheckView(APIView):
    """
    GET /api/health
    Public health check endpoint validating application and database responsiveness.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                db_healthy = row is not None and row[0] == 1
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'database': 'unhealthy',
                    'detail': str(e),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                'status': 'healthy',
                'database': 'connected',
                'service': 'BBMS Backend API',
            },
            status=status.HTTP_200_OK,
        )
