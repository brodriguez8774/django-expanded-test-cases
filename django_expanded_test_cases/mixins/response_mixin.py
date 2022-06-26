"""
Core testing logic that pertains to handling Response objects.
"""

# System Imports.
import re
from colorama import Fore, Style
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseBase

# User Imports.
from . import CoreTestCaseMixin
from django_expanded_test_cases.constants import UNDERLINE


class ResponseTestCaseMixin(CoreTestCaseMixin):
    """Includes testing logic used in handling Response objects."""

    @classmethod
    def set_up_class(cls, debug_print=None):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase, calling the literal function
        here would override instead.

        :param debug_print: Optional bool that indicates if debug output should print to console.
                            Param overrides setting value if both param and setting are set.
        """
        # Run parent setup logic.
        super().set_up_class(debug_print=debug_print)

    # region Debug Output Functions

    def show_debug_content(self, response_content):
        """Prints debug response page output."""

        # Handle for potential param types.
        if isinstance(response_content, HttpResponseBase):
            response_content = response_content.content.decode('utf-8')
        elif isinstance(response_content, bytes):
            response_content = response_content.decode('utf-8')

        # Standardize output for easier analysis.
        response_content = self.standardize_characters(response_content)
        response_content = self.standardize_newlines(response_content)

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.content'),
            fore=Fore.WHITE,
            style=f"{Style.BRIGHT}{UNDERLINE}",
        )

        # Print out data, if present.
        if response_content:
            self._debug_print(response_content)
            self._debug_print()

    def show_debug_headers(self, response_headers):
        """Prints debug response header data."""

        # Handle for potential param types.
        if isinstance(response_headers, HttpResponseBase):
            # Actual attr name seemed to change based on settings definitions.
            # Unsure of why though? May want to figure out details at later date.
            # This should account for both instances I'm pretty sure I encountered, though.
            if hasattr(response_headers, 'headers'):
                response_headers = response_headers.headers
            elif hasattr(response_headers, '_headers'):
                response_headers = response_headers._headers
            else:
                response_headers = None

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.headers'),
            fore=Fore.WHITE,
            style=f"{Style.BRIGHT}{UNDERLINE}",
        )

        # Print out data, if present.
        if response_headers is not None and len(response_headers) > 0:
            for key, value in response_headers.items():
                self._debug_print('    * "{0}": "{1}"'.format(key, value))
        else:
            self._debug_print('    No response headers found.')
        self._debug_print()

    def show_debug_context(self, response_context):
        """Prints debug response context data."""
        raise NotImplementedError()

    def show_debug_session_data(self, client):
        """Prints debug response session data."""

        # Handle for potential param types.
        if isinstance(client, HttpResponseBase):
            client = client.client

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'client.session'),
            fore=Fore.MAGENTA,
            style=f"{Style.BRIGHT}{UNDERLINE}",
        )

        if client is not None and len(client.session.items()) > 0:
            for key, value in client.session.items():
                self._debug_print('    * {0}: {1}'.format(key, value), fore=Fore.MAGENTA)
        else:
            self._debug_print('    No session data found.', fore=Fore.MAGENTA)
        self._debug_print('')

    def show_debug_form_data(self, response_context):
        """Prints debug response form data."""
        raise NotImplementedError()

    def show_debug_messages(self, response_context):
        """Prints debug response message data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            response_context = response_context.context

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.context["messages"]'),
            fore=Fore.BLUE,
            style=f"{Style.BRIGHT}{UNDERLINE}",
        )

        # Print out data, if present.
        if response_context is not None and 'messages' in response_context:
            messages = response_context['messages']
            if len(messages) > 0:
                for message in messages:
                    self._debug_print('    * "{0}"'.format(message), fore=Fore.BLUE)
            else:
                self._debug_print('    No context messages found.', fore=Fore.BLUE)
        self._debug_print()

    def show_debug_user_info(self, user):
        """Prints debug user data."""

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'User Info'),
            fore=Fore.CYAN,
            style=f"{Style.BRIGHT}{UNDERLINE}",
        )

        # Only proceed if we got a proper user model.
        if isinstance(user, get_user_model()):

            # General user information.
            self._debug_print('    * Username: "{0}"'.format(user.username), fore=Fore.CYAN)
            self._debug_print('    * First: "{0}"'.format(user.first_name), fore=Fore.CYAN)
            self._debug_print('    * Last: "{0}"'.format(user.last_name), fore=Fore.CYAN)
            self._debug_print('    * Email: "{0}"'.format(user.email), fore=Fore.CYAN)

            # User auth data.
            self._debug_print('    * is_authenticated: {0}'.format(user.is_authenticated), fore=Fore.CYAN)

            # User groups.
            self._debug_print('    * User Groups: {0}'.format(user.groups.all()), fore=Fore.CYAN)

            # User permissions.
            self._debug_print('    * User Permissions: {0}'.format(user.user_permissions.all()), fore=Fore.CYAN)

            self._debug_print()

        else:
            self._debug_print('    * Invalid user "{0}" of type "{1}". Expected "{2}".'.format(
                user,
                type(user),
                type(get_user_model()),
            ), fore=Fore.RED)
        self._debug_print()

    # endregion Debug Output Functions.

    def standardize_html_tags(self, value):
        """Standardizes spacing around html-esque elements, to remove unnecessary spacing.

        For example, "<h1> MyHeader </h1>" will simplify down to "<h1>MyHeader</h1>".

        Ensures that the actual expected value can be directly checked,
        instead of trying to account for extraneous template whitespacing.

        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Remove any whitespace around an opening html bracket ( < ).
        value = re.sub(r'(( )*)<(( )*)', '<', value)

        # Remove any whitespace around a closing html bracket ( > ).
        value = re.sub(r'(( )*)>(( )*)', '>', value)

        # Remove any whitespace around an opening array bracket ( [ ).
        value = re.sub(r'(( )*)\[(( )*)', '[', value)

        # Remove any whitespace around a closing array bracket ( ] ).
        value = re.sub(r'(( )*)](( )*)', ']', value)

        # Remove any whitespace around an opening dict bracket ( { ).
        value = re.sub(r'(( )*){(( )*)', '{', value)

        # Remove any whitespace around a closing dict bracket ( } ).
        value = re.sub(r'(( )*)}(( )*)', '}', value)

        return value

    def get_minimized_response_content(self, response, strip_newlines=False):
        """Returns response content, but with minimalistic formatting.

        For example, will trim all newline characters and repeating spaces.
        Also will standardize common characters to output in a single format.

        :param response: Response object or response content to parse.
        :param strip_newlines: Optional bool, indicating if all newlines should be converted into spaces,
            for extra-minimalistic formatting.
            Generally True for UnitTest direct comparison. False for console output/human examination.
        :return: Formatted response content.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            response_content = response.content.decode('utf-8')
        else:
            response_content = str(response)

        # Standardize basic characters, for easier comparison.
        response_content = self.standardize_characters(response_content)

        # Trim all extra whitespaces, for easier comparison.
        if strip_newlines:
            # All whitespace is converted into a single space.
            # Newlines are also converted into a single space.
            response_content = self.standardize_whitespace(response_content)
        else:
            # All whitespace is converted into a single space.
            # Repeating newlines are condensed down into a single newline.
            response_content = self.standardize_newlines(response_content)

        # Further trim whitespace around specific characters, for easier comparison.
        response_content = self.standardize_html_tags(response_content)

        return response_content


# Define acceptable imports on file.
__all__ = [
    'ResponseTestCaseMixin',
]
