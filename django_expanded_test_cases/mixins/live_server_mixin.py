"""
Universal mixin logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
import time
from textwrap import dedent

# Third-Party Imports.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService

# Internal Imports.
from django_expanded_test_cases.constants import (
    ETC_INCLUDE_RESPONSE_DEBUG_URL,
    ETC_INCLUDE_RESPONSE_DEBUG_CONTENT,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_OUTPUT_EMPHASIS_COLOR,

    ETC_SELENIUM_BROWSER,
    ETC_SELENIUM_HEADLESS,
    ETC_SELENIUM_DISABLE_CACHE,
    ETC_SELENIUM_DEBUG_PORT_START_VALUE,
    ETC_SELENIUM_WINDOW_POSITIONS,
    ETC_SELENIUM_EXTRA_BROWSER_OPTIONS,
    ETC_SELENIUM_PAGE_TIMEOUT_DEFAULT,
    ETC_SELENIUM_IMPLICIT_WAIT_DEFAULT,
    ETC_SELENIUM_DRIVER_LEVEL,
)
from django_expanded_test_cases.exceptions import EtcSeleniumRuntimeError, EtcSeleniumSetUpError
from django_expanded_test_cases.mixins.response_mixin import ResponseTestCaseMixin


# Module Variables.
# Starting debug port, to get around remote-debugging-port option using the same value for all generated drivers,
# Using the same port seems to cause issues with allowing proper switching between drivers.
# Each generated driver increments this value by one, to guarantee all tests among all files should have unique ports.
SELENIUM_DEBUG_PORT = ETC_SELENIUM_DEBUG_PORT_START_VALUE


class LiveServerMixin(ResponseTestCaseMixin):
    """Universal logic for all selenium LiveServer test cases."""
    @classmethod
    def setUpClass(cls, *args, initial_driver_count=1, debug_print=None, **kwargs):
        """Test logic setup run at the start of class creation.

        :param initial_driver_count: Number of drivers to generate at the start of test class creation.
                                     Defaults to 1. Set to 0 to skip creating drivers at class level.
        :param debug_print: Optional bool that indicates if debug output should print to console.
                            Param overrides setting value if both param and setting are set.
        """
        # Verify some project settings.
        if ETC_SELENIUM_DRIVER_LEVEL not in ['class', 'method']:
            raise ValueError('Unknown value for ETC_SELENIUM_DRIVER_LEVEL. Should be either "class" or "method".')

        cls._initial_driver_count = initial_driver_count

        # Call CoreMixin setup logic.
        super().setUpClass(*args, debug_print=debug_print, **kwargs)

        # Verify variable types.
        try:
            cls._initial_driver_count = int(cls._initial_driver_count)
        except (TypeError, ValueError):
            raise EtcSeleniumSetUpError(
                'The setUpClass() initial_driver_count variable must be an integer. '
                'It refers to the number of drivers that are started up on test class creation, and defaults to 1.'
            )

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

            except ModuleNotFoundError:
                # Fall back to manual installation handling.

                if cls._browser == 'chrome':
                    # For Chrome.
                    cls._service = ChromeService(executable_path='/usr/local/share/chromedriver')

                if cls._browser == 'chromium':
                    # For Chromium.
                    cls._service = ChromeService(executable_path='/usr/local/share/chromedriver')

            # Set required chrome options.
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

            # Everything else should handle the same for both.
            cls._browser = 'chrome'

        elif cls._browser == 'firefox':
            # Setup for Firefox browser.

            # Setup browser driver to launch browser with.
            try:
                # Attempt driver auto-install, if webdriver_manager package is present.
                cls._service = FireFoxService()

            except ModuleNotFoundError:
                # Fall back to manual installation handling.
                cls._service = FireFoxService(executable_path='/usr/bin/geckodriver')

            # Set required chrome options.
            firefoxOptions = webdriver.FirefoxOptions()

            # Add any user-provided options.
            if ETC_SELENIUM_EXTRA_BROWSER_OPTIONS:
                for browser_option in ETC_SELENIUM_EXTRA_BROWSER_OPTIONS:
                    firefoxOptions.add_argument(browser_option)

            # Save options.
            cls._options = firefoxOptions

        else:
            raise ValueError('Unknown browser "{0}".'.format(cls._browser))

        # Add universal options based on project settings.
        if ETC_SELENIUM_HEADLESS:
            cls._options.add_argument('headless')
        if ETC_SELENIUM_DISABLE_CACHE:
            cls._options.add_argument('disable-application-cache')

        # Handle window position values.
        cls._window_positions = None
        if ETC_SELENIUM_WINDOW_POSITIONS:
            window_positions = list(ETC_SELENIUM_WINDOW_POSITIONS)
            if len(window_positions) > 0:
                cls._window_positions = window_positions
                cls._window_position_index = 0

        if ETC_SELENIUM_DRIVER_LEVEL == 'class':
            # Create initial testing driver(s) at class level.
            for index in range(int(cls._initial_driver_count)):
                cls.create_driver(cls)

    def setUp(self, *args, **kwargs):
        """Test logic setup run at the start of function/method execution."""

        # Call parent logic.
        super().setUp(*args, **kwargs)

        self._error_displayed = False

        if ETC_SELENIUM_DRIVER_LEVEL == 'method':
            # Create initial testing driver(s) at method level.
            for index in range(int(self._initial_driver_count)):
                self.create_driver()

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        """Test logic setup run at the end of class execution, as part of termination/clean up."""

        # Call parent teardown logic.
        super().tearDownClass(*args, **kwargs)

        # Close all remaining driver instances for class.
        while len(cls._driver_set) > 0:
            cls.close_driver(cls, cls._driver_set[0])

    # region Utility Functions

    def create_driver(self, switch_window=True):
        """Creates new browser manager instance.

        Each driver represents one or more browser windows, each with a set of one or more tabs.
        :param switch_window: Bool indicating if window should be immediately switched to after creation.
        """
        try:

            # Handle window positions, if set.
            # If not provided, then defaults to however the OS spawns windows in.

            self._window_positions = ETC_SELENIUM_WINDOW_POSITIONS
            self._window_position_index = 0
            if self._window_positions:
                # Window position value exists. Attempt to read in.
                try:
                    # Pull x and y pixel location from provided data.
                    window_x, window_y = self._window_positions[self._window_position_index]
                except IndexError:
                    # Must have gone through all provided values. Loop back to first index.
                    self._window_position_index = 0
                    window_x, window_y = self._window_positions[self._window_position_index]

                # Rotate through provided values so that no consecutive two window spawns use the same location.
                self._window_position_index += 1

                # Add window position data to driver options.
                self._options.add_argument('window-position={0},{1}'.format(window_x, window_y))
            else:
                self._options.add_argument('window-position={0},{1}'.format(0, 0))

            # Avoid possible error when many drivers are opened.
            # See https://stackoverflow.com/a/56638103
            global SELENIUM_DEBUG_PORT
            SELENIUM_DEBUG_PORT += 1

            # Create instance, based on selected driver type.
            if self._browser == 'chrome':

                self._options.add_argument('--remote-debugging-port={0}'.format(SELENIUM_DEBUG_PORT))
                driver = webdriver.Chrome(service=self._service, options=self._options)
            elif self._browser == 'firefox':
                self._service = webdriver.firefox.service.Service(port=SELENIUM_DEBUG_PORT)
                driver = webdriver.Firefox(service=self._service, options=self._options)
            else:
                raise ValueError('Unknown browser "{0}".'.format(self._browser))

            # Set number of seconds to wait before giving up on page response.
            driver.set_page_load_timeout(ETC_SELENIUM_PAGE_TIMEOUT_DEFAULT)

            # Set number of seconds to wait before giving up on page element.
            driver.implicitly_wait(ETC_SELENIUM_IMPLICIT_WAIT_DEFAULT)

            # Make class aware of driver set.
            self._driver_set.append(driver)

            if switch_window:
                # Assume we want to auto-switch windows.
                driver.switch_to.window(driver.window_handles[-1])

        except ValueError as err:
            # Check type of error.
            if str(err) == 'I/O operation on closed file':
                # Likely is a known specific error.
                # Override output to be more descriptive/informative.
                exception_str = dedent(
                    """
                    Error attempting to open new Selenium Webdriver instance.
                    This is likely due to closing all prior Webdriver instances and then trying to open a new one.

                    To correct this issue, make sure at least one Webdriver instance is open at all times.

                    This includes leaving at least one driver instance open at the end of any test functions. The ETC
                    package should automatically handle cleanup and close all applicable pending windows/drivers at
                    the end of each test.
                    """
                )
                raise EtcSeleniumRuntimeError(exception_str)
            else:
                raise err

        return driver

    def get_driver(self, index=-1, switch_window=True):
        """Returns first driver off of driver stack, or creates new one if none are present.

        :param switch_window: Bool indicating if window should be immediately switched to after creation.
        """

        # Don't even attempt, index is not int.
        if not isinstance(index, int):
            return self.create_driver()

        # Attempt to get given index.
        try:
            driver = self._driver_set[index]
        except IndexError:
            # Invalid index. Create new instead.
            driver = self.create_driver()

        if switch_window:
            # Assume we want to auto-switch windows.
            driver.switch_to.window(driver.window_handles[-1])

        return driver

    def close_driver(self, driver):
        """Closes provided browser manager instance.

        :param driver: Driver manager object to close.
        """
        # Remove reference in class.
        self._driver_set.remove(driver)

        # Close driver itself.
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
        # Open blank new window and automatically switch.
        driver.switch_to.new_window('window')

    def open_new_tab(self, driver):
        """Opens a new window for the provided driver.

        :param driver: Driver manager object to generate window for.
        :return: New focus window.
        """
        # Open blank new window.
        driver.switch_to.new_window('tab')

        # Switch to recently created window.
        return self.switch_to_window(driver, len(driver.window_handles) - 1)

    def close_window(self, driver, window_index):
        """Closes a window at specific index for the provided driver.

        :param driver: Driver manager object containing the desired window.
        :param window_index: Index of window to close.
        """
        # Close window.
        self.switch_to_window(driver, window_index)
        driver.close()

    def close_all_windows(self, driver):
        """Closes all open windows for a given driver.

        :param driver: Driver manager object to close windows for.
        """
        # Iterate upon all windows until none remain.
        while len(driver.window_handles) > 1:
            self.close_window(driver, 0)

    def close_all_other_windows(self, driver, window_index_to_keep):
        """Closes all open windows, except for window at given index.

        :param driver: Driver manager object containing the desired window.
        :param window_index: Index of window to keep open.
        """
        # Iterate upon all windows until none remain.
        while len(driver.window_handles) > 2:
            if window_index_to_keep == 0:
                self.close_window_at_index(driver, 1)
            else:
                self.close_window_at_index(driver, 0)

    def switch_to_window(self, driver, window_index):
        """Sets window at specific driver/index to be the current focus.

        :param driver: Driver manager object containing the desired window.
        :param window_index: Index of window to switch to.
        :return: New focus window.
        """
        # Attempt to get window at specified driver index.
        try:
            focus_window = driver.window_handles[window_index]
        except IndexError:
            err_msg = 'Attempted to switch to window of index "{0}", but driver only has {1} windows open.'.format(
                window_index,
                len(driver.window_handles)
            )
            raise IndexError(err_msg)

        # Switch window to be focused.
        driver.switch_to.window(focus_window)

        # Return newly switched window.
        return focus_window

    def sleep_driver(self, seconds):
        """Halts driver for provided number of seconds.

        Useful for visually verifying browser state, when trying to debug tests.
        """
        time.sleep(seconds)

    def sleep_browser(self, seconds):
        """Halts browser for provided number of seconds. Alias for sleep_driver().

        Useful for visually verifying browser state, when trying to debug tests.
        """
        time.sleep(seconds)

    def is_webdriver(self, obj):
        """Verifies if object matches set of known web driver types."""

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
        if ETC_INCLUDE_RESPONSE_DEBUG_URL:
            self.show_debug_url(None)
        if ETC_INCLUDE_RESPONSE_DEBUG_CONTENT:
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

    def find_elements_by_text(self, content, text, element_type=None):
        """Finds all HTML elements that match the provided inner text.

        :param content: Content to search through.
        :param text: Element text to search for.
        :param element_type: Optionally filter by type of element as well (h1, p, li, etc).
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_elements_by_text(content, text, element_type=element_type)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    def find_element_by_text(self, content, text, element_type=None):
        """Finds first HTML element that matches the provided inner text.

        :param content: Content to search through.
        :param text: Element text to search for.
        :param element_type: Optionally filter by type of element as well (h1, p, li, etc).
        """
        self.current_url = None

        # Handle if webdriver was provided.
        # Otherwise assume was standard "page content".
        if self.is_webdriver(content):
            self.current_url = content.current_url
            content = content.page_source

        try:
            # Return original parent call with correct variables.
            return super().find_element_by_text(content, text, element_type=element_type)
        except Exception as err:
            self.show_debug_data(content)
            raise err

    # endregion Html Search Functions


# Define acceptable imports on file.
__all__ = [
    'LiveServerMixin',
]
