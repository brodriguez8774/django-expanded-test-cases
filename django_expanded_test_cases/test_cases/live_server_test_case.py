"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
import time

# Third-Party Imports.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService
from channels.testing import ChannelsLiveServerTestCase
from django.conf import settings

# Internal Imports.
from django_expanded_test_cases.mixins.response_mixin import ResponseTestCaseMixin


class LiveServerTestCase(ChannelsLiveServerTestCase, ResponseTestCaseMixin):
    """Testing functionality through selenium, to simulate web browser navigation."""

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls._driver_set = []

        # Import/Initialize some values based on chosen testing browser. Default to chrome.
        cls._browser = str(getattr(settings, 'SELENIUM_TEST_BROWSER', 'chrome')).lower()

        if cls._browser == 'chrome':
            # Setup for Chrome browser.

            # Setup browser driver to launch browser with.
            try:
                # Attempt driver auto-install, if webdriver_manager package is present.
                from webdriver_manager.chrome import ChromeDriverManager
                cls._service = ChromeService(executable_path=ChromeDriverManager().install())
            except ModuleNotFoundError:
                # Fall back to manual installation handling.
                # raise NotImplementedError('Currently not supported to')
                # cls._service = ChromeService(executable_path='/usr/bin/google-chrome')
                cls._service = ChromeService(executable_path='/usr/local/share/chromedriver')

        elif cls._browser == 'chromium':
            # Setup for Chromium browser.

            # Setup browser driver to launch browser with.
            try:
                # Attempt driver auto-install, if webdriver_manager package is present.
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.utils import ChromeType
                cls._service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            except ModuleNotFoundError:
                # Fall back to manual installation handling.
                # cls._service = ChromeService(executable_path='/usr/bin/google-chrome')
                cls._service = ChromeService(executable_path='/usr/local/share/chromedriver')

            # All further handling should behave the same as chrome.
            cls._browser = 'chrome'

        elif cls._browser == 'firefox':
            # Setup for Firefox browser.

            # Setup browser driver to launch browser with.
            try:
            # Attempt driver auto-install, if webdriver_manager package is present.
                from webdriver_manager.firefox import GeckoDriverManager
                cls._service = FireFoxService(executable_path=GeckoDriverManager().install())
            except ModuleNotFoundError:
                # Fall back to manual installation handling.
                cls._service = FireFoxService(executable_path='/usr/bin/geckodriver')

        else:
            raise ValueError('Unknown browser "{0}".'.format(cls._browser))

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

        self._error_displayed = False

    def subTest(self, *args, **kwargs):
        # Call CoreMixin logic.
        self.sub_test()

        # Run parent logic.
        return super().subTest(*args, **kwargs)

    def tearDown(self):
        # Close all remaining browser instances for test.
        self.close_all_drivers()

        # Call parent teardown logic.
        super().tearDown()

    def create_driver(self):
        """Creates new browser manager instance."""

        # Create instance, based on selected driver type.
        if self._browser == 'chrome':
            driver = webdriver.Chrome(service=self._service)
        elif self._browser == 'firefox':
            driver = webdriver.Firefox(service=self._service)
        else:
            raise ValueError('Unknown browser "{0}".'.format(self._browser))

        # Make class aware of window.
        self._driver_set.append(driver)

        return driver

    def close_driver(self, driver):
        """Closes provided browser manager instance.

        :param driver: Driver manager object to close.
        """
        # Remove reference in class.
        self._driver_set.remove(driver)

        # Close window.
        driver.quit()

    def close_all_drivers(self):
        """Closes all open browser manager instances."""
        while len(self._driver_set) > 0:
            self.close_driver(self._driver_set[0])

    def open_new_window(self, driver):
        """Opens a new window for the provided driver.

        :param driver: Driver manager object to generate window for.
        :return: New focus window.
        """
        # Open blank new window.
        driver.switch_to.new_window('window')

        # Switch to recently created window.
        return self.switch_to_window_at_index(driver, len(driver.window_handles) - 1)

    def open_new_tab(self, driver):
        """Opens a new window for the provided driver.

        :param driver: Driver manager object to generate window for.
        :return: New focus window.
        """
        # Open blank new window.
        driver.switch_to.new_window('tab')

        # Switch to recently created window.
        return self.switch_to_window_at_index(driver, len(driver.window_handles) - 1)

    def close_window_at_index(self, driver, window_index):
        """Closes a window at specific index for the provided driver.

        :param driver: Driver manager object containing the desired window.
        :param window_index: Index of window to close.
        """
        # Attempt to get window at specified driver index.
        try:
            focus_window = driver.window_handles[window_index]
        except IndexError:
            err_msg = 'Attempted to close to window of index "{0}", but driver only has "{1}" windows open.'.format(
                window_index,
                len(driver.window_handles)
            )
            raise IndexError(err_msg)

        # Close window.
        self.switch_to_window_at_index(driver, window_index)
        driver.execute_script('window.close();')

    def switch_to_window_at_index(self, driver, window_index):
        """Sets window at specific driver/index to be the current focus.

        :param driver: Driver manager object containing the desired window.
        :param window_index: Index of window to switch to.
        :return: New focus window.
        """
        # Attempt to get window at specified driver index.
        try:
            focus_window = driver.window_handles[window_index]
        except IndexError:
            err_msg = 'Attempted to switch to window of index "{0}", but driver only has "{1}" windows open.'.format(
                window_index,
                len(driver.window_handles)
            )
            raise IndexError(err_msg)

        # Switch window to be focused.
        driver.switch_to.window(focus_window)

        # Return newly switched window.
        return focus_window

    def sleep_browser(self, seconds):
        """Halts browser for provided number of seconds.

        Useful for visually verifying browser state, when trying to debug tests.
        """
        time.sleep(seconds)


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
