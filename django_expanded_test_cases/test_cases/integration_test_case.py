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
from django_expanded_test_cases.mixins.response_mixin import ResponseTestCaseMixin


class IntegrationTestCase(BaseTestCase, ResponseTestCaseMixin):
    """Testing functionality for views and other multi-part components."""

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize url variables.
        cls.login_url = reverse(settings.LOGIN_URL)
        cls._site_root_url = None

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

    # region Custom Assertions

    def assertResponse(self, url, *args, get=True, data=None, expected_status=200, **kwargs):
        """Verifies the view response object at given URL matches provided parameters.

        :param url: Url to get response object from.
        :param expected_status: Expected status code, after any redirections. Default code of 200.
        """
        # Run logic to get corresponding response object.
        response = self._get_page_response(url, *args, get=get, data=data, **kwargs)

        # Verify page status code.
        self.assertStatusCode(response, expected_status)

        # All assertions passed so far. Return response in case user wants to do further checks.
        return response

    def assertGetResponse(self, url, *args, data=None, expected_status=200, **kwargs):
        """Verifies a GET response was found at given URL, and matches provided parameters."""

        # Call base function to handle actual logic.
        return self.assertResponse(
            url,
            *args,
            get=True,
            data=data,
            expected_status=expected_status,
            **kwargs,
        )

    def assertPostResponse(self, url, *args, data=None, expected_status=200, **kwargs):
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

    def assertContextMessages(self, response, expected_messages, allow_partials=None):
        """Verifies the context messages.

        :param response: Response object to check against.
        :param expected_messages: Expected string for message data.
        :param allow_partials: Bool indicating if messages should fully match or allow partial matches.
        :return: Parsed out header string.
        """
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
