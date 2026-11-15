"""
URL routing for the dispatch app.

# BBMS-F-042
"""

from django.urls import path
from .views import DispatchDetailView

urlpatterns = [
    path('<int:request_id>', DispatchDetailView.as_view(), name='dispatch-detail'),
    path('<int:request_id>/', DispatchDetailView.as_view(), name='dispatch-detail-slash'),
]
