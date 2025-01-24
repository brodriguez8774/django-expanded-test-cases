"""
Tests for IntegrationTestCase class "debug console output" logic when handling JSON.
"""

# System Imports.
import io
import unittest.mock
from unittest import skipIf
from unittest.mock import patch

# Third-Party Imports.
from django import VERSION as django_version
from django.conf import settings

# Internal Imports.
from .test_integration_debug_output import IntegrationDebugOutputTestCase
from django_expanded_test_cases import IntegrationTestCase
from django_expanded_test_cases.constants import (
    ETC_OUTPUT_EMPHASIS_COLOR,
    ETC_OUTPUT_RESET_COLOR,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_RESPONSE_DEBUG_URL_COLOR,
    ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
    ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
    ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
    ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
)


class TestIntegrationDebugJsonOutput(IntegrationTestCase, IntegrationDebugOutputTestCase):
    """Tests for IntegrationTestCase class "debug output" logic when handling JSON."""

    @classmethod
    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS_IN_SETUPTESTDATA', True)
    def setUpTestData(cls, *args, **kwargs):
        """Override setting for faster tests."""
        super().setUpTestData(*args, **kwargs)

    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS_IN_SETUPTESTDATA', True)
    def setUp(self, *args, **kwargs):
        """Override setting for faster tests."""
        super().setUp(*args, **kwargs)

    # region Dict as Base

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__basic_dict__general(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the general JSON output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
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
                '-----------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/json/basic-dict/"\n'
                '-----------------------------------------------------\n'
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
                '  "test_list":\n'
                '  [\n'
                '    "Sublist Item 1",\n'
                '    "Sublist Item 2",\n'
                '    "Sublist Item 3",\n'
                '  ],\n'
                '  "request_headers":\n'
                '  {\n'
                '    "Cookie": "",\n'
                '    "Content-Type": "application/json",\n'
                '    "Accept": "application/json",\n'
                '  },\n'
                '  "none_type": None,\n'
                '  "int_type": 5,\n'
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
                '    * "Content-Length": "248"\n'
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

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__all_green(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__str_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "Test",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{8}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__dict_wrong_key(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Test": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__dict_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "Test",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__list_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Test",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__none_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": 'Test',
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {6}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__int_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 6,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {8}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__missing_str(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}{1}{0}\n'
                '  "{8}success{0}": "{8}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{7}{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__missing_dict(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{8}request_headers{0}":{0}\n'
                '  {8}{1}{0}\n'
                '    "{8}Cookie{0}": "{8}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{8}Accept{0}": "{8}application/json{0}",{0}\n'
                '  {8}{2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{7}{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__missing_list(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{8}test_list{0}":{0}\n'
                '  {8}[{0}\n'
                '    "{8}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {8}],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{7}{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__missing_none(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{8}none_type{0}": {8}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{7}{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__missing_int(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{8}int_type{0}": {8}5{0},{0}\n'
                '{7}{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__str_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": 5,
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{6}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__dict_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": "Test",
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {6}{1}{0}\n'
                '    "{8}Cookie{0}": "{8}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{8}Accept{0}": "{8}application/json{0}",{0}\n'
                '  {6}{2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__list_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": "Test",
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  {6}[{0}\n'
                '    "{8}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {6}],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__int_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": "5",
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {6}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__dict_length_mismatch__too_many(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Test": "Aaa",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {7}{1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {7}{2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__dict_length_mismatch__too_few(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {7}{1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {7}{2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__list_length_mismatch__too_many(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                        "Sublist Item 4",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  {7}[{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  {7}],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_dict__list_length_mismatch__too_few(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_json={
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "none_type": None,
                    "int_type": 5,
                },
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-dict/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{1}{0}\n'
                '  "{5}success{0}": "{5}This is a test Json response.{0}",{0}\n'
                '  "{5}test_list{0}":{0}\n'
                '  {7}[{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {7}],{0}\n'
                '  "{5}request_headers{0}":{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  "{5}none_type{0}": {5}None{0},{0}\n'
                '  "{5}int_type{0}": {5}5{0},{0}\n'
                '{2}{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    # endregion Dict as Base

    # region List as Base

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__basic_list__general(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the general JSON output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
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
                '-----------------------------------------------------\n'
                'Attempting to access url "127.0.0.1/json/basic-list/"\n'
                '-----------------------------------------------------\n'
                '\n'
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        actual_text = actual_text.replace(expected_text, '')

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '========== response.content ==========\n'
                '[\n'
                '  "List Item 1",\n'
                '  "List Item 2",\n'
                '  "List Item 3",\n'
                '  [\n'
                '    "Sublist Item 1",\n'
                '    "Sublist Item 2",\n'
                '    "Sublist Item 3",\n'
                '  ],\n'
                '  {\n'
                '    "Cookie": "",\n'
                '    "Content-Type": "application/json",\n'
                '    "Accept": "application/json",\n'
                '  },\n'
                '  None,\n'
                '  5,\n'
                ']\n'
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

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__all_green(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__str_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "Test",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{8}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__dict_wrong_key(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Test": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__dict_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "Test",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__list_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Test",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__none_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    "Test",
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {6}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__int_wrong_value(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    6,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {8}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__missing_str(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{8}List Item 2{0}",{0}\n'
                '  "{6}List Item 3{0}",{0}\n'
                '  {6}[{0}\n'
                '    "{8}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {6}],{0}\n'
                '  {6}{1}{0}\n'
                '    "{8}Cookie{0}": "{8}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{8}Accept{0}": "{8}application/json{0}",{0}\n'
                '  {6}{2},{0}\n'
                '  {6}None{0},{0}\n'
                '  {8}5{0},{0}\n'
                '{7}]{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__missing_dict(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {6}{1}{0}\n'
                '    "{8}Cookie{0}": "{8}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{8}Accept{0}": "{8}application/json{0}",{0}\n'
                '  {6}{2},{0}\n'
                '  {6}None{0},{0}\n'
                '  {8}5{0},{0}\n'
                '{7}]{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__missing_list(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  {6}[{0}\n'
                '    "{8}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {6}],{0}\n'
                '  {6}{1}{0}\n'
                '    "{8}Cookie{0}": "{8}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{8}Accept{0}": "{8}application/json{0}",{0}\n'
                '  {6}{2},{0}\n'
                '  {6}None{0},{0}\n'
                '  {8}5{0},{0}\n'
                '{7}]{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__missing_none(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {6}None{0},{0}\n'
                '  {8}5{0},{0}\n'
                '{7}]{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__missing_int(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '{7}[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {8}5{0},{0}\n'
                '{7}]{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__str_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    2,
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{6}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__dict_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "Test",
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {6}{1}{0}\n'
                '    "{8}Cookie{0}": "{8}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{8}Accept{0}": "{8}application/json{0}",{0}\n'
                '  {6}{2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__list_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    "Test",
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  {6}[{0}\n'
                '    "{8}Sublist Item 1{0}",{0}\n'
                '    "{8}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {6}],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__int_type_mismatch(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    "5",
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {6}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__dict_length_mismatch__too_many(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Test": "Test",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {7}{1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {7}{2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__dict_length_mismatch__too_few(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    {
                        "Cookie": "",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  [{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  ],{0}\n'
                '  {7}{1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{8}Content-Type{0}": "{8}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {7}{2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__list_length_mismatch__too_many(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                        "Test",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  {7}[{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{5}Sublist Item 3{0}",{0}\n'
                '  {7}],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    @skipIf(not settings.DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT, 'Test only works as expected with DEBUG PRINT.')
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__json_debug_output__highlighting__basic_list__list_length_mismatch__too_few(self, mock_stdout):
        """Verifying output of assertResponse, with different failure types.

        This one tests the JSON color highlighting output for assertJsonResponse.
        """

        # Force assertion error so we can check debug output.
        with self.assertRaises(AssertionError):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-list',
                expected_url='/json/basic-list/',
                expected_json=[
                    "List Item 1",
                    "List Item 2",
                    "List Item 3",
                    [
                        "Sublist Item 1",
                        "Sublist Item 2",
                    ],
                    {
                        "Cookie": "",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    None,
                    5,
                ],
            )
            # Force test to fail, even though above passes. To test all "green" output.
            self.assertTrue(False)

        # Stdout (aka console debug print out) is being captured by above unittest.mock.
        actual_text = mock_stdout.getvalue()

        with self.subTest('Test url section'):
            # Check for url section.
            expected_text = (
                '{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '{1}{2}Attempting to access url "127.0.0.1/json/basic-list/"{0}\n'
                '{1}{2}-----------------------------------------------------{0}\n'
                '\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                ETC_RESPONSE_DEBUG_URL_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip url section.
        # Note: Using `.replace` can be weird here, when checking for color output.
        # We instead trim the already-verified character length, for more reliable truncating.
        actual_text = actual_text[len(expected_text) :]

        with self.subTest('Test content section'):
            # Check for content section.
            expected_text = (
                '{0}\n'
                '{3}{4}========== response.content =========={0}\n'
                '[{0}\n'
                '  "{5}List Item 1{0}",{0}\n'
                '  "{5}List Item 2{0}",{0}\n'
                '  "{5}List Item 3{0}",{0}\n'
                '  {7}[{0}\n'
                '    "{5}Sublist Item 1{0}",{0}\n'
                '    "{5}Sublist Item 2{0}",{0}\n'
                '    "{8}Sublist Item 3{0}",{0}\n'
                '  {7}],{0}\n'
                '  {1}{0}\n'
                '    "{5}Cookie{0}": "{5}{0}",{0}\n'
                '    "{5}Content-Type{0}": "{5}application/json{0}",{0}\n'
                '    "{5}Accept{0}": "{5}application/json{0}",{0}\n'
                '  {2},{0}\n'
                '  {5}None{0},{0}\n'
                '  {5}5{0},{0}\n'
                ']{0}\n'
            ).format(
                ETC_OUTPUT_RESET_COLOR,
                '{',
                '}',
                ETC_RESPONSE_DEBUG_CONTENT_COLOR,
                ETC_OUTPUT_EMPHASIS_COLOR,
                ETC_RESPONSE_DEBUG_JSON_MATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_TYPE_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_LENGTH_MISMATCH_COLOR,
                ETC_RESPONSE_DEBUG_JSON_CONTENT_MISMATCH_COLOR,
            )
            self.assertTextStartsWith(expected_text, actual_text)

        # Passed. Strip content section.
        actual_text = actual_text.replace(expected_text, '')

    # endregion List as Base
