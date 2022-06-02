"""
Testing logic for views and other multi-part components.
"""

# System Imports.
import re
from django.conf import settings
from django.http.response import HttpResponseBase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

# User Imports.
from .base_test_case import BaseTestCase
from django_expanded_test_cases.mixins import ResponseTestCaseMixin


class IntegrationTestCase(BaseTestCase, ResponseTestCaseMixin):
    """Testing functionality for views and other multi-part components."""

    @classmethod
    def setUpClass(cls, *args, debug_print=None, **kwargs):
        # Run parent setup logic.
        super().setUpClass(debug_print=None)

        # Initialize url variables.
        cls.login_url = reverse(settings.LOGIN_URL)
        cls._site_root_url = None

    # region Custom Assertions

    def assertResponse(
        self,
        url, *args,
        get=True, data=None,
        expected_status=200, expected_title=None, expected_header=None, expected_messages=None, expected_content=None,
        **kwargs,
    ):
        """Verifies the view response object at given URL matches provided parameters.

        At minimum, gets a response object from parsing provided url, then asserts the status code matches.
        Optionally also allows testing:
            * Title - The expected title, aka what displays in the browser tab text at the top of the browser.
            * Header (H1 tag) - The expected H1 header tag on the page.
            * Messages - One or more messages, generated from the Django messages framework.
            * Content - One or more values that should physically appear within html rendering.

        :param url: Url to get response object from.
        :param get: Bool indicating if response is GET or POST. Defaults to GET.
        :param data: Optional dict of items to pass into response generation.
        :param expected_status: Expected status code, after any redirections. Default code of 200.
        :param expected_title: Expected page title to verify. Skips title test if left as None.
        :param expected_header: Expected page h1 to verify. Skips header test if left as None.
        :param expected_messages: Expected context messages to verify. Skips message test if left as None.
        :param expected_content: Expected page content elements to verify. Skips content test if left as None.
        """
        # Run logic to get corresponding response object.
        response = self._get_page_response(url, *args, get=get, data=data, **kwargs)

        # Optionally output all debug info for found response.
        if self._debug_print_bool:
            self.show_debug_content(response)
            # self.show_debug_context(response)
            self.show_debug_session_data(response)
            # self.show_debug_form_data(response)
            self.show_debug_messages(response)
            self.show_debug_user_info(response)

        # Verify page status code.
        self.assertStatusCode(response, expected_status)

        # Verify page title.
        if expected_title is not None:
            self.assertPageTitle(response, expected_title)

        # Verify page header.
        if expected_header is not None:
            self.assertPageHeader(response, expected_header)

        # Verify page messages.
        if expected_messages is not None:
            self.assertContextMessages(response, expected_messages, debug_output=False)

        # Verify page content.
        if expected_content is not None:
            self.assertPageContent(response, expected_content, debug_output=False)

        # All assertions passed so far. Return response in case user wants to do further checks.
        return response

    def assertGetResponse(
        self,
        url, *args,
        data=None,
        expected_status=200, expected_title=None, expected_header=None, expected_messages=None, expected_content=None,
        **kwargs,
    ):
        """Verifies a GET response was found at given URL, and matches provided parameters."""

        # Call base function to handle actual logic.
        return self.assertResponse(
            url,
            *args,
            get=True,
            data=data,
            expected_status=expected_status,
            expected_title=expected_title,
            expected_header=expected_header,
            expected_messages=expected_messages,
            expected_content=expected_content,
            **kwargs,
        )

    def assertPostResponse(
        self,
        url, *args,
        data=None,
        expected_status=200, expected_title=None, expected_header=None, expected_messages=None, expected_content=None,
        **kwargs,
    ):
        """Verifies a GET response was found at given URL, and matches provided parameters."""

        # Handle mutable data defaults.
        data = data or {}

        # Forcibly add values to "data" dict, so that POST doesn't validate to empty in view.
        # This guarantees that view serves as POST, like this specific assertion expects.
        if data == {}:
            # Has no values. Forcibly add a single key-value pair.
            data = {'UnitTest': True}

        # Call base function to handle actual logic.
        return self.assertResponse(
            url,
            *args,
            get=False,
            data=data,
            expected_status=expected_status,
            expected_title=expected_title,
            expected_header=expected_header,
            expected_messages=expected_messages,
            expected_content=expected_content,
            **kwargs,
        )

    def assertStatusCode(self, response, expected_status):
        """Verifies the page status code value.

        :param response: Response object to check against.
        :param expected_status: Expected status code, after any redirections.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            actual_status = response.status_code
        else:
            actual_status = int(response)

        # Check status.
        self.assertEqual(
            actual_status,
            expected_status,
            'Expected status code (after potential redirects) of "{0}". Actual code was "{1}"'.format(
                expected_status,
                actual_status,
            ),
        )

        # Return status in case user wants to run additional logic on it.
        return actual_status

    def assertPageContent(self, response, expected_content, debug_output=True):
        """Verifies the page content html, similar to the built-in assertContains() function.

        The main difference is that Django templating may create large amounts of whitespace in response html,
        often in places where we wouldn't intuitively expect it, when running tests.

        Technically, the built-in assertHTMLEqual() and assertInHTML() functions exist, and probably could accomplish
        the same assertions. But we still need to parse and format full response object, to display for test failure
        debugging. So I'm not sure if it's helpful at that point to use those or use separate assertions like here.
        Perhaps examine more closely at a later date.

        :param response: Response object to check against.
        :param expected_content: Expected full string (or set of strings) of HTML content.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out and formatted content string.
        """
        if debug_output:
            # Print out actual response content, for debug output.
            self.show_debug_content(response)

        # Sanitize and format actual response content.
        actual_content = self.get_minimized_response_content(response, strip_newlines=True)

        err_msg = 'Response content does not match expected.'

        # Handle possible types.
        if expected_content is None:
            expected_content = ''
        if isinstance(expected_content, list) or isinstance(expected_content, tuple):
            # The expected_content param is an array of items. Verify they all exist on page.
            for expected in expected_content:
                expected = self.get_minimized_response_content(expected, strip_newlines=True)
                self.assertIn(expected, actual_content, err_msg)

        else:
            # Not an array of items. Assume is a single str value.
            expected_content = self.get_minimized_response_content(expected_content, strip_newlines=True)
            self.assertIn(expected_content, actual_content, err_msg)

        # Return page content in case user wants to run additional logic on it.
        return actual_content

    def assertPageTitle(self, response, expected_title, exact_match=True):
        """Verifies the page title HTML element.

        Note: Some sites have titles with nested elements.
            Ex: "<title><page> | <app> | <website></title>"

        Thus the "exact_match" bool exists, to allow only testing for a specific unit in the title, instead of
        always having to type the full title for every test.

        :param response: Response object to check against.
        :param expected_title: Expected full string in title HTML element.
        :param exact_match: Bool indicating if title should be exact match, or partial.
        :return: Parsed out title string.
        """
        # Parse out title element from response.
        actual_title = self.get_page_title(response)

        # Remove title tag from expected value, if present.
        expected_title = str(expected_title).strip()
        if expected_title.startswith('<title>'):
            expected_title = expected_title[7:]
        if expected_title.endswith('</title>'):
            expected_title = expected_title[:-8]
        expected_title = expected_title.strip()

        # Check element.
        if exact_match:
            self.assertEqual(
                expected_title,
                actual_title,
                'Expected title HTML contents of "{0}" (using exact matching). Actual value was "{1}"'.format(
                    expected_title,
                    actual_title,
                )
            )
        else:
            self.assertIn(
                expected_title,
                actual_title,
                'Expected title HTML contents of "{0}" (using partial matching). Actual value was "{1}"'.format(
                    expected_title,
                    actual_title,
                )
            )

        # Return title in case user wants to run additional logic on it.
        return actual_title

    def assertPageHeader(self, response, expected_header):
        """Verifies the page H1 header HTML element.

        :param response: Response object to check against.
        :param expected_header: Expected full string in H1 header HTML element.
        :return: Parsed out header string.
        """
        # Parse out H1 header element from response.
        actual_header = self.get_page_header(response)

        # Remove H1 tag from expected value, if present.
        expected_header = str(expected_header).strip()
        if expected_header.startswith('<h1>'):
            expected_header = expected_header[4:]
        if expected_header.endswith('</h1>'):
            expected_header = expected_header[:-5]
        expected_header = expected_header.strip()

        # Check element.
        self.assertEqual(
            expected_header,
            actual_header,
            'Expected H1 header HTML contents of "{0}". Actual value was "{1}"'.format(
                expected_header,
                actual_header,
            )
        )

        # Return header in case user wants to run additional logic on it.
        return actual_header

    def assertContextMessages(self, response, expected_messages, allow_partials=None, debug_output=True):
        """Verifies the context messages.

        :param response: Response object to check against.
        :param expected_messages: Expected string for message data.
        :param allow_partials: Bool indicating if messages should fully match or allow partial matches.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out header string.
        """
        if debug_output:
            # Print out actual messages, for debug output.
            self.show_debug_messages(response)

        # Parse out settings values.
        if allow_partials is None:
            allow_partials = getattr(settings, 'DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS', True)
        else:
            allow_partials = bool(allow_partials)

        # Parse out message data from response.
        actual_messages = self.get_context_messages(response)

        # Check format of expected value.
        if isinstance(expected_messages, list) or isinstance(expected_messages, tuple):
            # Array of messages passed. Verify each inner value is a str.
            temp_messages = []
            for message in expected_messages:
                message = str(message).strip()
                if len(message) > 0:
                    temp_messages.append(message)
            expected_messages = temp_messages

        elif expected_messages is None:
            # Handle for none type. Not sure why anyone would pass this into the test though.
            expected_messages = []

        elif isinstance(expected_messages, str):
            # For everything else, assume is intended to be a single message.
            message = str(expected_messages).strip()
            expected_messages = []
            if len(message) > 0:
                expected_messages.append(message)

        if len(expected_messages) > 0:
            # For now, we only care about values passed for expected_messages.
            # We ignore any cases where a message exists in the context, but is not explicitly
            # checked by the user in the expected_messages param.

            # One or more messages are expected. Verify they are found.
            for expected_message in expected_messages:
                message_found = False

                # Handle based on partials allowed or not.
                if allow_partials:
                    # Partial message matching is allowed.
                    # Expected value must match or be a substring of a message in context.
                    index = 0
                    while message_found is False and index < len(actual_messages):
                        if expected_message in actual_messages[index]:
                            message_found = True
                        index += 1

                else:
                    # Partial message matching is NOT allowed.
                    # Expected value must exactly match message in context.

                    # Loop through all context messages until found, or all are checked.
                    if expected_message in actual_messages:
                        message_found = True

                # Raise assertion error if not found.
                self.assertTrue(
                    message_found,
                    'Failed to find message "{0}" in context (Partial matching {1} allowed).'.format(
                        expected_message,
                        'is' if allow_partials else 'is NOT'
                    ),
                )

    # endregion Custom Assertions

    # region Helper Functions

    def _get_page_response(self, url, *args, get=True, data=None, **kwargs):
        """Helper function for assertResponse().

        Fully parses provided user url, and returns corresponding response object.

        :param url: Url to get response object from.
        :return: Django response object for provided url.
        """
        # Handle mutable data defaults.
        data = data or {}

        # Preprocess all potential url values.
        url = str(url).strip()
        current_site = '127.0.0.1'
        url_args = ()
        url_kwargs = {}

        # Handle site_root_url value.
        if self.site_root_url is not None:
            current_site = self.site_root_url

        # Standardize if literal site url was provided and user included site_root.
        if url.startswith(current_site):
            url = url[len(current_site):]

        # If "args" key or "kwargs" key exists in function kwargs param, assume is meant for url reverse.
        if 'args' in kwargs.keys():
            url_args = kwargs['args']
        if 'kwargs' in kwargs.keys():
            url_kwargs = kwargs['kwargs']

        # Attempt to get reverse of provided url.
        try:
            url = reverse(url, args=url_args, kwargs=url_kwargs)
        except NoReverseMatch:
            # Could not find as reverse. Assume is literal url.
            if len(url) > 0 and url[-1] != '/':
                url += '/'

        # Make sure exactly one slash is prepended to the url value.
        url = url.lstrip('/').rstrip('/')
        if len(url) == 0:
            url = '/'
        else:
            url = '/{0}/'.format(url)

        # Log url we're attempting to access.
        if self.site_root_url is not None:
            current_site = '{0}{1}'.format(self.site_root_url, url)
        else:
            current_site = '127.0.0.1{0}'.format(url)
        self._debug_print('Attempting to access url "{0}"'.format(current_site))

        # Get response object.
        if bool(get):
            response = self.client.get(url, data=data, follow=True)
        else:
            response = self.client.post(url, data=data, follow=True)
        response.url = current_site
        return response

    def get_page_title(self, response):
        """Parses out title HTML element from provided response.

        :param response: Response object or response content to get title from.
        :return: Parsed out response title, formatted to have extra whitespace removed.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            response = response.content.decode('utf-8')
        elif isinstance(response, bytes):
            response = response.decode('utf-8')

        # Find title element.
        response_title = re.search(r'<title>([\S\s]+)</title>', response)

        # Check that some value was found.
        # Certain response types may have no title, such as file download responses.
        if response_title is None:
            # No value found. Convert to empty string.
            response_title = ''

        elif response_title is not None:
            # Value was found. Pull from capture group.
            response_title = response_title.group(1)

            # Strip any newlines, if present.
            response_title = re.sub(r'(\n|\r)+', '', response_title)

            # Remove any repeating whitespace, plus any outer whitespace.
            response_title = re.sub(r'(\s)+', ' ', response_title).strip()

        # Return formatted title value.
        return response_title

    def get_page_header(self, response):
        """Parses out H1 header HTML element from provided response.

        :param response: Response object or response content to get H1 header from.
        :return: Parsed out response header, formatted to have extra whitespace removed.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            response = response.content.decode('utf-8')
        elif isinstance(response, bytes):
            response = response.decode('utf-8')

        # Find header element.
        response_header = re.search(r'<h1>([\S\s]+)</h1>', response)

        # Check that some value was found.
        # Handles if response did not have the H1 header element defined for some reason.
        # For example, likely to occur in responses that provide file downloads.
        if response_header is None:
            # No value found. Convert to empty string.
            response_header = ''

        elif response_header is not None:
            # Value was found. Pull from capture group.
            response_header = response_header.group(1)

            # Strip any newlines, if present.
            response_header = re.sub(r'(\n|\r)+', '', response_header)

            # Remove any repeating whitespace, plus any outer whitespace.
            response_header = re.sub(r'(\s)+', ' ', response_header).strip()

        # Return formatted header value.
        return response_header

    def get_context_messages(self, response):
        """Parses out context messages from provided response.

        :param response: Response object or response context to get messages from.
        :return: Parsed out response messages.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            context = response.context
        else:
            context = response

        # Attempt to parse messages from context.
        found_messages = []
        if (context is not None) and ('messages' in context) and (len(context['messages']) > 0):
            # Messages found in response context.
            messages = context['messages']

            for message in messages:
                found_messages.append(str(message.message).strip())

        # Return found messages.
        return found_messages

    # endregion Helper Functions


# Define acceptable imports on file.
__all__ = [
    'IntegrationTestCase',
]
