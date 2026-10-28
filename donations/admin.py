"""Django admin configuration for the donations app."""

from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor', 'blood_group', 'component', 'quantity', 'donation_date', 'created_at']
    list_filter = ['blood_group', 'component', 'donation_date']
    search_fields = ['donor__username', 'donor__email']
