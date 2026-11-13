"""
Serializers for blood requests.

# BBMS-F-031: Hospital submits a blood request: group, component, quantity, urgency.
"""

from rest_framework import serializers
from .models import BloodRequest
from .validation import validate_request_stock


# BBMS-F-031
class BloodRequestCreateSerializer(serializers.Serializer):
    """
    Serializer for hospital blood request submission.
    Accepts both camelCase and snake_case field names.
    """
    blood_group = serializers.ChoiceField(choices=BloodRequest.BLOOD_GROUP_CHOICES, required=False)
    bloodGroup = serializers.ChoiceField(choices=BloodRequest.BLOOD_GROUP_CHOICES, required=False)

    component = serializers.ChoiceField(choices=BloodRequest.COMPONENT_CHOICES)
    quantity = serializers.IntegerField(min_value=1)

    urgency = serializers.ChoiceField(choices=BloodRequest.URGENCY_CHOICES, required=False, default='normal')

    def validate(self, attrs):
        blood_group = attrs.get('blood_group') or attrs.get('bloodGroup')
        if not blood_group:
            raise serializers.ValidationError({'blood_group': 'Blood group is required.'})

        component = attrs.get('component')
        quantity = attrs.get('quantity')

        # BBMS-F-032 hook (stub in PR 1, real check in PR 4)
        is_valid, error_msg = validate_request_stock(blood_group, component, quantity)
        if not is_valid:
            raise serializers.ValidationError({'quantity': error_msg or 'Requested quantity exceeds available stock.'})

        attrs['resolved_blood_group'] = blood_group
        return attrs


class BloodRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying blood requests.
    """
    hospital_name = serializers.CharField(source='hospital.username', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True, default=None)
    issued_by_name = serializers.CharField(source='issued_by.username', read_only=True, default=None)

    class Meta:
        model = BloodRequest
        fields = [
            'id',
            'hospital',
            'hospital_name',
            'blood_group',
            'component',
            'quantity',
            'urgency',
            'status',
            'created_at',
            'reviewed_by',
            'reviewed_by_name',
            'reviewed_at',
            'decision_note',
            'issued_by',
            'issued_by_name',
            'issued_at',
        ]
        read_only_fields = fields
