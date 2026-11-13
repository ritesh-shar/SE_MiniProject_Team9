"""
Donor reminder dispatching service communicating with the Node.js notification microservice.

# BBMS-F-051: Reminders to eligible donors through a Node.js notification service.
"""

import json
import logging
from datetime import date, timedelta
import urllib.request
import urllib.error

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from donations.models import Donation

logger = logging.getLogger(__name__)
User = get_user_model()


# BBMS-F-051
def find_eligible_donors():
    """
    Find all registered donors who are eligible to donate:
    Donors whose most recent donation was at least 90 days ago.
    """
    cutoff_date = date.today() - timedelta(days=90)
    eligible_donors = []

    donors = User.objects.filter(role='donor')
    for donor in donors:
        last_donation = Donation.objects.filter(donor=donor).order_by('-donation_date').first()
        if last_donation and last_donation.donation_date <= cutoff_date:
            eligible_donors.append({
                'donor': donor,
                'last_donation_date': last_donation.donation_date,
                'days_since': (date.today() - last_donation.donation_date).days,
            })
    return eligible_donors


# BBMS-F-051
def send_notification_to_service(recipient, message, donor_id=None):
    """
    Send a notification payload to the external Node.js notification service via urllib.
    Non-blocking: catches failures without raising exceptions to the caller.
    """
    service_url = getattr(settings, 'NOTIFICATION_SERVICE_URL', 'http://127.0.0.1:3000/notify')
    payload = {
        'donorId': donor_id,
        'recipient': recipient,
        'message': message,
        'channel': 'email',
    }
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        service_url,
        data=data_bytes,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.status in (200, 201, 202)
    except Exception as exc:
        # Non-blocking per specification
        logger.warning(f"Notification service call failed for donor {donor_id}: {exc}")
        return False


# BBMS-F-051
class SendRemindersView(APIView):
    """
    POST /api/requests/reminders/send
    Admin-triggered endpoint to identify 90+ day eligible donors and dispatch reminders.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ('admin', 'staff'):
            return Response(
                {'error': 'Administrator or staff access required.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        eligible = find_eligible_donors()
        sent_count = 0
        failed_count = 0

        for item in eligible:
            donor = item['donor']
            msg = (
                f"Dear {donor.username}, thank you for your commitment to saving lives. "
                f"It has been {item['days_since']} days since your last donation on {item['last_donation_date']}. "
                f"You are eligible to donate blood again! Please visit your nearest blood bank."
            )
            success = send_notification_to_service(
                recipient=donor.email or f"{donor.username}@bbms.local",
                message=msg,
                donor_id=donor.id,
            )
            if success:
                sent_count += 1
            else:
                failed_count += 1

        return Response(
            {
                'message': f'Reminder dispatch process completed. {len(eligible)} eligible donor(s) identified.',
                'eligible_count': len(eligible),
                'sent_count': sent_count,
                'failed_count': failed_count,
            },
            status=status.HTTP_200_OK,
        )
