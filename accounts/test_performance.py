"""
Performance tests for search and dashboard latency.

# BBMS-NF-001: 95% of search and dashboard requests answer within 2 s under normal load.
Acceptance Test ID: TC-Perf-01
Owner: Reyansh (PR #3)
"""

import time
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from inventory.models import BloodStock
from bloodrequests.models import BloodRequest

User = get_user_model()


class PerformanceLatencyTests(TestCase):
    """Test suite for BBMS-NF-001 (TC-Perf-01)."""

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='perf_admin',
            email='perf@bbms.org',
            password='AdminPassword123!',
            role='admin',
            is_staff=True,
        )

        # Seed realistic operational dataset
        for group in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
            for comp in ['whole_blood', 'red_cells', 'plasma', 'platelets']:
                BloodStock.objects.create(
                    blood_group=group,
                    component=comp,
                    units_available=25,
                )

        hospital = User.objects.create_user(
            username='perf_hosp',
            email='hosp@bbms.org',
            password='Pass!',
            role='hospital',
        )

        for i in range(15):
            BloodRequest.objects.create(
                hospital=hospital,
                blood_group='O+',
                component='whole_blood',
                quantity=1,
                status='pending',
            )

    # BBMS-NF-001 / TC-Perf-01
    def test_TC_Perf_01_95th_percentile_under_2s(self):
        """Execute 100 search and dashboard queries; verify 95th percentile response latency is under 2.0s."""
        self.client.force_authenticate(user=self.admin)

        latencies = []
        endpoints = [
            '/api/inventory/search?bloodGroup=O+&component=whole_blood',
            '/api/admin/dashboard',
        ]

        # Execute 100 requests
        for i in range(100):
            url = endpoints[i % 2]
            start = time.perf_counter()
            response = self.client.get(url)
            duration = time.perf_counter() - start

            self.assertEqual(response.status_code, 200)
            latencies.append(duration)

        latencies.sort()
        # 95th percentile index is element 94
        p95 = latencies[int(len(latencies) * 0.95)]

        self.assertLess(
            p95,
            2.0,
            f"95th percentile latency of {p95:.4f}s exceeded 2.0s threshold.",
        )
