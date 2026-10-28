"""
URL configuration for the BBMS project.

Shared file — built across two PRs:
  - Rithish P M (PR #1):  admin URL only
  - Ritesh Kumar Sharma (PR #2):  accounts, donations, inventory includes, and frontend static serving
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    # --- Rithish P M (PR #1) ---
    path('admin/', admin.site.urls),
]
