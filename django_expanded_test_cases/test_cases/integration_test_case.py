"""
Testing logic for views and other multi-part components.
"""

# System Imports.
from django.conf import settings
from django.urls import reverse

# User Imports.
from .base_test_case import BaseTestCase


class IntegrationTestCase(BaseTestCase):
    """Testing functionality for views and other multi-part components."""

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Get login url.
        cls.login_url = reverse(settings.LOGIN_URL)

    def setUp(self):
        # Run parent setup logic.
        super().setUp()


