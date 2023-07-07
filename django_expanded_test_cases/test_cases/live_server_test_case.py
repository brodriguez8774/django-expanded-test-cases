"""
Testing logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
import time

# Third-Party Imports.
from django.test import LiveServerTestCase as DjangoLiveServerTestCase
# from django.test.selenium import LiveServerTestCase
# from django.test.selenium import SeleniumTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService
from channels.testing import ChannelsLiveServerTestCase as DjangoChannelsLiveServerTestCase
from django.conf import settings

# Internal Imports.
from django_expanded_test_cases.mixins.response_mixin import ResponseTestCaseMixin

from django_expanded_test_cases.constants import (
    ETC_OUTPUT_ERROR_COLOR,
    ETC_RESPONSE_DEBUG_URL_COLOR,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_RESPONSE_DEBUG_HEADER_COLOR,
    ETC_RESPONSE_DEBUG_CONTEXT_COLOR,
    ETC_RESPONSE_DEBUG_MESSAGE_COLOR,
    ETC_RESPONSE_DEBUG_SESSION_COLOR,
    ETC_RESPONSE_DEBUG_FORM_COLOR,
    ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
    ETC_OUTPUT_EMPHASIS_COLOR,
)


class LiveServerTestCase(DjangoLiveServerTestCase, ResponseTestCaseMixin):
    """Testing functionality through selenium, to simulate web browser navigation."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreMixin setup logic.
        cls.set_up_class(debug_print=debug_print)

        # Populate some initial values.
        cls.site_root_url = None
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
        self.site_root_url = self.live_server_url

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

    # region Utility Functions

    def create_driver(self):
        """Creates new browser manager instance."""

        # Create instance, based on selected driver type.
        if self._browser == 'chrome':
            driver = webdriver.Chrome(service=self._service, options=self._options)
        elif self._browser == 'firefox':
            driver = webdriver.Firefox(service=self._service, options=self._options)
        else:
            raise ValueError('Unknown browser "{0}".'.format(self._browser))

        # Make class aware of window.
        self._driver_set.append(driver)

        # Intentionally wait one second to allow setup.
        # TODO: Is this needed?
        #  https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.LiveServerTestCase Seems to imply maybe it is beneficial.
        driver.implicitly_wait(10)

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

    def is_webdriver(self, obj):
        """Verifies if object matches set on known web driver types."""

        # Import all known drivers for type checking.
        from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
        from selenium.webdriver.chromium.webdriver import RemoteWebDriver as ChromiumDriver
        from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
        from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxDriver
        from selenium.webdriver.ie.webdriver import WebDriver as IeDriver
        from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver

        # Check against known drivers.
        if (
            isinstance(obj, ChromeDriver)
            or isinstance(obj, ChromiumDriver)
            or isinstance(obj, EdgeDriver)
            or isinstance(obj, FireFoxDriver)
            or isinstance(obj, IeDriver)
            or isinstance(obj, SafariDriver)
        ):
            # Matched a known driver.
            return True
        else:
            # Did not match any known drivers.
            return False

    def show_debug_data(self, content):
        """"""
        self.show_debug_url(None)
        self.show_debug_content(content)

    def show_debug_url(self, url):
        """Prints debug url output."""

        # Skip if no Url is present.
        if url is None or str(url).strip() == '':
            url = self.current_url
        if url is None or str(url).strip() == '':
            return
        else:
            return super().show_debug_url(url)

    def show_debug_content(self, content):
        """Prints debug response page output."""

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.content'),
            fore=ETC_RESPONSE_DEBUG_CONTENT_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # Print out data, if present.
        if content:
            self._debug_print(self.get_minimized_response_content(content))
            # self._debug_print(content)
            self._debug_print()

    # endregion Utility Functions


    # region Html Search Functions

    def find_elements_by_tag(self, content, element):
        """Finds all HTML elements that match the provided element tag.

        :param content: Content to search through.
        :param element: Html element to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_tag(content, element)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_tag(self, content, element):
        """Finds first HTML element that matches the provided element tag.

        :param content: Content to search through.
        :param element: Html element to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_tag(content, element)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_elements_by_id(self, content, element_id):
        """Finds all HTML elements that match the provided id.

        :param content: Content to search through.
        :param element_id: Element id to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_id(content, element_id)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_id(self, content, element_id):
        """Finds first HTML element that matches the provided id.

        :param content: Content to search through.
        :param element_id: Element id to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_id(content, element_id)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_elements_by_class(self, content, css_class):
        """Finds all HTML elements that match the provided css class.

        :param content: Content to search through.
        :param css_class: Css class to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_class(content, css_class)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_class(self, content, css_class):
        """Finds first HTML element that matches the provided css class.

        :param content: Content to search through.
        :param css_class: Css class to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_class(content, css_class)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_elements_by_css_selector(self, content, css_selector):
        """Finds all HTML elements that match the provided css selector.

        :param content: Content to search through.
        :param css_selector: Css selector to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_css_selector(content, css_selector)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_css_selector(self, content, css_selector):
        """Finds first HTML element that matches the provided css selector.

        :param content: Content to search through.
        :param css_selector: Css selector to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_css_selector(content, css_selector)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_elements_by_data_attribute(self, content, data_attribute, data_value):
        """Finds all HTML elements that match the provided data attribute and data value.

        :param content: Content to search through.
        :param data_attribute: The key of the data attribute to search for.
        :param data_value: The value of the data attribute to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_data_attribute(content, data_attribute, data_value)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_data_attribute(self, content, data_attribute, data_value):
        """Finds first HTML element that matches the provided data attribute and data value.

        :param content: Content to search through.
        :param data_attribute: The key of the data attribute to search for.
        :param data_value: The value of the data attribute to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_data_attribute(content, data_attribute, data_value)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_elements_by_name(self, content, element_name):
        """Finds all HTML elements that match the provided name attribute.

        :param content: Content to search through.
        :param element_name: Element name to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_name(content, element_name)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_name(self, content, element_name):
        """Finds first HTML element that matches the provided name attribute.

        :param content: Content to search through.
        :param element_name: Element name to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_name(content, element_name)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_elements_by_link_text(self, content, link_text):
        """Finds all HTML elements that match the provided link text.

        :param content: Content to search through.
        :param link_text: Link text to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_link_text(content, link_text)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_link_text(self, content, link_text):
        """Finds first HTML element that matches the provided link text.

        :param content: Content to search through.
        :param link_text: Link text to search for.
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_link_text(content, link_text)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    # endregion Html Search Functions


# Define acceptable imports on file.
__all__ = [
    'LiveServerTestCase',
]
