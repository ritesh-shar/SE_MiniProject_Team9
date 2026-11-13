"""
API views for audit log inspection.

# BBMS-SR-004: Log all authentication attempts and administrative actions.
# BBMS-NF-005: Audit trail of all inventory and request changes, kept at least 3 years.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import AuditLog


# BBMS-SR-004, BBMS-NF-005
class AuditLogListView(APIView):
    """
    GET /api/audit
    Administrative endpoint to inspect audit trail events.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response(
                {'error': 'Administrator access required to view audit trail.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = AuditLog.objects.all()

        event_type = request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        limit = int(request.query_params.get('limit', 100))
        logs = queryset[:limit]

        data = [
            {
                'id': l.id,
                'event_type': l.event_type,
                'username': l.user.username if l.user else None,
                'ip_address': l.ip_address,
                'timestamp': l.timestamp.isoformat(),
                'description': l.description,
                'extra_data': l.extra_data,
            }
            for l in logs
        ]

        return Response(data, status=status.HTTP_200_OK)
