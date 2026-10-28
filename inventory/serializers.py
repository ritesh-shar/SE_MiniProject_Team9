"""
Serializers for blood stock inventory and search.

# BBMS-F-020: Inventory stock serialization.
# BBMS-F-030: Search results serialization.
"""

from rest_framework import serializers
from .models import BloodStock


class BloodStockSerializer(serializers.ModelSerializer):
    """Serializer for blood inventory stock records."""
    component_display = serializers.CharField(source='get_component_display', read_only=True)

    class Meta:
        model = BloodStock
        fields = [
            'id',
            'blood_group',
            'component',
            'component_display',
            'units_available',
            'last_updated',
        ]
        read_only_fields = fields
