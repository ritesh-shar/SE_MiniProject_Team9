"""Django admin configuration for the inventory app."""

from django.contrib import admin
from .models import BloodStock


@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ['id', 'blood_group', 'component', 'units_available', 'last_updated']
    list_filter = ['blood_group', 'component']
    search_fields = ['blood_group', 'component']
