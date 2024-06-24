"""
Tests for test_cases/integration_test_case.py "helper function" utilities and logic.
"""

# System Imports.
import io
import unittest.mock
from unittest.mock import patch

# Third-Party Imports.
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Login Page\n'
                '    * text: Pretend this is a login page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/login/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/login/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Check third subsection.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Check third subsection.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Check third subsection.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Check third subsection.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Check third subsection.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Check third subsection.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: test_superuser\n'
                '    * perms: PermWrapper(<SimpleLazyObject: <User: test_superuser>>)\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text_1 = (
                '========== client.session ==========\n'
                '    * _auth_user_id: 1\n'
                '    * _auth_user_backend: django.contrib.auth.backends.ModelBackend\n'
                '    * _auth_user_hash: '
            )
            expected_text_2 = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: test_admin\n'
                '    * perms: PermWrapper(<SimpleLazyObject: <User: test_admin>>)\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text_1 = (
                '========== client.session ==========\n'
                '    * _auth_user_id: 2\n'
                '    * _auth_user_backend: django.contrib.auth.backends.ModelBackend\n'
                '    * _auth_user_hash: '
            )
            expected_text_2 = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: Home Page\n'
                '    * text: Pretend this is the project landing page.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/template-response/home/\'>\n'
                '    * user: test_user\n'
                '    * perms: PermWrapper(<SimpleLazyObject: <User: test_user>>)\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/template-response/home/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
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

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_2, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text_1 = (
                '========== client.session ==========\n'
                '    * _auth_user_id: 4\n'
                '    * _auth_user_backend: django.contrib.auth.backends.ModelBackend\n'
                '    * _auth_user_hash: '
            )
            expected_text_2 = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
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
            # Problematic lines are the `csrf_token` line and the `perms: PermWrapper line`.
            expected_text_1 = (
                '========== response.context ==========\n'
                '    * header: View with Three Messages\n'
                '    * text: Pretend useful stuff is displayed here, for three-message render() view.\n'
                '    * csrf_token: '
            )
            expected_text_2 = (
                '\n'
                '    * request: <WSGIRequest: GET \'/views/three-messages/\'>\n'
                '    * user: AnonymousUser\n'
                '    * perms: "PermWrapper(<SimpleLazyObject: <django.c"..."nonymousUser object at '
            )
            expected_text_3 = (
                '>>)"\n'
                '    * messages: <FallbackStorage: request=<WSGIRequest: GET \'/views/three-messages/\'>>\n'
                '    * DEFAULT_MESSAGE_LEVELS: {\'DEBUG\': 10, \'INFO\': 20, \'SUCCESS\': 25, \'WARNING\': 30, \'ERROR\': 40}\n'
                '    * True: True\n'
                '    * False: False\n'
                '    * None: None\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text_1, actual_text)

            # Passed first check. Strip away.
            actual_text = actual_text.replace(expected_text_1, '')
            # Also strip out problematic dynamic characters of csrf text.
            actual_text = actual_text[67:]

            # Passed second check. Strip away.
            actual_text = actual_text.replace(expected_text_2, '')
            # Also strip out problematic dynamic characters of PermWrapper text.
            actual_text = actual_text[14:]

            # Should be good to verify the rest of the section.
            self.assertTextStartsWith(expected_text_3, actual_text)

        # Passed. Strip context section.
        actual_text = actual_text.replace(expected_text_3, '')

        with self.subTest('Test session section'):
            # Check for session section.
            expected_text = (
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
                '========== Form Data ==========\n'
                '    No form data found.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test user section'):
            # Check for user section.
            expected_text = (
                '========== User Info ==========\n'
                '    Anonymous user. No user is logged in.\n'
                '\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip user section.
        actual_text = actual_text.replace(expected_text, '')
