"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService
from channels.testing import ChannelsLiveServerTestCase
from django.conf import settings

# User Imports.
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

    def tearDown(self):
        # Close all remaining browser instances for test.
        self.close_all_drivers()

        # Call parent teardown logic.
        super().tearDown()

    def create_driver(self):
        """Creates new browser window instance."""

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
        """Closes provided browser window instance.

        :param driver: Driver/window object to close.
        """
        # Remove reference in class.
        self._driver_set.remove(driver)

        # Close window.
        driver.quit()

    def close_all_drivers(self):
        """Closes all open browser window instances."""
        while len(self._driver_set) > 0:
            self.close_driver(self._driver_set[0])

    def sleep_browser(self, seconds):
        """Halts browser for provided number of seconds.

        Useful for visually verifying browser state, when trying to debug tests.
        """
        time.sleep(seconds)


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
