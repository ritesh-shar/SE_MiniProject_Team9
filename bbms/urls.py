"""
URL configuration for the BBMS project.

Shared file — built across two PRs:
  - Rithish P M (PR #1):  admin URL only
  - Ritesh Kumar Sharma (PR #2):  accounts, donations, inventory includes, and frontend static serving
"""

from django.contrib import admin
from django.urls import path
from django.urls import re_path, include
from django.conf import settings
from django.views.static import serve
from donations.views import DonationRecordView
from inventory.views import InventoryListView
from bloodrequests.views import BloodRequestView
from bloodrequests.dashboard_views import AdminDashboardView
from bloodrequests.health_views import HealthCheckView

urlpatterns = [
    # --- Rithish P M (PR #1) ---
    path('admin/', admin.site.urls),

    # --- Ritesh Kumar Sharma (PR #2) ---
    path('api/auth/', include('accounts.urls')),
    path('api/donations', DonationRecordView.as_view(), name='donation-record-root'),
    path('api/donations/', include('donations.urls')),
    path('api/inventory', InventoryListView.as_view(), name='inventory-list-root'),
    path('api/inventory/', include('inventory.urls')),

    # --- Rithish P M (PR #1 - Sprint 2) ---
    path('api/requests', BloodRequestView.as_view(), name='bloodrequest-root'),
    path('api/requests/', include('bloodrequests.urls')),
    path('api/admin/dashboard', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('api/health', HealthCheckView.as_view(), name='health-check'),

    # --- Reyansh (PR #3 - Sprint 2) ---
    path('api/audit/', include('audit.urls')),
]


# --- Frontend static serving in DEBUG mode (Ritesh Kumar Sharma — PR #2) ---
if settings.DEBUG:
    frontend_dir = settings.BASE_DIR / 'frontend'

    def frontend_index(request):
        return serve(request, 'index.html', document_root=str(frontend_dir))

    urlpatterns += [
        path('', frontend_index, name='frontend-root'),
        re_path(r'^(?P<path>.*)$', serve, {'document_root': str(frontend_dir)}, name='frontend-static'),
    ]
