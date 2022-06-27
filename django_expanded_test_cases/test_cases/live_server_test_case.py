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

        # Import/Initialize some values based on chosen testing browser. Default to chrome.
        cls._browser = str(getattr(settings, 'SELENIUM_TEST_BROWSER', 'chrome')).lower()

        if cls._browser == 'chrome':
            # Setup for Chrome browser.
            from webdriver_manager.chrome import ChromeDriverManager
            cls._service = ChromeService(executable_path=ChromeDriverManager().install())
        elif cls._browser == 'chromium':
            # Setup for Chromium browser.
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.utils import ChromeType
            cls._service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            cls._browser = 'chrome'
        elif cls._browser == 'firefox':
            # Setup for Firefox browser.
            from webdriver_manager.firefox import GeckoDriverManager
            cls._service = FireFoxService(executable_path=GeckoDriverManager().install())
        else:
            raise ValueError('Unknown browser "{0}".'.format(cls._browser))

    def create_driver(self):
        """Creates new browser window instance."""
        if self._browser == 'chrome':
            driver = webdriver.Chrome(service=self._service)
        elif self._browser == 'firefox':
            driver = webdriver.Firefox(service=self._service)

        self.sleep_browser(10)

        driver.quit()

    def sleep_browser(self, seconds):
        """Halts browser for provided number of seconds.

        Useful for visually verifying browser state, when trying to debug tests.
        """
        time.sleep(seconds)


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
