"""
Management command to seed Sprint 2 demo data.

# BBMS-F-031, BBMS-F-040, BBMS-F-021, BBMS-F-022, BBMS-F-051
Usage:
    python manage.py seed_demo_s2
"""

from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.utils import timezone

from bloodrequests.models import BloodRequest
from donations.models import Donation
from inventory.models import BloodStock

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds Sprint 2 demo data: sample requests, near-expiry units, low-stock items, and eligible donors.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Sprint 2 demo data...'))

        # Ensure Sprint 1 demo users and stock exist
        try:
            call_command('seed_demo')
        except Exception:
            pass

        hospital = User.objects.filter(username='demo_hospital').first()
        staff = User.objects.filter(username='demo_staff').first()
        admin = User.objects.filter(username='demo_admin').first()
        donor = User.objects.filter(username='demo_donor').first()

        now = timezone.now()
        today = date.today()

        # 1. Sample Blood Requests
        if hospital:
            # Pending request (for 2-minute demo approval/issue)
            BloodRequest.objects.get_or_create(
                hospital=hospital,
                blood_group='O+',
                component='whole_blood',
                quantity=2,
                urgency='urgent',
                status='pending',
            )

            # Another pending request
            BloodRequest.objects.get_or_create(
                hospital=hospital,
                blood_group='A+',
                component='red_cells',
                quantity=3,
                urgency='normal',
                status='pending',
            )

            # An approved request
            BloodRequest.objects.get_or_create(
                hospital=hospital,
                blood_group='B+',
                component='platelets',
                quantity=1,
                urgency='critical',
                status='approved',
                defaults={
                    'reviewed_by': staff,
                    'reviewed_at': now - timedelta(hours=2),
                    'decision_note': 'Approved for emergency surgical unit.',
                }
            )

            # An issued request
            BloodRequest.objects.get_or_create(
                hospital=hospital,
                blood_group='O-',
                component='whole_blood',
                quantity=1,
                urgency='urgent',
                status='issued',
                defaults={
                    'reviewed_by': staff,
                    'reviewed_at': now - timedelta(days=1),
                    'decision_note': 'Approved for trauma patient.',
                    'issued_by': staff,
                    'issued_at': now - timedelta(hours=20),
                }
            )

            # A rejected request
            BloodRequest.objects.get_or_create(
                hospital=hospital,
                blood_group='AB-',
                component='plasma',
                quantity=50,
                urgency='normal',
                status='rejected',
                defaults={
                    'reviewed_by': admin,
                    'reviewed_at': now - timedelta(days=2),
                    'decision_note': 'Stock unavailable for requested volume.',
                }
            )

        # 2. Donation unit near expiry (F-021: Whole blood shelf life 35 days; 32 days old = 3 days to expiry)
        if donor:
            Donation.objects.get_or_create(
                donor=donor,
                blood_group='O+',
                component='whole_blood',
                quantity=1,
                donation_date=today - timedelta(days=32),
            )

            # Eligible donor for reminders (F-051: last donation 100 days ago)
            Donation.objects.get_or_create(
                donor=donor,
                blood_group='O+',
                component='plasma',
                quantity=1,
                donation_date=today - timedelta(days=100),
            )

        # 3. Low-stock blood stock (F-022: AB- whole blood set to 1 unit)
        stock_ab_neg, _ = BloodStock.objects.get_or_create(
            blood_group='AB-',
            component='whole_blood',
            defaults={'units_available': 1}
        )
        stock_ab_neg.units_available = 1
        stock_ab_neg.save()

        self.stdout.write(self.style.SUCCESS('Sprint 2 demo data successfully seeded.'))
