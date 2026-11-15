"""
Management command to purge expired audit records.

# BBMS-NF-005: Audit trail of all inventory and request changes, kept at least 3 years.
Owner: Ritesh Babu Reddy (PR #4)
"""

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.dateparse import parse_date

from audit.models import AuditLog


# BBMS-NF-005
class Command(BaseCommand):
    help = 'Purges audit logs strictly older than 3 years. Refuses to delete anything under 3 years old.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--before',
            type=str,
            help='Optional purge cutoff date (YYYY-MM-DD). Must be at least 3 years in the past.',
        )

    def handle(self, *args, **options):
        now = timezone.now()
        statutory_limit = now - timedelta(days=3 * 365)  # 3-year minimum retention

        before_str = options.get('before')
        if before_str:
            parsed = parse_date(before_str)
            if not parsed:
                raise CommandError(f"Invalid date format: '{before_str}'. Expected YYYY-MM-DD.")
            cutoff = timezone.make_aware(datetime.combine(parsed, datetime.min.time()))

            if cutoff > statutory_limit:
                raise CommandError(
                    f"Refusing purge: Cutoff date {before_str} violates the mandatory 3-year statutory audit retention requirement (BBMS-NF-005)."
                )
        else:
            cutoff = statutory_limit

        # Delete only records strictly older than cutoff
        deleted_count, _ = AuditLog.objects.filter(timestamp__lt=cutoff).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully purged {deleted_count} audit record(s) older than {cutoff.strftime('%Y-%m-%d')}."
            )
        )
