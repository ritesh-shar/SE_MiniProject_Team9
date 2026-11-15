"""
URL routing for the inventory app.

Shared file:
  - Ritesh Kumar Sharma (PR #2): Inventory stock list route
  - Ritesh Babu Reddy (PR #4): Search route
"""

from django.urls import path
from .views import InventoryListView
from .search import BloodSearchView
from .alert_views import ExpiryAlertView, LowStockAlertView

urlpatterns = [
    # --- Ritesh Kumar Sharma (PR #2) ---
    path('', InventoryListView.as_view(), name='inventory-list'),

    # --- Ritesh Babu Reddy (PR #4) ---
    path('search', BloodSearchView.as_view(), name='inventory-search'),
    path('search/', BloodSearchView.as_view(), name='inventory-search-slash'),

    # --- Ritesh Babu Reddy (PR #4) - Inventory Alerts ---
    path('alerts/expiry', ExpiryAlertView.as_view(), name='inventory-alerts-expiry'),
    path('alerts/expiry/', ExpiryAlertView.as_view(), name='inventory-alerts-expiry-slash'),
    path('alerts/low-stock', LowStockAlertView.as_view(), name='inventory-alerts-low-stock'),
    path('alerts/low-stock/', LowStockAlertView.as_view(), name='inventory-alerts-low-stock-slash'),
]
