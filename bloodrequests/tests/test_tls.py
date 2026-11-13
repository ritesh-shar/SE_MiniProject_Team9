"""
Unit tests for TLS enforcement.

# BBMS-SR-001: TLS 1.2+ mandatory for client-server connections.
Acceptance Test ID: TC-Sec-01
Owner: Rithish P M (PR #1)
"""

from django.test import TestCase, override_settings
from django.test.client import Client


class TLSSecurityTests(TestCase):
    """Test suite for BBMS-SR-001 (TC-Sec-01)."""

    def setUp(self):
        self.client = Client()

    # BBMS-SR-001 / TC-Sec-01 (Pass case: Redirect HTTP to HTTPS when enabled)
    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_TC_Sec_01_http_redirects_to_https_when_ssl_redirect_enabled(self):
        """When SECURE_SSL_REDIRECT is active, standard HTTP requests are redirected to HTTPS."""
        response = self.client.get('/api/health', secure=False)
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response.url.startswith('https://'))

    # BBMS-SR-001 / TC-Sec-01 (Direct HTTPS request allowed)
    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_TC_Sec_01_https_request_succeeds(self):
        """Requests over HTTPS succeed directly without redirection."""
        response = self.client.get('/api/health', secure=True)
        self.assertEqual(response.status_code, 200)
