"""
URL routing for the donations app.

# BBMS-F-010: POST /api/donations
# GET /api/donations/history
"""

from django.urls import path
from .views import DonationRecordView, DonationHistoryView

urlpatterns = [
    path('', DonationRecordView.as_view(), name='donation-record'),
    path('history', DonationHistoryView.as_view(), name='donation-history'),
    path('history/', DonationHistoryView.as_view(), name='donation-history-slash'),
]
