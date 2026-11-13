"""
URL routing for the bloodrequests app.

Shared file:
  - Rithish P M (PR #1): Submit, list, export, reminders routes
  - Ritesh Kumar Sharma (PR #2): Review and issue routes
"""

from django.urls import path
from .views import BloodRequestView
from .export_views import DonationExportView, InventoryExportView
from .reminders import SendRemindersView

urlpatterns = [
    # --- Rithish P M (PR #1) ---
    path('', BloodRequestView.as_view(), name='bloodrequest-list-create'),
    path('export/donations', DonationExportView.as_view(), name='export-donations'),
    path('export/inventory', InventoryExportView.as_view(), name='export-inventory'),
    path('reminders/send', SendRemindersView.as_view(), name='send-reminders'),
]
