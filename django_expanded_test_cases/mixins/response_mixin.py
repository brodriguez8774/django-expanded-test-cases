"""
Core testing logic that pertains to handling Response objects.
"""

# System Imports.
import json
import logging
import re
import warnings
from urllib.parse import parse_qs

# Third-Party Imports.
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import BaseForm, BaseFormSet
from django.forms.formsets import ManagementForm
from django.http.response import HttpResponseBase

# Internal Imports.
from . import CoreTestCaseMixin
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django_expanded_test_cases.constants import (
    ETC_DEBUG_PRINT__RESPONSE_SEPARATOR,
    ETC_DEBUG_PRINT__SKIP_DISPLAY,
    ETC_INCLUDE_RESPONSE_DEBUG_CONTENT,
    ETC_INCLUDE_RESPONSE_DEBUG_CONTEXT,
    ETC_INCLUDE_RESPONSE_DEBUG_FORMS,
    ETC_INCLUDE_RESPONSE_DEBUG_HEADER,
    ETC_INCLUDE_RESPONSE_DEBUG_MESSAGES,
    ETC_INCLUDE_RESPONSE_DEBUG_SESSION,
    ETC_INCLUDE_RESPONSE_DEBUG_USER_INFO,
    ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
    ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
    ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
    ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
    ETC_OUTPUT_EMPHASIS_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_RESET_COLOR,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_RESPONSE_DEBUG_CONTEXT_COLOR,
    ETC_RESPONSE_DEBUG_FORM_COLOR,
    ETC_RESPONSE_DEBUG_HEADER_COLOR,
    ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
    ETC_RESPONSE_DEBUG_MESSAGE_COLOR,
    ETC_RESPONSE_DEBUG_SESSION_COLOR,
    ETC_RESPONSE_DEBUG_URL_COLOR,
    ETC_SKIP_CONTENT_AFTER,
    ETC_SKIP_CONTENT_BEFORE,
    ETC_SKIP_CONTENT_HEAD,
)


# Initialize logging.
logger = logging.getLogger(__name__)


class ResponseTestCaseMixin(CoreTestCaseMixin):
    """Includes testing logic used in handling Response objects."""

    @classmethod
    def setUpClass(cls, *args, debug_print=None, **kwargs):
        """Test logic setup run at the start of class creation.

        :param debug_print: Optional bool that indicates if debug output should print to console.
                            Param overrides setting value if both param and setting are set.
        """
        # Run parent setup logic.
        super().setUpClass(*args, debug_print=debug_print, **kwargs)

    # region Debug Output Functions

    def full_debug_print(self, response, return_format='html', post_data=None, expected_json=None):
        """Attempts to display debug output for all of response data."""

        # Handle mutable data defaults.
        post_data = post_data or {}

        # Parse out different debug types.
        if ETC_INCLUDE_RESPONSE_DEBUG_CONTENT:
            if return_format == 'html':
                self.show_debug_content(response)
            elif return_format == 'json':
                self.show_debug_json_content(response, expected_json)
            else:
                raise ValueError('Currently supported return_format values are `html` or `json`.')
        if ETC_INCLUDE_RESPONSE_DEBUG_HEADER:
            self.show_debug_headers(response)
        if ETC_INCLUDE_RESPONSE_DEBUG_CONTEXT:
            self.show_debug_context(response)
        if ETC_INCLUDE_RESPONSE_DEBUG_SESSION:
            self.show_debug_session_data(response)
        if ETC_INCLUDE_RESPONSE_DEBUG_MESSAGES:
            self.show_debug_messages(response)
        if ETC_INCLUDE_RESPONSE_DEBUG_FORMS:
            self.show_debug_form_data(response, post_data)
        if ETC_INCLUDE_RESPONSE_DEBUG_USER_INFO:
            self.show_debug_user_info(response)

        # Optionally display custom debug-output separators for additional end-of-assertion clarity.
        if len(ETC_DEBUG_PRINT__RESPONSE_SEPARATOR) > 0:
            self._debug_print(ETC_DEBUG_PRINT__RESPONSE_SEPARATOR)

    def show_debug_url(self, url):
        """Prints debug url output."""

        # Ensure url is in consistent format.
        url = self.standardize_url(url, append_root=True)
        message = 'Attempting to access url "{0}"'.format(url)

        self._debug_print('\n\n')
        self._debug_print(
            '{0}'.format('-' * len(message)),
            fore=ETC_RESPONSE_DEBUG_URL_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )
        self._debug_print(
            message,
            fore=ETC_RESPONSE_DEBUG_URL_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )
        self._debug_print(
            '{0}'.format('-' * len(message)),
            fore=ETC_RESPONSE_DEBUG_URL_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

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

        # Handle ETC_SKIP_CONTENT_HEAD variable, if defined.
        skip_content_before = ETC_SKIP_CONTENT_BEFORE
        if ETC_SKIP_CONTENT_HEAD and skip_content_before is None:
            skip_content_before = '</head>'

        # Optionally attempt to trim content based on SKIP BEFORE/AFTER settings values.
        if skip_content_before is not None and len(skip_content_before) > 0:
            # Content was specified to skip.
            # Use regex to find and remove output.

            # Standardize provided settings string, so that it's easier to compare against and trim.
            skip_content_before = self.standardize_characters(skip_content_before)
            skip_content_before = self.standardize_whitespace(skip_content_before)

            # Correct some potential problematic characters specifically for this section of logic.
            with warnings.catch_warnings() as warn:
                skip_content_before = skip_content_before.replace('^', '\\^')
                skip_content_before = skip_content_before.replace('$', '\\$')
                skip_content_before = skip_content_before.replace('|', '\\|')
                skip_content_before = skip_content_before.replace('(', '\\(')
                skip_content_before = skip_content_before.replace(')', '\\)')
                skip_content_before = skip_content_before.replace(' ', '\\s+')

            # Trim the output.
            response_content = re.sub(
                r'^([\s\S]*){0}\s+'.format(skip_content_before),
                '',
                response_content,
            )

        if ETC_SKIP_CONTENT_AFTER is not None and len(ETC_SKIP_CONTENT_AFTER) > 0:
            # Content was specified to skip.
            # Use regex to find and remove output.

            # Standardize provided settings string, so that it's easier to compare against and trim.
            skip_content_after = self.standardize_characters(ETC_SKIP_CONTENT_AFTER)
            skip_content_after = self.standardize_whitespace(skip_content_after)

            # Correct some potential problematic characters specifically for this section of logic.
            with warnings.catch_warnings() as warn:
                skip_content_after = skip_content_after.replace('^', '\\^')
                skip_content_after = skip_content_after.replace('$', '\\$')
                skip_content_after = skip_content_after.replace('|', '\\|')
                skip_content_after = skip_content_after.replace('(', '\\(')
                skip_content_after = skip_content_after.replace(')', '\\)')
                skip_content_after = skip_content_after.replace(' ', '\\s+')

            # Trim the output.
            response_content = re.sub(
                r'\s+{0}([\s\S]*)$'.format(skip_content_after),
                '',
                response_content,
            )

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.content'),
            fore=ETC_RESPONSE_DEBUG_CONTENT_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # Print out data, if present.
        if response_content:

            # Attempt to remove all regex matches from content to display.
            for match_attempt in ETC_DEBUG_PRINT__SKIP_DISPLAY:

                # For each string, modify to match output formatting and convert to regex.
                match_attempt = r'{0}'.format(self.get_minimized_response_content(match_attempt))

                # Attempt to do content strip.
                response_content = re.sub(match_attempt, '', response_content)

            # Display content to console (only shows up on test error).
            self._debug_print(response_content)
            self._debug_print()

    def show_debug_json_content(self, response_content, expected_json):
        """Prints debug json response page output."""

        # Handle for potential param types.
        if isinstance(response_content, HttpResponseBase):
            # Try to get json_content variable, if present.
            if hasattr(response_content, 'json_content'):
                response_content = response_content.json_content
            else:
                # Attempt to parse from original content value.
                try:
                    response_content = json.loads(response_content.content.decode('utf-8'))
                except:
                    # Failed to parse original content value as Pythonic json object.
                    # Fall back to original content display method.
                    return self.show_debug_content(response_content.content.decode('utf-8'))
        elif isinstance(response_content, bytes):
            # Attempt to parse from original content value.
            try:
                response_content = json.loads(response_content.decode('utf-8'))
            except:
                # Failed to parse original content value as Pythonic json object.
                # Fall back to original content display method.
                return self.show_debug_content(response_content.decode('utf-8'))

        # If we made it this far, we should have a pythonic version of our json object.
        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.content'),
            fore=ETC_RESPONSE_DEBUG_CONTENT_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # Debug output based on if expected is provided or not.
        # Easier to just do the if statement once, depending on mode.
        if expected_json is not None:
            self._recurse_show_debug_json_content_with_coloring(response_content, expected_json)
        else:
            self._recurse_show_debug_json_content(response_content)
        self._debug_print()

    def _recurse_show_debug_json_content(self, data, indentation_level=1):
        """Recursive function to display full json data."""

        # Determine indentation formatting.
        if indentation_level == 1:
            prior_indentation = ''
        else:
            prior_indentation = '  ' * (indentation_level - 1)
        indentation = '  ' * indentation_level

        # Output values based on variable type.
        if isinstance(data, dict):
            # Dictionary type handling.

            self._debug_print(
                '{0}{1}'.format(prior_indentation, '{'),
            )

            for key, value in data.items():

                if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):
                    # Recursively call function to handle more complicated types.
                    self._debug_print(
                        '{0}"{1}":'.format(indentation, key),
                    )
                    self._recurse_show_debug_json_content(
                        value,
                        indentation_level=(indentation_level + 1),
                    )
                else:
                    # Simple types.
                    if isinstance(value, str):
                        # Add quotes for strings.
                        self._debug_print(
                            '{0}"{1}": "{2}",'.format(indentation, key, value),
                        )
                    else:
                        self._debug_print(
                            '{0}"{1}": {2},'.format(indentation, key, value),
                        )

            if indentation_level > 1:
                self._debug_print(
                    '{0}{1}'.format(prior_indentation, '},'),
                )
            else:
                self._debug_print(
                    '{0}{1}'.format(prior_indentation, '}'),
                )

        elif isinstance(data, list) or isinstance(data, tuple):
            # Array type handling.
            self._debug_print(
                '{0}{1}'.format(prior_indentation, '['),
            )

            for value in data:
                if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):
                    # Recursively call function to handle more complicated types.
                    self._recurse_show_debug_json_content(
                        value,
                        indentation_level=(indentation_level + 1),
                    )
                else:
                    # Simple types.
                    if isinstance(value, str):
                        # Add quotes for strings.
                        self._debug_print(
                            '{0}"{1}",'.format(indentation, value),
                        )
                    else:
                        self._debug_print(
                            '{0}{1},'.format(indentation, value),
                        )

            if indentation_level > 1:
                self._debug_print(
                    '{0}{1}'.format(prior_indentation, '],'),
                )
            else:
                self._debug_print(
                    '{0}{1}'.format(prior_indentation, ']'),
                )

        else:
            # All others.
            if isinstance(data, str):
                # Add quotes for strings.
                self._debug_print(
                    '{0}"{1}"'.format(indentation, data),
                )
            else:
                self._debug_print(
                    '{0}{1}'.format(indentation, data),
                )

    def _recurse_show_debug_json_content_with_coloring(
        self,
        actual_data,
        expected_data,
        indentation_level=1,
        level_exists=True,
    ):
        """Recursive function to display full json data."""

        next_level_exists = level_exists

        # Determine indentation formatting.
        if indentation_level == 1:
            prior_indentation = ''
        else:
            prior_indentation = '  ' * (indentation_level - 1)
        indentation = '  ' * indentation_level

        # Output values based on variable type.
        if isinstance(actual_data, dict):
            # Dictionary type handling.

            # Handle for container checks.
            # TODO: This maybe could be more efficiently organized.
            #   But at this point I just want it to work for now.
            container_text_color = ''
            if not level_exists:
                container_text_color = ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR
            elif type(actual_data) != type(expected_data):
                container_text_color = ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR
            elif len(actual_data) != len(expected_data):
                container_text_color = ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR

            self._debug_print(
                '{0}{1}{2}'.format(
                    prior_indentation,
                    container_text_color,
                    '{',
                ),
            )

            for key, value in actual_data.items():

                # Handle format of dict key.
                key_display = None
                next_expected = None
                next_level_exists = level_exists

                # Handle if prior recurse parent indicates this section doesn't exist in expected.
                if not level_exists:
                    key_display = '{0}{1}{2}'.format(
                        ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                        key,
                        ETC_OUTPUT_RESET_COLOR,
                    )

                # Determine if key is present.
                elif isinstance(expected_data, dict):
                    # Expected and actual are both dictionaries. Compare keys.
                    if key in expected_data.keys():
                        # Key is found in actual and expected.
                        next_expected = expected_data[key]
                        key_display = '{0}{1}{2}'.format(
                            ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                            key,
                            ETC_OUTPUT_RESET_COLOR,
                        )

                if key_display is None:
                    # Key present in actual but missing in expected.
                    key_display = '{0}{1}{2}'.format(
                        ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                        key,
                        ETC_OUTPUT_RESET_COLOR,
                    )
                    next_level_exists = False

                if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):
                    # Recursively call function to handle more complicated types.
                    self._debug_print(
                        '{0}"{1}":'.format(indentation, key_display),
                    )
                    self._recurse_show_debug_json_content_with_coloring(
                        value,
                        next_expected,
                        indentation_level=(indentation_level + 1),
                        level_exists=next_level_exists,
                    )

                else:
                    # Simple types.

                    # Handle if prior recurse parent indicates this section doesn't exist in expected.
                    if not next_level_exists:
                        value_display = '{0}{1}{2}'.format(
                            ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                            value,
                            ETC_OUTPUT_RESET_COLOR,
                        )

                    # Determine if values match.
                    elif type(value) != type(next_expected):
                        # Types don't match.
                        value_display = '{0}{1}{2}'.format(
                            ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                            value,
                            ETC_OUTPUT_RESET_COLOR,
                        )

                    elif value != next_expected:
                        # Values do not match.
                        value_display = '{0}{1}{2}'.format(
                            ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                            value,
                            ETC_OUTPUT_RESET_COLOR,
                        )
                    else:
                        # Everything matches up. All green.
                        value_display = '{0}{1}{2}'.format(
                            ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                            value,
                            ETC_OUTPUT_RESET_COLOR,
                        )

                    if isinstance(value, str):
                        # Add quotes for strings.
                        self._debug_print(
                            '{0}"{1}": "{2}",'.format(indentation, key_display, value_display),
                        )
                    else:
                        self._debug_print(
                            '{0}"{1}": {2},'.format(indentation, key_display, value_display),
                        )

            if indentation_level > 1:
                self._debug_print(
                    '{0}{1}{2}'.format(
                        prior_indentation,
                        container_text_color,
                        '},',
                    ),
                )
            else:
                self._debug_print(
                    '{0}{1}{2}'.format(
                        prior_indentation,
                        container_text_color,
                        '}',
                    ),
                )

        elif isinstance(actual_data, list) or isinstance(actual_data, tuple):
            # Array type handling.

            # Handle for container checks.
            # TODO: This maybe could be more efficiently organized.
            #   But at this point I just want it to work for now.
            container_text_color = ''
            if not level_exists:
                container_text_color = ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR
            elif type(actual_data) != type(expected_data):
                container_text_color = ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR
            elif len(actual_data) != len(expected_data):
                container_text_color = ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR

            self._debug_print(
                '{0}{1}{2}'.format(
                    prior_indentation,
                    container_text_color,
                    '[',
                ),
            )

            for index in range(len(actual_data)):
                value = actual_data[index]
                value_display = None
                next_expected = None
                next_level_exists = level_exists

                # Handle if prior recurse parent indicates this section doesn't exist in expected.
                if not level_exists:
                    value_display = '{0}{1}{2}'.format(
                        ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                        value,
                        ETC_OUTPUT_RESET_COLOR,
                    )

                # Determine if index is present.
                elif isinstance(expected_data, list) or isinstance(expected_data, tuple):
                    # Check if index also exists in expected.
                    if len(expected_data) > index:
                        # Index exists in actual and expected.
                        # Verify types match.

                        next_expected = expected_data[index]
                        if type(value) != type(next_expected):
                            # Types don't match.
                            value_display = '{0}{1}{2}'.format(
                                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                                value,
                                ETC_OUTPUT_RESET_COLOR,
                            )

                        else:
                            # Types do match.
                            # Check if equal number of items, if type dict or array.
                            if (
                                # Verify is equivalent to dict or array types.
                                isinstance(value, dict)
                                or isinstance(value, list)
                                or isinstance(value, tuple)
                            ) and (
                                # Verify lengths of objects match.
                                len(value)
                                != len(next_expected)
                            ):
                                # Is dict or array type and lengths do not match.
                                value_display = '{0}{1}{2}'.format(
                                    ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                                    value,
                                    ETC_OUTPUT_RESET_COLOR,
                                )
                            else:
                                # Verify values match.
                                if value != next_expected:
                                    # Expected and actual do not match.
                                    value_display = '{0}{1}{2}'.format(
                                        ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                                        value,
                                        ETC_OUTPUT_RESET_COLOR,
                                    )

                                else:
                                    # Everything matches up. All green.
                                    value_display = '{0}{1}{2}'.format(
                                        ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                                        value,
                                        ETC_OUTPUT_RESET_COLOR,
                                    )

                if value_display is None:
                    # Index present in actual but missing in expected.
                    value_display = '{0}{1}{2}'.format(
                        ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
                        value,
                        ETC_OUTPUT_RESET_COLOR,
                    )
                    next_level_exists = False

                if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):
                    # Recursively call function to handle more complicated types.
                    self._recurse_show_debug_json_content_with_coloring(
                        value,
                        next_expected,
                        indentation_level=(indentation_level + 1),
                        level_exists=next_level_exists,
                    )
                else:
                    # Simple types.
                    if isinstance(value, str):
                        # Add quotes for strings.
                        self._debug_print(
                            '{0}"{1}",'.format(indentation, value_display),
                        )
                    else:
                        self._debug_print(
                            '{0}{1},'.format(indentation, value_display),
                        )

            if indentation_level > 1:
                self._debug_print(
                    '{0}{1}{2}'.format(
                        prior_indentation,
                        container_text_color,
                        '],',
                    ),
                )
            else:
                self._debug_print(
                    '{0}{1}{2}'.format(
                        prior_indentation,
                        container_text_color,
                        ']',
                    ),
                )

        else:
            # All others.
            if isinstance(actual_data, str):
                # Add quotes for strings.
                self._debug_print(
                    '{0}"{1}"'.format(indentation, actual_data),
                )
            else:
                self._debug_print(
                    '{0}{1}'.format(indentation, actual_data),
                )

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
            fore=ETC_RESPONSE_DEBUG_HEADER_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # Print out data, if present.
        if response_headers is not None and len(response_headers) > 0:
            for key, value in response_headers.items():
                self._debug_print(
                    '    * "{0}": "{1}"'.format(key, value),
                    fore=ETC_RESPONSE_DEBUG_HEADER_COLOR,
                )
        else:
            self._debug_print('    No response headers found.')
        self._debug_print()

    def show_debug_context(self, response_context):
        """Prints debug response context data."""

        # Note: This uses the same logic as below `show_debug_form_data` function.
        #   Should probably change both to match, if either ever needs to be adjusted.

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            if hasattr(response_context, 'context'):
                response_context = response_context.context or {}
            else:
                response_context = {}

        if response_context is not None:
            # Attempt to access key object. If fails, attempt to generate dict of values.
            try:
                response_context.keys()

            except AttributeError:
                # Handling for:
                #     * django.template.context.RequestContext
                #     * django.template.context.Context
                # No guarantee this will work for other arbitrary types.
                # Handle as they come up.
                temp_dict = {}
                for context in response_context:
                    temp_dict = {**temp_dict, **context}
                response_context = temp_dict

            except Exception as err:
                # Error occurred.
                # Check if error is due to ContextDict/ContextList object being passed.
                # Unsure why this happens, but seems to occur in tests that access Django 4.2.7 admin views?
                # Needs further research. For now, this seems like enough to bypass it
                # and have no immediately noticeable side effects.
                from django.test.utils import ContextList

                if isinstance(response_context, ContextList):
                    # Skip output.
                    return

                else:
                    # Raise original error.
                    raise err

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.context'),
            fore=ETC_RESPONSE_DEBUG_CONTEXT_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # NOTE: Response context object is strange, in that it's basically a dictionary,
        # and it allows .keys() but not .values(). Thus, iterate on keys only and pull respective value.
        if response_context is not None and len(response_context.keys()) > 0:

            context_list = []

            # Fix for
            # RemovedInDjango50Warning: The "default.html" templates for forms and formsets will be removed.
            # Warning, prior to Django 5.0. Seems to trigger due to ETC accessing context in an "unexpected" way.
            with warnings.catch_warnings(record=True) as warn:

                # Iterate through context values.
                for key in response_context.keys():
                    context_value = str(response_context.get(key))

                    # Sanitize display if newlines are in value.
                    context_value = self.standardize_whitespace(context_value)

                    # Truncate display if very long.
                    if len(context_value) > 80:
                        context_value = '"{0}"..."{1}"'.format(context_value[:40], context_value[-40:])

                    # Append to context list.
                    context_list.append([key, context_value])

            # Sort context list for consistent output.
            sorted_list = sorted(context_list, key=lambda x: str(x[0]).lower())

            # Output sorted context list.
            for item in sorted_list:
                self._debug_print(
                    '    * {0}: {1}'.format(item[0], item[1]),
                    fore=ETC_RESPONSE_DEBUG_CONTEXT_COLOR,
                )

        else:
            self._debug_print('    No context data found.', fore=ETC_RESPONSE_DEBUG_CONTEXT_COLOR)
        self._debug_print()

    def show_debug_session_data(self, client):
        """Prints debug response session data."""

        # Handle for potential param types.
        if isinstance(client, HttpResponseBase):
            if hasattr(client, 'client'):
                client = client.client
            else:
                client = None

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'client.session'),
            fore=ETC_RESPONSE_DEBUG_SESSION_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        if client is not None and len(client.session.items()) > 0:
            for key, value in client.session.items():
                self._debug_print('    * {0}: {1}'.format(key, value), fore=ETC_RESPONSE_DEBUG_SESSION_COLOR)
        else:
            self._debug_print('    No session data found.', fore=ETC_RESPONSE_DEBUG_SESSION_COLOR)
        self._debug_print()

    def show_debug_messages(self, response_context):
        """Prints debug response message data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            if hasattr(response_context, 'context'):
                response_context = response_context.context or {}
            else:
                response_context = {}

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.context["messages"]'),
            fore=ETC_RESPONSE_DEBUG_MESSAGE_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # Print out data, if present.
        if response_context is not None and 'messages' in response_context:
            messages = response_context['messages']
            if len(messages) > 0:
                for message in messages:
                    self._debug_print('    * "{0}"'.format(message), fore=ETC_RESPONSE_DEBUG_MESSAGE_COLOR)
            else:
                self._debug_print('    No context messages found.', fore=ETC_RESPONSE_DEBUG_MESSAGE_COLOR)
        else:
            self._debug_print('    No context messages found.', fore=ETC_RESPONSE_DEBUG_MESSAGE_COLOR)
        self._debug_print()

    def show_debug_form_data(self, response_context, post_data):
        """Prints debug response form data."""

        # Note: This uses the same logic as above `show_debug_context` function.
        #   Should probably change both to match, if either ever needs to be adjusted.

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            if hasattr(response_context, 'context'):
                response_context = response_context.context or {}
            else:
                response_context = {}

        if response_context is not None:
            # Attempt to access key object. If fails, attempt to generate dict of values.
            try:
                response_context.keys()

            except AttributeError:
                # Handling for:
                #     * django.template.context.RequestContext
                #     * django.template.context.Context
                # No guarantee this will work for other arbitrary types.
                # Handle as they come up.
                temp_dict = {}
                for context in response_context:
                    temp_dict = {**temp_dict, **context}
                response_context = temp_dict

            except Exception as err:
                # Error occurred.
                # Check if error is due to ContextDict/ContextList object being passed.
                # Unsure why this happens, but seems to occur in tests that access Django 4.2.7 admin views?
                # Needs further research. For now, this seems like enough to bypass it
                # and have no immediately noticeable side effects.
                from django.test.utils import ContextList

                if isinstance(response_context, ContextList):
                    # Skip output.
                    return

                else:
                    # Raise original error.
                    raise err

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'Form Data'),
            fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        found_forms = {}
        found_formsets = {}
        found_formset_forms = []
        found_formset_management_forms = {}

        # NOTE: Response context object is strange, in that it's basically a dictionary,
        # and it allows .keys() but not .values(). Thus, iterate on keys only and pull respective value.
        if response_context is not None and len(response_context.keys()) > 0:

            for key in response_context.keys():
                # Determine any forms/formsets in context.

                # Grab context value.
                context_value = response_context.get(key)

                # Handle finding a "management form". This helps manage formsets.
                if isinstance(context_value, ManagementForm):
                    # Save to list of known management forms.
                    found_formset_management_forms[context_value.prefix] = context_value

                # Handle finding of forms in context.
                elif isinstance(context_value, BaseForm):

                    # Save to list of known forms.
                    found_forms[key] = context_value

                # Handle finding of formsets in context.
                elif isinstance(context_value, BaseFormSet):

                    # Save to list of known formsets.
                    found_formsets[key] = context_value

                    # Save to list of forms that are known part of the formset.
                    found_formset_forms.append(context_value.forms)

            # Do some extra pre-processing.
            # TODO: This seems to be due to Django always creating a "form" context value,
            #   even if the actual passed value is named different?
            #   Leads to duplicate instances of the form, with potential namespace clashing.
            #   Also seems to affect handling of formset "management form" logic. Bleh.
            #   Need to research why this is.
            has_duplicate = False
            if 'form' in found_forms.keys():
                for form_id, possible_duplicate in found_forms.items():
                    if form_id != 'form' and found_forms['form'] == possible_duplicate:
                        has_duplicate = True
                        break
            if has_duplicate:
                del found_forms['form']

            # Process found forms from context, if any.
            for form_name, form in found_forms.items():
                # Only debug output if form is not part of formset.
                if form not in found_formset_forms:

                    self._debug_print(
                        '\nForm (Context Id: "{0}")\n'.format(form_name),
                        fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                    )

                    self._debug_print_form_info(form, post_data)

            # Process found formsets from context, if any.
            for formset_name, formset in found_formsets.items():

                self._debug_print(
                    '\nFormset (Context Id: "{0}")\n'.format(formset_name),
                    fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                )

                # Handle management form for formset.
                found_manager_form = False
                for management_prefix, management_form in found_formset_management_forms.items():
                    if management_prefix == formset.prefix:
                        found_manager_form = True
                        self._debug_print_form_info(management_form, post_data, formset_identifier='management')

                # Handle if failed to find manager form.
                if not found_manager_form:
                    self._debug_print(
                        (
                            '    '
                            'Could not locate formset manager form. '
                            'Is the view having namespace collisions with the value "form"?'
                        ),
                        fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                    )

                # Handle associated sub-forms for formset.
                for index, form in enumerate(formset):
                    self._debug_print_form_info(form, post_data, formset_identifier=index)

        if not found_forms and not found_formsets:
            # No identifiable form or formset data present on page.
            self._debug_print('    No form data found.', fore=ETC_RESPONSE_DEBUG_FORM_COLOR)

        self._debug_print()

    def _debug_print_form_info(self, form, post_data, formset_identifier=None):
        """Inner logic to print main debug info for each processed form."""

        # Add extra indentation if displaying formset.
        if formset_identifier is not None:
            extra_indent = '    '

            # Handle name output for form.
            if formset_identifier == 'management':
                self._debug_print(
                    '    Management Form:\n',
                    fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                )
            else:
                self._debug_print()

                self._debug_print(
                    '    Sub-Form #{0}:\n'.format(formset_identifier + 1),
                    fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                )
        else:
            extra_indent = ''

        # Print general form data.
        self._debug_print(
            '{0}    Provided Form Fields:'.format(extra_indent),
            fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
        )
        fields_submitted = False
        for key in form.fields.keys():

            if formset_identifier == 'management':
                # Handling for management form fields.
                try:
                    updated_key = 'form-{0}'.format(key)
                    self._debug_print(
                        '            * {0}: {1}'.format(
                            updated_key,
                            form.data[updated_key],
                        ),
                        fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                    )
                except KeyError:
                    pass

            else:
                # Standard form-field handling.

                # Handle if is formset key.
                if formset_identifier is not None:
                    key = 'form-{0}-{1}'.format(formset_identifier, key)

                # Check if form field was provided as part of page POST.
                if key in post_data.keys():
                    fields_submitted = True

                # Get actual form field data, according to form.
                if key in form.data.keys():
                    self._debug_print(
                        '{0}        * {1}: {2}'.format(
                            extra_indent,
                            key,
                            form.data[key],
                        ),
                        fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                    )

        # Handle if could not output form field data.
        if fields_submitted and len(form.data) == 0:
            # Handle if can't read form data, despite being in POST.
            self._debug_print(
                (
                    '{0}        '
                    'Form field data found in POST, but not present in form. '
                    'Is your view configured correctly?'
                ).format(extra_indent),
                fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
            )
        if not fields_submitted and formset_identifier != 'management':
            # Handle if no data was submitted.
            self._debug_print(
                '{0}        No form field data submitted.'.format(extra_indent),
                fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
            )

        # Print form data errors if present.
        if not form.is_valid():
            self._debug_print()
            if len(form.errors) > 0 or len(form.non_field_errors()) > 0:
                self._debug_print(
                    '{0}    Form Invalid:'.format(extra_indent),
                    fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                )
                if len(form.non_field_errors()) > 0:
                    self._debug_print(
                        '{0}        Non-field Errors:'.format(extra_indent),
                        fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                    )
                    for error in form.non_field_errors():
                        self._debug_print(
                            '{0}            * "{1}"'.format(extra_indent, error),
                            fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                        )

                if len(form.errors) > 0:
                    self._debug_print(
                        '{0}        Field Errors:'.format(extra_indent),
                        fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                    )

                    for error_field, error_text in form.errors.items():

                        # Get actual error text value, minus surrounding html.
                        error_text = error_text.data[0].message

                        if formset_identifier is not None and formset_identifier != 'management':
                            error_field = 'form-{0}-{1}'.format(formset_identifier, error_field)

                        # Display field value.
                        self._debug_print(
                            '{0}            * {1}: "{2}"'.format(
                                extra_indent,
                                error_field,
                                error_text,
                            ),
                            fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                        )

        else:
            # No errors found in form.

            if formset_identifier is None:
                # Output for standard form.
                self._debug_print(
                    '    Form validated successfully.',
                    fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                )
            else:
                # Output for formset form.
                self._debug_print(
                    '        Formset sub-form validated successfully.',
                    fore=ETC_RESPONSE_DEBUG_FORM_COLOR,
                )

    def show_debug_user_info(self, user):
        """Prints debug user data."""

        # Imported here to prevent potential "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser

        # Handle for potential param types.
        if isinstance(user, HttpResponseBase):
            if hasattr(user, 'user'):
                user = user.user
            else:
                user = None

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'User Info'),
            fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
            style=ETC_OUTPUT_EMPHASIS_COLOR,
        )

        # Only proceed if we got a proper user model.
        if isinstance(user, get_user_model()):

            # General user information.
            self._debug_print('    * pk: "{0}"'.format(user.pk), fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR)
            self._debug_print(
                '    * Username: "{0}"'.format(user.username),
                fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
            )
            self._debug_print(
                '    * First: "{0}"'.format(user.first_name),
                fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
            )
            self._debug_print('    * Last: "{0}"'.format(user.last_name), fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR)
            self._debug_print('    * Email: "{0}"'.format(user.email), fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR)

            # User auth data.
            self._debug_print(
                '    * is_authenticated: {0}'.format(user.is_authenticated),
                fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
            )

            # User groups.
            self._debug_print(
                '    * User Groups: {0}'.format(user.groups.all()), fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR
            )

            # User permissions.
            self._debug_print(
                '    * User Permissions: {0}'.format(user.user_permissions.all()),
                fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
            )

        elif isinstance(user, AnonymousUser):
            self._debug_print('    Anonymous user. No user is logged in.', fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR)

        elif user is None:
            self._debug_print('    User not defined. Was None type.', fore=ETC_RESPONSE_DEBUG_USER_INFO_COLOR)

        else:
            self._debug_print(
                '    * Invalid user "{0}" of type "{1}". Expected "{2}".'.format(
                    user,
                    type(user),
                    type(get_user_model()),
                ),
                fore=ETC_OUTPUT_ERROR_COLOR,
            )
        self._debug_print()
        self._debug_print()

    # endregion Debug Output Functions.

    def standardize_url(
        self,
        url,
        url_args=None,
        url_kwargs=None,
        url_query_params=None,
        append_root=True,
        display_warning=False,
    ):
        """Attempts to standardize URL value, such as in event url is in format for reverse() function.

        :param url: Url value to attempt to parse and standardize.
        :param url_args: Additional "args" to pass for reverse() function, if applicable.
        :param url_kwargs: Additional "kwargs" to pass for reverse() function, if applicable.
        :param url_query_params: The set of <key: value> pairs to append to end of GET url string.
        :param append_root: Bool indicating if "site root" should be included in url (if not already).
        :param display_warning: Indicates if warning for APPEND_SLASH should be shown or not.
        :return: Attempt at fully-formatted url.
        """

        # Handle mutable data defaults.
        url_args = url_args or ()
        url_kwargs = url_kwargs or {}
        url_query_params = url_query_params or {}

        # Preprocess all potential url values.
        url = str(url).strip()

        # Attempt to get reverse of provided url.
        try:
            url = reverse(url, args=url_args, kwargs=url_kwargs)

            # PART 1 for providing warning based on APPEND_SLASH setting.
            # See https://stackoverflow.com/a/42213107 for discussion on why this setting exists
            # as well as how Django generally handles url composition.
            if display_warning:

                if settings.APPEND_SLASH:
                    # As per project Django settings, url should have a trailing slash.
                    if len(url) > 0 and url[-1] != '/':
                        warn_msg = (
                            'Django setting APPEND_SLASH is set to True, '
                            'but url reverse did not resolve with trailing slash. '
                            'This may cause UnitTests with ETC to fail. '
                            'Consider appending a url slash. '
                            'Url was: {0}'
                        ).format(url)
                        # Create console warning message.
                        warnings.warn(warn_msg)
                        # Create logging warning message.
                        logging.warning(warn_msg)

                else:
                    # As per project Django settings, url should NOT have a trailing slash.
                    if len(url) > 0 and url[-1] == '/':
                        warn_msg = (
                            'Django setting APPEND_SLASH is set to False, '
                            'but url reverse resolved with a trailing slash. '
                            'This may cause UnitTests with ETC to fail. '
                            'Consider removing the trailing url slash. '
                            'Url was: {0}'
                        ).format(url)
                        # Create console warning message.
                        warnings.warn(warn_msg)
                        # Create logging warning message.
                        logging.warning(warn_msg)

        except NoReverseMatch:
            # Could not find as reverse. Assume is literal url.

            # PART 2 for providing warning based on APPEND_SLASH setting.
            # See https://stackoverflow.com/a/42213107 for discussion on why this setting exists
            # as well as how Django generally handles url composition.
            if display_warning:

                # First make sure it wasn't a reverse string that failed to resolve properly.
                # We do this by removing potentially prepended `http:` / `https:` values, then
                # checking for the : character. As it's very unlikely to have such in a standard django url.
                # If content exists both before and after the : character, then it was probably a
                # reverse string that failed. Otherwise it's likely a full url that was provided.
                is_probably_reverse = False
                url_check = url.lstrip('http:').lstrip('https:')
                url_check = url_check.split(':')

                if len(url_check) == 2 and len(url_check[0]) > 0 and len(url_check[1]) > 0:
                    is_probably_reverse = True

                if not is_probably_reverse:
                    # Is most likely not a reverse string. Display applicable warnings.

                    # Get the url portion that does NOT include potential url get params.
                    url_check = url.split('?')
                    if len(url_check) > 0:
                        url_check = url_check[0]

                    if settings.APPEND_SLASH:
                        # As per project Django settings, url should have a trailing slash.
                        if len(url_check) > 0 and url_check[-1] != '/':
                            warn_msg = (
                                'Django setting APPEND_SLASH is set to True, '
                                'but provided url does not contain a trailing slash. '
                                'This may cause UnitTests with ETC to fail. '
                                'Consider appending a url slash. '
                                'Url was: {0}'
                            ).format(url)
                            # Create console warning message.
                            warnings.warn(warn_msg)
                            # Create logging warning message.
                            logging.warning(warn_msg)

                    else:
                        # As per project Django settings, url should NOT have a trailing slash.
                        if len(url_check) > 0 and url_check[-1] == '/':
                            warn_msg = (
                                'Django setting APPEND_SLASH is set to False, '
                                'but provided url contained a trailing slash. '
                                'This may cause UnitTests with ETC to fail. '
                                'Consider removing the trailing url slash. '
                                'Url was: {0}'
                            ).format(url)
                            # Create console warning message.
                            warnings.warn(warn_msg)
                            # Create logging warning message.
                            logging.warning(warn_msg)

            # Trim any known extra values on literal url str.
            # Remove http prefix, if present.
            if url.startswith('http'):
                url = url.lstrip('https:')
            # Remove any extra slashes on either side.
            url = str(url).strip().lstrip('/').rstrip('/')
            # Remove any custom url prefix domain.
            site_root_check = str(self.site_root_url).strip()
            if site_root_check.startswith('http'):
                site_root_check = site_root_check.lstrip('https:')
            site_root_check = site_root_check.lstrip('/').rstrip('/')
            if url.startswith(site_root_check):
                url = url[len(site_root_check) :]
            # Remove standard 127 url prefix domain.
            elif url.startswith('127.0.0.1'):
                url = url.lstrip('127.0.0.1')
            # Remove standard localhost url prefix domain.
            elif url.startswith('localhost'):
                url = url.lstrip('localhost')

            # Check if empty url.
            if len(url) == 0:
                # Empty url. Populate to single slash.
                url = '/'
            else:
                # Non-empty url.

                # Handle for prepend slash.
                # Only apply if not already present.
                if not url.startswith('/'):
                    url = '/{0}'.format(url)

                # Handle if GET args are included within url.
                split_url = url.split('?')
                if len(split_url) == 1:
                    # No GET args found.
                    url = split_url[0]
                else:
                    # Url GET args found. Temporarily split to prevent errors.
                    url = split_url.pop(0)

                    # Convert query params to expected dictionary format for passing as proper kwargs.
                    url_args = '{0}'.format('?'.join(x for x in split_url))
                    temp_dict = parse_qs(url_args)
                    for key, value in temp_dict.items():
                        url_query_params[key] = value[0]

                # Handle for append slash.
                # Only apply if not already present and settings.APPEND_SLASH is true.
                if settings.APPEND_SLASH and not url.endswith('/'):
                    url = '{0}/'.format(url)

        if url_query_params:
            url = self.generate_get_url(url, **url_query_params)

        # Finally, prepend site root to url, if applicable.
        if append_root:
            url = '{0}{1}'.format(self.site_root_url, url)

        # Return final full url.
        return url

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

    # region Html Search Functions

    def find_elements_by_tag(self, content, element):
        """Finds all HTML elements that match the provided element tag.

        :param content: Content to search through.
        :param element: Html element to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Sanitize provided element value. We don't care how the user was provided the syntax.
        element = self.get_minimized_response_content(element)
        element = element.lstrip('<').rstrip('>').strip('/').strip()

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(name=element)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Validate parsed value.
        if not len(element_list) > 0:
            self.fail(f'Unable to find element "<{element}>" in content. Provided content was:\n{content}')

        # Return found list.
        return element_list

    def find_element_by_tag(self, content, element):
        """Finds first HTML element that matches the provided element tag.

        :param content: Content to search through.
        :param element: Html element to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Sanitize provided element value. We don't care how the user was provided the syntax.
        element = self.get_minimized_response_content(element)
        element = element.lstrip('<').rstrip('>').strip('/').strip()

        # Call parent function logic.
        element_list = self.find_elements_by_tag(content, element)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "<{element}>" element. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_id(self, content, element_id):
        """Finds all HTML elements that match the provided id.

        :param content: Content to search through.
        :param element_id: Element id to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(id=element_id)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find id "{element_id}" in content. Provided content was:\n{content}')

        # Provide warning if two or more values were found.
        if len(element_list) > 1:
            logger.warning(
                'It\'s considered bad practice to have multiple matching id tags in one html response. '
                'Consider refactoring elements to keep each id unique.\n'
                'Found {0} total elements with id of "{1}".'.format(len(element_list), element_id)
            )

        # Return found values.
        return element_list

    def find_element_by_id(self, content, element_id):
        """Finds first HTML element that matches the provided id.

        :param content: Content to search through.
        :param element_id: Element id to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_id(content, element_id)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{element_id}" id. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_class(self, content, css_class):
        """Finds all HTML elements that match the provided css class.

        :param content: Content to search through.
        :param css_class: Css class to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(class_=css_class)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find class "{css_class}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_class(self, content, css_class):
        """Finds first HTML element that matches the provided css class.

        :param content: Content to search through.
        :param css_class: Css class to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_class(content, css_class)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{css_class}" class. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_css_selector(self, content, css_selector):
        """Finds all HTML elements that match the provided css selector.

        :param content: Content to search through.
        :param css_selector: Css selector to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.select(css_selector)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find css selector "{css_selector}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_css_selector(self, content, css_selector):
        """Finds first HTML element that matches the provided css selector.

        :param content: Content to search through.
        :param css_selector: Css selector to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_css_selector(content, css_selector)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{css_selector}" css selector. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_data_attribute(self, content, data_attribute, data_value):
        """Finds all HTML elements that match the provided data attribute and data value.

        :param content: Content to search through.
        :param data_attribute: The key of the data attribute to search for.
        :param data_value: The value of the data attribute to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        attr_dict = {data_attribute: data_value}
        elements = soup.find_all(attrs=attr_dict)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(
                f'Unable to find data attribute "{data_attribute}" with value "{data_value}" in content. Provided '
                f'content was:\n{content}'
            )

        # Return found values.
        return element_list

    def find_element_by_data_attribute(self, content, data_attribute, data_value):
        """Finds first HTML element that matches the provided data attribute and data value.

        :param content: Content to search through.
        :param data_attribute: The key of the data attribute to search for.
        :param data_value: The value of the data attribute to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_data_attribute(content, data_attribute, data_value)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{data_attribute}" data attribute with value "{data_value}". '
                f'Expected only one instance. Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_name(self, content, element_name):
        """Finds all HTML elements that match the provided name attribute.

        :param content: Content to search through.
        :param element_name: Element name to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        attr_dict = {'name': element_name}
        elements = soup.find_all(attrs=attr_dict)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find name "{element_name}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_name(self, content, element_name):
        """Finds first HTML element that matches the provided name attribute.

        :param content: Content to search through.
        :param element_name: Element name to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_name(content, element_name)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{element_name}" name. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_link_text(self, content, link_text):
        """Finds all HTML elements that match the provided link text.

        :param content: Content to search through.
        :param link_text: Link text to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(href=link_text)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find link text "{link_text}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_link_text(self, content, link_text):
        """Finds first HTML element that matches the provided link text.

        :param content: Content to search through.
        :param link_text: Link text to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_link_text(content, link_text)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{link_text}" link text. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_text(self, content, text, element_type=None):
        """Finds all HTML elements that contain the provided inner text.

        :param content: Content to search through.
        :param text: Element text to search for.
        :param element_type: Optionally filter by type of element as well (h1, p, li, etc).
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        if not element_type:
            elements = soup.find_all(string=re.compile('{0}'.format(text)))
        else:
            elements = soup.find_all(str(element_type), string=re.compile('{0}'.format(text)))
        if element_type:
            element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]
        else:
            element_list = [self.get_minimized_response_content(element.parent.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            type_substring = ''
            if element_type:
                type_substring = ' under element type of "{0}"'.format(element_type)
            self.fail(
                f'Unable to find element text "{text}" in content{type_substring}. Provided content was:\n{content}'
            )

        # Return found values.
        return element_list

    def find_element_by_text(self, content, text, element_type=None):
        """Finds first HTML element that matches the provided inner text.

        :param content: Content to search through.
        :param text: Element text to search for.
        :param element_type: Optionally filter by type of element as well (h1, p, li, etc).
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_text(content, text, element_type=element_type)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{text}" element text. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    # endregion Html Search Functions


# Define acceptable imports on file.
__all__ = [
    'ResponseTestCaseMixin',
]
