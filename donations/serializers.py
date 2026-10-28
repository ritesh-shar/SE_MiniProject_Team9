"""
Serializers for blood donation recording and history.

# BBMS-F-010: Record donation serializer and donation history serializer.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Donation

User = get_user_model()


class RecordDonationSerializer(serializers.Serializer):
    """
    Serializer for recording a new donation.
    Accepts both camelCase and snake_case field names for compatibility.
    """
    donorId = serializers.IntegerField(required=False)
    donor_id = serializers.IntegerField(required=False)
    bloodGroup = serializers.ChoiceField(choices=Donation.BLOOD_GROUP_CHOICES, required=False)
    blood_group = serializers.ChoiceField(choices=Donation.BLOOD_GROUP_CHOICES, required=False)
    component = serializers.ChoiceField(choices=Donation.COMPONENT_CHOICES)
    quantity = serializers.IntegerField(min_value=1)
    donationDate = serializers.DateField(required=False)
    donation_date = serializers.DateField(required=False)

    def validate(self, attrs):
        donor_id = attrs.get('donorId') or attrs.get('donor_id')
        if not donor_id:
            raise serializers.ValidationError({'donorId': 'This field is required.'})

        blood_group = attrs.get('bloodGroup') or attrs.get('blood_group')
        if not blood_group:
            raise serializers.ValidationError({'bloodGroup': 'This field is required.'})

        donation_date = attrs.get('donationDate') or attrs.get('donation_date')
        if not donation_date:
            raise serializers.ValidationError({'donationDate': 'This field is required.'})

        attrs['resolved_donor_id'] = donor_id
        attrs['resolved_blood_group'] = blood_group
        attrs['resolved_donation_date'] = donation_date
        return attrs


class DonationSerializer(serializers.ModelSerializer):
    """Serializer for displaying donation records in history."""
    donor_username = serializers.CharField(source='donor.username', read_only=True)

    class Meta:
        model = Donation
        fields = [
            'id',
            'donor',
            'donor_username',
            'blood_group',
            'component',
            'quantity',
            'donation_date',
            'created_at',
        ]
        read_only_fields = fields
