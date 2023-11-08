"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.

# Third-Party Imports.
from channels.testing import ChannelsLiveServerTestCase as DjangoChannelsLiveServerTestCase

# Internal Imports.
from django_expanded_test_cases.mixins.live_server_mixin import LiveServerMixin


class ChannelsLiveServerTestCase(DjangoChannelsLiveServerTestCase, LiveServerMixin):
    """Uses DjangoChannels package to test functionality through selenium. Simulates web browser navigation."""

    @classmethod
    def setUpClass(cls, *args, debug_print=None, **kwargs):
        """Test logic setup run at the start of class creation."""

        # Call parent logic.
        return_val = super().setUpClass()
        LiveServerMixin.setUpClass(*args, debug_print=debug_print, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    @classmethod
    def setUpTestData(cls, *args, **kwargs):
        """Test logic setup run at the start of class creation, specifically for data setup."""

        # Call parent logic.
        return_val = super().setUpTestData()
        LiveServerMixin.setUpTestData(*args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def setUp(self, *args, **kwargs):
        """Test logic setup run at the start of function/method execution."""

        # Call parent logic.
        return_val = super().setUp()
        LiveServerMixin.setUp(self, *args, **kwargs)

        self._error_displayed = False

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def subTest(self, *args, **kwargs):
        """Test logic setup run every time we enter a subtest."""

        # Call parent logic.
        return_val = super().subTest()
        LiveServerMixin.subTest(self, *args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        """Test logic setup run at the end of class execution, as part of termination/clean up."""

        # Call parent logic.
        return_val = super().tearDownClass()
        LiveServerMixin.tearDownClass(*args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def tearDown(self, *args, **kwargs):
        """Test logic setup run at the end of function/method execution, as part of termination/clean up."""

        # Call parent logic.
        return_val = super().tearDown()
        LiveServerMixin.tearDown(self, *args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val


# Define acceptable imports on file.
__all__ = [
    'ChannelsLiveServerTestCase',
]
