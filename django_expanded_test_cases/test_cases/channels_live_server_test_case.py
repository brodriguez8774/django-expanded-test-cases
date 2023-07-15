"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.

# Third-Party Imports.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService
from channels.testing import ChannelsLiveServerTestCase as DjangoChannelsLiveServerTestCase
from django.conf import settings

# Internal Imports.
from django_expanded_test_cases.mixins.live_server_mixin import LiveServerMixin


class ChannelsLiveServerTestCase(DjangoChannelsLiveServerTestCase, LiveServerMixin):
    """Uses DjangoChannels package to test functionality through selenium. Simulates web browser navigation."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreMixin setup logic.
        cls.set_up_class(debug_print=debug_print)

        # Populate some initial values.
        cls._driver_set = []
        cls._options = None

        # Import/Initialize some values based on chosen testing browser. Default to chrome.
        cls._browser = str(getattr(settings, 'SELENIUM_TEST_BROWSER', 'chrome')).lower()

        if cls._browser == 'chrome':
            # Setup for Chrome browser.

            # Setup browser driver to launch browser with.
            try:
                # Attempt driver auto-install, if webdriver_manager package is present.
                from webdriver_manager.chrome import ChromeDriverManager
                cls._service = ChromeService(executable_path=ChromeDriverManager().install())

                # Set required options to prevent crashing.
                chromeOptions = webdriver.ChromeOptions()
                chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
                chromeOptions.add_argument("--no-sandbox")
                chromeOptions.add_argument("--disable-setuid-sandbox")
                chromeOptions.add_argument("--remote-debugging-port=9222")
                chromeOptions.add_argument("--disable-dev-shm-using")
                chromeOptions.add_argument("--disable-extensions")
                chromeOptions.add_argument("--disable-gpu")
                chromeOptions.add_argument("disable-infobars")

                # Save options.
                cls._options = chromeOptions

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

        # Create initial testing driver.
        cls.create_driver(cls)

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


# Define acceptable imports on file.
__all__ = [
    'ChannelsLiveServerTestCase',
]
