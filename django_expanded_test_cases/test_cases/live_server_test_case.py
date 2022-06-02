"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
from channels.testing import ChannelsLiveServerTestCase

# User Imports.
from django_expanded_test_cases.mixins.response_mixin import ResponseTestCaseMixin


class LiveServerTestCase(ChannelsLiveServerTestCase, ResponseTestCaseMixin):
    """Testing functionality through selenium, to simulate web browser navigation."""

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
