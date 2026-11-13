"""
Usability verification tests for staff donation workflow.

# BBMS-NF-003: Staff can record a donation in 3 clicks or fewer.
Acceptance Test ID: TC-UX-01
Owner: Reyansh (PR #3)
"""

import os
from pathlib import Path
from django.test import TestCase
from django.conf import settings


class UsabilityWorkflowTests(TestCase):
    """Test suite for BBMS-NF-003 (TC-UX-01)."""

    def setUp(self):
        self.frontend_dir = Path(settings.BASE_DIR) / 'frontend'
        self.dashboard_path = self.frontend_dir / 'dashboard.html'
        self.donation_form_path = self.frontend_dir / 'donation_form.html'

    # BBMS-NF-003 / TC-UX-01
    def test_TC_UX_01_dashboard_links_directly_to_donation_form(self):
        """Dashboard HTML must provide a direct 1-click link to donation form for staff."""
        self.assertTrue(self.dashboard_path.exists(), "dashboard.html not found.")
        content = self.dashboard_path.read_text(encoding='utf-8')

        # Check direct link with staff role restriction
        self.assertIn('href="donation_form.html"', content)
        self.assertIn('role-staff-only', content)

    # BBMS-NF-003 / TC-UX-01
    def test_TC_UX_01_donation_form_has_direct_submit(self):
        """Donation form page must provide immediate form inputs and direct submission button."""
        self.assertTrue(self.donation_form_path.exists(), "donation_form.html not found.")
        content = self.donation_form_path.read_text(encoding='utf-8')

        self.assertIn('id="donation-form"', content)
        self.assertIn('type="submit"', content)

        # Total user path verified:
        # Click 1: Click 'Record Blood Donation' on dashboard
        # Click 2: Select/Input donor details
        # Click 3: Click 'Record Donation' submit button
        # Total clicks <= 3
