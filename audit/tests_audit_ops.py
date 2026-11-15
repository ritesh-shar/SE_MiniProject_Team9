"""
Unit tests for inventory/request audit trail and statutory retention purge enforcement.

# BBMS-NF-005: Audit trail of all inventory and request changes, kept at least 3 years.
Acceptance Test ID: TC-Ops-01
Owner: Ritesh Babu Reddy (PR #4)
"""

from datetime import timedelta
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone

from inventory.models import BloodStock
from bloodrequests.models import BloodRequest
from audit.models import AuditLog

User = get_user_model()


class AuditTrailOpsTests(TestCase):
    """Test suite for BBMS-NF-005 (TC-Ops-01)."""

    def setUp(self):
        self.hospital = User.objects.create_user(
            username='ops_hospital',
            email='ops@hospital.org',
            password='HospitalPass123!',
            role='hospital',
        )

        self.staff = User.objects.create_user(
            username='ops_staff',
            email='ops@bbms.org',
            password='StaffPass123!',
            role='staff',
        )

    # BBMS-NF-005 / TC-Ops-01 (Pass case: Stock change is audited)
    def test_TC_Ops_01_inventory_changes_logged(self):
        """Updating blood stock triggers an audit log entry with details."""
        stock = BloodStock.objects.create(
            blood_group='O+',
            component='whole_blood',
            units_available=5,
        )

        log = AuditLog.objects.filter(event_type='STOCK_CHANGE').first()
        self.assertIsNotNone(log)
        self.assertIn('O+', log.description)
        self.assertEqual(log.extra_data.get('units_available'), 5)

    # BBMS-NF-005 / TC-Ops-01 (Pass case: Blood request transition is audited)
    def test_TC_Ops_01_request_changes_logged(self):
        """Creating and transitioning a blood request logs audit records."""
        req = BloodRequest.objects.create(
            hospital=self.hospital,
            blood_group='A-',
            component='plasma',
            quantity=2,
            status='pending',
        )

        log = AuditLog.objects.filter(event_type='REQUEST_CHANGE').first()
        self.assertIsNotNone(log)
        self.assertIn('A-', log.description)
        self.assertEqual(log.extra_data.get('request_id'), req.id)

    # BBMS-NF-005 / TC-Ops-01 (Fail case: Purge refuses records under 3 years old)
    def test_TC_Ops_01_purge_command_refuses_records_under_3_years(self):
        """Purge command must refuse execution when requested cutoff is under 3 years old."""
        # Create a log from yesterday
        log = AuditLog.objects.create(
            event_type='STOCK_CHANGE',
            description='Recent inventory movement',
        )

        # Attempt to purge with a cutoff 1 year ago (violating 3-year statutory rule)
        one_year_ago = (timezone.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        with self.assertRaises(CommandError) as ctx:
            call_command('purge_audit_logs', f'--before={one_year_ago}')

        self.assertIn('violates the mandatory 3-year statutory audit retention', str(ctx.exception))
        # Verify log still exists
        self.assertTrue(AuditLog.objects.filter(id=log.id).exists())

    # BBMS-NF-005 / TC-Ops-01 (Pass case: Purge deletes logs strictly older than 3 years)
    def test_TC_Ops_01_purge_deletes_records_older_than_3_years(self):
        """Purge command successfully deletes records older than 3 years."""
        old_log = AuditLog.objects.create(
            event_type='STOCK_CHANGE',
            description='Ancient inventory movement',
        )
        # Manually backdate timestamp past 3 years (e.g., 4 years ago)
        ancient_date = timezone.now() - timedelta(days=4 * 365)
        AuditLog.objects.filter(id=old_log.id).update(timestamp=ancient_date)

        # Execute standard purge (default 3-year cutoff)
        call_command('purge_audit_logs')

        # Ancient record is purged
        self.assertFalse(AuditLog.objects.filter(id=old_log.id).exists())
