"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
from channels.testing import ChannelsLiveServerTestCase

# User Imports.
from django_expanded_test_cases.mixins.core_mixin import CoreTestCaseMixin


class LiveServerTestCase(ChannelsLiveServerTestCase, CoreTestCaseMixin):
    """Testing functionality through selenium, to simulate web browser navigation."""

    def setUp(self):
        # Run parent setup logic.
        super().setUp()
