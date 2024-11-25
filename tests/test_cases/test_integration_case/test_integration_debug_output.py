"""
Tests for test_cases/integration_test_case.py "helper function" utilities and logic.
"""

# System Imports.
import io
import unittest.mock
from unittest.mock import patch

# Third-Party Imports.
from django import VERSION as django_version
from django.conf import settings
from django.test import override_settings

# Internal Imports.
from django_expanded_test_cases import IntegrationTestCase
from django_expanded_test_cases.constants import (
    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_EMPHASIS_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_RESET_COLOR,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_RESPONSE_DEBUG_CONTEXT_COLOR,
    ETC_RESPONSE_DEBUG_FORM_COLOR,
    ETC_RESPONSE_DEBUG_HEADER_COLOR,
    ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
    ETC_RESPONSE_DEBUG_MESSAGE_COLOR,
    ETC_RESPONSE_DEBUG_SESSION_COLOR,
    ETC_RESPONSE_DEBUG_URL_COLOR,
)


# Module Variables.
SKIP_BEFORE_VALUE__FULL = """
<head>
 <meta charset="utf-8">
 <title>View with Three Messages | Test Views</title>
</head>
<body>
"""
SKIP_BEFORE_VALUE__MINIMAL = """
<body>
"""

SKIP_AFTER_VALUE__FULL = """
 <h1>View with Three Messages Header</h1>
 <p>Pretend useful stuff is displayed here, for three-message render() view.</p>
</body>
"""
SKIP_AFTER_VALUE__MINIMAL = """
<h1>
"""


class IntegrationDebugOutputTestCase:

    def strip_text_colors(self, text):
        """Strip out all potential color values, for easier testing."""

        # Make sure value is a populated string.
        text = str(text)
        if len(text) < 1:
            return text

        # Remove all possible color values in string.
        # NOTE: Would probably be more efficient with a re.sub() regex replacement, but gives a
        #   tokenizer parse error. Not worth fixing for now, so using a lazy str.replace() instead.
        text = text.replace(ETC_OUTPUT_ACTUALS_ERROR_COLOR, '')
        text = text.replace(ETC_OUTPUT_ACTUALS_MATCH_COLOR, '')
        text = text.replace(ETC_OUTPUT_EMPHASIS_COLOR, '')
        text = text.replace(ETC_OUTPUT_ERROR_COLOR, '')
        text = text.replace(ETC_OUTPUT_EXPECTED_ERROR_COLOR, '')
        text = text.replace(ETC_OUTPUT_EXPECTED_MATCH_COLOR, '')
        text = text.replace(ETC_OUTPUT_RESET_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_CONTENT_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_CONTEXT_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_FORM_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_HEADER_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_USER_INFO_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_MESSAGE_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_SESSION_COLOR, '')
        text = text.replace(ETC_RESPONSE_DEBUG_URL_COLOR, '')

        # Return updated value.
        return text


class TestIntegrationBaseDebugOutput(IntegrationTestCase, IntegrationDebugOutputTestCase):
    """Tests for IntegrationTestCase class "debug output" logic."""

    # region Different Pages

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_pages__login_page(self, mock_stdout):
        """Verifying output of assertResponse, with different pages."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:login',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '-------------------------------------------\n'
                'Attempting to access url "127.0.0.1/login/"\n'
                '-------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Login Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Login Page Header</h1>\n'
                ' <p>Pretend this is a login page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "192"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/login/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Login Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/login/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/login/\'>\n'
                    '    * text: Pretend this is a login page.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_pages__home_page(self, mock_stdout):
        """Verifying output of assertResponse, with different pages."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_pages__message_page(self, mock_stdout):
        """Verifying output of assertResponse, with different pages."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>View with Three Messages | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>View with Three Messages Header</h1>\n'
                ' <p>Pretend useful stuff is displayed here, for three-message render() view.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    # endregion Different Pages

    # region Different Assertions

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_assertions__url(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        These tests should effectively run the same as the
        test__general_debug_output__different_pages__home_page test.
        The point of these tests is to verify output stays the same.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                expected_url='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_assertions__header(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        These tests should effectively run the same as the
        test__general_debug_output__different_pages__home_page test.
        The point of these tests is to verify output stays the same.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                expected_header='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_assertions__messages(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        These tests should effectively run the same as the
        test__general_debug_output__different_pages__home_page test.
        The point of these tests is to verify output stays the same.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                expected_messages='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_assertions__content(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        These tests should effectively run the same as the
        test__general_debug_output__different_pages__home_page test.
        The point of these tests is to verify output stays the same.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                expected_content='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__json_response(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON output for assertJsonResponse.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-index',
                expected_url='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/json/index/"\n'
                '------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '{\n'
                '  "success": "This is a test Json response.",\n'
                '  "request_headers":\n'
                '  {\n'
                '    "Cookie": "",\n'
                '    "Content-Type": "application/json",\n'
                '    "Accept": "application/json",\n'
                '  }\n'
                '}\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "application/json"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "145"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.

            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    No context data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip Context section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    # endregion Different Assertions

    # region Different Users

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_users__super_user(self, mock_stdout):
        """Verifying output of assertResponse, with different user types."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                user=self.test_superuser,
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: test_superuser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: PermWrapper(<SimpleLazyObject: <User: test_superuser>>)\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: test_superuser\n'
                    '\n'
                    '\n'
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed. Strip context section.
                actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    * _auth_user_id: 1\n'
                '    * _auth_user_backend: django.contrib.auth.backends.ModelBackend\n'
                '    * _auth_user_hash: '
            )
            expected_text_2 = (
                # Comment to prevent "Black" formatting.
                '\n'
                '\n'
                '\n'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    * pk: "1"\n'
                '    * Username: "test_superuser"\n'
                '    * First: "SuperUserFirst"\n'
                '    * Last: "SuperUserLast"\n'
                '    * Email: "super_user@example.com"\n'
                '    * is_authenticated: True\n'
                '    * User Groups: <QuerySet []>\n'
                '    * User Permissions: <QuerySet []>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_users__admin_user(self, mock_stdout):
        """Verifying output of assertResponse, with different user types."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                user=self.test_admin,
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: test_admin\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: PermWrapper(<SimpleLazyObject: <User: test_admin>>)\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: test_admin\n'
                    '\n'
                    '\n'
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed. Strip context section.
                actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    * _auth_user_id: 2\n'
                '    * _auth_user_backend: django.contrib.auth.backends.ModelBackend\n'
                '    * _auth_user_hash: '
            )
            expected_text_2 = (
                # Comment to prevent "Black" formatting.
                '\n'
                '\n'
                '\n'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    * pk: "2"\n'
                '    * Username: "test_admin"\n'
                '    * First: "AdminUserFirst"\n'
                '    * Last: "AdminUserLast"\n'
                '    * Email: "admin_user@example.com"\n'
                '    * is_authenticated: True\n'
                '    * User Groups: <QuerySet []>\n'
                '    * User Permissions: <QuerySet []>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__different_users__standard_user(self, mock_stdout):
        """Verifying output of assertResponse, with different user types."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:template-response-home',
                user=self.test_user,
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/template-response/home/"\n'
                '------------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Home Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Home Page Header</h1>\n'
                ' <p>Pretend this is the project landing page.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "202"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: test_user\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: Home Page\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                    '    * None: None\n'
                    '    * perms: PermWrapper(<SimpleLazyObject: <User: test_user>>)\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * text: Pretend this is the project landing page.\n'
                    '    * True: True\n'
                    '    * user: test_user\n'
                    '\n'
                    '\n'
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed. Strip context section.
                actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    * _auth_user_id: 4\n'
                '    * _auth_user_backend: django.contrib.auth.backends.ModelBackend\n'
                '    * _auth_user_hash: '
            )
            expected_text_2 = (
                # Comment to prevent "Black" formatting.
                '\n'
                '\n'
                '\n'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    * pk: "4"\n'
                '    * Username: "test_user"\n'
                '    * First: "UserFirst"\n'
                '    * Last: "UserLast"\n'
                '    * Email: "user@example.com"\n'
                '    * is_authenticated: True\n'
                '    * User Groups: <QuerySet []>\n'
                '    * User Permissions: <QuerySet []>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    # endregion Different Users

    # region Form Handling

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_form__success(self, mock_stdout):
        """Verifying output of form debug, in case where for validates successfully."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-form',
            data={'required_charfield': 'Testing', 'required_intfield': 5},
            expected_title='Basic Form Page | Test Views',
            expected_messages=['Form submitted successfully.'],
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-form/"\n'
                '------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Form Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Form submitted successfully.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>Basic Form Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="required_charfield" value="Testing" maxlength="100" required id="id_required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="optional_charfield" maxlength="100" id="id_optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="required_intfield" value="5" required id="id_required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="optional_intfield" id="id_optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "1277"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="required_charfi"..."00" required id="id_required_charfield">"\n'
                    '    * fields: "[(<django.forms.boundfield.BoundField ob"..."undField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>, [])]"\n'
                    '    * form: "<div> <label for="id_required_charfield""..."field" id="id_optional_intfield"> </div>"\n'
                    '    * header: Basic Form Page\n'
                    '    * hidden_fields: []\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-form/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-form/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'required_charfield\', \'is_hidde"..."orms/widgets/text.html\', \'type\': \'text\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Form submitted successfully."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    Provided Form Fields:\n'
                '        * required_charfield: Testing\n'
                '        * required_intfield: 5\n'
                '\n'
                '    Form validated successfully.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_form__success__with_reset(self, mock_stdout):
        """Verifying output of form debug, in case where for validates successfully."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-form',
            data={
                'required_charfield': 'Testing',
                'required_intfield': 5,
                "reset_form_on_success": True,
            },
            expected_title='Basic Form Page | Test Views',
            expected_messages=['Form submitted successfully.'],
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-form/"\n'
                '------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Form Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Form submitted successfully.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>Basic Form Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="required_charfield" maxlength="100" required id="id_required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="optional_charfield" maxlength="100" id="id_optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="required_intfield" required id="id_required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="optional_intfield" id="id_optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "1251"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="required_charfi"..."00" required id="id_required_charfield">"\n'
                    '    * fields: "[(<django.forms.boundfield.BoundField ob"..."undField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>, [])]"\n'
                    '    * form: "<div> <label for="id_required_charfield""..."field" id="id_optional_intfield"> </div>"\n'
                    '    * header: Basic Form Page\n'
                    '    * hidden_fields: []\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-form/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-form/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'required_charfield\', \'is_hidde"..."orms/widgets/text.html\', \'type\': \'text\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Form submitted successfully."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    Provided Form Fields:\n'
                '        Form field data found in POST, but not present in form. '
                'Is your view configured correctly?'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_form__failure__missing_fields(self, mock_stdout):
        """Verifying output of form debug, in case where fields are missing."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-form',
            data={'optional_charfield': 'Testing', 'optional_intfield': 5},
            expected_title='Basic Form Page | Test Views',
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-form/"\n'
                '------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Form Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Basic Form Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <hr>\n'
                ' <ul class="errorlist"><li>This field is required.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="required_charfield" maxlength="100" required aria-invalid="true" id="id_required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="optional_charfield" value="Testing" maxlength="100" id="id_optional_charfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>This field is required.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="required_intfield" required aria-invalid="true" id="id_required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="optional_intfield" value="5" id="id_optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "1329"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="required_charfi"..."valid="true" id="id_required_charfield">"\n'
                    '    * fields: "[(<django.forms.boundfield.BoundField ob"..."undField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>, [])]"\n'
                    '    * form: "<div> <label for="id_required_charfield""..."ue="5" id="id_optional_intfield"> </div>"\n'
                    '    * header: Basic Form Page\n'
                    '    * hidden_fields: []\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-form/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-form/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'required_charfield\', \'is_hidde"..."orms/widgets/text.html\', \'type\': \'text\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    Provided Form Fields:\n'
                '        * optional_charfield: Testing\n'
                '        * optional_intfield: 5\n'
                '\n'
                '    Form Invalid:\n'
                '        Field Errors:\n'
                '            * required_charfield: "This field is required."\n'
                '            * required_intfield: "This field is required."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_form__failure__raise_general_form_error(self, mock_stdout):
        """Verifying output of form debug, in case where general form error is raised."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-form',
            data={
                'required_charfield': 'Testing',
                'required_intfield': 90,
                'optional_intfield': 21,
            },
            expected_title='Basic Form Page | Test Views',
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-form/"\n'
                '------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Form Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Basic Form Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <hr>\n'
                ' <ul class="errorlist nonfield"><li>Invalid values. IntFields cannot add up to above 100.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="required_charfield" value="Testing" maxlength="100" required id="id_required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="optional_charfield" maxlength="100" id="id_optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="required_intfield" value="90" required id="id_required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="optional_intfield" value="21" id="id_optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "1286"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: "<ul class="errorlist nonfield"><li>Inval"..."ds cannot add up to above 100.</li></ul>"\n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="required_charfi"..."00" required id="id_required_charfield">"\n'
                    '    * fields: "[(<django.forms.boundfield.BoundField ob"..."undField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>, [])]"\n'
                    '    * form: "<ul class="errorlist nonfield"><li>Inval"..."e="21" id="id_optional_intfield"> </div>"\n'
                    '    * header: Basic Form Page\n'
                    '    * hidden_fields: []\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-form/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-form/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'required_charfield\', \'is_hidde"..."orms/widgets/text.html\', \'type\': \'text\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    Provided Form Fields:\n'
                '        * required_charfield: Testing\n'
                '        * required_intfield: 90\n'
                '        * optional_intfield: 21\n'
                '\n'
                '    Form Invalid:\n'
                '        Non-field Errors:\n'
                '            * "Invalid values. IntFields cannot add up to above 100."\n'
                '        Field Errors:\n'
                '            * __all__: "Invalid values. IntFields cannot add up to above 100."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_form__failure__raise_field_error(self, mock_stdout):
        """Verifying output of form debug, in case where fields are missing."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-form',
            data={
                'required_charfield': 'Testing',
                'required_intfield': -1,
                'optional_intfield': -5,
            },
            expected_title='Basic Form Page | Test Views',
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-form/"\n'
                '------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Form Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Basic Form Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="required_charfield" value="Testing" maxlength="100" required id="id_required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="optional_charfield" maxlength="100" id="id_optional_charfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>Cannot set "IntField - Required" to a negative value.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="required_intfield" value="-1" required aria-invalid="true" id="id_required_intfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>Cannot set "IntField - Optional" to a negative value.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="optional_intfield" value="-5" aria-invalid="true" id="id_optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "1418"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="required_charfi"..."00" required id="id_required_charfield">"\n'
                    '    * fields: "[(<django.forms.boundfield.BoundField ob"..."eld - Optional" to a negative value.\'])]"'
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of fields text.
                # actual_text = actual_text[14:]

                expected_text_3 = (
                    '    * form: "<div> <label for="id_required_charfield""...""true" id="id_optional_intfield"> </div>"\n'
                    '    * header: Basic Form Page\n'
                    '    * hidden_fields: []\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-form/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[52:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-form/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'required_charfield\', \'is_hidde"..."orms/widgets/text.html\', \'type\': \'text\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    Provided Form Fields:\n'
                '        * required_charfield: Testing\n'
                '        * required_intfield: -1\n'
                '        * optional_intfield: -5\n'
                '\n'
                '    Form Invalid:\n'
                '        Field Errors:\n'
                '            * required_intfield: "Cannot set "IntField - Required" to a negative value."\n'
                '            * optional_intfield: "Cannot set "IntField - Optional" to a negative value."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_formset__success(self, mock_stdout):
        """Verifying output of form debug, in case where form validates successfully."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-formset',
            data={
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "2",
                'form-0-required_charfield': 'Testing 1',
                'form-0-required_intfield': 10,
                'form-1-required_charfield': 'Testing 2',
                'form-1-required_intfield': 20,
            },
            expected_title='Basic Formset Page | Test Views',
            expected_messages=['Formset submitted successfully.'],
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '---------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-formset/"\n'
                '---------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Formset Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Formset submitted successfully.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>Basic Formset Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <input type="hidden" name="form-TOTAL_FORMS" value="2" id="id_form-TOTAL_FORMS"><input type="hidden" name="form-INITIAL_FORMS" value="2" id="id_form-INITIAL_FORMS"><input type="hidden" name="form-MIN_NUM_FORMS" id="id_form-MIN_NUM_FORMS"><input type="hidden" name="form-MAX_NUM_FORMS" id="id_form-MAX_NUM_FORMS">\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-0-required_charfield" value="Testing 1" maxlength="100" id="id_form-0-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-0-optional_charfield" maxlength="100" id="id_form-0-optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-0-required_intfield" value="10" id="id_form-0-required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-0-optional_intfield" id="id_form-0-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-1-required_charfield" value="Testing 2" maxlength="100" id="id_form-1-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-1-optional_charfield" maxlength="100" id="id_form-1-optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-1-required_intfield" value="20" id="id_form-1-required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-1-optional_intfield" id="id_form-1-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "2559"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `hidden_fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_form-0-required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="form-0-required"...""100" id="id_form-0-required_charfield">"\n'
                    '    * fields: []\n'
                    '    * form: "<input type="hidden" name="form-TOTAL_FO"..."X_NUM_FORMS" id="id_form-MAX_NUM_FORMS">"\n'
                    '    * formset: "<input type="hidden" name="form-TOTAL_FO"..."id="id_form-1-optional_intfield"> </div>"\n'
                    '    * header: Basic Formset Page\n'
                    '    * hidden_fields: "[<django.forms.boundfield.BoundField obj"..."ld.BoundField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of hidden_fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>]"\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-formset/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-formset/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'form-TOTAL_FORMS\', \'is_hidden\'"..."/widgets/hidden.html\', \'type\': \'hidden\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Formset submitted successfully."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '\n'
                'Formset (Context Id: "formset")\n'
                '\n'
                '    Management Form:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-TOTAL_FORMS: 2\n'
                '            * form-INITIAL_FORMS: 2\n'
                '        Formset sub-form validated successfully.\n'
                '\n'
                '    Sub-Form #1:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-0-required_charfield: Testing 1\n'
                '            * form-0-required_intfield: 10\n'
                '        Formset sub-form validated successfully.\n'
                '\n'
                '    Sub-Form #2:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-1-required_charfield: Testing 2\n'
                '            * form-1-required_intfield: 20\n'
                '        Formset sub-form validated successfully.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_formset__failure__missing_fields(self, mock_stdout):
        """Verifying output of form debug, in case where form validates successfully."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-formset',
            data={
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "2",
                'form-0-required_intfield': 10,
                'form-1-required_charfield': 'Testing 2',
            },
            expected_title='Basic Formset Page | Test Views',
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '---------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-formset/"\n'
                '---------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Formset Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Basic Formset Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <input type="hidden" name="form-TOTAL_FORMS" value="2" id="id_form-TOTAL_FORMS"><input type="hidden" name="form-INITIAL_FORMS" value="2" id="id_form-INITIAL_FORMS"><input type="hidden" name="form-MIN_NUM_FORMS" id="id_form-MIN_NUM_FORMS"><input type="hidden" name="form-MAX_NUM_FORMS" id="id_form-MAX_NUM_FORMS">\n'
                ' <hr>\n'
                ' <ul class="errorlist"><li>This field is required.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-0-required_charfield" maxlength="100" aria-invalid="true" id="id_form-0-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-0-optional_charfield" maxlength="100" id="id_form-0-optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-0-required_intfield" value="10" id="id_form-0-required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-0-optional_intfield" id="id_form-0-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-1-required_charfield" value="Testing 2" maxlength="100" id="id_form-1-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-1-optional_charfield" maxlength="100" id="id_form-1-optional_charfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>This field is required.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-1-required_intfield" aria-invalid="true" id="id_form-1-required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-1-optional_intfield" id="id_form-1-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "2579"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `hidden_fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_form-0-required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="form-0-required"..."true" id="id_form-0-required_charfield">"\n'
                    '    * fields: []\n'
                    '    * form: "<input type="hidden" name="form-TOTAL_FO"..."X_NUM_FORMS" id="id_form-MAX_NUM_FORMS">"\n'
                    '    * formset: "<input type="hidden" name="form-TOTAL_FO"..."id="id_form-1-optional_intfield"> </div>"\n'
                    '    * header: Basic Formset Page\n'
                    '    * hidden_fields: "[<django.forms.boundfield.BoundField obj"..."ld.BoundField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of hidden_fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>]"\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-formset/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-formset/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'form-TOTAL_FORMS\', \'is_hidden\'"..."/widgets/hidden.html\', \'type\': \'hidden\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '\n'
                'Formset (Context Id: "formset")\n'
                '\n'
                '    Management Form:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-TOTAL_FORMS: 2\n'
                '            * form-INITIAL_FORMS: 2\n'
                '        Formset sub-form validated successfully.\n'
                '\n'
                '    Sub-Form #1:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-0-required_intfield: 10\n'
                '\n'
                '        Form Invalid:\n'
                '            Field Errors:\n'
                '                * form-0-required_charfield: "This field is required."\n'
                '\n'
                '    Sub-Form #2:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-1-required_charfield: Testing 2\n'
                '\n'
                '        Form Invalid:\n'
                '            Field Errors:\n'
                '                * form-1-required_intfield: "This field is required."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_formset__failure__raise_general_form_error(self, mock_stdout):
        """Verifying output of form debug, in case where form validates successfully."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-formset',
            data={
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "2",
                'form-0-required_charfield': 'Testing 1',
                'form-0-required_intfield': 55,
                'form-0-optional_intfield': 65,
                'form-1-required_charfield': 'Testing 2',
                'form-1-required_intfield': 75,
                'form-1-optional_intfield': 85,
            },
            expected_title='Basic Formset Page | Test Views',
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '---------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-formset/"\n'
                '---------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Formset Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Basic Formset Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <input type="hidden" name="form-TOTAL_FORMS" value="2" id="id_form-TOTAL_FORMS"><input type="hidden" name="form-INITIAL_FORMS" value="2" id="id_form-INITIAL_FORMS"><input type="hidden" name="form-MIN_NUM_FORMS" id="id_form-MIN_NUM_FORMS"><input type="hidden" name="form-MAX_NUM_FORMS" id="id_form-MAX_NUM_FORMS">\n'
                ' <hr>\n'
                ' <ul class="errorlist nonfield"><li>Invalid values. IntFields cannot add up to above 100.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-0-required_charfield" value="Testing 1" maxlength="100" id="id_form-0-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-0-optional_charfield" maxlength="100" id="id_form-0-optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-0-required_intfield" value="55" id="id_form-0-required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-0-optional_intfield" value="65" id="id_form-0-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <ul class="errorlist nonfield"><li>Invalid values. IntFields cannot add up to above 100.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-1-required_charfield" value="Testing 2" maxlength="100" id="id_form-1-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-1-optional_charfield" maxlength="100" id="id_form-1-optional_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-1-required_intfield" value="75" id="id_form-1-required_intfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-1-optional_intfield" value="85" id="id_form-1-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "2681"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `hidden_fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_form-0-required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="form-0-required"...""100" id="id_form-0-required_charfield">"\n'
                    '    * fields: []\n'
                    '    * form: "<input type="hidden" name="form-TOTAL_FO"..."X_NUM_FORMS" id="id_form-MAX_NUM_FORMS">"\n'
                    '    * formset: "<input type="hidden" name="form-TOTAL_FO"..."id="id_form-1-optional_intfield"> </div>"\n'
                    '    * header: Basic Formset Page\n'
                    '    * hidden_fields: "[<django.forms.boundfield.BoundField obj"..."ld.BoundField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of hidden_fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>]"\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-formset/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-formset/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'form-TOTAL_FORMS\', \'is_hidden\'"..."/widgets/hidden.html\', \'type\': \'hidden\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '\n'
                'Formset (Context Id: "formset")\n'
                '\n'
                '    Management Form:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-TOTAL_FORMS: 2\n'
                '            * form-INITIAL_FORMS: 2\n'
                '        Formset sub-form validated successfully.\n'
                '\n'
                '    Sub-Form #1:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-0-required_charfield: Testing 1\n'
                '            * form-0-required_intfield: 55\n'
                '            * form-0-optional_intfield: 65\n'
                '\n'
                '        Form Invalid:\n'
                '            Non-field Errors:\n'
                '                * "Invalid values. IntFields cannot add up to above 100."\n'
                '            Field Errors:\n'
                '                * form-0-__all__: "Invalid values. IntFields cannot add up to above 100."\n'
                '\n'
                '    Sub-Form #2:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-1-required_charfield: Testing 2\n'
                '            * form-1-required_intfield: 75\n'
                '            * form-1-optional_intfield: 85\n'
                '\n'
                '        Form Invalid:\n'
                '            Non-field Errors:\n'
                '                * "Invalid values. IntFields cannot add up to above 100."\n'
                '            Field Errors:\n'
                '                * form-1-__all__: "Invalid values. IntFields cannot add up to above 100."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__form_handling__basic_formset__failure__raise_field_error(self, mock_stdout):
        """Verifying output of form debug, in case where form validates successfully."""

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        self.assertPostResponse(
            'django_expanded_test_cases:response-with-basic-formset',
            data={
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "2",
                'form-0-required_charfield': 'Testing 1',
                'form-0-required_intfield': -1,
                'form-0-optional_intfield': -2,
                'form-1-required_charfield': 'Testing 2',
                'form-1-required_intfield': -3,
                'form-1-optional_intfield': -4,
            },
            expected_title='Basic Formset Page | Test Views',
        )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '---------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/forms/basic-formset/"\n'
                '---------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text_1 = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>Basic Formset Page | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <h1>Basic Formset Page Header</h1>\n'
                ' <form method="POST">\n'
                ' <input type="hidden" name="csrfmiddlewaretoken" value="'
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Check for content section.
            expected_text_2 = (
                '">\n'
                ' <input type="hidden" name="form-TOTAL_FORMS" value="2" id="id_form-TOTAL_FORMS"><input type="hidden" name="form-INITIAL_FORMS" value="2" id="id_form-INITIAL_FORMS"><input type="hidden" name="form-MIN_NUM_FORMS" id="id_form-MIN_NUM_FORMS"><input type="hidden" name="form-MAX_NUM_FORMS" id="id_form-MAX_NUM_FORMS">\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-0-required_charfield" value="Testing 1" maxlength="100" id="id_form-0-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-0-optional_charfield" maxlength="100" id="id_form-0-optional_charfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>Cannot set "IntField - Required" to a negative value.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-0-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-0-required_intfield" value="-1" aria-invalid="true" id="id_form-0-required_intfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>Cannot set "IntField - Optional" to a negative value.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-0-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-0-optional_intfield" value="-2" aria-invalid="true" id="id_form-0-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_charfield">CharField - Required:</label>\n'
                ' <input type="text" name="form-1-required_charfield" value="Testing 2" maxlength="100" id="id_form-1-required_charfield">\n'
                ' </p>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_charfield">CharField - Optional:</label>\n'
                ' <input type="text" name="form-1-optional_charfield" maxlength="100" id="id_form-1-optional_charfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>Cannot set "IntField - Required" to a negative value.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-1-required_intfield">IntField - Required:</label>\n'
                ' <input type="number" name="form-1-required_intfield" value="-3" aria-invalid="true" id="id_form-1-required_intfield">\n'
                ' </p>\n'
                ' <ul class="errorlist"><li>Cannot set "IntField - Optional" to a negative value.</li></ul>\n'
                ' <p>\n'
                ' <label for="id_form-1-optional_intfield">IntField - Optional:</label>\n'
                ' <input type="number" name="form-1-optional_intfield" value="-4" aria-invalid="true" id="id_form-1-optional_intfield">\n'
                ' </p>\n'
                ' <hr>\n'
                ' <input type="submit" value="Submit">\n'
                ' </form>\n'
                '</body>\n'
                '\n'
                '\n'
            )

            # Check second subsection.
            self.assertTextStartsWith(expected_text_2, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Vary": "Cookie"\n'
                '    * "Content-Length": "2945"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `hidden_fields` line.
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                '========== response.context ==========\n'
                '    * attrs: {\'for\': \'id_form-0-required_charfield\'}\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[64:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * error_class: errorlist nonfield\n'
                    '    * errors: \n'
                    '    * False: False\n'
                    '    * field: "<input type="text" name="form-0-required"...""100" id="id_form-0-required_charfield">"\n'
                    '    * fields: []\n'
                    '    * form: "<input type="hidden" name="form-TOTAL_FO"..."X_NUM_FORMS" id="id_form-MAX_NUM_FORMS">"\n'
                    '    * formset: "<input type="hidden" name="form-TOTAL_FO"..."id="id_form-1-optional_intfield"> </div>"\n'
                    '    * header: Basic Formset Page\n'
                    '    * hidden_fields: "[<django.forms.boundfield.BoundField obj"..."ld.BoundField object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # # Also strip out problematic dynamic characters of hidden_fields text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>]"\n'
                    '    * label: CharField - Required:\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: POST \'/forms/basic-formset/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[51:]

                expected_text_4 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: POST \'/forms/basic-formset/\'>\n'
                    '    * tag: label\n'
                    '    * True: True\n'
                    '    * use_tag: True\n'
                    '    * user: AnonymousUser\n'
                    '    * widget: "{\'name\': \'form-TOTAL_FORMS\', \'is_hidden\'"..."/widgets/hidden.html\', \'type\': \'hidden\'}"\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    No context messages found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '\n'
                'Formset (Context Id: "formset")\n'
                '\n'
                '    Management Form:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-TOTAL_FORMS: 2\n'
                '            * form-INITIAL_FORMS: 2\n'
                '        Formset sub-form validated successfully.\n'
                '\n'
                '    Sub-Form #1:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-0-required_charfield: Testing 1\n'
                '            * form-0-required_intfield: -1\n'
                '            * form-0-optional_intfield: -2\n'
                '\n'
                '        Form Invalid:\n'
                '            Field Errors:\n'
                '                * form-0-required_intfield: "Cannot set "IntField - Required" to a negative value."\n'
                '                * form-0-optional_intfield: "Cannot set "IntField - Optional" to a negative value."\n'
                '\n'
                '    Sub-Form #2:\n'
                '\n'
                '        Provided Form Fields:\n'
                '            * form-1-required_charfield: Testing 2\n'
                '            * form-1-required_intfield: -3\n'
                '            * form-1-optional_intfield: -4\n'
                '\n'
                '        Form Invalid:\n'
                '            Field Errors:\n'
                '                * form-1-required_intfield: "Cannot set "IntField - Required" to a negative value."\n'
                '                * form-1-optional_intfield: "Cannot set "IntField - Optional" to a negative value."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    # endregion Form Handling


class TestIntegrationDebugOutputWithSettings(IntegrationTestCase, IntegrationDebugOutputTestCase):
    """Tests for IntegrationTestCase class "debug output" logic,
    when using class variables to modify project handling.
    """

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__FULL)
    @override_settings(ETC_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__FULL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__FULL,
    )
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_before__full(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_BEFORE variable.

        Checks that expected section is skipped when provided full html to skip.
        """

        with self.subTest('Setting sanity checking'):
            # Verify actual project settings values.
            self.assertEqual(
                getattr(settings, "DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE", None),
                SKIP_BEFORE_VALUE__FULL,
            )

            from django_expanded_test_cases.constants import ETC_SKIP_CONTENT_BEFORE

            self.assertEqual(ETC_SKIP_CONTENT_BEFORE, SKIP_BEFORE_VALUE__FULL)

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>View with Three Messages Header</h1>\n'
                ' <p>Pretend useful stuff is displayed here, for three-message render() view.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__MINIMAL)
    @override_settings(ETC_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__MINIMAL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__MINIMAL,
    )
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_before__minimal(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_BEFORE variable.

        Checks that expected section is skipped when provided minimal html to skip.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>View with Three Messages Header</h1>\n'
                ' <p>Pretend useful stuff is displayed here, for three-message render() view.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__FULL)
    @override_settings(ETC_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__FULL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__FULL,
    )
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_after__full(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_AFTER variable.

        Checks that expected section is skipped when provided full html to skip.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>View with Three Messages | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__MINIMAL)
    @override_settings(ETC_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__MINIMAL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__MINIMAL,
    )
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_after__minimal(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_AFTER variable.

        Checks that expected section is skipped when provided minimal html to skip.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<head>\n'
                ' <meta charset="utf-8">\n'
                ' <title>View with Three Messages | Test Views</title>\n'
                '</head>\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__FULL)
    @override_settings(ETC_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__FULL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__FULL,
    )
    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__FULL)
    @override_settings(ETC_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__FULL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__FULL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__FULL,
    )
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_both__full(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_BEFORE variable.

        Checks that expected section is skipped when provided full html to skip.
        """

        with self.subTest('Setting sanity checking'):
            # Verify actual project settings values.
            self.assertEqual(
                getattr(settings, "DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE", None),
                SKIP_BEFORE_VALUE__FULL,
            )

            from django_expanded_test_cases.constants import ETC_SKIP_CONTENT_BEFORE

            self.assertEqual(ETC_SKIP_CONTENT_BEFORE, SKIP_BEFORE_VALUE__FULL)

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__MINIMAL)
    @override_settings(ETC_SKIP_CONTENT_BEFORE=SKIP_BEFORE_VALUE__MINIMAL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_BEFORE",
        SKIP_BEFORE_VALUE__MINIMAL,
    )
    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__MINIMAL)
    @override_settings(ETC_SKIP_CONTENT_AFTER=SKIP_AFTER_VALUE__MINIMAL)
    @patch(
        "django_expanded_test_cases.constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__MINIMAL,
    )
    @patch(
        "django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_AFTER",
        SKIP_AFTER_VALUE__MINIMAL,
    )
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_both__minimal(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_BEFORE variable.

        Checks that expected section is skipped when provided minimal html to skip.
        """

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')

    @override_settings(DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_HEAD=True)
    @override_settings(ETC_SKIP_CONTENT_HEAD=True)
    @patch("django_expanded_test_cases.constants.ETC_SKIP_CONTENT_HEAD", True)
    @patch("django_expanded_test_cases.constants.general_handling_constants.ETC_SKIP_CONTENT_HEAD", True)
    @patch("django_expanded_test_cases.mixins.response_mixin.ETC_SKIP_CONTENT_HEAD", True)
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__general_debug_output__skip_content_head(self, mock_stdout):
        """Verifying output of assertResponse, with SKIP_CONTENT_HEAD variable.

        Checks that expected section is skipped when provided full html to skip.
        """

        with self.subTest('Setting sanity checking'):
            # Verify actual project settings values.
            self.assertEqual(
                getattr(settings, "DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_HEAD", None),
                True,
            )

            from django_expanded_test_cases.constants import ETC_SKIP_CONTENT_HEAD

            self.assertEqual(ETC_SKIP_CONTENT_HEAD, True)

        # Set error output to not truncate text comparison errors for these tests.
        self.maxDiff = None

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_title='Testing',
            )

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        # Here we also trim away any potential included text coloring, just for ease of UnitTesting.
        # We maybe could test for text coloring here too. But that would make tests much more annoying,
        # for something that is both optional, and should be exceedingly obvious if it stops working.
        actual_text = self.strip_text_colors(mock_stdout.getvalue())

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '----------------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/views/three-messages/"\n'
                '----------------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '<body>\n'
                ' <ul>\n'
                ' <li><p>\n'
                ' Test info message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test warning message.\n'
                ' </p></li>\n'
                ' <li><p>\n'
                ' Test error message.\n'
                ' </p></li>\n'
                ' </ul>\n'
                ' <h1>View with Three Messages Header</h1>\n'
                ' <p>Pretend useful stuff is displayed here, for three-message render() view.</p>\n'
                '</body>\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test header section'):
            # Check for header section.
            expected_text = (
                '========== response.headers ==========\n'
                '    * "Content-Type": "text/html; charset=utf-8"\n'
                '    * "X-Frame-Options": "DENY"\n'
                '    * "Content-Length": "506"\n'
                '    * "X-Content-Type-Options": "nosniff"\n'
                '    * "Referrer-Policy": "same-origin"\n'
            )

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '\n'
                    '\n'
                )
            else:
                # Handling for all newer Django versions.
                expected_text += (
                    # Comment to prevent "Black" formatting.
                    '    * "Cross-Origin-Opener-Policy": "same-origin"\n'
                    '\n'
                    '\n'
                )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip header section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test context section'):
            # Check for context section.
            # Due to the reference to several dynamic references, we need to split this into multiple checks.
            #
            # Django v4 or Later - Problematic lines are:
            #   * The `csrf_token` line
            #   * The `perms` line.
            # Django v3 or Earlier - Problematic lines are:
            #   * The `csrf_token` line.
            #   * The `perms` line.
            #   * The `messages` line.

            expected_text_1 = (
                # Comment to prevent "Black" formatting.
                '========== response.context ==========\n'
                '    * csrf_token: '
            )

            # Check first subsection.
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Handle based on Django version.
            if django_version[0] < 4:
                # Handling for Django 3 or lower.

                expected_text_2 = (
                    '\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * user: AnonymousUser\n'
                    '    * perms: <django.contrib.auth.context_processors.PermWrapper object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    # Comment to prevent "Black" formatting.
                    '>\n'
                    '    * messages: "<django.contrib.messages.storage.fallbac"..."allbackStorage object at '
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_4 = (
                    '>"\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * True: True\n'
                    '    * False: False\n'
                    '    * None: None\n'
                    '\n'
                    '\n'
                )

                # Check fourth subsection.
                self.assertTextStartsWith(expected_text_4, actual_text)

                # Passed fourth check. Strip away.
                actual_text = actual_text.replace(expected_text_4, '')

            else:
                # Handling for all newer Django versions.

                expected_text_2 = (
                    '\n'
                    '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                    '    * False: False\n'
                    '    * header: View with Three Messages\n'
                    '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                    '    * None: None\n'
                    '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
                )

                # Check second subsection.
                self.assertTextStartsWith(expected_text_2, actual_text)

                # Passed second check. Strip away.
                actual_text = actual_text.replace(expected_text_2, '')
                # Also strip out problematic dynamic characters of PermWrapper text.
                actual_text = actual_text[14:]

                expected_text_3 = (
                    '>>)"\n'
                    '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                    '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                    '    * True: True\n'
                    '    * user: AnonymousUser\n'
                    '\n'
                    '\n'
                )

                # Check third subsection.
                self.assertTextStartsWith(expected_text_3, actual_text)

                # Passed third check. Strip away.
                actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== client.session ==========\n'
                '    No session data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip session section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test message section'):
            # Check for message section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== response.context["messages"] ==========\n'
                '    * "Test info message."\n'
                '    * "Test warning message."\n'
                '    * "Test error message."\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip message section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test form section'):
            # Check for form section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip form section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                # Comment to prevent "Black" formatting.
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')
