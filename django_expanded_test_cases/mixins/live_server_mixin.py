"""
Universal mixin logic for live server instances, such as through selenium.
Useful for testing things like JavaScript logic.

Tends to take longer to test. So consider using IntegrationTestCase instead, when possible.
"""

# System Imports.
import time

# Third-Party Imports.
from selenium import webdriver

# Internal Imports.
from django_expanded_test_cases.constants import (
    ETC_INCLUDE_RESPONSE_DEBUG_URL,
    ETC_INCLUDE_RESPONSE_DEBUG_CONTENT,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_OUTPUT_EMPHASIS_COLOR,
)
from django_expanded_test_cases.mixins.response_mixin import ResponseTestCaseMixin


class LiveServerMixin(ResponseTestCaseMixin):
    """Universal logic for all selenium LiveServer test cases."""

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

        # Set to check page for 5 seconds before giving up on element.
        driver.implicitly_wait(5)

        return driver

    def get_driver(self):
        """Returns first driver off of driver stack, or creates new one if none are present."""
        try:
            return self._driver_set[-1]
        except IndexError:
            return self.create_driver()

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

    # endregion Html Search Functions


# Define acceptable imports on file.
__all__ = [
    'LiveServerMixin',
]
