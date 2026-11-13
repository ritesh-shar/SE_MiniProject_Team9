"""
Unit tests for application health check.

# BBMS-NF-002: 99.5% uptime (verified by review and a health check).
Acceptance Test ID: TC-Uptime-01
Owner: Rithish P M (PR #1)
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HealthCheckTests(TestCase):
    """Test suite for BBMS-NF-002 health monitoring."""

    def setUp(self):
        self.client = APIClient()
        self.endpoint = '/api/health'

    # BBMS-NF-002 (Pass case)
    def test_health_check_returns_ok_when_database_connected(self):
        """Public health check endpoint returns 200 OK with database connected status."""
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'healthy')
        self.assertEqual(response.data.get('database'), 'connected')
