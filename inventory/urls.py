"""
URL routing for the inventory app.

Shared file:
  - Ritesh Kumar Sharma (PR #2): Inventory stock list route
  - Ritesh Babu Reddy (PR #4): Search route
"""

from django.urls import path
from .views import InventoryListView
from .search import BloodSearchView

urlpatterns = [
    # --- Ritesh Kumar Sharma (PR #2) ---
    path('', InventoryListView.as_view(), name='inventory-list'),

    # --- Ritesh Babu Reddy (PR #4) ---
    path('search', BloodSearchView.as_view(), name='inventory-search'),
    path('search/', BloodSearchView.as_view(), name='inventory-search-slash'),
]
