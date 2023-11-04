"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.

# Third-Party Imports.
from django.test import LiveServerTestCase as DjangoLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService

# Internal Imports.
from django_expanded_test_cases.constants import (
    ETC_SELENIUM_BROWSER,
    ETC_SELENIUM_HEADLESS,
    ETC_SELENIUM_DISABLE_CACHE,
    ETC_SELENIUM_EXTRA_BROWSER_OPTIONS,
)
from django_expanded_test_cases.mixins.live_server_mixin import LiveServerMixin


class LiveServerTestCase(DjangoLiveServerTestCase, LiveServerMixin):
    """Uses Django package to test functionality through selenium. Simulates web browser navigation."""

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
        cls._browser = str(ETC_SELENIUM_BROWSER).lower()

        if cls._browser in ['chrome', 'chromium']:
            # Setup for Chrome/Chromium browser.

            # Setup browser driver to launch browser with.
            try:
                # Attempt driver auto-install, if webdriver_manager package is present.
                cls._service = ChromeService()

                # Set required options to prevent crashing.
                chromeOptions = webdriver.ChromeOptions()
                # Disable any existing extensions on local chrome setup, for consistent test runs across machines.
                chromeOptions.add_argument('--disable-extensions')

                # Add any user-provided options.
                if ETC_SELENIUM_EXTRA_BROWSER_OPTIONS:
                    for browser_option in ETC_SELENIUM_EXTRA_BROWSER_OPTIONS:
                        chromeOptions.add_argument(browser_option)

                # TODO: Document these? Seemed to come up a lot in googling errors and whatnot.
                # # Avoid possible error in certain development environments about resource limits.
                # # Error is along the lines of "DevToolsActivePort file doesn't exist".
                # # See https://stackoverflow.com/a/69175552
                # chromeOptions.add_argument('--disable-dev-shm-using')
                # # Avoid possible error when many drivers are opened.
                # # See https://stackoverflow.com/a/56638103
                # chromeOptions.add_argument("--remote-debugging-port=9222")

                # Save options.
                cls._options = chromeOptions

            except ModuleNotFoundError:
                # Fall back to manual installation handling.

                if cls._browser == 'chrome':
                    # For Chrome.
                    cls._service = ChromeService(executable_path='/usr/local/share/chromedriver')

                if cls._browser == 'chromium':
                    # For Chromium.
                    cls._service = ChromeService(executable_path='/usr/local/share/chromedriver')

            # Everything else should handle the same for both.
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

        # Add universal options based on project settings.
        if ETC_SELENIUM_HEADLESS:
            cls._options.add_argument('headless')
        if ETC_SELENIUM_DISABLE_CACHE:
            cls._options.add_argument('disable-application-cache')

        # Create initial testing driver, one for each test.
        cls.driver = cls.create_driver(cls)

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

        self._error_displayed = False

    def subTest(self, *args, **kwargs):
        # Call CoreMixin logic.
        self.sub_test()

        # Run parent logic.
        return super().subTest(*args, **kwargs)

    @classmethod
    def tearDownClass(cls):
        # Close all remaining driver instances for class.
        while len(cls._driver_set) > 0:
            cls.close_driver(cls, cls._driver_set[0])

        # Call parent teardown logic.
        super().tearDownClass()

    def tearDown(self):
        # TODO: Below seems probably unecessary? Research more.
        # # Close all remaining window instances for test.
        # # (Or at least attempt to for default driver for test).
        # self.close_all_windows(self.driver)

        # Call parent teardown logic.
        super().tearDown()


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
