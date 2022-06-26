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

    def show_debug_content(self, response_content, strip_start=None, strip_end=None):
        """Prints debug response page output."""

        # Handle for potential param types.
        if isinstance(response_content, HttpResponseBase):
            response_content = response_content.content.decode('utf-8')
        elif isinstance(response_content, bytes):
            response_content = response_content.decode('utf-8')
        else:
            response_content = str(response_content)

        # Standardize output for easier analysis.
        response_content = self.standardize_characters(response_content)
        response_content = self.standardize_newlines(response_content)

        # Print out section header.
        self._debug_print()
        self._debug_print('strip_start:')
        self._debug_print(strip_start)
        self._debug_print('strip_end:')
        self._debug_print(strip_end)
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.content'),
            fore=Fore.WHITE,
            style=f"{Style.BRIGHT}{UNDERLINE}",
        )

        if response_content:
            # Check if strip sections provided.
            if strip_start or strip_end:
                # One or both strip sections provided. Add subsection coloring logic.

                # Validate and initialize for coloring.
                if strip_start is None:
                    strip_start = ''
                strip_start = str(strip_start)
                if strip_end is None:
                    strip_end = ''
                strip_end = str(strip_end)

                self._debug_print('\n\n\n\n')
                self._debug_print()
                self._debug_print('----------------------')
                self._debug_print()
                self._debug_print('response_content:')
                self._debug_print(response_content)

                # Parse out subsections.
                response_content, start_subsection = self._strip_content_subsection(
                    response_content,
                    strip_start,
                    'content_starts_after',
                )
                response_content, end_subsection = self._strip_content_subsection(
                    response_content,
                    strip_end,
                    'content_ends_before',
                )

                self._debug_print()
                self._debug_print('----------------------')
                self._debug_print()
                self._debug_print('start_subsection:')
                self._debug_print(start_subsection)
                self._debug_print()
                self._debug_print('----------------------')
                self._debug_print()
                self._debug_print('end_subsection:')
                self._debug_print(end_subsection)
                self._debug_print()
                self._debug_print('----------------------')
                self._debug_print()
                self._debug_print('response_subsection:')
                self._debug_print(response_content)
                self._debug_print()
                self._debug_print('----------------------')
                self._debug_print()
                self._debug_print('\n\n\n\n')

                # Print sections, divided by coloring.
                # self._debug_print(response_content)
                self._debug_print('{0}{1}{2}{3}{4}{5}'.format(
                    Fore.YELLOW,
                    start_subsection,
                    Style.RESET_ALL,
                    response_content,
                    Fore.YELLOW,
                    end_subsection,
                ))
                self._debug_print()

            else:
                # No strip sections. Provide standard content output.
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

    def _strip_content_subsection(self, current_content_subsection, strip_section, section_desc):
        """Strips provided value out of current content subsection.

        :param current_content_subsection: Current subsection of content, after previous value strippings.
        :param strip_section: Current value intended to be stripped out of content for search.
        :param section_desc: "content_starts_after" / "content_ends_before" variable name.
        :raises: Assertion failure if "strip" value does not exist in content subsection.
        :return: Stripped content subsection.
        """
        if strip_section is None or strip_section == '':
            return current_content_subsection, ''

        current_content_subsection = self.get_minimized_response_content(
            current_content_subsection,
            strip_newlines=False,
        )

        # Check which section type we're handling.
        if section_desc == 'content_starts_after':

            # First check that value actually exists in provided response.
            # Because we can't strip if this initial value is not present.
            stripped_val = self._verify_strip_content_value(
                current_content_subsection,
                strip_section,
                section_desc,
            )

            # If we made it this far, then value exists. Generate subsections.
            modified_subsection = stripped_val.join(current_content_subsection.split(stripped_val)[1:])
            stripped_subsection = current_content_subsection.split(stripped_val)[0] + stripped_val

            print('\n')
            print('modified_subsection:')
            print(modified_subsection)
            print('\n')
            print('stripped_subsection:')
            print(stripped_subsection)
            print('\n')

            return (modified_subsection, stripped_subsection)
        elif section_desc == 'content_ends_before':

            # First check that value actually exists in provided response.
            # Because we can't strip if this initial value is not present.
            stripped_val = self._verify_strip_content_value(
                current_content_subsection,
                strip_section,
                section_desc,
            )

            # If we made it this far, then value exists. Generate subsections.
            modified_subsection = stripped_val.join(current_content_subsection.split(stripped_val)[:1])
            stripped_subsection = stripped_val + current_content_subsection.split(stripped_val)[-1]
            return (modified_subsection, stripped_subsection)
        else:
            raise ValueError('Unknown section descriptor of "{0}".'.format(section_desc))

    def _verify_strip_content_value(self, current_content_subsection, strip_section, section_desc):
        """Verifies that provided "strip" value is found in current content section.

        :param current_content_subsection: Current subsection of content, after previous value strippings.
        :param strip_section: Current value intended to be stripped out of content for search.
        :param section_desc: "content_starts_after" / "content_ends_before" variable name.
        :raises: Assertion failure if "strip" value does not exist in content subsection.
        :return: Minimized strip section.
        """
        strip_err_msg = 'Could not find "{0}" value in content response. Provided value was:\n{1}'

        # Get minimized strip value.
        # strip_minimized = self.get_minimized_response_content(strip_section, strip_newlines=True)
        # content_minimized = self.get_minimized_response_content(current_content_subsection, strip_newlines=True)

        # Problem: Template output might not match user-provided test values.
        # However, can't solve this with the normal "remove all whitespace" solution, because we want to ultimately
        #   output the stripped value to the console. Removing whitespacing would break the formatting.
        #   But we also still need to be able to find matches (despite whitespace inconsistencies) and strip down
        #   subsections, as long as everything except whitespace matches.
        # Was considering using regex. But then maybe have to sanitize the entire "standardization" for regex output
        #   and ugh. It gets messy and complicated very fast.
        # Spent like 6+ hours trying to determine initial logic, make new functions, create tests, determine problem
        #   location, etc etc. Giving up for the moment.
        strip_minimized = re.sub(r'((\s)+)', '((\s)+)', strip_section)
        content_minimized = current_content_subsection

        print('\n\n\n\n')
        print('strip_minimized:')
        print(strip_minimized)
        print('')
        print('current_content_subsection:')
        print(current_content_subsection)
        print('')
        print('content_minimized:')
        print(content_minimized)

        # verify that strip value is found in current content subsection.
        # if strip_minimized not in content_minimized:
        if not re.search(strip_minimized, content_minimized):
            # Not found. Raise error.
            display_strip = self.get_minimized_response_content(strip_section, strip_newlines=False)
            # print('')
            # print('display_strip:')
            # print(display_strip)
            # print('\n\n\n\n')
            self.fail(strip_err_msg.format(section_desc, display_strip))

        # Return minimized strip value, so we don't have to recompute it later.
        return strip_minimized

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
