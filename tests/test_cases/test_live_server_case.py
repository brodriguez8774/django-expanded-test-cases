"""
Tests for test_cases/live_server_test_case.py.
"""

# System Imports.
import unittest

# Internal Imports.
from django_expanded_test_cases import LiveServerTestCase


def skip_if_channels_not_installed():
    """Skip decorator, to handle when channels package is not installed."""
    try:
        from channels.testing import ChannelsLiveServerTestCase

        # If we made it this far, channels is installed. Proceed with test.
        return False
    except ModuleNotFoundError:
        # Failed to import channels. Skip test.
        return True


class LiveServerClassTest(LiveServerTestCase):
    """Tests for LiveServerTestCase class."""

    @classmethod
    @unittest.skipIf(skip_if_channels_not_installed(), 'Requires "channels" package.')
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

    @unittest.skipIf(skip_if_channels_not_installed(), 'Requires "channels" package.')
    def setUp(self):
        # Run parent setup logic.
        super().setUp()

    @unittest.skipIf(skip_if_channels_not_installed(), 'Requires "channels" package.')
    def __int__(self, *args, **kwargs):
        # Run parent setup logic.
        super().__init__(*args, **kwargs)

    # def test_window_generate_destroy(self):
    #     driver = self.create_driver()
    #
    #     window2 = self.open_new_window(driver)
    #     self.sleep_browser(1)
    #     tab_2 = self.open_new_tab(driver)
    #
    #     # for index in range(10):
    #     #     self.switch_window_at_index(driver, index % 3)
    #     #     self.sleep_browser(1)

    # @unittest.skipIf(skip_if_channels_not_installed(), 'Requires "channels" package.')
    # def test_aaa(self):
    #     window = self.create_driver()
    #     window2 = self.create_driver()
    #     window3 = self.create_driver()
    #
    #     self.sleep_browser(10)
    #
    #     self.close_driver(window)
    #     # self.close_all_drivers()
    #     #
    #     # self.sleep_browser(5)
    #
    #     self.assertTrue(True)
    #     self.assertFalse(True)

    # @unittest.skipIf(skip_if_channels_not_installed(), 'Requires "channels" package.')
    # def test_bbb(self):
    #     self.assertTrue(True)
    #     self.assertFalse(True)
