"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.

# Third-Party Imports.
from django.test import LiveServerTestCase as DjangoLiveServerTestCase


# Internal Imports.
from django_expanded_test_cases.mixins.live_server_mixin import LiveServerMixin


class LiveServerTestCase(DjangoLiveServerTestCase, LiveServerMixin):
    """Uses Django package to test functionality through selenium. Simulates web browser navigation."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call Mixin setup logic.
        cls.set_up_class(debug_print=debug_print)

    @classmethod
    def setUpTestData(cls):
        # Run parent setup logic.
        super().setUpTestData()

        # Initialize default data models.
        cls.set_up_test_data()

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

        # Also call Mixin setup logic.
        self.set_up()

        self._error_displayed = False

    def subTest(self, *args, **kwargs):
        # Call CoreMixin logic.
        self.sub_test()

        # Run parent logic.
        return super().subTest(*args, **kwargs)

    @classmethod
    def tearDownClass(cls):
        # Call Mixin setup logic.
        cls.tear_down_class()

        # Call parent teardown logic.
        super().tearDownClass()


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
