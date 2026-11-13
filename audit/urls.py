"""
URL routing for the audit app.

# BBMS-SR-004, BBMS-NF-005
"""

from django.urls import path
from .views import AuditLogListView

urlpatterns = [
    path('', AuditLogListView.as_view(), name='audit-log-list'),
]
