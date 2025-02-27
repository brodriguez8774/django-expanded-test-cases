"""
Tests for IntegrationTestCase class custom assertions and testing checks.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.http import HttpResponse
from django.test import override_settings
from django.urls import reverse
from pytest import warns

# Internal Imports.
from django_expanded_test_cases import IntegrationTestCase
from django_expanded_test_cases.constants import (
    COLORAMA_PRESENT,
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_RESET_COLOR,
    UNDERLINE_RESET as ETC_UNDERLINE_RESET,
)


class IntegrationAssertionTestCase:
    """Tests for IntegrationTestCase class custom assertions and testing checks.

    This class is a parent class that should not run by itself.
    It needs to be imported into other classes to execute.
    """

    @classmethod
    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS_IN_SETUPTESTDATA', True)
    def setUpTestData(cls, *args, **kwargs):
        """Override setting for faster tests."""
        super().setUpTestData(*args, **kwargs)

    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS_IN_SETUPTESTDATA', True)
    def setUp(self, *args, **kwargs):
        """Override setting for faster tests."""
        super().setUp(*args, **kwargs)

    # region Response Assertion Tests

    def test__assertResponse__url(self):
        """
        Tests URL value returned response object in assertResponse() function.
        Checks various possible urls to ensure consistent behavior.
        """

        # Warning handling for APPEND_SLASH setting, since these tests check
        # a variety of urls, some of which are garbage.
        expected_warn_msg = (
            'Django setting APPEND_SLASH is set to True, '
            'but provided url does not contain a trailing slash. '
            'This may cause UnitTests with ETC to fail. '
            'Consider appending a url slash. '
            'Url was: {0}'
        )

        with self.subTest('With no site_root_url value defined - Via literal value'):

            with self.subTest('Test 404 page url'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('bad_url', expected_status=404)
                    self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('bad_url', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/bad_url/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
                    self.assertText('/bad_url/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('bad_url/', expected_status=404)

                    # Provided values.
                    self.assertText('bad_url/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/bad_url/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
                    self.assertText('/bad_url/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/bad_url/', expected_status=404)

                    # Provided values.
                    self.assertText('127.0.0.1/bad_url/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/bad_url/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
                    self.assertText('/bad_url/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///bad_url///', expected_status=404)

                    # Provided values.
                    self.assertText('///bad_url///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/bad_url/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
                    self.assertText('/bad_url/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "index" page url'):

                with self.subTest('With no slashes'):
                    response = self.assertResponse('')

                    # Provided values.
                    self.assertText('', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
                    self.assertText('/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('/')

                    # Provided values.
                    self.assertText('/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
                    self.assertText('/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/')

                    # Provided values.
                    self.assertText('127.0.0.1/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
                    self.assertText('/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('//////')

                    # Provided values.
                    self.assertText('//////', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
                    self.assertText('/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "home" page url'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('home')
                    self.assertText(expected_warn_msg.format('home'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('home', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/home/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
                    self.assertText('/home/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('home/')

                    # Provided values.
                    self.assertText('home/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/home/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
                    self.assertText('/home/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes on both sides'):
                    response = self.assertResponse('/home/')

                    # Provided values.
                    self.assertText('/home/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/home/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
                    self.assertText('/home/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/home/')

                    # Provided values.
                    self.assertText('127.0.0.1/home/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/home/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
                    self.assertText('/home/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///home///')

                    # Provided values.
                    self.assertText('///home///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/home/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
                    self.assertText('/home/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "login" page url'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('login')
                    self.assertText(expected_warn_msg.format('login'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('login', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/login/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
                    self.assertText('/login/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('login/')

                    # Provided values.
                    self.assertText('login/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/login/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
                    self.assertText('/login/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes on both sides'):
                    response = self.assertResponse('/login/')

                    # Provided values.
                    self.assertText('/login/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/login/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
                    self.assertText('/login/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/login/')

                    # Provided values.
                    self.assertText('127.0.0.1/login/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/login/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
                    self.assertText('/login/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With no slashes'):
                    response = self.assertResponse('///login///')

                    # Provided values.
                    self.assertText('///login///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/login/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
                    self.assertText('/login/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "one message" page url'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('views/one-message')
                    self.assertText(expected_warn_msg.format('views/one-message'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('views/one-message', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/one-message/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('views/one-message/')

                    # Provided values.
                    self.assertText('views/one-message/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/one-message/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes on both sides'):
                    response = self.assertResponse('/views/one-message/')

                    # Provided values.
                    self.assertText('/views/one-message/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/one-message/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/views/one-message/')

                    # Provided values.
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/one-message/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///views/one-message///')

                    # Provided values.
                    self.assertText('///views/one-message///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/one-message/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "two messages" page url'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('views/two-messages')
                    self.assertText(expected_warn_msg.format('views/two-messages'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('views/two-messages', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('views/two-messages/')

                    # Provided values.
                    self.assertText('views/two-messages/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes on both ends'):
                    response = self.assertResponse('/views/two-messages/')

                    # Provided values.
                    self.assertText('/views/two-messages/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/views/two-messages/')

                    # Provided values.
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///views/two-messages///')

                    # Provided values.
                    self.assertText('///views/two-messages///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "three messages" page url'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('views/three-messages')
                    self.assertText(expected_warn_msg.format('views/three-messages'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('views/three-messages', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('views/three-messages/')

                    # Provided values.
                    self.assertText('views/three-messages/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes on both ends'):
                    response = self.assertResponse('/views/three-messages/')

                    # Provided values.
                    self.assertText('/views/three-messages/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/views/three-messages/')

                    # Provided values.
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///views/three-messages///')

                    # Provided values.
                    self.assertText('///views/three-messages///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
                    self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page #1'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('user/detail/1')
                    self.assertText(expected_warn_msg.format('user/detail/1'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('user/detail/1', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('user/detail/1/')

                    # Provided values.
                    self.assertText('user/detail/1/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes on both ends'):
                    response = self.assertResponse('/user/detail/1/')

                    # Provided values.
                    self.assertText('/user/detail/1/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/user/detail/1/')

                    # Provided values.
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///user/detail/1///')

                    # Provided values.
                    self.assertText('///user/detail/1///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page #2'):

                with self.subTest('With no slashes'):
                    with warns(Warning) as warning_info:
                        response = self.assertResponse('user/detail/2')
                    self.assertText(expected_warn_msg.format('user/detail/2'), warning_info[0].message.args[0])

                    # Provided values.
                    self.assertText('user/detail/2', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slash at end'):
                    response = self.assertResponse('user/detail/2/')

                    # Provided values.
                    self.assertText('user/detail/2/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With slashes at both ends'):
                    response = self.assertResponse('/user/detail/2/')

                    # Provided values.
                    self.assertText('/user/detail/2/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('As full url'):
                    response = self.assertResponse('127.0.0.1/user/detail/2/')

                    # Provided values.
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

                with self.subTest('With too many slashes'):
                    response = self.assertResponse('///user/detail/2///')

                    # Provided values.
                    self.assertText('///user/detail/2///', response.url_data.provided.url)
                    self.assertEqual(tuple(), response.url_data.provided.args)
                    self.assertEqual({}, response.url_data.provided.kwargs)
                    self.assertEqual({}, response.url_data.provided.query_params)

                    # Computed values.
                    self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                    self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                    self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                    self.assertIsNone(response.url_data.computed.redirect_url)
                    self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With no site_root_url value defined - Via reverse()'):

            with self.subTest('Test "index" page url'):
                response = self.assertResponse('django_expanded_test_cases:index')

                # Provided values.
                self.assertText('django_expanded_test_cases:index', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "home" page url'):
                response = self.assertResponse('django_expanded_test_cases:home')

                # Provided values.
                self.assertText('django_expanded_test_cases:home', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/home/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
                self.assertText('/home/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "login" page url'):
                response = self.assertResponse('django_expanded_test_cases:login')

                # Provided values.
                self.assertText('django_expanded_test_cases:login', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
                self.assertText('/login/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "one message" page url'):
                response = self.assertResponse('django_expanded_test_cases:response-with-one-message')

                # Provided values.
                self.assertText('django_expanded_test_cases:response-with-one-message', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
                self.assertText('/views/one-message/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "two messages" page url'):
                response = self.assertResponse('django_expanded_test_cases:response-with-two-messages')

                # Provided values.
                self.assertText('django_expanded_test_cases:response-with-two-messages', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
                self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "three pages" page url'):
                response = self.assertResponse('django_expanded_test_cases:response-with-three-messages')

                # Provided values.
                self.assertText(
                    'django_expanded_test_cases:response-with-three-messages',
                    response.url_data.provided.url,
                )
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
                self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With custom site_root_url value defined'):
            self.site_root_url = 'https://my_really_cool_site.com/'

            with self.subTest('Test index" page url'):
                response = self.assertResponse('django_expanded_test_cases:index')

                # Provided values.
                self.assertText('django_expanded_test_cases:index', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/', response.url_data.computed.initial_url)
                self.assertText('https://my_really_cool_site.com/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('https://my_really_cool_site.com/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "home" page url'):
                response = self.assertResponse('django_expanded_test_cases:home')

                # Provided values.
                self.assertText('django_expanded_test_cases:home', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/home/', response.url_data.computed.initial_url)
                self.assertText('https://my_really_cool_site.com/home/', response.url_data.computed.full_initial_url)
                self.assertText('/home/', response.url_data.computed.final_url)
                self.assertText('https://my_really_cool_site.com/home/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "login" page url'):
                response = self.assertResponse('django_expanded_test_cases:login')

                # Provided values.
                self.assertText('django_expanded_test_cases:login', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/', response.url_data.computed.initial_url)
                self.assertText('https://my_really_cool_site.com/login/', response.url_data.computed.full_initial_url)
                self.assertText('/login/', response.url_data.computed.final_url)
                self.assertText('https://my_really_cool_site.com/login/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "one message" page url'):
                response = self.assertResponse('django_expanded_test_cases:response-with-one-message')

                # Provided values.
                self.assertText('django_expanded_test_cases:response-with-one-message', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/views/one-message/', response.url_data.computed.initial_url)
                self.assertText(
                    'https://my_really_cool_site.com/views/one-message/',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/views/one-message/', response.url_data.computed.final_url)
                self.assertText(
                    'https://my_really_cool_site.com/views/one-message/',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "two messages" page url'):
                response = self.assertResponse('django_expanded_test_cases:response-with-two-messages')

                # Provided values.
                self.assertText('django_expanded_test_cases:response-with-two-messages', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
                self.assertText(
                    'https://my_really_cool_site.com/views/two-messages/',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/views/two-messages/', response.url_data.computed.final_url)
                self.assertText(
                    'https://my_really_cool_site.com/views/two-messages/',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "three messages" page url'):
                response = self.assertResponse('django_expanded_test_cases:response-with-three-messages')

                # Provided values.
                self.assertText(
                    'django_expanded_test_cases:response-with-three-messages',
                    response.url_data.provided.url,
                )
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
                self.assertText(
                    'https://my_really_cool_site.com/views/three-messages/',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/views/three-messages/', response.url_data.computed.final_url)
                self.assertText(
                    'https://my_really_cool_site.com/views/three-messages/',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

    def test__assertResponse__url__with_args(self):
        """
        Tests URL value returned response object in assertResponse() function.
        """
        with self.subTest('With no site_root_url value defined - Via standard args/kwargs'):

            with self.subTest('Test "user detail" page url via args'):
                response = self.assertResponse('django_expanded_test_cases:user-detail', args=(1,))

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual((1,), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs'):
                response = self.assertResponse('django_expanded_test_cases:user-detail', kwargs={'pk': 2})

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({'pk': 2}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via args plus query params'):
                response = self.assertResponse(
                    'django_expanded_test_cases:user-detail',
                    args=(1,),
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual((1,), response.url_data.provided.args)
                self.assertEqual(
                    {},
                    response.url_data.provided.kwargs,
                )
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    '127.0.0.1/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    '127.0.0.1/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs plus query params'):
                response = self.assertResponse(
                    'django_expanded_test_cases:user-detail',
                    kwargs={'pk': 2},
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({'pk': 2}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    '127.0.0.1/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    '127.0.0.1/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With no site_root_url value defined - Via url_args/url_kwargs'):

            with self.subTest('Test "user detail" page url via args'):
                response = self.assertResponse('django_expanded_test_cases:user-detail', url_args=(1,))

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual((1,), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs'):
                response = self.assertResponse('django_expanded_test_cases:user-detail', url_kwargs={'pk': 2})

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({'pk': 2}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via args plus query params'):
                response = self.assertResponse(
                    'django_expanded_test_cases:user-detail',
                    url_args=(1,),
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual((1,), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    '127.0.0.1/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    '127.0.0.1/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs plus query params'):
                response = self.assertResponse(
                    'django_expanded_test_cases:user-detail',
                    url_kwargs={'pk': 2},
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({'pk': 2}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    '127.0.0.1/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    '127.0.0.1/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With no site_root_url value defined - Via reverse()'):

            with self.subTest('Test "user detail" page via args'):
                response = self.assertResponse(reverse('django_expanded_test_cases:user-detail', args=(1,)))

                # Provided values.
                self.assertText('/user/detail/1/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
                self.assertText('/user/detail/1/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs'):
                response = self.assertResponse(
                    reverse(
                        'django_expanded_test_cases:user-detail',
                        kwargs={'pk': 2},
                    ),
                )

                # Provided values.
                self.assertText('/user/detail/2/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
                self.assertText('/user/detail/2/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via args plus query params'):
                response = self.assertResponse(
                    reverse('django_expanded_test_cases:user-detail', args=(1,)),
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('/user/detail/1/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    '127.0.0.1/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    '127.0.0.1/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs plus query params'):
                response = self.assertResponse(
                    reverse('django_expanded_test_cases:user-detail', kwargs={'pk': 2}),
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('/user/detail/2/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    '127.0.0.1/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    '127.0.0.1/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With custom site_root_url value defined'):
            self.site_root_url = 'https://my_really_cool_site.com/'

            with self.subTest('Test "user detail" page via args plus query params'):
                response = self.assertResponse(
                    'django_expanded_test_cases:user-detail',
                    args=(1,),
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual((1,), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    'https://my_really_cool_site.com/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/1/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    'https://my_really_cool_site.com/user/detail/1/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('Test "user detail" page via kwargs plus query params'):
                response = self.assertResponse(
                    'django_expanded_test_cases:user-detail',
                    kwargs={'pk': 2},
                    url_query_params={
                        'test_1': 'aaa',
                        'test_2': 'bbb',
                    },
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:user-detail', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({'pk': 2}, response.url_data.provided.kwargs)
                self.assertEqual({'test_1': 'aaa', 'test_2': 'bbb'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.initial_url)
                self.assertText(
                    'https://my_really_cool_site.com/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_initial_url,
                )
                self.assertText('/user/detail/2/?test_1=aaa&test_2=bbb', response.url_data.computed.final_url)
                self.assertText(
                    'https://my_really_cool_site.com/user/detail/2/?test_1=aaa&test_2=bbb',
                    response.url_data.computed.full_final_url,
                )
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

    def test__assertResponse__url__with_query_params(self):
        """
        Tests URL value returned response object in assertResponse() function.
        """

        expected_warn_msg = (
            'Django setting APPEND_SLASH is set to True, '
            'but provided url does not contain a trailing slash. '
            'This may cause UnitTests with ETC to fail. '
            'Consider appending a url slash. '
            'Url was: {0}'
        )

        with self.subTest('Login page with "next" built into url - No ending slash'):

            with self.subTest('With base url'):
                with warns(Warning) as warning_info:
                    response = self.assertResponse('/login?next=%2Fhome_page%2F')
                self.assertText(
                    expected_warn_msg.format('/login?next=%2Fhome_page%2F'),
                    warning_info[0].message.args[0],
                )

                # Provided values.
                self.assertText('/login?next=%2Fhome_page%2F', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('With site root'):
                with warns(Warning) as warning_info:
                    response = self.assertResponse('127.0.0.1/login?next=%2Fhome_page%2F')
                self.assertText(
                    expected_warn_msg.format('127.0.0.1/login?next=%2Fhome_page%2F'),
                    warning_info[0].message.args[0],
                )

                # Provided values.
                self.assertText('127.0.0.1/login?next=%2Fhome_page%2F', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('Login page with "next" built into url - With ending slash'):

            with self.subTest('With base url'):
                response = self.assertResponse('/login/?next=%2Fhome_page%2F/')

                # Provided values.
                self.assertText('/login/?next=%2Fhome_page%2F/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('With site root'):
                response = self.assertResponse('127.0.0.1/login/?next=%2Fhome_page%2F/')

                # Provided values.
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('Login page with "next" built via generate_get_url() function - No ending slash'):

            with self.subTest('With base url'):
                response = self.assertResponse(self.generate_get_url('/login', next='/home_page/'))

                # Provided values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('With site root'):
                response = self.assertResponse(self.generate_get_url('127.0.0.1/login', next='/home_page/'))

                # Provided values.
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('Login page with "next" built via generate_get_url() function - With ending slash'):

            with self.subTest('With base url'):
                response = self.assertResponse(self.generate_get_url('/login/', next='/home_page/'))

                # Provided values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('With site root'):
                response = self.assertResponse(self.generate_get_url('127.0.0.1/login/', next='/home_page/'))

                # Provided values.
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('Login page with "next" provided as query_param kwarg - No ending slash'):

            with self.subTest('With base url'):
                with warns(Warning) as warning_info:
                    response = self.assertResponse('/login', url_query_params={'next': '/home_page/'})
                self.assertText(
                    expected_warn_msg.format('/login'),
                    warning_info[0].message.args[0],
                )

                # Provided values.
                self.assertText('/login', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'next': '/home_page/'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('With site root'):
                with warns(Warning) as warning_info:
                    response = self.assertResponse('127.0.0.1/login', url_query_params={'next': '/home_page/'})
                self.assertText(
                    expected_warn_msg.format('127.0.0.1/login'),
                    warning_info[0].message.args[0],
                )

                # Provided values.
                self.assertText('127.0.0.1/login', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'next': '/home_page/'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('Login page with "next" provided as query_param kwarg - With ending slash'):

            with self.subTest('With base url'):
                response = self.assertResponse('/login/', url_query_params={'next': '/home_page/'})

                # Provided values.
                self.assertText('/login/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'next': '/home_page/'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

            with self.subTest('With site root'):
                response = self.assertResponse('127.0.0.1/login/', url_query_params={'next': '/home_page/'})

                # Provided values.
                self.assertText('127.0.0.1/login/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({'next': '/home_page/'}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_initial_url)
                self.assertText('/login/?next=%2Fhome_page%2F', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/login/?next=%2Fhome_page%2F', response.url_data.computed.full_final_url)
                self.assertIsNone(response.url_data.computed.redirect_url)
                self.assertIsNone(response.url_data.computed.full_redirect_url)

    def test__assertResponse__url_redirect(self):
        """
        Tests "url_redirect" functionality of assertResponse() function.
        """
        exception_msg = 'Response didn\'t redirect as expected. Response code was 200 (expected 302).'

        with self.subTest('With view that redirects'):

            with self.subTest('With literal url'):
                response = self.assertResponse('redirect/index/')

                # Provided values.
                self.assertText('redirect/index/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/redirect/index/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/redirect/index/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertText('/', response.url_data.computed.redirect_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_redirect_url)

                response = self.assertResponse('redirect/index/', expected_redirect_url='/')

                # Provided values.
                self.assertText('redirect/index/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/redirect/index/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/redirect/index/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertText('/', response.url_data.computed.redirect_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_redirect_url)

                response = self.assertResponse(
                    'redirect/index/',
                    expected_redirect_url='django_expanded_test_cases:index',
                )

                # Provided values.
                self.assertText('redirect/index/', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/redirect/index/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/redirect/index/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertText('/', response.url_data.computed.redirect_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_redirect_url)

            with self.subTest('Using reverse'):

                response = self.assertResponse('django_expanded_test_cases:redirect-to-index')

                # Provided values.
                self.assertText('django_expanded_test_cases:redirect-to-index', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/redirect/index/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/redirect/index/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertText('/', response.url_data.computed.redirect_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_redirect_url)

                response = self.assertResponse(
                    'django_expanded_test_cases:redirect-to-index',
                    expected_redirect_url='/',
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:redirect-to-index', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/redirect/index/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/redirect/index/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertText('/', response.url_data.computed.redirect_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_redirect_url)

                response = self.assertResponse(
                    'django_expanded_test_cases:redirect-to-index',
                    expected_redirect_url='django_expanded_test_cases:index',
                )

                # Provided values.
                self.assertText('django_expanded_test_cases:redirect-to-index', response.url_data.provided.url)
                self.assertEqual(tuple(), response.url_data.provided.args)
                self.assertEqual({}, response.url_data.provided.kwargs)
                self.assertEqual({}, response.url_data.provided.query_params)

                # Computed values.
                self.assertText('/redirect/index/', response.url_data.computed.initial_url)
                self.assertText('127.0.0.1/redirect/index/', response.url_data.computed.full_initial_url)
                self.assertText('/', response.url_data.computed.final_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
                self.assertText('/', response.url_data.computed.redirect_url)
                self.assertText('127.0.0.1/', response.url_data.computed.full_redirect_url)

        with self.subTest('With view that does not redirect'):
            # Using direct url.
            self.assertResponse('')
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '',
                    expected_redirect_url='/',
                )
            self.assertText(exception_msg, str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '',
                    expected_redirect_url='django_expanded_test_cases:index',
                )
            self.assertText(exception_msg, str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'login/',
                    expected_redirect_url='django_expanded_test_cases:index',
                )
            self.assertText(exception_msg, str(err.exception))

            # Using reverse.
            self.assertResponse('django_expanded_test_cases:index')
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:index',
                    expected_redirect_url='/',
                )
            self.assertText(exception_msg, str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:index',
                    expected_redirect_url='django_expanded_test_cases:index',
                )
            self.assertText(exception_msg, str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:login',
                    expected_redirect_url='django_expanded_test_cases:index',
                )
            self.assertText(exception_msg, str(err.exception))

    def test__assertResponse__url_redirect__with_args(self):
        """
        Tests "url_redirect" functionality of assertResponse() function,
        when accessing a view via url args.
        """

        with self.subTest('Provide via standard reverse'):

            # Reverse, as args.
            response = self.assertResponse(
                # Standard url reverse, as the passed url.
                reverse(
                    'django_expanded_test_cases:redirect-with-args',
                    args=(1, 'As standard url reverse() args'),
                ),
                # Url we expect to end up at.
                expected_redirect_url=reverse(
                    'django_expanded_test_cases:template-response-with-args',
                    args=(1, 'As standard url reverse() args'),
                ),
                # Expected content on final page.
                expected_content=[
                    'id: "1"',
                    'name: "As standard url reverse() args"',
                ],
            )

            # Provided values.
            self.assertText(
                '/redirect/with_args/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.provided.url,
            )
            self.assertEqual(tuple(), response.url_data.provided.args)
            self.assertEqual({}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText(
                '/redirect/with_args/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.computed.initial_url,
            )
            self.assertText(
                '127.0.0.1/redirect/with_args/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText(
                '/template-response/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.computed.final_url,
            )
            self.assertText(
                '127.0.0.1/template-response/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.computed.full_final_url,
            )
            self.assertText(
                '/template-response/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.computed.redirect_url,
            )
            self.assertText(
                '127.0.0.1/template-response/1/As%20standard%20url%20reverse()%20args/',
                response.url_data.computed.full_redirect_url,
            )

            # Reverse, as kwargs.
            response = self.assertResponse(
                # Standard url reverse, as the passed url.
                reverse(
                    'django_expanded_test_cases:redirect-with-args',
                    kwargs={
                        'id': 2,
                        'name': 'As standard url reverse() kwargs',
                    },
                ),
                # Url we expect to end up at.
                expected_redirect_url=reverse(
                    'django_expanded_test_cases:template-response-with-args',
                    kwargs={
                        'id': 2,
                        'name': 'As standard url reverse() kwargs',
                    },
                ),
                # Expected content on final page.
                expected_content=[
                    'id: "2"',
                    'name: "As standard url reverse() kwargs"',
                ],
            )

            # Provided values.
            self.assertText(
                '/redirect/with_args/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.provided.url,
            )
            self.assertEqual(tuple(), response.url_data.provided.args)
            self.assertEqual({}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText(
                '/redirect/with_args/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.computed.initial_url,
            )
            self.assertText(
                '127.0.0.1/redirect/with_args/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText(
                '/template-response/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.computed.final_url,
            )
            self.assertText(
                '127.0.0.1/template-response/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.computed.full_final_url,
            )
            self.assertText(
                '/template-response/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.computed.redirect_url,
            )
            self.assertText(
                '127.0.0.1/template-response/2/As%20standard%20url%20reverse()%20kwargs/',
                response.url_data.computed.full_redirect_url,
            )

        with self.subTest('Provide via individually passed values'):
            # As of version 0.8, args/kwargs should no longer be considered for url parameters.
            # Ensure redirects to 404 instead, as technically no args/kwawrgs are provided for url generation.

            expected_warn_msg = (
                "Supplemental args/kwargs have been provided to an assertResponse statement. "
                "Any supplemental args/kwargs are exclusively used to provide custom data to "
                "built-in hook functions, but no hook functions seem to be implemented for your project. "
                "Either remove the use of args/kwargs in the assertion, or implement one of the hook functions."
            )

            # As args.
            with warns(Warning) as warning_msgs:
                response = self.assertResponse(
                    # Desired url, as standard reverse string.
                    'django_expanded_test_cases:redirect-with-args',
                    # Individual args to use for url.
                    3,
                    'As passed args',
                    # Expect to fail to find page.
                    expected_status=404,
                    # Expected content on final page.
                    expected_content=[
                        '<title>Not Found</title>',
                        '<h1>Not Found</h1>',
                        '<p>The requested resource was not found on this server.</p>',
                    ],
                )
            self.assertText(expected_warn_msg, warning_msgs[0].message.args[0])

            # Provided values.
            self.assertText('django_expanded_test_cases:redirect-with-args', response.url_data.provided.url)
            self.assertEqual(tuple(), response.url_data.provided.args)
            self.assertEqual({}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText('/django_expanded_test_cases:redirect-with-args/', response.url_data.computed.initial_url)
            self.assertText(
                '127.0.0.1/django_expanded_test_cases:redirect-with-args/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/django_expanded_test_cases:redirect-with-args/', response.url_data.computed.final_url)
            self.assertText(
                '127.0.0.1/django_expanded_test_cases:redirect-with-args/',
                response.url_data.computed.full_final_url,
            )
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # As kwargs.
            with warns(Warning) as warning_msgs:
                response = self.assertResponse(
                    # Desired url, as standard reverse string.
                    'django_expanded_test_cases:redirect-with-args',
                    # Individual args to use for url.
                    id=6,
                    name='As individually passed kwargs',
                    # Expect to fail to find page.
                    expected_status=404,
                    # Expected content on final page.
                    expected_content=[
                        '<title>Not Found</title>',
                        '<h1>Not Found</h1>',
                        '<p>The requested resource was not found on this server.</p>',
                    ],
                )
            self.assertText(expected_warn_msg, warning_msgs[0].message.args[0])

            # Provided values.
            self.assertText('django_expanded_test_cases:redirect-with-args', response.url_data.provided.url)
            self.assertEqual(tuple(), response.url_data.provided.args)
            self.assertEqual({}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText('/django_expanded_test_cases:redirect-with-args/', response.url_data.computed.initial_url)
            self.assertText(
                '127.0.0.1/django_expanded_test_cases:redirect-with-args/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/django_expanded_test_cases:redirect-with-args/', response.url_data.computed.final_url)
            self.assertText(
                '127.0.0.1/django_expanded_test_cases:redirect-with-args/',
                response.url_data.computed.full_final_url,
            )
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('Provide via args keyword'):

            response = self.assertResponse(
                # Desired url, as standard reverse string.
                'django_expanded_test_cases:redirect-with-args',
                # Url we expect to end up at.
                expected_redirect_url='django_expanded_test_cases:template-response-with-args',
                # Args for url.
                args=[4, 'As url_args'],
                redirect_args=(4, 'As url_args'),
                # Expected content on final page.
                expected_content=[
                    'id: "4"',
                    'name: "As url_args"',
                ],
            )

            # Provided values.
            self.assertText('django_expanded_test_cases:redirect-with-args', response.url_data.provided.url)
            self.assertEqual((4, 'As url_args'), response.url_data.provided.args)
            self.assertEqual({}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText('/redirect/with_args/4/As%20url_args/', response.url_data.computed.initial_url)
            self.assertText(
                '127.0.0.1/redirect/with_args/4/As%20url_args/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/template-response/4/As%20url_args/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/template-response/4/As%20url_args/', response.url_data.computed.full_final_url)
            self.assertText('/template-response/4/As%20url_args/', response.url_data.computed.redirect_url)
            self.assertText(
                '127.0.0.1/template-response/4/As%20url_args/',
                response.url_data.computed.full_redirect_url,
            )

        with self.subTest('Provide via kwargs keyword'):

            response = self.assertResponse(
                # Desired url, as standard reverse string.
                'django_expanded_test_cases:redirect-with-args',
                # Url we expect to end up at.
                expected_redirect_url='django_expanded_test_cases:template-response-with-args',
                # Args for url.
                kwargs={'id': 5, 'name': 'As url_kwargs'},
                redirect_kwargs={'id': 5, 'name': 'As url_kwargs'},
                # Expected content on final page.
                expected_content=[
                    'id: "5"',
                    'name: "As url_kwargs"',
                ],
            )

            # Provided values.
            self.assertText('django_expanded_test_cases:redirect-with-args', response.url_data.provided.url)
            self.assertEqual(tuple(), response.url_data.provided.args)
            self.assertEqual({'id': 5, 'name': 'As url_kwargs'}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText('/redirect/with_args/5/As%20url_kwargs/', response.url_data.computed.initial_url)
            self.assertText(
                '127.0.0.1/redirect/with_args/5/As%20url_kwargs/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/template-response/5/As%20url_kwargs/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/template-response/5/As%20url_kwargs/', response.url_data.computed.full_final_url)
            self.assertText('/template-response/5/As%20url_kwargs/', response.url_data.computed.redirect_url)
            self.assertText(
                '127.0.0.1/template-response/5/As%20url_kwargs/',
                response.url_data.computed.full_redirect_url,
            )

        with self.subTest('Provide via url_args keyword'):

            response = self.assertResponse(
                # Desired url, as standard reverse string.
                'django_expanded_test_cases:redirect-with-args',
                # Url we expect to end up at.
                expected_redirect_url='django_expanded_test_cases:template-response-with-args',
                # Args for url.
                url_args=[6, 'As url_args'],
                redirect_args=(6, 'As url_args'),
                # Expected content on final page.
                expected_content=[
                    'id: "6"',
                    'name: "As url_args"',
                ],
            )

            # Provided values.
            self.assertText('django_expanded_test_cases:redirect-with-args', response.url_data.provided.url)
            self.assertEqual((6, 'As url_args'), response.url_data.provided.args)
            self.assertEqual({}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText('/redirect/with_args/6/As%20url_args/', response.url_data.computed.initial_url)
            self.assertText(
                '127.0.0.1/redirect/with_args/6/As%20url_args/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/template-response/6/As%20url_args/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/template-response/6/As%20url_args/', response.url_data.computed.full_final_url)
            self.assertText('/template-response/6/As%20url_args/', response.url_data.computed.redirect_url)
            self.assertText(
                '127.0.0.1/template-response/6/As%20url_args/',
                response.url_data.computed.full_redirect_url,
            )

        with self.subTest('Provide via url_kwargs keyword'):

            response = self.assertResponse(
                # Desired url, as standard reverse string.
                'django_expanded_test_cases:redirect-with-args',
                # Url we expect to end up at.
                expected_redirect_url='django_expanded_test_cases:template-response-with-args',
                # Args for url.
                url_kwargs={'id': 7, 'name': 'As url_kwargs'},
                redirect_kwargs={'id': 7, 'name': 'As url_kwargs'},
                # Expected content on final page.
                expected_content=[
                    'id: "7"',
                    'name: "As url_kwargs"',
                ],
            )

            # Provided values.
            self.assertText('django_expanded_test_cases:redirect-with-args', response.url_data.provided.url)
            self.assertEqual(tuple(), response.url_data.provided.args)
            self.assertEqual({'id': 7, 'name': 'As url_kwargs'}, response.url_data.provided.kwargs)
            self.assertEqual({}, response.url_data.provided.query_params)

            # Computed values.
            self.assertText('/redirect/with_args/7/As%20url_kwargs/', response.url_data.computed.initial_url)
            self.assertText(
                '127.0.0.1/redirect/with_args/7/As%20url_kwargs/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/template-response/7/As%20url_kwargs/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/template-response/7/As%20url_kwargs/', response.url_data.computed.full_final_url)
            self.assertText('/template-response/7/As%20url_kwargs/', response.url_data.computed.redirect_url)
            self.assertText(
                '127.0.0.1/template-response/7/As%20url_kwargs/',
                response.url_data.computed.full_redirect_url,
            )

    @override_settings(APPEND_SLASH=True)
    def test__assertResponse__url_trailing_slash__with_append_slash_true(self):

        with self.subTest('Verify Patch Settings'):
            """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

            # Verify actual project settings values.
            self.assertTrue(getattr(settings, "APPEND_SLASH"))

        with self.subTest('Url provided as reverse, has trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home/',
            )

        with self.subTest('Url provided as reverse, no trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                self.assertResponse(
                    'django_expanded_test_cases:home-no-trailing-slash',
                    expected_status=200,
                    expected_title='Home Page | Test Views',
                    expected_header='Home Page Header',
                    expected_url='/home-no-slash',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to True, '
                'but url reverse did not resolve with trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider appending a url slash. '
                'Url was: /home-no-slash'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])

        with self.subTest('Url provided as literal url, has trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                '/home/',
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home/',
            )

        with self.subTest('Url provided as literal url, no trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                self.assertResponse(
                    '/home-no-slash',
                    expected_status=404,
                    expected_title='Not Found',
                    expected_header='Not Found',
                    expected_url='/home-no-slash/',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to True, '
                'but provided url does not contain a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider appending a url slash. '
                'Url was: /home-no-slash'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])

        with self.subTest('Url provided as literal url with GET params, has trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                '/home/',
                url_query_params={'testing': True},
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home/?testing=True',
            )

        with self.subTest('Url provided as literal url with GET params, no trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertResponse(
                    '/home-no-slash',
                    url_query_params={'testing': True},
                    expected_status=404,
                    expected_title='Not Found',
                    expected_header='Not Found',
                    expected_url='/home-no-slash/?testing=True',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to True, '
                'but provided url does not contain a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider appending a url slash. '
                'Url was: /home-no-slash'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])
            self.assertText('/home-no-slash/?testing=True', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home-no-slash/?testing=True', response.url_data.computed.full_final_url)

        with self.subTest('Url provided as literal full url (127.0.0.1), has trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                '127.0.0.1/home/',
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home/',
            )

        with self.subTest('Url provided as literal full url (127.0.0.1), no trailing slash'):

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                self.assertResponse(
                    '127.0.0.1/home-no-slash',
                    expected_status=404,
                    expected_title='Not Found',
                    expected_header='Not Found',
                    expected_url='/home-no-slash/',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to True, '
                'but provided url does not contain a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider appending a url slash. '
                'Url was: 127.0.0.1/home-no-slash'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])

    @override_settings(APPEND_SLASH=False)
    def test__assertResponse__url_trailing_slash__with_append_slash_false(self):

        with self.subTest('Verify Patch Settings'):
            """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

            # Verify actual project settings values.
            self.assertFalse(getattr(settings, "APPEND_SLASH"))

        with self.subTest('Url provided as reverse, has trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                self.assertResponse(
                    'django_expanded_test_cases:home',
                    expected_status=200,
                    expected_title='Home Page | Test Views',
                    expected_header='Home Page Header',
                    expected_url='/home/',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to False, '
                'but url reverse resolved with a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider removing the trailing url slash. '
                'Url was: /home/'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])

        with self.subTest('Url provided as reverse, no trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                'django_expanded_test_cases:home-no-trailing-slash',
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home-no-slash',
            )

        with self.subTest('Url provided as literal url, has trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                self.assertResponse(
                    '/home/',
                    expected_status=404,
                    expected_title='Not Found',
                    expected_header='Not Found',
                    expected_url='/home',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to False, '
                'but provided url contained a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider removing the trailing url slash. '
                'Url was: /home/'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])

        with self.subTest('Url provided as literal url, no trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                '/home-no-slash',
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home-no-slash',
            )

        with self.subTest('Url provided as literal url with GET params, has trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertResponse(
                    '/home/',
                    url_query_params={'testing': True},
                    expected_status=404,
                    expected_title='Not Found',
                    expected_header='Not Found',
                    expected_url='/home?testing=True',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to False, '
                'but provided url contained a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider removing the trailing url slash. '
                'Url was: /home/'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])
            self.assertText('/home?testing=True', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home?testing=True', response.url_data.computed.full_final_url)

        with self.subTest('Url provided as literal url with GET params, no trailing slash'):

            # Verify we get the expected page.
            self.assertResponse(
                '/home-no-slash',
                url_query_params={'testing': True},
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home-no-slash?testing=True',
            )

        with self.subTest('Url provided as literal full url (127.0.0.1), has trailing slash'):

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                self.assertResponse(
                    '127.0.0.1/home/',
                    expected_status=404,
                    expected_title='Not Found',
                    expected_header='Not Found',
                    expected_url='/home',
                )

            # Define expected warnings that should have occurred.
            expected_warns = (
                'Django setting APPEND_SLASH is set to False, '
                'but provided url contained a trailing slash. '
                'This may cause UnitTests with ETC to fail. '
                'Consider removing the trailing url slash. '
                'Url was: 127.0.0.1/home/'
            )

            # Assert warnings match.
            self.assertText(expected_warns, warning_info[0].message.args[0])

        with self.subTest('Url provided as literal full url (127.0.0.1), no trailing slash'):

            #  Verify we get the expected page.
            self.assertResponse(
                '127.0.0.1/home-no-slash',
                expected_status=200,
                expected_title='Home Page | Test Views',
                expected_header='Home Page Header',
                expected_url='/home-no-slash',
            )

    def test__assertResponse__status_code(self):
        """
        Tests "status_code" functionality of assertResponse() function.
        """
        exception_msg = '{0} != {1} : Expected status code (after potential redirects) of "{1}". Actual code was "{0}".'

        expected_warn_msg = (
            'Django setting APPEND_SLASH is set to True, '
            'but provided url does not contain a trailing slash. '
            'This may cause UnitTests with ETC to fail. '
            'Consider appending a url slash. '
            'Url was: {0}'
        )

        with self.subTest('With status_code=200 - Basic view'):
            # Test 200 in direct url.
            response = self.assertResponse('')
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url.
            response = self.assertResponse('django_expanded_test_cases:index')
            self.assertEqual(response.status_code, 200)

            # With non-200 code provided.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_status=400)
            self.assertText(exception_msg.format(200, 400), str(err.exception))

        with self.subTest('With status_code=200 - View with params'):
            # Test 200 in direct url.
            response = self.assertResponse('user/detail/1/')
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url, via args.
            response = self.assertResponse('django_expanded_test_cases:user-detail', args=(2,))
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url, via kwargs.
            response = self.assertResponse('django_expanded_test_cases:user-detail', kwargs={'pk': 3})
            self.assertEqual(response.status_code, 200)

            # With non-200 code provided.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('user/detail/1/', expected_status=500)
            self.assertText(exception_msg.format(200, 500), str(err.exception))

        with self.subTest('With status_code=404'):
            # Test 404 in direct url.
            with warns(Warning) as warning_info:
                response = self.assertResponse('bad_url', expected_status=404)
            self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via args.
            response = self.assertResponse(
                'django_expanded_test_cases:user-detail',
                args=(234,),
                expected_status=404,
            )
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via kwargs.
            response = self.assertResponse(
                'django_expanded_test_cases:user-detail',
                kwargs={'pk': 345},
                expected_status=404,
            )
            self.assertEqual(response.status_code, 404)

            # With non-404 code provided.
            with self.assertRaises(AssertionError) as err:
                with warns(Warning) as warning_info:
                    self.assertResponse('bad_url', expected_status=200)
            self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])
            self.assertText(exception_msg.format(404, 200), str(err.exception))

    def test__assertResponse__expected_url__success(self):
        """
        Tests `expected_url` and `expected_final_url` functionality of assertResponse() function,
        in cases where it should succeed.
        """

        expected_warn_msg = (
            'Django setting APPEND_SLASH is set to True, '
            'but provided url does not contain a trailing slash. '
            'This may cause UnitTests with ETC to fail. '
            'Consider appending a url slash. '
            'Url was: {0}'
        )

        with self.subTest('With no site_root_url value defined - Via literal value'):
            # Test 404 page url.
            with warns(Warning) as warning_info:
                response = self.assertResponse(
                    'bad_url',
                    expected_url='/bad_url/',
                    expected_final_url='/bad_url/',
                    expected_status=404,
                )
            self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])
            self.assertText('/bad_url/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                'bad_url/',
                expected_url='/bad_url/',
                expected_final_url='/bad_url/',
                expected_status=404,
            )
            self.assertText('/bad_url/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/bad_url/',
                expected_url='/bad_url/',
                expected_final_url='/bad_url/',
                expected_status=404,
            )
            self.assertText('/bad_url/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '///bad_url///',
                expected_url='/bad_url/',
                expected_final_url='/bad_url/',
                expected_status=404,
            )
            self.assertText('/bad_url/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_initial_url)
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "index" page url.
            response = self.assertResponse(
                '',
                expected_url='/',
                expected_final_url='/',
            )
            self.assertText('/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/',
                expected_url='/',
                expected_final_url='/',
            )
            self.assertText('/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/',
                expected_url='/',
                expected_final_url='/',
            )
            self.assertText('/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "home" page url.
            with warns(Warning) as warning_info:
                response = self.assertResponse(
                    'home',
                    expected_url='/home/',
                    expected_final_url='/home/',
                )
            self.assertText(expected_warn_msg.format('home'), warning_info[0].message.args[0])
            self.assertText('/home/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                'home/',
                expected_url='/home/',
                expected_final_url='/home/',
            )
            self.assertText('/home/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/home/',
                expected_url='/home/',
                expected_final_url='/home/',
            )
            self.assertText('/home/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/home/',
                expected_url='/home/',
                expected_final_url='/home/',
            )
            self.assertText('/home/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "login" page url.
            with warns(Warning) as warning_info:
                response = self.assertResponse(
                    'login',
                    expected_url='/login/',
                )
            self.assertText(expected_warn_msg.format('login'), warning_info[0].message.args[0])
            self.assertText('/login/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                'login/',
                expected_url='/login/',
                expected_final_url='/login/',
            )
            self.assertText('/login/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/login/',
                expected_url='/login/',
                expected_final_url='/login/',
            )
            self.assertText('/login/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/login/',
                expected_url='/login/',
                expected_final_url='/login/',
            )
            self.assertText('/login/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "one message" page url.
            response = self.assertResponse(
                'views/one-message/',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
            )
            self.assertText('/views/one-message/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/views/one-message/',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
            )
            self.assertText('/views/one-message/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/views/one-message/',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
            )
            self.assertText('/views/one-message/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "two messages" page url.
            response = self.assertResponse(
                'views/two-messages/',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
            )
            self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/views/two-messages/',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
            )
            self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/views/two-messages/',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
            )
            self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "three messages" page url.
            response = self.assertResponse(
                'views/three-messages/',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
            )
            self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/views/three-messages/',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
            )
            self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/views/three-messages/',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
            )
            self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "user detail" page url via args.
            response = self.assertResponse(
                'user/detail/1/',
                expected_url='/user/detail/1/',
                expected_final_url='/user/detail/1/',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/user/detail/1/',
                expected_url='/user/detail/1/',
                expected_final_url='/user/detail/1/',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/user/detail/1/',
                expected_url='/user/detail/1/',
                expected_final_url='/user/detail/1/',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_initial_url)
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "user detail" page url via kwargs.
            response = self.assertResponse(
                'user/detail/2/',
                expected_url='/user/detail/2/',
                expected_final_url='/user/detail/2/',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '/user/detail/2/',
                expected_url='/user/detail/2/',
                expected_final_url='/user/detail/2/',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)
            response = self.assertResponse(
                '127.0.0.1/user/detail/2/',
                expected_url='/user/detail/2/',
                expected_final_url='/user/detail/2/',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_initial_url)
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With no site_root_url value defined - Via reverse()'):
            # Test "index" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:index',
                expected_url='/',
                expected_final_url='/',
            )
            self.assertText('/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_initial_url)
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "home" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:home',
                expected_final_url='/home/',
            )
            self.assertText('/home/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_initial_url)
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "login" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:login',
                expected_final_url='/login/',
            )
            self.assertText('/login/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_initial_url)
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "one message" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:response-with-one-message',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
            )
            self.assertText('/views/one-message/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_initial_url)
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "two messages" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:response-with-two-messages',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
            )
            self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "three messages" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
            )
            self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_initial_url)
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With custom site_root_url value defined'):
            self.site_root_url = 'https://my_really_cool_site.com/'

            # Test "index" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:index',
                expected_url='/',
                expected_final_url='/',
            )
            self.assertText('/', response.url_data.computed.initial_url)
            self.assertText('https://my_really_cool_site.com/', response.url_data.computed.full_initial_url)
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('https://my_really_cool_site.com/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "home" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:home',
                expected_url='/home/',
                expected_final_url='/home/',
            )
            self.assertText('/home/', response.url_data.computed.initial_url)
            self.assertText('https://my_really_cool_site.com/home/', response.url_data.computed.full_initial_url)
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('https://my_really_cool_site.com/home/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "login" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:login',
                expected_url='/login/',
                expected_final_url='/login/',
            )
            self.assertText('/login/', response.url_data.computed.initial_url)
            self.assertText('https://my_really_cool_site.com/login/', response.url_data.computed.full_initial_url)
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('https://my_really_cool_site.com/login/', response.url_data.computed.full_final_url)
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "one message" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:response-with-one-message',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
            )
            self.assertText('/views/one-message/', response.url_data.computed.initial_url)
            self.assertText(
                'https://my_really_cool_site.com/views/one-message/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText(
                'https://my_really_cool_site.com/views/one-message/',
                response.url_data.computed.full_final_url,
            )
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "two messages" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:response-with-two-messages',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
            )
            self.assertText('/views/two-messages/', response.url_data.computed.initial_url)
            self.assertText(
                'https://my_really_cool_site.com/views/two-messages/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText(
                'https://my_really_cool_site.com/views/two-messages/',
                response.url_data.computed.full_final_url,
            )
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

            # Test "three messages" page url.
            response = self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
            )
            self.assertText('/views/three-messages/', response.url_data.computed.initial_url)
            self.assertText(
                'https://my_really_cool_site.com/views/three-messages/',
                response.url_data.computed.full_initial_url,
            )
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText(
                'https://my_really_cool_site.com/views/three-messages/',
                response.url_data.computed.full_final_url,
            )
            self.assertIsNone(response.url_data.computed.redirect_url)
            self.assertIsNone(response.url_data.computed.full_redirect_url)

        with self.subTest('With view that redirects'):
            # Using direct url.
            self.assertResponse(
                'redirect/index/',
                expected_url='/redirect/index/',
            )
            self.assertResponse(
                'redirect/index/',
                expected_url='/redirect/index/',
                expected_redirect_url='/',
                expected_final_url='/',
            )
            self.assertResponse(
                'redirect/index/',
                expected_url='/redirect/index/',
                expected_redirect_url='django_expanded_test_cases:index',
                expected_final_url=reverse('django_expanded_test_cases:index'),
            )

            # Using reverse.
            self.assertResponse(
                'django_expanded_test_cases:redirect-to-index',
                expected_url='/redirect/index/',
            )
            self.assertResponse(
                'django_expanded_test_cases:redirect-to-index',
                expected_url='/redirect/index/',
                expected_redirect_url='/',
                expected_final_url='/',
            )
            self.assertResponse(
                'django_expanded_test_cases:redirect-to-index',
                expected_url='/redirect/index/',
                expected_redirect_url='django_expanded_test_cases:index',
                expected_final_url=reverse('django_expanded_test_cases:index'),
            )

        with self.subTest('Verify error on urls that don\'t match'):
            expected_err_msg = (
                # Comment to prevent "black" formatting.
                'Expected Url and actual Url do not match. \n'
                'Expected Url: \n'
                '"{0}" \n'
                'Actual Url: \n'
                '"{1}" \n'
            )
            wrong_url = '/wrong_url/'

            # Test 404 page url.
            with self.assertRaises(AssertionError) as err:
                with warns(Warning) as warning_info:
                    self.assertResponse(
                        'bad_url',
                        expected_url=wrong_url,
                        expected_final_url=wrong_url,
                        expected_status=404,
                    )
            self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])
            self.assertEqual(expected_err_msg.format(wrong_url, '/bad_url/'), str(err.exception))

            # Test "index" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/'), str(err.exception))

            # Test "home" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'home/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/home/'), str(err.exception))

            # Test "login" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'login/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/login/'), str(err.exception))

            # Test "one message" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/one-message/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/views/one-message/'), str(err.exception))

            # Test "two messages" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/two-messages/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/views/two-messages/'), str(err.exception))

            # Test "three messages" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/three-messages/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/views/three-messages/'), str(err.exception))

            # Test "user detail" page url via args.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'user/detail/1/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/user/detail/1/'), str(err.exception))

            # Test "user detail" page url via kwargs.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'user/detail/2/',
                    expected_url=wrong_url,
                    expected_final_url=wrong_url,
                )
            self.assertEqual(expected_err_msg.format(wrong_url, '/user/detail/2/'), str(err.exception))

    def test__assertResponse__expected_url__failure(self):
        """
        Tests `expected_url` and `expected_final_url` functionality of assertResponse() function,
        in cases where it should fail.
        """

        expected_url_err_msg = (
            # Comment to prevent "black" formatting.
            'Expected Url and actual Url do not match. \n'
            'Expected Url: \n'
            '"{0}" \n'
            'Actual Url: \n'
            '"{1}" \n'
        )
        expected_final_url_err_msg = (
            # Comment to prevent "black" formatting.
            'Expected final_url and actual final_url do not match. \n'
            'Expected final_url: \n'
            '"{0}" \n'
            'Actual final_url: \n'
            '"{1}" \n'
        )

        with self.subTest('Test "index" page url'):

            # Fails on expected_url test.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '/',
                    expected_url='/views/1/',
                    expected_final_url='/',
                )
            self.assertEqual(
                expected_url_err_msg.format('/views/1/', '/'),
                str(err.exception),
            )

            # Fails on expected_final_url test.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '/',
                    expected_url='/',
                    expected_final_url='/views/2/',
                )
            self.assertEqual(
                expected_final_url_err_msg.format('/views/2/', '/'),
                str(err.exception),
            )

        with self.subTest('Test "home" page url'):

            # Fails on expected_url test.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '/home/',
                    expected_url='/views/1/',
                    expected_final_url='/home/',
                )
            self.assertEqual(
                expected_url_err_msg.format('/views/1/', '/home/'),
                str(err.exception),
            )

            # Fails on expected_final_url test.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    '/home/',
                    expected_url='/home/',
                    expected_final_url='/views/2/',
                )
            self.assertEqual(
                expected_final_url_err_msg.format('/views/2/', '/home/'),
                str(err.exception),
            )

        with self.subTest('Test "one message" page url'):

            # Fails on expected_url test.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/one-message/',
                    expected_url='/views/1/',
                    expected_final_url='/views/one-message/',
                )
            self.assertEqual(
                expected_url_err_msg.format('/views/1/', '/views/one-message/'),
                str(err.exception),
            )

            # Fails on expected_final_url test.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/one-message/',
                    expected_url='/views/one-message/',
                    expected_final_url='/views/2/',
                )
            self.assertEqual(
                expected_final_url_err_msg.format('/views/2/', '/views/one-message/'),
                str(err.exception),
            )

    def test__assertResponse__view_should_redirect__success(self):
        """
        Tests "expected_url" functionality of assertResponse() function, with assertions that should succeed.
        """

        expected_warn_msg = (
            'Django setting APPEND_SLASH is set to True, '
            'but provided url does not contain a trailing slash. '
            'This may cause UnitTests with ETC to fail. '
            'Consider appending a url slash. '
            'Url was: {0}'
        )

        with self.subTest('With view that doesn\'t redirect'):

            # Test 404 page url.
            with warns(Warning) as warning_info:
                response = self.assertResponse(
                    'bad_url',
                    expected_url='/bad_url/',
                    expected_final_url='/bad_url/',
                    expected_status=404,
                    view_should_redirect=False,
                )
            self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                'bad_url/',
                expected_url='/bad_url/',
                expected_final_url='/bad_url/',
                expected_status=404,
                view_should_redirect=False,
            )
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/bad_url/',
                expected_url='/bad_url/',
                expected_final_url='/bad_url/',
                expected_status=404,
                view_should_redirect=False,
            )
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '///bad_url///',
                expected_url='/bad_url/',
                expected_final_url='/bad_url/',
                expected_status=404,
                view_should_redirect=False,
            )
            self.assertText('/bad_url/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/bad_url/', response.url_data.computed.full_final_url)

            # Test "index" page url.
            response = self.assertResponse(
                '',
                expected_url='/',
                expected_final_url='/',
                view_should_redirect=False,
            )
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/',
                expected_url='/',
                expected_final_url='/',
                view_should_redirect=False,
            )
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/',
                expected_url='/',
                expected_final_url='/',
                view_should_redirect=False,
            )
            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)

            # Test "home" page url.
            response = self.assertResponse(
                'home/',
                expected_url='/home/',
                expected_final_url='/home/',
                view_should_redirect=False,
            )
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/home/',
                expected_url='/home/',
                expected_final_url='/home/',
                view_should_redirect=False,
            )
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/home/',
                expected_url='/home/',
                expected_final_url='/home/',
                view_should_redirect=False,
            )
            self.assertText('/home/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/home/', response.url_data.computed.full_final_url)

            # Test "login" page url.
            response = self.assertResponse(
                'login/',
                expected_url='/login/',
                expected_final_url='/login/',
                view_should_redirect=False,
            )
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/login/',
                expected_url='/login/',
                expected_final_url='/login/',
                view_should_redirect=False,
            )
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/login/',
                expected_url='/login/',
                expected_final_url='/login/',
                view_should_redirect=False,
            )
            self.assertText('/login/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/login/', response.url_data.computed.full_final_url)

            # Test "one message" page url.
            response = self.assertResponse(
                'views/one-message/',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
                view_should_redirect=False,
            )
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/views/one-message/',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
                view_should_redirect=False,
            )
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/views/one-message/',
                expected_url='/views/one-message/',
                expected_final_url='/views/one-message/',
                view_should_redirect=False,
            )
            self.assertText('/views/one-message/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/one-message/', response.url_data.computed.full_final_url)

            # Test "two messages" page url.
            response = self.assertResponse(
                'views/two-messages/',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
                view_should_redirect=False,
            )
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/views/two-messages/',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
                view_should_redirect=False,
            )
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/views/two-messages/',
                expected_url='/views/two-messages/',
                expected_final_url='/views/two-messages/',
                view_should_redirect=False,
            )
            self.assertText('/views/two-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/two-messages/', response.url_data.computed.full_final_url)

            # Test "three messages" page url.
            response = self.assertResponse(
                'views/three-messages/',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
                view_should_redirect=False,
            )
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/views/three-messages/',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
                view_should_redirect=False,
            )
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/views/three-messages/',
                expected_url='/views/three-messages/',
                expected_final_url='/views/three-messages/',
                view_should_redirect=False,
            )
            self.assertText('/views/three-messages/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/views/three-messages/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via args.
            response = self.assertResponse(
                'user/detail/1/',
                expected_url='/user/detail/1/',
                expected_final_url='/user/detail/1/',
                view_should_redirect=False,
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/user/detail/1/',
                expected_url='/user/detail/1/',
                expected_final_url='/user/detail/1/',
                view_should_redirect=False,
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/user/detail/1/',
                expected_url='/user/detail/1/',
                expected_final_url='/user/detail/1/',
                view_should_redirect=False,
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertResponse(
                'user/detail/2/',
                expected_url='/user/detail/2/',
                expected_final_url='/user/detail/2/',
                view_should_redirect=False,
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '/user/detail/2/',
                expected_url='/user/detail/2/',
                expected_final_url='/user/detail/2/',
                view_should_redirect=False,
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)
            response = self.assertResponse(
                '127.0.0.1/user/detail/2/',
                expected_url='/user/detail/2/',
                expected_final_url='/user/detail/2/',
                view_should_redirect=False,
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

        with self.subTest('With view that redirects'):
            # Using direct url.
            self.assertResponse(
                'redirect/index/',
                expected_url='/redirect/index/',
                expected_redirect_url='/',
                expected_final_url='/',
                view_should_redirect=True,
            )
            self.assertResponse(
                'redirect/index/',
                expected_url='/redirect/index/',
                expected_redirect_url='django_expanded_test_cases:index',
                expected_final_url=reverse('django_expanded_test_cases:index'),
                view_should_redirect=True,
            )

            # Using reverse.
            self.assertResponse(
                'django_expanded_test_cases:redirect-to-index',
                expected_url='/redirect/index/',
                expected_redirect_url='/',
                expected_final_url='/',
                view_should_redirect=True,
            )
            self.assertResponse(
                'django_expanded_test_cases:redirect-to-index',
                expected_url='/redirect/index/',
                expected_redirect_url='django_expanded_test_cases:index',
                expected_final_url=reverse('django_expanded_test_cases:index'),
                view_should_redirect=True,
            )

    def test__assertResponse__view_should_redirect__failure(self):
        """
        Tests "expected_url" functionality of assertResponse() function, with assertions that should fail.
        """

        expected_warn_msg = (
            'Django setting APPEND_SLASH is set to True, '
            'but provided url does not contain a trailing slash. '
            'This may cause UnitTests with ETC to fail. '
            'Consider appending a url slash. '
            'Url was: {0}'
        )

        with self.subTest('With view that doesn\'t redirect'):

            # Test 404 page url.
            with self.assertRaises(AssertionError) as err:
                with warns(Warning) as warning_info:
                    self.assertResponse(
                        'bad_url',
                        expected_url='/bad_url/',
                        expected_status=404,
                        view_should_redirect=True,
                    )
            self.assertText(expected_warn_msg.format('bad_url'), warning_info[0].message.args[0])
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

            # Test "index" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('', expected_url='/', view_should_redirect=True)
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

            # Test "home" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('home/', expected_url='/home/', view_should_redirect=True)
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

            # Test "login" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('login/', expected_url='/login/', view_should_redirect=True)
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

            # Test "one message" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/one-message/',
                    expected_url='/views/one-message/',
                    view_should_redirect=True,
                )
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

            # Test "three messages" page url.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'views/three-messages/',
                    expected_url='/views/three-messages/',
                    view_should_redirect=True,
                )
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

            # Test "user detail" page url via kwargs.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'user/detail/2/',
                    expected_url='/user/detail/2/',
                    view_should_redirect=True,
                )
            self.assertEqual(str(err.exception), 'Expected a page redirect, but response did not redirect.')

        with self.subTest('With view that redirects'):

            with self.subTest('Fails using direct url'):
                with self.assertRaises(AssertionError) as err:
                    self.assertResponse(
                        '/redirect/index/',
                        expected_url='/redirect/index/',
                        expected_redirect_url='/',
                        view_should_redirect=False,
                    )
                self.assertEqual(
                    'Expected no page redirects, but response processed one or more redirects.',
                    str(err.exception),
                )

            with self.subTest('Fails using reverse'):
                with self.assertRaises(AssertionError) as err:
                    self.assertResponse(
                        'django_expanded_test_cases:redirect-to-index',
                        expected_url=reverse('django_expanded_test_cases:redirect-to-index'),
                        expected_redirect_url='django_expanded_test_cases:index',
                        view_should_redirect=False,
                    )
                self.assertEqual(
                    'Expected no page redirects, but response processed one or more redirects.',
                    str(err.exception),
                )

            with self.subTest('Fails due to wrong redirect url provided'):
                with self.assertRaises(AssertionError) as err:
                    self.assertResponse(
                        'django_expanded_test_cases:redirect-to-one-message',
                        expected_url=reverse('django_expanded_test_cases:redirect-to-one-message'),
                        expected_redirect_url='django_expanded_test_cases:response-with-basic-form',
                        expected_message='Redirecting to one-message view.',
                        view_should_redirect=True,
                    )
                self.assertEqual(
                    (
                        # Comment to prevent "black" formatting.
                        'Response expected_redirect_url didn\'t match. '
                        'Expected url was "{0}". Actual url was "{1}".'
                    ).format(
                        reverse('django_expanded_test_cases:response-with-basic-form'),
                        reverse('django_expanded_test_cases:response-with-one-message'),
                    ),
                    str(err.exception),
                )

            with self.subTest('Verify generic redirect check happens first'):
                with self.assertRaises(AssertionError) as err:
                    self.assertResponse(
                        'django_expanded_test_cases:redirect-to-one-message',
                        expected_url=reverse('django_expanded_test_cases:redirect-to-one-message'),
                        expected_redirect_url='django_expanded_test_cases:response-with-basic-form',
                        view_should_redirect=False,
                    )
                self.assertEqual(
                    'Expected no page redirects, but response processed one or more redirects.',
                    str(err.exception),
                )

    def test__assertResponse__expected_title(self):
        """
        Tests "expected_title" functionality of assertResponse() function.
        """
        exception_msg = (
            'Expected title HTML contents of "Wrong Title" (using exact matching). '
            'Actual value was "Home Page | Test Views".'
        )

        with self.subTest('Title match'):
            self.assertResponse('django_expanded_test_cases:home', expected_title='Home Page | Test Views')

        with self.subTest('Title mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:home', expected_title='Wrong Title')
            self.assertText(exception_msg, str(err.exception))

    def test__assertResponse__expected_header(self):
        """
        Tests "expected_header" functionality of assertResponse() function.
        """
        exception_msg = 'Expected H1 header HTML contents of "Wrong Header". Actual value was "Home Page Header".'

        with self.subTest('Header match'):
            self.assertResponse('django_expanded_test_cases:home', expected_header='Home Page Header')

        with self.subTest('Header mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:home', expected_header='Wrong Header')
            self.assertText(exception_msg, str(err.exception))

    def test__assertResponse__expected_messages(self):
        """
        Tests "expected_messages" functionality of assertResponse() function.
        """
        exception_msg = 'Failed to find message "{0}" in context (using {1} matching).'

        with self.subTest('No messages on page - match'):
            self.assertResponse('django_expanded_test_cases:index', expected_messages='')
            self.assertResponse('django_expanded_test_cases:index', expected_messages=[''])

        with self.subTest('No messages on page - mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_messages='Wrong message.')
            self.assertText(exception_msg.format('Wrong message.', 'exact'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_messages=['Wrong message.'])
            self.assertText(exception_msg.format('Wrong message.', 'exact'), str(err.exception))

        with self.subTest('Multiple messages on page - match'):
            self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_messages='Test info message.',
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_messages=['Test warning message.'],
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_messages=[
                    'Test info message.',
                    'Test warning message.',
                ],
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_messages=[
                    'Test info message.',
                    'Test warning message.',
                    'Test error message.',
                ],
            )

        with self.subTest('Multiple messages on page - mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:response-with-three-messages',
                    expected_messages='Wrong message.',
                )
            self.assertText(exception_msg.format('Wrong message.', 'exact'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:response-with-three-messages',
                    expected_messages=[
                        'Test info message.',
                        'Wrong message.',
                    ],
                )
            self.assertText(exception_msg.format('Wrong message.', 'exact'), str(err.exception))

    def test__assertResponse__expected_not_messages(self):
        """
        Tests "expected_not_messages" functionality of assertResponse() function.
        """
        exception_msg = 'Expected to not find message. Found message "{0}" in context (using {1} matching).'

        with self.subTest('No messages on page - match'):
            self.assertResponse('django_expanded_test_cases:index', expected_not_messages='')
            self.assertResponse('django_expanded_test_cases:index', expected_not_messages=[''])

        with self.subTest('No messages on page - mismatch'):
            self.assertResponse('django_expanded_test_cases:index', expected_not_messages='Wrong message.')
            self.assertResponse('django_expanded_test_cases:index', expected_not_messages=['Wrong message.'])

        with self.subTest('Multiple messages on page - match'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:response-with-three-messages',
                    expected_not_messages='Test info message.',
                )
            self.assertText(exception_msg.format('Test info message.', 'exact'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:response-with-three-messages',
                    expected_not_messages=['Test warning message.'],
                )
            self.assertText(exception_msg.format('Test warning message.', 'exact'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:response-with-three-messages',
                    expected_not_messages=[
                        'Test info message.',
                        'Test warning message.',
                    ],
                )
            self.assertText(exception_msg.format('Test info message.', 'exact'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:response-with-three-messages',
                    expected_not_messages=[
                        'Test info message.',
                        'Test warning message.',
                        'Test error message.',
                    ],
                )
            self.assertText(exception_msg.format('Test info message.', 'exact'), str(err.exception))

        with self.subTest('Multiple messages on page - mismatch'):
            self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_not_messages='Wrong message.',
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-three-messages',
                expected_not_messages=[
                    'Testing here.',
                    'Wrong message.',
                ],
            )

    def test__assertResponse__expected_content(self):
        """
        Tests "expected_content" functionality of assertResponse() function.
        """
        exception_msg = 'Could not find expected content value in response. Provided value was:\n{0}'

        with self.subTest('Content match - With tags'):
            # With non-repeating values.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    '<title>Home Page | Test Views</title>',
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is',
                    'the project landing page.</p>',
                ],
            )

            # With repeated values.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    '<title>Home Page | Test Views</title>',
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is',
                    'is the project',
                    'the project landing page.</p>',
                ],
                ignore_content_ordering=True,  # Ignore because we recheck the same values.
            )

        with self.subTest('Content match - Without tags'):
            # With non-repeating values.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    'Home Page | Test Views',
                    'Home Page Header',
                    'Pretend this is',
                    'the project landing page.',
                ],
            )

            # With repeated values.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    'Home Page | Test Views',
                    'Home Page Header',
                    'Pretend this is',
                    'is the project',
                    'the project landing page.',
                ],
                ignore_content_ordering=True,  # Ignore because we recheck the same values.
            )

        with self.subTest('Content mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:home', expected_content='Wrong value')
            self.assertText(exception_msg.format('Wrong value'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:home',
                    expected_content=[
                        'Home Page Header',
                        'Pretend this is',
                        'Wrong value',
                    ],
                )
            self.assertTextStartsWith(exception_msg.format('Wrong value'), str(err.exception))

        with self.subTest('With search subsections'):
            # Strip start.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content='<p>Pretend this is the project landing page.</p>',
                content_starts_after='<h1>Home Page Header</h1>',
            )
            # Strip end.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content='<title>Home Page | Test Views</title>',
                content_ends_before='<h1>Home Page Header</h1>',
            )
            # Strip both.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content='<h1>Home Page Header</h1>',
                content_starts_after='<title>Home Page | Test Views</title>',
                content_ends_before='<p>Pretend this is the project landing page.</p>',
            )

        with self.subTest('With content blocks'):
            # Entire page as one block.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content="""
                <head>
                    <meta charset="utf-8">
                    <title>Home Page | Test Views</title>
                </head>
                <body>
                    <h1>Home Page Header</h1>
                    <p>Pretend this is the project landing page.</p>
                </body>
                """,
            )
            # Header and body each a block.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    """
                    <head>
                        <meta charset="utf-8">
                        <title>Home Page | Test Views</title>
                    </head>
                    """,
                    """
                    <body>
                        <h1>Home Page Header</h1>
                        <p>Pretend this is the project landing page.</p>
                    </body>
                    """,
                ],
            )
            # With start stripped.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    """
                    <body>
                        <h1>Home Page Header</h1>
                        <p>Pretend this is the project landing page.</p>
                    </body>
                    """,
                ],
                content_starts_after='</head>',
            )
            # With end stripped.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    """
                    <head>
                        <meta charset="utf-8">
                        <title>Home Page | Test Views</title>
                    </head>
                    """,
                ],
                content_ends_before='<body>',
            )
            # With both stripped.
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_content=[
                    """
                    <title>Home Page | Test Views</title>
                    </head>
                    <body>
                    <h1>Home Page Header</h1>
                    """,
                ],
                content_starts_after='<meta charset="utf-8">',
                content_ends_before='<p>Pretend this is the project landing page.</p>',
            )

    def test__assertPageContent__expected_content__repeating_elements(self):
        with self.subTest('Sanity check, making sure each individual content section is found from full response'):
            self.assertResponse(
                'django_expanded_test_cases:response-with-repeating-elements',
                expected_content=['<p>Test First Unique Line</p>'],
                content_starts_after='<p>Repeating Line</p>',
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-repeating-elements',
                expected_content=['<p>Test Second Unique Line</p>'],
                content_starts_after='<p>Repeating Line</p>',
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-repeating-elements',
                expected_content=['<p>Test Third Unique Line</p>'],
                content_starts_after='<p>Repeating Line</p>',
            )
            self.assertResponse(
                'django_expanded_test_cases:response-with-repeating-elements',
                expected_content=['<p>Repeating Line</p>'],
            )

        with self.subTest('Check all values together'):
            self.assertResponse(
                'django_expanded_test_cases:response-with-repeating-elements',
                expected_content=[
                    '<p>Repeating Line</p>',
                    '<p>Test First Unique Line</p>',
                    '<p>Repeating Line</p>',
                    '<p>Test Second Unique Line</p>',
                    '<p>Repeating Line</p>',
                    '<p>Test Third Unique Line</p>',
                    '<p>Repeating Line</p>',
                ],
            )

    def test__assertResponse__expected_not_content(self):
        """
        Tests "expected_not_content" functionality of assertResponse() function.
        """
        exception_msg = 'Found content in response. Expected content to not be present. Content was:\n{0}'

        self.assertResponse(
            'django_expanded_test_cases:home',
            expected_not_content=[
                '<title>HomePage | Test Views</title>',
                '<h1>Home PageHeader</h1>',
                '<p>Pretend is',
                'the project page.</p>',
            ],
        )

        with self.assertRaises(AssertionError) as err:
            self.assertResponse(
                'django_expanded_test_cases:home',
                expected_not_content=[
                    '<title>Home Page | Test Views</title>',
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is',
                    'the project landing page.</p>',
                ],
            )
        self.assertText(exception_msg.format('<title>Home Page | Test Views</title>'), str(err.exception))

    def test__assertGetResponse(self):
        """Tests assertGetResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """

        with self.subTest('Basic response test.'):
            response = self.assertGetResponse('django_expanded_test_cases:index')

            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)

        with self.subTest('View with params, provided as standard args/kwargs'):
            # Test "user detail" page url via args.
            response = self.assertGetResponse(
                'django_expanded_test_cases:user-detail',
                args=(1,),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_superuser"</p></li>',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertGetResponse(
                'django_expanded_test_cases:user-detail',
                kwargs={'pk': 2},
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_admin"</p></li>',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

        with self.subTest('View with params, provided as url_args/url_kwargs'):
            # Test "user detail" page url via args.
            response = self.assertGetResponse(
                'django_expanded_test_cases:user-detail',
                url_args=(1,),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_superuser"</p></li>',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertGetResponse(
                'django_expanded_test_cases:user-detail',
                url_kwargs={'pk': 2},
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_admin"</p></li>',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

        with self.subTest('View with params, provided as reverse()'):
            # Test "user detail" page url via args.
            response = self.assertGetResponse(
                reverse('django_expanded_test_cases:user-detail', args=(1,)),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_superuser"</p></li>',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertGetResponse(
                reverse('django_expanded_test_cases:user-detail', kwargs={'pk': 2}),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_admin"</p></li>',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

    def test__assertPostResponse(self):
        """Tests assertPostResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """

        with self.subTest('Basic response test.'):
            response = self.assertPostResponse('django_expanded_test_cases:index')

            self.assertText('/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)

        with self.subTest('View with params, provided as standard args/kwargs'):
            # Test "user detail" page url via args.
            response = self.assertPostResponse(
                'django_expanded_test_cases:user-detail',
                args=(1,),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_superuser"</p></li>',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertPostResponse(
                'django_expanded_test_cases:user-detail',
                kwargs={'pk': 2},
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_admin"</p></li>',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

        with self.subTest('View with params, provided as url_args/url_kwargs'):
            # Test "user detail" page url via args.
            response = self.assertPostResponse(
                'django_expanded_test_cases:user-detail',
                url_args=(1,),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_superuser"</p></li>',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertPostResponse(
                'django_expanded_test_cases:user-detail',
                url_kwargs={'pk': 2},
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_admin"</p></li>',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

        with self.subTest('View with params, provided as reverse()'):
            # Test "user detail" page url via args.
            response = self.assertPostResponse(
                reverse('django_expanded_test_cases:user-detail', args=(1,)),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_superuser"</p></li>',
            )
            self.assertText('/user/detail/1/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/1/', response.url_data.computed.full_final_url)

            # Test "user detail" page url via kwargs.
            response = self.assertPostResponse(
                reverse('django_expanded_test_cases:user-detail', kwargs={'pk': 2}),
                expected_title='User Detail Page | Test Views',
                expected_header='User Detail Page Header',
                expected_content='<li><p>Username: "test_admin"</p></li>',
            )
            self.assertText('/user/detail/2/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/user/detail/2/', response.url_data.computed.full_final_url)

    def test__assertJsonResponse(self):
        """Tests assertJsonResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """

        self.maxDiff = None

        with self.subTest('Basic response test'):
            response = self.assertJsonResponse('django_expanded_test_cases:json-response-basic-dict')

            self.assertText('/json/basic-dict/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/json/basic-dict/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)
            self.assertText(
                (
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list": ['
                    '"Sublist Item 1", '
                    '"Sublist Item 2", '
                    '"Sublist Item 3"'
                    '], '
                    '"request_headers": {'
                    '"Cookie": "", '
                    '"Content-Type": "application/json", '
                    '"Accept": "application/json"'
                    '}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
                response.content.decode('utf-8'),
            )
            self.assertEqual(
                {
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
                    'none_type': None,
                    'int_type': 5,
                },
                response.json_content,
            )

        with self.subTest('Verify Content-Type header can override.'):
            response = self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                headers={'Content-Type': "text/testing"},
            )

            self.assertText('/json/basic-dict/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/json/basic-dict/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)
            self.assertText(
                (
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list": ['
                    '"Sublist Item 1", '
                    '"Sublist Item 2", '
                    '"Sublist Item 3"'
                    '], '
                    '"request_headers": {'
                    '"Cookie": "", '
                    '"Content-Type": "text/testing", '
                    '"Accept": "application/json"'
                    '}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
                response.content.decode('utf-8'),
            )
            self.assertEqual(
                {
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Content-Type": "text/testing",
                        "Accept": "application/json",
                    },
                    'none_type': None,
                    'int_type': 5,
                },
                response.json_content,
            )

        with self.subTest('Verify Accept header can override'):
            response = self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                headers={'Accept': 'text/testing'},
            )

            self.assertText('/json/basic-dict/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/json/basic-dict/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)
            self.assertText(
                (
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list": ['
                    '"Sublist Item 1", '
                    '"Sublist Item 2", '
                    '"Sublist Item 3"'
                    '], '
                    '"request_headers": {'
                    '"Cookie": "", '
                    '"Accept": "text/testing", '
                    '"Content-Type": "application/json"'
                    '}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
                response.content.decode('utf-8'),
            )
            self.assertEqual(
                {
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Accept": "text/testing",
                        "Content-Type": "application/json",
                    },
                    'none_type': None,
                    'int_type': 5,
                },
                response.json_content,
            )

        with self.subTest('Verify can add additional headers'):
            response = self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                headers={"Test Header": "Testing!"},
            )

            self.assertText('/json/basic-dict/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/json/basic-dict/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)
            self.assertText(
                (
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list": ['
                    '"Sublist Item 1", '
                    '"Sublist Item 2", '
                    '"Sublist Item 3"'
                    '], '
                    '"request_headers": {'
                    '"Cookie": "", '
                    '"Test Header": "Testing!", '
                    '"Content-Type": "application/json", '
                    '"Accept": "application/json"'
                    '}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
                response.content.decode('utf-8'),
            )
            self.assertEqual(
                {
                    "success": "This is a test Json response.",
                    "test_list": [
                        "Sublist Item 1",
                        "Sublist Item 2",
                        "Sublist Item 3",
                    ],
                    "request_headers": {
                        "Cookie": "",
                        "Test Header": "Testing!",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    'none_type': None,
                    'int_type': 5,
                },
                response.json_content,
            )

        with self.subTest('Verify changing return_format does not error and removes json_content variable'):
            response = self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                return_format='html',
            )

            self.assertText('/json/basic-dict/', response.url_data.computed.final_url)
            self.assertText('127.0.0.1/json/basic-dict/', response.url_data.computed.full_final_url)
            self.assertEqual(response.status_code, 200)
            self.assertText(
                (
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list": ['
                    '"Sublist Item 1", '
                    '"Sublist Item 2", '
                    '"Sublist Item 3"'
                    '], '
                    '"request_headers": {'
                    '"Cookie": "", '
                    '"Content-Type": "application/json", '
                    '"Accept": "application/json"'
                    '}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
                response.content.decode('utf-8'),
            )
            self.assertFalse(hasattr(response, 'json_content'))

        with self.subTest('Verify setting bad return_format causes error'):

            with self.assertRaises(ValueError) as err:
                response = self.assertJsonResponse(
                    'django_expanded_test_cases:json-response-basic-dict',
                    return_format='unsupported',
                )
            self.assertText(
                'Invalid return_format arg. Currently supported return_format values are `html` or `json`.',
                str(err.exception),
            )

        with self.subTest('Basic response test, merged into one assertion'):
            self.assertJsonResponse(
                'django_expanded_test_cases:json-response-basic-dict',
                expected_url='/json/basic-dict/',
                expected_content=(
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list": ['
                    '"Sublist Item 1", '
                    '"Sublist Item 2", '
                    '"Sublist Item 3"'
                    '], '
                    '"request_headers": {'
                    '"Cookie": "", '
                    '"Content-Type": "application/json", '
                    '"Accept": "application/json"'
                    '}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
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
                    'none_type': None,
                    'int_type': 5,
                },
            )

        with self.subTest('Basic response test, merged into one assertion - Content fails when wrong'):
            with self.assertRaises(AssertionError) as err:
                response = self.assertJsonResponse(
                    'django_expanded_test_cases:json-response-basic-dict',
                    expected_url='/json/basic-dict/',
                    expected_content=(
                        '{'
                        '"success": "This is a test Json response.", '
                        '"test_list": ['
                        '"Sublist Item 1", '
                        '"Sublist Item 2", '
                        '"Sublist Item 3"'
                        '], '
                        '"request_headers": {'
                        '"Cookie": "", '
                        '"Content-Type": "text/html", '
                        '"Accept": "text/html"'
                        '}, '
                        '"none_type": null, '
                        '"int_type": 5'
                        '}'
                    ),
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
                        'none_type': None,
                        'int_type': 5,
                    },
                )
            self.assertText(
                (
                    'Could not find expected content value in response. Provided value was:\n'
                    '{'
                    '"success": "This is a test Json response.", '
                    '"test_list":["Sublist Item 1", "Sublist Item 2", "Sublist Item 3"], '
                    '"request_headers":{"Cookie": "", "Content-Type": "text/html", "Accept": "text/html"}, '
                    '"none_type": null, '
                    '"int_type": 5'
                    '}'
                ),
                str(err.exception),
            )

        with self.subTest('Basic response test, merged into one assertion - Json fails when wrong'):
            with self.assertRaises(AssertionError) as err:
                self.assertJsonResponse(
                    'django_expanded_test_cases:json-response-basic-dict',
                    expected_url='/json/basic-dict/',
                    expected_content=(
                        '{'
                        '"success": "This is a test Json response.", '
                        '"test_list": ['
                        '"Sublist Item 1", '
                        '"Sublist Item 2", '
                        '"Sublist Item 3"'
                        '], '
                        '"request_headers": {'
                        '"Cookie": "", '
                        '"Content-Type": "application/json", '
                        '"Accept": "application/json"'
                        '}, '
                        '"none_type": null, '
                        '"int_type": 5'
                        '}'
                    ),
                    expected_json={
                        "success": "This is a test Json response.",
                        "test_list": [
                            "Sublist Item 1",
                            "Sublist Item 2",
                            "Sublist Item 3",
                        ],
                        "request_headers": {
                            "Cookie": "",
                            "Content-Type": "text/html",
                            "Accept": "text/html",
                        },
                        'none_type': None,
                        'int_type': 5,
                    },
                )
            self.assertText(
                (
                    'Could not find expected json value in response. Provided value was:\n'
                    "{"
                    "'success': 'This is a test Json response.', "
                    "'test_list': ['Sublist Item 1', 'Sublist Item 2', 'Sublist Item 3'], "
                    "'request_headers': {'Cookie': '', 'Content-Type': 'text/html', 'Accept': 'text/html'}, "
                    "'none_type': None, "
                    "'int_type': 5"
                    "}"
                ),
                str(err.exception),
            )

        with self.subTest('Basic response test, raises error if expected_json is provided but return_type is not json'):
            with self.assertRaises(ValueError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:json-response-basic-dict',
                    expected_url='/json/basic-dict/',
                    expected_content=(
                        '{'
                        '"success": "This is a test Json response.", '
                        '"test_list": ['
                        '"Sublist Item 1", '
                        '"Sublist Item 2", '
                        '"Sublist Item 3"'
                        '], '
                        '"request_headers": {'
                        '"Cookie": "", '
                        '"Content-Type": "application/json", '
                        '"Accept": "application/json"'
                        '}, '
                        '"none_type": null, '
                        '"int_type": 5'
                        '}'
                    ),
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
                        'none_type': None,
                        'int_type': 5,
                    },
                )
            self.assertText(
                (
                    'Assertion was not expecting a JSON return object, yet expected_json arg was provided. '
                    'Either provide a return_format arg of `json`, or consider using the assertJsonResponse assertion.'
                ),
                str(err.exception),
            )

    # endregion Response Assertion Tests

    # region Element Assertion Tests

    def test__assertResponseRedirects__success(self):
        """
        Tests assertResponseRedirects() function, in cases when it should succeed.
        """
        with self.subTest('With view that redirects'):
            # Using direct url.
            self.assertRedirects(
                'redirect/index/',
                expected_redirect_url='/',
            )
            self.assertRedirects(
                'redirect/index/',
                expected_redirect_url='django_expanded_test_cases:index',
            )

            # Using reverse.
            self.assertRedirects(
                'django_expanded_test_cases:redirect-to-index',
                expected_redirect_url='/',
            )
            self.assertRedirects(
                'django_expanded_test_cases:redirect-to-index',
                expected_redirect_url='django_expanded_test_cases:index',
            )

    def test__assertResponseRedirects__failure(self):
        """
        Tests assertResponseRedirects() function, in cases when it should fail.
        """
        exception_msg__incorrect_code = (
            # Comment to prevent "black" formatting.
            'Response didn\'t redirect as expected. '
            'Response code was {0} (expected 302).'
        )
        exception_msg__incorrect_url = (
            # Comment to prevent "black" formatting.
            'Response expected_redirect_url didn\'t match. '
            'Expected url was "{0}". Actual url was "{1}".'
        )

        with self.subTest('With view that does not redirect - Invalid page'):

            request = self._get_page_response('bad_page/')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='/',
                )
            self.assertText(exception_msg__incorrect_code.format(request.status_code), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:invalid',
                )
            self.assertText(exception_msg__incorrect_code.format(request.status_code), str(err.exception))

        with self.subTest('With view that does not redirect - Index page'):

            request = self._get_page_response('')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='/',
                )
            self.assertText(exception_msg__incorrect_code.format(request.status_code), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:index',
                )
            self.assertText(exception_msg__incorrect_code.format(request.status_code), str(err.exception))

        with self.subTest('With view that does not redirect - Non-index page'):

            request = self._get_page_response('login/')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='/',
                )
            self.assertText(exception_msg__incorrect_code.format(request.status_code), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:login',
                )
            self.assertText(exception_msg__incorrect_code.format(request.status_code), str(err.exception))

        with self.subTest('With incorrect view'):

            # Redirect to "one message" view, but expecting redirect to other pages.
            request = self._get_page_response('django_expanded_test_cases:redirect-to-index')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:redirect-to-one-message',
                )
            self.assertText(
                exception_msg__incorrect_url.format(
                    reverse('django_expanded_test_cases:redirect-to-one-message'),
                    request.url_data.computed.redirect_url,
                ),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:redirect-to-basic-form',
                )
            self.assertText(
                exception_msg__incorrect_url.format(
                    reverse('django_expanded_test_cases:redirect-to-basic-form'),
                    request.url_data.computed.redirect_url,
                ),
                str(err.exception),
            )

            # Redirect to "basic form" view, but expecting redirect to other pages.
            request = self._get_page_response('django_expanded_test_cases:redirect-to-basic-form')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:redirect-to-index',
                )
            self.assertText(
                exception_msg__incorrect_url.format(
                    reverse('django_expanded_test_cases:redirect-to-index'),
                    request.url_data.computed.redirect_url,
                ),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(
                    request,
                    expected_redirect_url='django_expanded_test_cases:redirect-to-one-message',
                )
            self.assertText(
                exception_msg__incorrect_url.format(
                    reverse('django_expanded_test_cases:redirect-to-one-message'),
                    request.url_data.computed.redirect_url,
                ),
                str(err.exception),
            )

    def test__assertStatusCode__success(self):
        """
        Tests assertStatusCode() function, in cases when it should succeed.
        """
        with self.subTest('Status 200'):
            response = HttpResponse(status=200)
            self.assertStatusCode(response, 200)
            self.assertStatusCode(response.status_code, 200)

        with self.subTest('Status 400'):
            response = HttpResponse(status=400)
            self.assertStatusCode(response, 400)
            self.assertStatusCode(response.status_code, 400)

        with self.subTest('Status 403'):
            response = HttpResponse(status=403)
            self.assertStatusCode(response, 403)
            self.assertStatusCode(response.status_code, 403)

        with self.subTest('Status 404'):
            response = HttpResponse(status=404)
            self.assertStatusCode(response, 404)
            self.assertStatusCode(response.status_code, 404)

        with self.subTest('Status 500'):
            response = HttpResponse(status=500)
            self.assertStatusCode(response, 500)
            self.assertStatusCode(response.status_code, 500)

    def test__assertStatusCode__failure(self):
        """
        Tests assertStatusCode() function, in cases when it should fail.
        """
        exception_msg = '{0} != {1} : Expected status code (after potential redirects) of "{1}". Actual code was "{0}".'

        with self.subTest('Expected 200, got 404'):
            response = HttpResponse(status=404)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 200)
            self.assertText(exception_msg.format('404', '200'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 200)
            self.assertText(exception_msg.format('404', '200'), str(err.exception))

        with self.subTest('Expected 404, got 200'):
            response = HttpResponse(status=200)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 404)
            self.assertText(exception_msg.format('200', '404'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 404)
            self.assertText(exception_msg.format('200', '404'), str(err.exception))

        with self.subTest('Expected 200, got 500'):
            response = HttpResponse(status=500)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 200)
            self.assertText(exception_msg.format('500', '200'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 200)
            self.assertText(exception_msg.format('500', '200'), str(err.exception))

        with self.subTest('Expected 500, got 200'):
            response = HttpResponse(status=200)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 500)
            self.assertText(exception_msg.format('200', '500'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 500)
            self.assertText(exception_msg.format('200', '500'), str(err.exception))

    def test__assertPageTitle__success(self):
        """
        Tests assertPageTitle() function, in cases when it should succeed.
        """
        with self.subTest('Including title tag in expected'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, '<title>Test Title</title>')

        with self.subTest('Including title tag in expected, with extra whitespace around tag'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(
                response,
                '   <title>    Test Title    </title>   ',
            )

        with self.subTest('No title element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertPageTitle(response, '')

        with self.subTest('Title exists, but is empty'):
            response = HttpResponse('<title></title>')
            self.assertPageTitle(response, '')

        with self.subTest('Title exists, but is whitespace'):
            response = HttpResponse('<title>   </title>')
            self.assertPageTitle(response, '')

        with self.subTest('Basic title'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, 'Test Title')

        with self.subTest('Basic title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<title>   Test    Title   </title>')
            self.assertPageTitle(response, 'Test Title')

        with self.subTest('Complex title - Exact Match'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertPageTitle(
                response,
                'Test Title | My Custom App | My Really Cool Site',
                allow_partials=False,
            )

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating) - Exact Match'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertPageTitle(
                response,
                'Test Title | My Custom App | My Really Cool Site',
                allow_partials=False,
            )

        with self.subTest('Complex title - Loose Match'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertPageTitle(
                response,
                'Test Title',
                allow_partials=True,
            )
            self.assertPageTitle(
                response,
                'My Custom App',
                allow_partials=True,
            )
            self.assertPageTitle(
                response,
                'My Really Cool Site',
                allow_partials=True,
            )

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating) - Loose Match'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertPageTitle(
                response,
                'Test Title',
                allow_partials=True,
            )
            self.assertPageTitle(
                response,
                'My Custom App',
                allow_partials=True,
            )
            self.assertPageTitle(
                response,
                'My Really Cool Site',
                allow_partials=True,
            )

        with self.subTest('Title has non-standard values in base page'):
            # Test with "standard" values.
            response = HttpResponse('<title>This Title has Two Arrows => =></title>')
            self.assertPageTitle(response, 'This Title has Two Arrows => =>')

            # Test with "mixed" values.
            response = HttpResponse('<title>This Title has Two Arrows &equals;&gt; =></title>')
            self.assertPageTitle(response, 'This Title has Two Arrows => =>')

            # Test with "non-standard" values.
            response = HttpResponse('<title>This Title has Two Arrows &equals;&gt; &equals;&gt;</title>')
            self.assertPageTitle(response, 'This Title has Two Arrows => =>')

    def test__assertPageTitle__failure(self):
        """
        Tests assertPageTitle() function, in cases when it should fail.
        """
        exception_msg = 'Expected title HTML contents of "{0}" (using {2} matching). Actual value was "{1}".'

        with self.subTest('Checking for title when none exists'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertPageTitle(response, 'Test Title')
            self.assertText(
                exception_msg.format('Test Title', '', 'exact'),
                str(err.exception),
            )

        with self.subTest('Expected value is on page, but not in title tag'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Test Title')
            self.assertText(
                exception_msg.format('Test Title', '', 'exact'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><p>Test Title</p>')
                self.assertPageTitle(response, 'Test Title')
            self.assertText(
                exception_msg.format('Test Title', '', 'exact'),
                str(err.exception),
            )

        with self.subTest('Assuming extra whitespace is still present'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>   Test    Title   </title>')
                self.assertPageTitle(response, '   Test    Title   ')
            self.assertText(
                exception_msg.format('Test    Title', 'Test Title', 'exact'),
                str(err.exception),
            )

        with self.subTest('Set to exact match, but only passing in title subsection'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'Test Title')
            self.assertText(
                exception_msg.format(
                    'Test Title',
                    'Test Title | My Custom App | My Really Cool Site',
                    'exact',
                ),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'My Custom App')
            self.assertText(
                exception_msg.format(
                    'My Custom App',
                    'Test Title | My Custom App | My Really Cool Site',
                    'exact',
                ),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'My Really Cool Site')
            self.assertText(
                exception_msg.format(
                    'My Really Cool Site',
                    'Test Title | My Custom App | My Really Cool Site',
                    'exact',
                ),
                str(err.exception),
            )

        with self.subTest('Set to partial match, but value is not in title'):
            # Full mismatch.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Wrong Value', allow_partials=True)
            self.assertText(
                exception_msg.format('Wrong Value', '', 'partial'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title</title>')
                self.assertPageTitle(response, 'Wrong Value', allow_partials=True)
            self.assertText(
                exception_msg.format('Wrong Value', 'Test Title', 'partial'),
                str(err.exception),
            )

            # Partial match, but also has extra.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Test Title and More', allow_partials=True)
            self.assertText(
                exception_msg.format('Test Title and More', '', 'partial'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title</title>')
                self.assertPageTitle(response, 'Test Title and More', allow_partials=True)
            self.assertText(
                exception_msg.format('Test Title and More', 'Test Title', 'partial'),
                str(err.exception),
            )

        with self.subTest('Multiple Titles - Two and no spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Title 1</title><title>Title 2</title>')
                self.assertPageTitle(response, '')
            self.assertText(
                (
                    'Found multiple titles (2 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Titles - Two with spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title > Title 1 < /title><title > Title 2 < /title>')
                self.assertPageTitle(response, '')
            self.assertText(
                (
                    'Found multiple titles (2 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Titles - Two with line breaks'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Title 1</title>\n<br>\n<title>Title 2</title>')
                self.assertPageTitle(response, '')
            self.assertText(
                (
                    'Found multiple titles (2 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Titles - Three'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Title 1</title><title>Title 2</title><title>Title 3</title>')
                self.assertPageTitle(response, '')
            self.assertText(
                (
                    'Found multiple titles (3 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Titles - Many, assorted'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse(
                    """
                    <title>Testing</title
                    <title>Title 1< /title><title>Title 2</ title>

                    <br>

                    <title>Title 3</title><p>This is a test p tag.</p></title><title > Title 4 < /title><title>Title 5</title>
                    """
                )
                self.assertPageTitle(response, '')
            self.assertText(
                (
                    'Found multiple titles (5 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                ),
                str(err.exception),
            )

    def test__assertPageHeader__success(self):
        """
        Tests assertPageHeader() function, in cases when it should succeed.
        """
        with self.subTest('Including header tag in expected'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertPageHeader(response, '<h1>Test Header</h1>')

        with self.subTest('Including header tag in expected, with extra whitespace around tag'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertPageHeader(response, '   <h1>    Test Header    </h1>   ')

        with self.subTest('No header element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertPageHeader(response, '')

        with self.subTest('Header exists, but is empty'):
            response = HttpResponse('<h1></h1>')
            self.assertPageHeader(response, '')

        with self.subTest('Header exists, but is whitespace'):
            response = HttpResponse('<h1>   </h1>')
            self.assertPageHeader(response, '')

        with self.subTest('Basic header'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertPageHeader(response, 'Test Header')

        with self.subTest('Basic header, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<h1>   Test    Header   </h1>')
            self.assertPageHeader(response, 'Test Header')

    def test__assertPageHeader__failure(self):
        """
        Tests assertPageHeader() function, in cases when it should fail.
        """
        exception_msg = 'Expected H1 header HTML contents of "{0}". Actual value was "{1}".'

        with self.subTest('Checking for header when none exists'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertPageHeader(response, 'Test Header')
            self.assertText(
                exception_msg.format('Test Header', ''),
                str(err.exception),
            )

        with self.subTest('Expected value is on page, but not in header tag'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Header')
                self.assertPageHeader(response, 'Test Header')
            self.assertText(
                exception_msg.format('Test Header', ''),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h2>Test Header</h2><p>Test Header</p>')
                self.assertPageHeader(response, 'Test Header')
            self.assertText(
                exception_msg.format('Test Header', ''),
                str(err.exception),
            )

        with self.subTest('Assuming extra whitespace is still present'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>   Test    Header   </h1>')
                self.assertPageHeader(response, '   Test    Header   ')
            self.assertText(
                exception_msg.format('Test    Header', 'Test Header'),
                str(err.exception),
            )

        with self.subTest('Expected value is present, plus extra'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Header</h1>')
                self.assertPageHeader(response, 'Test Header plus Extra')
            self.assertText(
                exception_msg.format('Test Header plus Extra', 'Test Header'),
                str(err.exception),
            )

        with self.subTest('Multiple Headers - Two and no spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Header 1</h1><h1>Header 2</h1>')
                self.assertPageHeader(response, '')
            self.assertText(
                (
                    'Found multiple headers (2 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Headers - Two with spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1 > Header 1 < /h1><h1 > Header 2 < /h1>')
                self.assertPageHeader(response, '')
            self.assertText(
                (
                    'Found multiple headers (2 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Headers - Two with line breaks'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Header 1</h1>\n<br>\n<h1>Header 2</h1>')
                self.assertPageHeader(response, '')
            self.assertText(
                (
                    'Found multiple headers (2 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Headers - Three'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Header 1</h1><h1>Header 2</h1><h1>Header 3</h1>')
                self.assertPageHeader(response, '')
            self.assertText(
                (
                    'Found multiple headers (3 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                ),
                str(err.exception),
            )

        with self.subTest('Multiple Headers - Many, assorted'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse(
                    """
                    <h1>Testing</h1
                    <h1>Header 1< /h1><h1>Header 2</ h1>

                    <br>

                    <h1>Header 3</h1><p>This is a test p tag.</p></h1><h1 > Header 4 < /h1><h1>Header 5</h1>
                    """
                )
                self.assertPageHeader(response, '')
            self.assertText(
                (
                    'Found multiple headers (5 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                ),
                str(err.exception),
            )

    def test__assertContextMessages__success__allow_partials__as_arg(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        We only do a minimal amount of testing for this function here.
        We assume a majority of testing will occur in the "disallow_partials" set.
        """

        with self.subTest('Check for single message partial, single message exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertContextMessages(
                response,
                'This is a test message.',
                allow_partials=True,
            )
            self.assertContextMessages(
                response,
                'is a test message',
                allow_partials=True,
            )
            self.assertContextMessages(
                response,
                'test',
                allow_partials=True,
            )

        with self.subTest('Check for three message partials, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(
                response,
                ['info', 'warning message.', 'Test error'],
                allow_partials=True,
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', True)
    def test__assertContextMessages__success__allow_partials__as_setting(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        We only do a minimal amount of testing for this function here.
        We assume a majority of testing will occur in the "disallow_partials" set.
        """

        with self.subTest('Check for single message partial, single message exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertContextMessages(response, 'This is a test message.')
            self.assertContextMessages(response, 'is a test message')
            self.assertContextMessages(response, 'test')

        with self.subTest('Check for three message partials, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(response, ['info', 'warning message', 'Test error'])

    def test__assertContextMessages__success__disallow_partials__as_arg(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        The majority of tests for this function exist here.
        """

        with self.subTest('Check for single message, single message exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertContextMessages(
                response,
                'This is a test message.',
                allow_partials=False,
            )

        with self.subTest('Check for single message, two messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertContextMessages(
                response,
                'Test message #1.',
                allow_partials=False,
            )
            self.assertContextMessages(
                response,
                'Test message #2.',
                allow_partials=False,
            )

        with self.subTest('Check for single message, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(
                response,
                'Test info message.',
                allow_partials=False,
            )
            self.assertContextMessages(
                response,
                'Test warning message.',
                allow_partials=False,
            )
            self.assertContextMessages(
                response,
                'Test error message.',
                allow_partials=False,
            )

        with self.subTest('Check for two messages, two messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertContextMessages(
                response,
                [
                    'Test message #1.',
                    'Test message #2.',
                ],
                allow_partials=False,
            )

        with self.subTest('Check for two messages, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(
                response,
                [
                    'Test info message.',
                    'Test warning message.',
                ],
                allow_partials=False,
            )
            self.assertContextMessages(
                response,
                [
                    'Test info message.',
                    'Test error message.',
                ],
                allow_partials=False,
            )
            self.assertContextMessages(
                response,
                [
                    'Test warning message.',
                    'Test error message.',
                ],
                allow_partials=False,
            )

        with self.subTest('Check for three messages, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(
                response,
                [
                    'Test info message.',
                    'Test warning message.',
                    'Test error message.',
                ],
                allow_partials=False,
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertContextMessages__success__disallow_partials__as_setting(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        The majority of tests for this function exist here.
        """

        with self.subTest('Check for single message, single message exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertContextMessages(response, 'This is a test message.')

        with self.subTest('Check for single message, two messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertContextMessages(response, 'Test message #1.')
            self.assertContextMessages(response, 'Test message #2.')

        with self.subTest('Check for single message, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(response, 'Test info message.')
            self.assertContextMessages(response, 'Test warning message.')
            self.assertContextMessages(response, 'Test error message.')

        with self.subTest('Check for two messages, two messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertContextMessages(response, ['Test message #1.', 'Test message #2.'])

        with self.subTest('Check for two messages, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(response, ['Test info message.', 'Test warning message.'])
            self.assertContextMessages(response, ['Test info message.', 'Test error message.'])
            self.assertContextMessages(response, ['Test warning message.', 'Test error message.'])

        with self.subTest('Check for three messages, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertContextMessages(response, ['Test info message.', 'Test warning message.', 'Test error message.'])

    def test__assertContextMessages__failure__allow_partials__as_arg(self):
        """Tests assertContextMessages() function, in cases when it should fail."""

        exception_msg = 'Failed to find message "{0}" in context (using {1} matching).'

        with self.subTest('Check for single message, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for single message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'This is a test message. And more.',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('This is a test message. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for single message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Test message #1. And more.',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Test message #1. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for single message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Test info message. And more.',
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Test info message. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple messages, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Testing here',
                        'Fake',
                        'Idk',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Testing here',
                        'Fake',
                        'Idk',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'This is a test message. And more.',
                        'More. This is a test message.',
                        'More. This is a test message. And more.',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('This is a test message. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Testing here',
                        'Fake',
                        'Idk',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Test message #1. And more.',
                        'More. Test message #2.',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Test message #1. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'This message',
                        'Fake',
                        'Idk',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('This message', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Test info message. And more.',
                        'More. Test warning message.',
                        'More. Test error message. And More',
                    ],
                    allow_partials=True,
                )

            self.assertText(
                exception_msg.format('Test info message. And more.', 'partial'),
                str(err.exception),
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', True)
    def test__assertContextMessages__failure__allow_partials__as_arg__as_setting(self):
        """Tests assertContextMessages() function, in cases when it should fail."""

        exception_msg = 'Failed to find message "{0}" in context (using {1} matching).'

        with self.subTest('Check for single message, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for single message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'This is a test message. And more.',
                )

            self.assertText(
                exception_msg.format('This is a test message. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for single message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Test message #1. And more.',
                )

            self.assertText(
                exception_msg.format('Test message #1. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for single message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Testing here',
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'Test info message. And more.',
                )

            self.assertText(
                exception_msg.format('Test info message. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple messages, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Testing here',
                        'Fake',
                        'Idk',
                    ],
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Testing here',
                        'Fake',
                        'Idk',
                    ],
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'This is a test message. And more.',
                        'More. This is a test message.',
                        'More. This is a test message. And more.',
                    ],
                )

            self.assertText(
                exception_msg.format('This is a test message. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Testing here',
                        'Fake',
                        'Idk',
                    ],
                )

            self.assertText(
                exception_msg.format('Testing here', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Test message #1. And more.',
                        'More. Test message #2.',
                    ],
                )

            self.assertText(
                exception_msg.format('Test message #1. And more.', 'partial'),
                str(err.exception),
            )

        with self.subTest('Check for multiple message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'This message',
                        'Fake',
                        'Idk',
                    ],
                )

            self.assertText(
                exception_msg.format('This message', 'partial'),
                str(err.exception),
            )

            # Extra in message.
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    [
                        'Test info message. And more.',
                        'More. Test warning message.',
                        'More. Test error message. And More',
                    ],
                )

            self.assertText(
                exception_msg.format('Test info message. And more.', 'partial'),
                str(err.exception),
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertContextMessages__failure__disallow_partials__as_setting(self):
        """Tests assertContextMessages() function, in cases when it should fail."""

        exception_msg = 'Failed to find message "{0}" in context (using {1} matching).'

        with self.subTest('Checking for single message, none exist'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:home')
                self.assertContextMessages(
                    response,
                    'This is a test message.',
                )
            self.assertText(
                exception_msg.format('This is a test message.', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for single message, but it\'s only a partial match'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'This is a test message',
                )
            self.assertText(
                exception_msg.format('This is a test message', 'exact'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'test message.',
                )
            self.assertText(
                exception_msg.format('test message.', 'exact'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    'test',
                )
            self.assertText(
                exception_msg.format('test', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for single message, one exists but doesn\'t match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertContextMessages(response, 'Testing!')
            self.assertText(
                exception_msg.format('Testing!', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for single message, multiple exist but don\'t match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response(
                    'django_expanded_test_cases:response-with-three-messages',
                )
                self.assertContextMessages(response, 'Testing!')
            self.assertText(
                exception_msg.format('Testing!', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for two messages, none exist'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:home')
                self.assertContextMessages(
                    response,
                    ['This is a test message.', 'Another message.'],
                )
            self.assertText(
                exception_msg.format('This is a test message.', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for two messages, but only one exists'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertContextMessages(
                    response,
                    ['This is a test message.', 'Another message.'],
                )
            self.assertText(
                exception_msg.format('Another message.', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for two messages, multiple exist but one doesn\'t match'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    ['Test info message.', 'Another message.'],
                )
            self.assertText(
                exception_msg.format('Another message.', 'exact'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(
                    response,
                    ['Bad message', 'Test info message.'],
                )
            self.assertText(
                exception_msg.format('Bad message', 'exact'),
                str(err.exception),
            )

        with self.subTest('Checking for two messages, multiple exist but none match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertContextMessages(
                    response,
                    ['Testing!', 'Testing again!'],
                )
            self.assertText(
                exception_msg.format('Testing!', 'exact'),
                str(err.exception),
            )

    def test__assertNotContextMessages__success__allow_partials__as_arg(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            self.assertNotContextMessages(
                response,
                'Testing here',
                allow_partials=True,
            )

        with self.subTest('Check for single message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                'Testing here',
                allow_partials=True,
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                'This is a test message. And more.',
                allow_partials=True,
            )

        with self.subTest('Check for single message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                'Testing here',
                allow_partials=True,
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                'Test message #1. And more.',
                allow_partials=True,
            )

        with self.subTest('Check for single message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                'Testing here',
                allow_partials=True,
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                'Test info message. And more.',
                allow_partials=True,
            )

        with self.subTest('Check for multiple messages, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            self.assertNotContextMessages(
                response,
                [
                    'Testing here',
                    'Fake',
                    'Idk',
                ],
                allow_partials=True,
            )

        with self.subTest('Check for multiple message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                [
                    'Testing here',
                    'Fake',
                    'Idk',
                ],
                allow_partials=True,
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                [
                    'This is a test message. And more.',
                    'More. This is a test message.',
                    'More. This is a test message. And more.',
                ],
                allow_partials=True,
            )

        with self.subTest('Check for multiple message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                [
                    'Testing here',
                    'Fake',
                    'Idk',
                ],
                allow_partials=True,
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                [
                    'Test message #1. And more.',
                    'More. Test message #2.',
                ],
                allow_partials=True,
            )

        with self.subTest('Check for multiple message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                [
                    'This message',
                    'Fake',
                    'Idk',
                ],
                allow_partials=True,
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                [
                    'Test info message. And more.',
                    'More. Test warning message.',
                    'More. Test error message. And More',
                ],
                allow_partials=True,
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', True)
    def test__assertNotContextMessages__success__allow_partials__as_setting(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            self.assertNotContextMessages(
                response,
                'Testing here',
            )

        with self.subTest('Check for single message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                'Testing here',
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                'This is a test message. And more.',
            )

        with self.subTest('Check for single message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                'Testing here',
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                'Test message #1. And more.',
            )

        with self.subTest('Check for single message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                'Testing here',
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                'Test info message. And more.',
            )

        with self.subTest('Check for multiple messages, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')

            self.assertNotContextMessages(
                response,
                [
                    'Testing here',
                    'Fake',
                    'Idk',
                ],
            )

        with self.subTest('Check for multiple message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                [
                    'Testing here',
                    'Fake',
                    'Idk',
                ],
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                [
                    'This is a test message. And more.',
                    'More. This is a test message.',
                    'More. This is a test message. And more.',
                ],
            )

        with self.subTest('Check for multiple message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                [
                    'Testing here',
                    'Fake',
                    'Idk',
                ],
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                [
                    'Test message #1. And more.',
                    'More. Test message #2.',
                ],
            )

        with self.subTest('Check for multiple message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')

            # Full message mismatch.
            self.assertNotContextMessages(
                response,
                [
                    'This message',
                    'Fake',
                    'Idk',
                ],
            )

            # Extra in message.
            self.assertNotContextMessages(
                response,
                [
                    'Test info message. And more.',
                    'More. Test warning message.',
                    'More. Test error message. And More',
                ],
            )

    def test__assertNotContextMessages__success__disallow_partials__as_arg(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
                allow_partials=False,
            )

        with self.subTest('Check for single message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
                allow_partials=False,
            )

        with self.subTest('Check for single message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
                allow_partials=False,
            )

        with self.subTest('Check for single message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
                allow_partials=False,
            )

        with self.subTest('Check for single message, but it\'s only a partial match'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertNotContextMessages(
                response,
                'This is a test',
                allow_partials=False,
            )

        with self.subTest('Check for multiple messages, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
                allow_partials=False,
            )

        with self.subTest('Check for multiple messages, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
                allow_partials=False,
            )

        with self.subTest('Check for multiple messages, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
                allow_partials=False,
            )

        with self.subTest('Check for multiple messages, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
                allow_partials=False,
            )

        with self.subTest('Check for multiple messages, but it\'s only a partial match'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertNotContextMessages(
                response,
                [
                    'Test info',
                    'warning message.',
                    'error',
                ],
                allow_partials=False,
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertNotContextMessages__success__disallow_partials__as_setting(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
            )

        with self.subTest('Check for single message, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
            )

        with self.subTest('Check for single message, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
            )

        with self.subTest('Check for single message, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertNotContextMessages(
                response,
                'This message should not exist.',
            )

        with self.subTest('Check for single message, but it\'s only a partial match'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertNotContextMessages(
                response,
                'This is a test',
            )

        with self.subTest('Check for multiple messages, no messages exist'):
            response = self._get_page_response('django_expanded_test_cases:home')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
            )

        with self.subTest('Check for multiple messages, one messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
            )

        with self.subTest('Check for multiple messages, two messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
            )

        with self.subTest('Check for multiple messages, three messages exist'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertNotContextMessages(
                response,
                [
                    'This message should not exist.',
                    'Fake message.',
                    'Idk bro',
                ],
            )

        with self.subTest('Check for multiple messages, but it\'s only a partial match'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
            self.assertNotContextMessages(
                response,
                [
                    'Test info',
                    'warning message.',
                    'error',
                ],
            )

    def test__assertNotContextMessages__failure__allow_partials__as_arg(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    'is a test',
                    allow_partials=True,
                )

        with self.subTest('Check for single message, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    'message #1.',
                    allow_partials=True,
                )

        with self.subTest('Check for single message, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    'warning message',
                    allow_partials=True,
                )

        with self.subTest('Check for multiple messages, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    ['is a test'],
                    allow_partials=True,
                )

        with self.subTest('Check for multiple messages, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'message #1.',
                        'message #2.',
                    ],
                    allow_partials=True,
                )

        with self.subTest('Check for multiple messages, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'Test info',
                        'warning message.',
                        'error',
                    ],
                    allow_partials=True,
                )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', True)
    def test__assertNotContextMessages__failure__allow_partials__as_setting(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    'is a test',
                )

        with self.subTest('Check for single message, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    'message #1.',
                )

        with self.subTest('Check for single message, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    'warning message',
                )

        with self.subTest('Check for multiple messages, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    ['is a test'],
                )

        with self.subTest('Check for multiple messages, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'message #1.',
                        'message #2.',
                    ],
                )

        with self.subTest('Check for multiple messages, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'Test info',
                        'warning message.',
                        'error',
                    ],
                )

    def test__assertNotContextMessages__failure__disallow_partials__as_arg(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    'This is a test message.',
                    allow_partials=False,
                )

        with self.subTest('Check for single message, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    'Test message #1.',
                    allow_partials=False,
                )

        with self.subTest('Check for single message, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    'Test warning message.',
                    allow_partials=False,
                )

        with self.subTest('Check for multiple messages, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    ['This is a test message.'],
                    allow_partials=False,
                )

        with self.subTest('Check for multiple messages, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'Test message #1.',
                        'Test message #2.',
                    ],
                    allow_partials=False,
                )

        with self.subTest('Check for multiple messages, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'Test info message.',
                        'Test warning message.',
                        'Test error message.',
                    ],
                    allow_partials=False,
                )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertNotContextMessages__failure__disallow_partials__as_setting(self):
        """Tests assertNotContextMessages() function, in cases when it should succeed."""

        with self.subTest('Check for single message, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    'This is a test message.',
                )

        with self.subTest('Check for single message, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    'Test message #1.',
                )

        with self.subTest('Check for single message, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    'Test warning message.',
                )

        with self.subTest('Check for multiple messages, single message exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
                self.assertNotContextMessages(
                    response,
                    ['This is a test message.'],
                )

        with self.subTest('Check for multiple messages, two messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'Test message #1.',
                        'Test message #2.',
                    ],
                )

        with self.subTest('Check for multiple messages, three messages exists'):

            with self.assertRaises(AssertionError):
                response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
                self.assertNotContextMessages(
                    response,
                    [
                        'Test info message.',
                        'Test warning message.',
                        'Test error message.',
                    ],
                )

    def test__assertPageContent__success(self):
        """Tests assertPageContent() function, in cases when it should succeed."""

        with self.subTest('Empty response, no value passed.'):
            response = HttpResponse('')
            self.assertPageContent(response, '')

        with self.subTest('Minimal Response, no value passed'):
            response = HttpResponse('<h1>Test Title</h1>')
            self.assertPageContent(response, '')

        with self.subTest('Minimal Response - No change'):
            response = HttpResponse('<h1>Test Title</h1>')
            self.assertPageContent(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Outer whitespace'):
            response = HttpResponse('&nbsp; <h1>Test Title</h1> &nbsp; ')
            self.assertPageContent(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            self.assertPageContent(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            self.assertPageContent(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - With Newlines'):
            response = HttpResponse('<h1>Test  \n  Title</h1>')
            self.assertPageContent(response, '<h1>Test Title</h1>')

        with self.subTest('Standard Response, no value passed'):
            response = self._get_page_response('django_expanded_test_cases:login')
            self.assertPageContent(response, '')

        with self.subTest('Standard Response - Login Page'):
            response = self._get_page_response('django_expanded_test_cases:login')
            self.assertPageContent(
                response,
                '<h1>Login Page Header</h1><p>Pretend this is a login page.</p>',
            )

        with self.subTest('Standard Response, missing part of value'):
            response = self._get_page_response('django_expanded_test_cases:login')
            self.assertPageContent(response, '<h1>Login Page Header</h1>')
            self.assertPageContent(response, '<p>Pretend this is a login page.</p>')

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('django_expanded_test_cases:home')
            self.assertPageContent(
                response,
                '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>',
            )

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('django_expanded_test_cases:template-response-home')
            self.assertPageContent(
                response,
                '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>',
            )

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            self.assertPageContent(
                response,
                (
                    '<ul><li><p>This is a test message.</p></li></ul>'
                    '<h1>View with One Message Header</h1>'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>'
                ),
            )

        with self.subTest('Standard Response - Set of items on home page'):
            response = self._get_page_response('django_expanded_test_cases:home')
            # Test as list.
            self.assertPageContent(
                response,
                [
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is the project landing page.</p>',
                    'Pretend this',
                    'project landing',
                ],
                ignore_ordering=True,  # Ignore because we recheck the same values.
            )
            # Test as tuple.
            self.assertPageContent(
                response,
                (
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is the project landing page.</p>',
                    'Pretend this',
                    'project landing',
                ),
                ignore_ordering=True,  # Ignore because we recheck the same values.
            )

        with self.subTest('Standard Response - Set of items on user page - As list'):
            response = self._get_page_response(
                'django_expanded_test_cases:user-detail',
                args=(1,),
                user=self.test_user,
            )

            # Standard, ordered page match.
            self.assertPageContent(
                response,
                [
                    '<h1>User Detail Page Header</h1>',
                    'Username: "test_superuser"',
                    'First Name: "SuperUserFirst"',
                    'Last Name: "SuperUserLast"',
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                ],
            )

            # With repeating values.
            self.assertPageContent(
                response,
                [
                    '<h1>User Detail Page Header</h1>',
                    'User Detail',
                    'Username: "test_superuser"',
                    'First Name: "SuperUserFirst"',
                    'Last Name: "SuperUserLast"',
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                ],
                ignore_ordering=True,  # Ignore because we recheck the same values.
            )

            # Standard page match but values are unordered.
            self.assertPageContent(
                response,
                [
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                    'Username: "test_superuser"',
                    'First Name: "SuperUserFirst"',
                    'Last Name: "SuperUserLast"',
                    '<h1>User Detail Page Header</h1>',
                ],
                ignore_ordering=True,  # Ignore because unordered.
            )

        with self.subTest('Standard Response - Set of items on user page - As Tuple'):
            response = self._get_page_response(
                'django_expanded_test_cases:user-detail',
                args=(1,),
                user=self.test_user,
            )

            # Standard, ordered page match.
            self.assertPageContent(
                response,
                (
                    '<h1>User Detail Page Header</h1>',
                    'Username: "test_superuser"',
                    'First Name: "SuperUserFirst"',
                    'Last Name: "SuperUserLast"',
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                ),
            )

            # With repeating values.
            self.assertPageContent(
                response,
                (
                    '<h1>User Detail Page Header</h1>',
                    'User Detail',
                    'Username: "test_superuser"',
                    'First Name: "SuperUserFirst"',
                    'Last Name: "SuperUserLast"',
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                ),
                ignore_ordering=True,  # Ignore because we recheck the same values.
            )

            # Standard page match but values are unordered.
            self.assertPageContent(
                response,
                (
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                    'Username: "test_superuser"',
                    'First Name: "SuperUserFirst"',
                    'Last Name: "SuperUserLast"',
                    '<h1>User Detail Page Header</h1>',
                ),
                ignore_ordering=True,  # Ignore because unordered.
            )

        with self.subTest('Standard Response - Checking repeated values on page'):
            """
            Ensures the str.split() logic does not entirely remove values from the 'actual' response search space, for
            later checks. Aka, if we check for an <hr> tag in output, it only removes the first one found, not every
            single one in the entire response output.

            This is important for repeated checks against similar/identical values, where the test is maybe testing
            more for value ordering and instance count, rather than just that the value exists at all.
            """
            response = self._get_page_response('django_expanded_test_cases:home')
            self.assertPageContent(
                response,
                [
                    'Home Page',
                    'body>',
                    'h1',
                    'Home Page Header</h1>',
                    '<p>',
                    'Pretend ',
                    'this',
                    'is the project landing page.</p>',
                    '<p>Pretend this',
                    'project landing',
                    '</p>',
                    '</body>',
                ],
                ignore_ordering=True,  # Ignore because we recheck the same values.
            )

    def test__assertPageContent__success_with_limited_search_space(self):
        with self.subTest('Standard Response - With "content_starts_after" defined'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value.
            self.assertPageContent(
                response,
                expected_content='<p>Pretend this is the project landing page.</p>',
                content_starts_after='<h1>Home Page Header</h1>',
            )

            # Expected as array.
            self.assertPageContent(
                response,
                expected_content=[
                    '<p>Pretend this is the project landing page.</p>',
                    '</body>',
                ],
                content_starts_after='<h1>Home Page Header</h1>',
            )

        with self.subTest('Standard Response - With multi-lined "content_starts_after" defined'):
            # Can be useful in cases such as where there is no directly-unique element in desired section.
            # But there are groupings of elements together that make a unique desired section to limit by.
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value.
            self.assertPageContent(
                response,
                expected_content='<p>Pretend this is the project landing page.</p>',
                content_starts_after='<h1>Home Page Header</h1>',
            )

            # Expected as array.
            self.assertPageContent(
                response,
                expected_content=[
                    """
                    <body>
                        <h1>Home Page Header</h1>
                        <p>Pretend this is the project landing page.</p>
                    </body>
                    """,
                ],
                content_starts_after="""
                <head>
                    <meta charset="utf-8">
                    <title>Home Page | Test Views</title>
                </head>
                """,
            )

        with self.subTest('Standard Response - With "content_ends_before" defined'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value.
            self.assertPageContent(
                response,
                expected_content='<meta charset="utf-8">',
                content_ends_before='<h1>Home Page Header</h1>',
            )

            # Expected as array.
            self.assertPageContent(
                response,
                expected_content=[
                    '<head>',
                    '<meta charset="utf-8">',
                    '<title>Home Page | Test Views</title>',
                    '</head>',
                    '<body>',
                ],
                content_ends_before='<h1>Home Page Header</h1>',
            )

        with self.subTest('Standard Response - With multi-lined "content_ends_before" defined'):
            # Can be useful in cases such as where there is no directly-unique element in desired section.
            # But there are groupings of elements together that make a unique desired section to limit by.
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value.
            self.assertPageContent(
                response,
                expected_content='<meta charset="utf-8">',
                content_ends_before='<h1>Home Page Header</h1>',
            )

            # Expected as array.
            self.assertPageContent(
                response,
                expected_content=[
                    """
                    <head>
                        <meta charset="utf-8">
                        <title>Home Page | Test Views</title>
                    </head>
                    """,
                ],
                content_ends_before="""
                <body>
                    <h1>Home Page Header</h1>
                    <p>Pretend this is the project landing page.</p>
                </body>
                """,
            )

        with self.subTest('Standard Response - With both content containers defined'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value.
            self.assertPageContent(
                response,
                expected_content='<h1>Home Page Header</h1>',
                content_starts_after='<title>Home Page | Test Views</title>',
                content_ends_before='<p>Pretend this is the project landing page.</p>',
            )

            # Expected as array.
            self.assertPageContent(
                response,
                expected_content=[
                    '</head>',
                    '<body>',
                    '<h1>Home Page Header</h1>',
                ],
                content_starts_after='<title>Home Page | Test Views</title>',
                content_ends_before='<p>Pretend this is the project landing page.</p>',
            )

    def test__assertPageContent__failure(self):
        """
        Tests assertPageContent() function, in cases when it should fail.
        """
        exception_msg_not_found = 'Could not find expected content value in response. Provided value was:\n{0}'
        exception_msg_bad_order = (
            'Expected content value was found, but ordering of values do not match. Problem value:\n{0}'
        )

        with self.subTest('Empty response, but value passed.'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg_not_found.format('<h1>Test Title</h1>'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Wrong value passed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>Testing</h1>')
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - With additional error info provided.'):
            # First verify as standard not-found in array.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(
                    response,
                    [
                        '<h1>Testing</h1>',
                    ],
                )
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>'),
                str(err.exception),
            )

            # Now actually verify same thing, but with extra error info (as list).
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(
                    response,
                    [
                        ['<h1>Testing</h1>', 'Extra error stuff here!'],
                    ],
                )
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>\n\nExtra error stuff here!'),
                str(err.exception),
            )

            # Now actually verify same thing, but with extra error info (as tuple).
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(
                    response,
                    [
                        ('<h1>Testing</h1>', 'Extra error stuff here!'),
                    ],
                )
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>\n\nExtra error stuff here!'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - With additional error info provided and ignore ordering.'):
            # First verify as standard not-found in array.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(
                    response,
                    [
                        '<h1>Testing</h1>',
                    ],
                    ignore_ordering=True,
                )
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>'),
                str(err.exception),
            )

            # Now actually verify same thing, but with extra error info (as list).
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(
                    response,
                    [
                        ['<h1>Testing</h1>', 'Extra error stuff here!'],
                    ],
                    ignore_ordering=True,
                )
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>\n\nExtra error stuff here!'),
                str(err.exception),
            )

            # Now actually verify same thing, but with extra error info (as tuple).
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(
                    response,
                    [
                        ('<h1>Testing</h1>', 'Extra error stuff here!'),
                    ],
                    ignore_ordering=True,
                )
            self.assertText(
                exception_msg_not_found.format('<h1>Testing</h1>\n\nExtra error stuff here!'),
                str(err.exception),
            )

        with self.subTest('Standard Response - Wrong value passed'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:login')
                self.assertPageContent(response, '<h1>Testing Header</h1><p>Pretend this is a page.</p>')
            self.assertText(
                exception_msg_not_found.format('<h1>Testing Header</h1><p>Pretend this is a page.</p>'),
                str(err.exception),
            )

        with self.subTest('Standard Response - Set of items with wrong values'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Test as list.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ['<h1>Test Page Header</h1>'],
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('<h1>Test Page Header</h1>'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ['Wrong Content'],
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('Wrong Content'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ['<h1>Home Page Wrong'],
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('<h1>Home Page Wrong'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ['Wrong Page Header</h1>'],
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('Wrong Page Header</h1>'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ['<h1>Home Page Header</h1>', 'Wrong text'],
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('Wrong text'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ['<h1>Wrong Header</h1>', 'project landing page'],
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('<h1>Wrong Header</h1>'),
                str(err.exception),
            )
            # Test as tuple.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ('<h1>Test Page Header</h1>',),
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('<h1>Test Page Header</h1>'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ('Wrong Content',),
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('Wrong Content'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ('<h1>Home Page Wrong',),
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('<h1>Home Page Wrong'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ('Wrong Page Header</h1>',),
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('Wrong Page Header</h1>'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ('<h1>Home Page Header</h1>', 'Wrong text'),
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('Wrong text'),
                str(err.exception),
            )
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    ('<h1>Wrong Header</h1>', 'project landing page'),
                )
            self.assertTextStartsWith(
                exception_msg_not_found.format('<h1>Wrong Header</h1>'),
                str(err.exception),
            )

        with self.subTest('Standard Response - Wrong ordering'):
            response = self._get_page_response(
                'django_expanded_test_cases:user-detail',
                args=(1,),
            )

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string at top.
                self.assertPageContent(
                    response,
                    [
                        'First Name: "SuperUserFirst"',
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "SuperUserLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertTextStartsWith(
                exception_msg_bad_order.format('<h1>User Detail Page Header</h1>'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after header.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'First Name: "SuperUserFirst"',
                        'Username: "test_superuser"',
                        'Last Name: "SuperUserLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertTextStartsWith(
                exception_msg_bad_order.format('Username: "test_superuser"'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after last name.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "SuperUserLast"',
                        'First Name: "SuperUserFirst"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertTextStartsWith(
                exception_msg_bad_order.format('First Name: "SuperUserFirst"'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after active.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "SuperUserLast"',
                        'Is Active: "True"',
                        'First Name: "SuperUserFirst"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertTextStartsWith(
                exception_msg_bad_order.format('First Name: "SuperUserFirst"'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after superuser.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "SuperUserLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'First Name: "SuperUserFirst"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertTextStartsWith(
                exception_msg_bad_order.format('First Name: "SuperUserFirst"'),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after staff.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "SuperUserLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                        'First Name: "SuperUserFirst"',
                    ],
                )
            self.assertTextStartsWith(
                exception_msg_bad_order.format('First Name: "SuperUserFirst"'),
                str(err.exception),
            )

    def test__assertPageContent__failure__with_bad_search_space(self):
        exception_msg = 'Could not find "{0}" value in content response. Provided value was:\n{1}'
        response = self._get_page_response('django_expanded_test_cases:home')

        # Bad content_starts_after values.
        with self.subTest('With content_starts_after not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_starts_after='Wrong value.',
                )
            self.assertText(
                exception_msg.format('content_starts_after', 'Wrong value.'),
                str(err.exception),
            )
        with self.subTest('With content_starts_after not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='Wrong content value.',
                    content_starts_after='Wrong value.',
                )
            self.assertText(
                exception_msg.format('content_starts_after', 'Wrong value.'),
                str(err.exception),
            )
        with self.subTest('With content_starts_after found with extra'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_starts_after='Home Page Header plus Extra',
                )
            self.assertText(
                exception_msg.format('content_starts_after', 'Home Page Header plus Extra'),
                str(err.exception),
            )

        # Bad content_ends_before values.
        with self.subTest('With content_ends_before not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_ends_before='Wrong value.',
                )
            self.assertText(
                exception_msg.format('content_ends_before', 'Wrong value.'),
                str(err.exception),
            )
        with self.subTest('With content_ends_before and expected_content not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='Wrong content value.',
                    content_ends_before='Wrong value.',
                )
            self.assertText(
                exception_msg.format('content_ends_before', 'Wrong value.'),
                str(err.exception),
            )
        with self.subTest('With content_ends_before found with extra'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_ends_before='Home Page Header plus Extra',
                )
            self.assertText(
                exception_msg.format('content_ends_before', 'Home Page Header plus Extra'),
                str(err.exception),
            )

    def test__assertPageContent__fail__with_limited_search_space(self):
        exception_msg = 'Expected content value was found, but occurred in "{0}" section. Expected was:\n{1}'
        response = self._get_page_response('django_expanded_test_cases:home')

        with self.subTest('Standard Response - With content_starts_after defined'):
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<head>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<head>'),
                str(err.exception),
            )
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<meta charset="utf-8">',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
                str(err.exception),
            )
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='</head>',
                    content_starts_after='<h1>Home Page Header</h1>',
                    ignore_ordering=True,
                )
            self.assertText(
                exception_msg.format('content_starts_after', '</head>'),
                str(err.exception),
            )
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<body>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<body>'),
                str(err.exception),
            )
            # Expected as single value - With exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<h1>Home Page Header</h1>'),
                str(err.exception),
            )
            # Expected as single value - With partial of exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='h1>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', 'h1>'),
                str(err.exception),
            )

            # Expected as array.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<meta charset="utf-8">',
                        '<title>Home Page | Test Views</title>',
                    ],
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
                str(err.exception),
            )
            # Expected as array - With ignore_ordering.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<meta charset="utf-8">',
                        '<title>Home Page | Test Views</title>',
                    ],
                    ignore_ordering=True,
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
                str(err.exception),
            )
            # Expected as array - With ignore_ordering and content mis-ordered.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<title>Home Page | Test Views</title>',
                        '<meta charset="utf-8">',
                    ],
                    ignore_ordering=True,
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_starts_after', '<title>Home Page | Test Views</title>'),
                str(err.exception),
            )

        with self.subTest('Standard Response - With content_ends_before defined'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value - Exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', '<h1>Home Page Header</h1>'),
                str(err.exception),
            )
            # Expected as single value - Partial of exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='h1>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', 'h1>'),
                str(err.exception),
            )
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<p>Pretend this is the project landing page.</p>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as single value - With ignore_ordering (should have no effect here).
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<p>Pretend this is the project landing page.</p>',
                    ignore_ordering=True,
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='</body>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', '</body>'),
                str(err.exception),
            )

            # Expected as array.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<p>Pretend this is the project landing page.</p>',
                        '</body>',
                    ],
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as array - With ignore_ordering.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<p>Pretend this is the project landing page.</p>',
                        '</body>',
                    ],
                    ignore_ordering=True,
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as array - With ignore_ordering and content mis-ordered.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '</body>',
                        '<p>Pretend this is the project landing page.</p>',
                    ],
                    ignore_ordering=True,
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_ends_before', '</body>'),
                str(err.exception),
            )

        with self.subTest('Standard Response - With both content containers defined'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Expected as single value - above search area.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<meta charset="utf-8">',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
                str(err.exception),
            )
            # Expected as single value - above search area, exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<title>Home Page | Test Views</title>',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<title>Home Page | Test Views</title>'),
                str(err.exception),
            )
            # Expected as single value - below search area.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='</body>',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', '</body>'),
                str(err.exception),
            )
            # Expected as single value - below search area, exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<p>Pretend this is the project landing page.</p>',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertText(
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as single value - with ignore_ordering (should have no effect here).
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<meta charset="utf-8">',
                    ignore_ordering=True,
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertText(
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
                str(err.exception),
            )

            # Expected as array - Above search area.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<head>',
                        '<meta charset="utf-8">',
                    ],
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_starts_after', '<head>'),
                str(err.exception),
            )
            # Expected as array - Above search area, with ignore_ordering.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<head>',
                        '<meta charset="utf-8">',
                    ],
                    ignore_ordering=True,
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_starts_after', '<head>'),
                str(err.exception),
            )
            # Expected as array - Above search area, with ignore_ordering and content mis-ordered.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '<meta charset="utf-8">',
                        '<head>',
                    ],
                    ignore_ordering=True,
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
                str(err.exception),
            )
            # Expected as array - Below search area.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        'the project landing page.</p>',
                        '</body>',
                    ],
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_ends_before', 'the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as array - Below search area, with ignore_ordering.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        'the project landing page.</p>',
                        '</body>',
                    ],
                    ignore_ordering=True,
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_ends_before', 'the project landing page.</p>'),
                str(err.exception),
            )
            # Expected as array - Below search area, with ignore_ordering and content mis-ordered.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content=[
                        '</body>',
                        'the project landing page.</p>',
                    ],
                    ignore_ordering=True,
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is',
                )
            self.assertTextStartsWith(
                exception_msg.format('content_ends_before', '</body>'),
                str(err.exception),
            )

    def test__assertPageContent__fail__with_content_casing_mismatch__exact_match(self):
        exception_msg = (
            'Expected content value was found, but letter capitalization did not match. Expected was:\n'
            '{0}\n'
            '\n'
            'Found was:\n'
            '{1}'
        )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1> ...'),
                str(err.exception),
            )

    def test__assertPageContent__fail__with_content_casing_mismatch__extra_characters_before(self):
        exception_msg = (
            'Expected content value was found, but letter capitalization did not match. Expected was:\n'
            '{0}\n'
            '\n'
            'Found was:\n'
            '{1}'
        )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>Test Title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <div>123456789</div><h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>This is a test p tag.</p></div><h1>Test Title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... est p tag.</p></div><h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>Testing</p><h1>Test Title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <p>Testing</p><h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <div>123456789</div><h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>This is a test p tag.</p></div><h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... est p tag.</p></div><h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>Testing</p><h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <p>Testing</p><h1>Test Title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV>123456789</DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <DIV>123456789</DIV><H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV><P>THIS IS A TEST P TAG.</P></DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... EST P TAG.</P></DIV><H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<P>TESTING</P><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <P>TESTING</P><H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV>123456789</DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <DIV>123456789</DIV><H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV><P>THIS IS A TEST P TAG.</P></DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... EST P TAG.</P></DIV><H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<P>TESTING</P><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <P>TESTING</P><H1>TEST TITLE</H1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <div>123456789</div><h1>test title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>this is a test p tag.</p></div><h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... est p tag.</p></div><h1>test title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>testing</p><h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <p>testing</p><h1>test title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <div>123456789</div><h1>test title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>this is a test p tag.</p></div><h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... est p tag.</p></div><h1>test title</h1> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>testing</p><h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <p>testing</p><h1>test title</h1> ...'),
                str(err.exception),
            )

    def test__assertPageContent__fail__with_content_casing_mismatch__extra_characters_after(self):
        exception_msg = (
            'Expected content value was found, but letter capitalization did not match. Expected was:\n'
            '{0}\n'
            '\n'
            'Found was:\n'
            '{1}'
        )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div>123456789</div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1><div>123456789</div> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div><p>This is a test p tag.</p></div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1><div><p>This is a te ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><p>Testing</p>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1><p>Testing</p> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div>123456789</div>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1><div>123456789</div> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div><p>This is a test p tag.</p></div>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1><div><p>This is a te ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><p>Testing</p>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1><p>Testing</p> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV>123456789</DIV>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1><DIV>123456789</DIV> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV><P>THIS IS A TEST P TAG.</P></DIV>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1><DIV><P>THIS IS A TE ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><P>TESTING</P>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1><P>TESTING</P> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV>123456789</DIV>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1><DIV>123456789</DIV> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV><P>THIS IS A TEST P TAG.</P></DIV>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1><DIV><P>THIS IS A TE ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><P>TESTING</P>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertText(
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1><P>TESTING</P> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div>123456789</div>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1><div>123456789</div> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div><p>this is a test p tag.</p></div>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1><div><p>this is a te ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><p>testing/p>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertText(
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1><p>testing/p> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div>123456789</div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1><div>123456789</div> ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div><p>this is a test p tag.</p></div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1><div><p>this is a te ...'),
                str(err.exception),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><p>testing/p>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertText(
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1><p>testing/p> ...'),
                str(err.exception),
            )

    def test__assertPageContent__fail__with_content_casing_mismatch__actual_response_object(self):
        exception_msg = (
            'Expected content value was found, but letter capitalization did not match. Expected was:\n'
            '{0}\n'
            '\n'
            'Found was:\n'
            '{1}'
        )

        with self.subTest('Standard Response - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:home')
                self.assertPageContent(response, '<H1>HOME PAGE HEADER</H1>')
            self.assertText(
                exception_msg.format(
                    '<H1>HOME PAGE HEADER</H1>',
                    '... /title></head><body><h1>Home Page Header</h1><p>Pretend this is t ...',
                ),
                str(err.exception),
            )

        with self.subTest('Standard Response - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:home')
                self.assertPageContent(response, '<h1>home page header</h1>')
            self.assertText(
                exception_msg.format(
                    '<h1>home page header</h1>',
                    '... /title></head><body><h1>Home Page Header</h1><p>Pretend this is t ...',
                ),
                str(err.exception),
            )

        with self.subTest('Standard Response - With response mixed and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:home')
                self.assertPageContent(response, '<h1>home Page header</h1>')
            self.assertText(
                exception_msg.format(
                    '<h1>home Page header</h1>',
                    '... /title></head><body><h1>Home Page Header</h1><p>Pretend this is t ...',
                ),
                str(err.exception),
            )

    def test__assertPageContent__edge_case__user_content_has_str_format_syntax__single_assertion(self):
        """Testing with assertPageContent when user content has string formatting syntax.
        Such as { or } characters, without the matching equivalent other side.

        When dealing with only a single statement to check for in content.
        """

        with self.subTest('Success Check - Has { character.'):

            response = HttpResponse('<title>My title has { in it, oops!</title>')
            self.assertPageContent(response, '<title>My title has { in it, oops!</title>')

        with self.subTest('Success Check - Has } character.'):

            response = HttpResponse('<title>My title has } in it, oops!</title>')
            self.assertPageContent(response, '<title>My title has } in it, oops!</title>')

        with self.subTest('Success Check - Has { and } characters (standard order).'):

            response = HttpResponse('<title>My title has { and } in it, oops!</title>')
            self.assertPageContent(response, '<title>My title has { and } in it, oops!</title>')

        with self.subTest('Success Check - Has { and } characters (reverse order).'):

            response = HttpResponse('<title>My title has } and { in it, oops!</title>')
            self.assertPageContent(response, '<title>My title has } and { in it, oops!</title>')

        with self.subTest('Failure Check - Expected { character.'):

            response = HttpResponse('<title>Test Title</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '{')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '{\n'
                ),
                str(err.exception),
            )

            # Expecting single character in tag.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>{</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>{</title>\n'
                ),
                str(err.exception),
            )

            # Full value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has { in it, oops!</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has{in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Expected } character.'):

            response = HttpResponse('<title>Test Title</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '}')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '}\n'
                ),
                str(err.exception),
            )

            # Expecting single character in tag.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>}</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>}</title>\n'
                ),
                str(err.exception),
            )

            # Full value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has } in it, oops!</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has}in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Expected { and } characters (standard order).'):

            response = HttpResponse('<title>Test Title</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '{ }')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '{}\n'
                ),
                str(err.exception),
            )

            # Expecting single character in tag.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>{ }</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>{}</title>\n'
                ),
                str(err.exception),
            )

            # Full value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has { and } in it, oops!</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has{and}in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Expected { and } characters (reverse order).'):

            response = HttpResponse('<title>Test Title</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '} {')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '}{\n'
                ),
                str(err.exception),
            )

            # Expecting single character in tag.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>} {</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>}{</title>\n'
                ),
                str(err.exception),
            )

            # Full value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has } and { in it, oops!</title>')
            self.assertEqual(
                (
                    # So black does not one-line this.
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has}and{in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect { character.'):

            response = HttpResponse('<title>My title has { in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has  in it, oops!</title>')
            self.assertEqual(
                (
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect } character.'):

            response = HttpResponse('<title>My title has } in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has  in it, oops!</title>')
            self.assertEqual(
                (
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect { and } characters (standard order).'):

            response = HttpResponse('<title>My title has { and } in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has  in it, oops!</title>')
            self.assertEqual(
                (
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has in it, oops!</title>\n'
                ),
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect { and } characters (reverse order).'):

            response = HttpResponse('<title>My title has } and { in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, '<title>My title has  in it, oops!</title>')
            self.assertEqual(
                (
                    'Could not find expected content value in response. Provided value was:\n'
                    '<title>My title has in it, oops!</title>\n'
                ),
                str(err.exception),
            )

    def test__assertPageContent__edge_case__user_content_has_str_format_syntax__multi_assertion(self):
        """Testing with assertPageContent when user content has string formatting syntax.
        Such as { or } characters, without the matching equivalent other side.

        When dealing with multiple statements to check for in content.
        """

        with self.subTest('Success Check - Has { character.'):

            # Generate response.
            response = HttpResponse('<title>My title has { in it, oops!</title>')

            self.assertPageContent(
                response,
                [
                    '<title>',
                    'My',
                    'title',
                    'has',
                    '{',
                    'in it,',
                    'oops!',
                    '</title>',
                ],
            )

        with self.subTest('Success Check - Has } character.'):

            # Generate response.
            response = HttpResponse('<title>My title has } in it, oops!</title>')

            self.assertPageContent(
                response,
                [
                    '<title>',
                    'My',
                    'title',
                    'has',
                    '}',
                    'in it,',
                    'oops!',
                    '</title>',
                ],
            )

        with self.subTest('Success Check - Has { and } characters (standard order).'):

            # Generate response.
            response = HttpResponse('<title>My title has { and } in it, oops!</title>')

            self.assertPageContent(
                response,
                [
                    '<title>',
                    'My',
                    'title',
                    'has',
                    '{ and }',
                    'in it,',
                    'oops!',
                    '</title>',
                ],
            )

        with self.subTest('Success Check - Has { and } characters (reverse order).'):

            # Generate response.
            response = HttpResponse('<title>My title has } and { in it, oops!</title>')

            self.assertPageContent(
                response,
                [
                    '<title>',
                    'My',
                    'title',
                    'has',
                    '} and {',
                    'in it,',
                    'oops!',
                    '</title>',
                ],
            )

        with self.subTest('Failure Check - Expected { character.'):

            # Generate response.
            response = HttpResponse('<title>My title has blah in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has',
                        '{',
                        'in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Expected } character.'):
            # Generate response.
            response = HttpResponse('<title>My title has blah in it, oops!</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has',
                        '}',
                        'in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Expected { and } characters (standard order).'):
            # Generate response.
            response = HttpResponse('<title>My title has blah in it, oops!</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has',
                        '{ and }',
                        'in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Expected { and } characters (reverse order).'):
            # Generate response.
            response = HttpResponse('<title>My title has blah in it, oops!</title>')

            # Expecting single character.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has',
                        '} and {',
                        'in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect { character.'):

            response = HttpResponse('<title>My title has { in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect } character.'):

            response = HttpResponse('<title>My title has } in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect { and } characters (standard order).'):

            response = HttpResponse('<title>My title has { and } in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

        with self.subTest('Failure Check - Didn\'t expect { and } characters (reverse order).'):

            response = HttpResponse('<title>My title has } and { in it, oops!</title>')

            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    [
                        '<title>',
                        'My',
                        'title',
                        'has in it,',
                        'oops!',
                        '</title>',
                    ],
                )
            self.assertTextStartsWith(
                'Could not find expected content value in response. Provided value was:\n',
                str(err.exception),
            )

    def test__assertPageContent__verifying_contextual_output__default(self):
        """Verifies contextual output for assertContent, when multiple values are provided in a single statement.
        This tests the default setting value.
        """
        response = HttpResponse('<span>This is my test span.</span>')

        if COLORAMA_PRESENT:
            output_color_before = ETC_OUTPUT_EXPECTED_MATCH_COLOR
            output_color_after = ETC_OUTPUT_ACTUALS_MATCH_COLOR
            output_color_error = ETC_OUTPUT_ERROR_COLOR
            output_color_reset = ETC_OUTPUT_RESET_COLOR
        else:
            output_color_before = ''
            output_color_after = ''
            output_color_error = ''
            output_color_reset = ETC_UNDERLINE_RESET

        # Test with full values.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    '<span>',
                    'This',
                    'is',
                    'my',
                    'testing',
                    'span',
                    '.',
                    '</span>',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * is{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
                '{3}    * .{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing before.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'testing',
                    'span',
                    '.',
                    '</span>',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
                '{3}    * .{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing after.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    '<span>',
                    'This',
                    'is',
                    'my',
                    'testing',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * is{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test only one per side.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'my',
                    'testing',
                    'span',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing all.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'testing',
                ],
            )
        self.assertText(
            ('Could not find expected content value in response. Provided value was:\n' 'testing\n'),
            str(err.exception),
        )

    @patch(
        "django_expanded_test_cases.test_cases.integration_test_case.ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH",
        1,
    )
    def test__assertPageContent__verifying_contextual_output__one(self):
        """Verifies contextual output for assertContent, when multiple values are provided in a single statement.
        This tests settings value of 1 contextual item output.
        """
        response = HttpResponse('<span>This is my test span.</span>')

        if COLORAMA_PRESENT:
            output_color_before = ETC_OUTPUT_EXPECTED_MATCH_COLOR
            output_color_after = ETC_OUTPUT_ACTUALS_MATCH_COLOR
            output_color_error = ETC_OUTPUT_ERROR_COLOR
            output_color_reset = ETC_OUTPUT_RESET_COLOR
        else:
            output_color_before = ''
            output_color_after = ''
            output_color_error = ''
            output_color_reset = ETC_UNDERLINE_RESET

        # Test with full values.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    '<span>',
                    'This',
                    'is',
                    'my',
                    'testing',
                    'span',
                    '.',
                    '</span>',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing before.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'testing',
                    'span',
                    '.',
                    '</span>',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing after.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    '<span>',
                    'This',
                    'is',
                    'my',
                    'testing',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test only one per side.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'my',
                    'testing',
                    'span',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing all.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'testing',
                ],
            )
        self.assertText(
            ('Could not find expected content value in response. Provided value was:\n' 'testing\n'),
            str(err.exception),
        )

    @patch(
        "django_expanded_test_cases.test_cases.integration_test_case.ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH",
        3,
    )
    def test__assertPageContent__verifying_contextual_output__three(self):
        """Verifies contextual output for assertContent, when multiple values are provided in a single statement.
        This tests settings value of 3 contextual item outputs.
        """
        response = HttpResponse('<span>This is my test span.</span>')

        if COLORAMA_PRESENT:
            output_color_before = ETC_OUTPUT_EXPECTED_MATCH_COLOR
            output_color_after = ETC_OUTPUT_ACTUALS_MATCH_COLOR
            output_color_error = ETC_OUTPUT_ERROR_COLOR
            output_color_reset = ETC_OUTPUT_RESET_COLOR
        else:
            output_color_before = ''
            output_color_after = ''
            output_color_error = ''
            output_color_reset = ETC_UNDERLINE_RESET

        # Test with full values.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    '<span>',
                    'This',
                    'is',
                    'my',
                    'testing',
                    'span',
                    '.',
                    '</span>',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * This{0}\n'
                '{1}    * is{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
                '{3}    * .{0}\n'
                '{3}    * </span>{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing before.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'testing',
                    'span',
                    '.',
                    '</span>',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
                '{3}    * .{0}\n'
                '{3}    * </span>{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing after.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    '<span>',
                    'This',
                    'is',
                    'my',
                    'testing',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * This{0}\n'
                '{1}    * is{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test only one per side.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'my',
                    'testing',
                    'span',
                ],
            )
        self.assertText(
            (
                'Could not find expected content value in response. Provided value was:\n'
                'testing\n'
                '\n'
                '\n'
                'Surrounding Checks:\n'
                '{1}Content Checks Before:{0}\n'
                '{1}    * my{0}\n'
                '{2}Failed Check:{0}\n'
                '{2}  > * testing{0}\n'
                '{3}Content Checks After:{0}\n'
                '{3}    * span{0}\n'
            ).format(
                output_color_reset,
                output_color_before,
                output_color_error,
                output_color_after,
            ),
            str(err.exception),
        )

        # Test missing all.
        with self.assertRaises(AssertionError) as err:
            self.assertPageContent(
                response,
                [
                    'testing',
                ],
            )
        self.assertText(
            ('Could not find expected content value in response. Provided value was:\n' 'testing\n'),
            str(err.exception),
        )

    def test__assertNotPageContent__success(self):
        """
        Tests assertNotPageContent() function, in cases when it should succeed.
        """

        with self.subTest('Empty response, no value passed.'):
            # Technically this one "matches".
            # But it's effectively impossible to verify "empty string" is not present in a given section of text.
            # Thus we skip raising errors on any case of empty-strings.
            response = HttpResponse('')
            self.assertNotPageContent(response, '')

        with self.subTest('Empty response, but value passed.'):
            response = HttpResponse('')
            self.assertNotPageContent(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response, no value passed'):
            # Same as above, or any other case with empty-strings.
            response = HttpResponse('<h1>Test Title</h1>')
            self.assertNotPageContent(response, '')

        with self.subTest('Minimal Response - Wrong value passed'):
            response = HttpResponse('<h1>Test Title</h1>')
            self.assertNotPageContent(response, '<h1>Testing</h1>')
            self.assertNotPageContent(response, '<h1>Test</h1>')
            self.assertNotPageContent(response, '<h1>Title</h1>')

        with self.subTest('Standard Response, no value passed'):
            # Same as above, or any other case with empty-strings.
            response = self._get_page_response('django_expanded_test_cases:login')
            self.assertNotPageContent(response, '')

        with self.subTest('Standard Response - Wrong value passed'):
            response = self._get_page_response('django_expanded_test_cases:login')
            self.assertNotPageContent(
                response,
                '<h1>Testing Header</h1><p>Pretend this is a page.</p>',
            )

        with self.subTest('Standard Response - Set of items with wrong values'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # Test as list.
            # First verify value we know SHOULD be there.
            self.assertPageContent(response, ['<h1>Home Page Header</h1>'])

            # Now ensure we FAIL to find variations of it.
            self.assertNotPageContent(response, ['<h1>HomePage Header</h1>'])
            self.assertNotPageContent(response, ['<h1>Home PageHeader</h1>'])
            self.assertNotPageContent(response, ['<h1>HomePageHeader</h1>'])
            self.assertNotPageContent(response, ['<h1>Home Pge Header</h1>'])
            self.assertNotPageContent(response, ['HomePage Header'])
            self.assertNotPageContent(response, ['Home PageHeader'])
            self.assertNotPageContent(response, ['HomePageHeader'])
            self.assertNotPageContent(response, ['Home Pge Header'])
            self.assertNotPageContent(response, ['Home PageHeader</h1>'])
            self.assertNotPageContent(response, ['<h1>HomePage Header'])
            self.assertNotPageContent(response, ['<h2>Home Page Header</h2>'])

            # Ensure other content is consistently NOT found.
            self.assertNotPageContent(response, ['Wrong Content'])
            self.assertNotPageContent(response, ['<h1>Home Page Wrong'])
            self.assertNotPageContent(response, ['Wrong Page Header</h1>'])

            # Ensure multiple values are also all not found.
            # Above values, but all in a single list. All should fail to be found.
            self.assertNotPageContent(
                response,
                [
                    '<h1>HomePage Header</h1>',
                    '<h1>Home PageHeader</h1>',
                    '<h1>HomePageHeader</h1>',
                    '<h1>Home Pge Header</h1>',
                    'HomePage Header',
                    'Home PageHeader',
                    'HomePageHeader',
                    'Home Pge Header',
                    'Home PageHeader</h1>',
                    '<h1>HomePage Header',
                    '<h2>Home Page Header</h2>',
                ],
            )
            # Multiple values that should not be present.
            self.assertNotPageContent(
                response,
                [
                    'Wrong Content',
                    'Wrong text',
                    '<h1>Home Page Wrong',
                    '<h1>Wrong Header</h1>',
                    'Wrong Page Header</h1>',
                ],
            )

            # Test as tuple.
            # First verify value we know SHOULD be there.
            self.assertPageContent(response, ('<h1>Home Page Header</h1>',))

            # Now ensure we FAIL to find variations of it.
            self.assertNotPageContent(response, ('<h1>HomePage Header</h1>',))
            self.assertNotPageContent(response, ('<h1>Home PageHeader</h1>',))
            self.assertNotPageContent(response, ('<h1>HomePageHeader</h1>',))
            self.assertNotPageContent(response, ('<h1>Home Pge Header</h1>',))
            self.assertNotPageContent(response, ('HomePage Header',))
            self.assertNotPageContent(response, ('Home PageHeader',))
            self.assertNotPageContent(response, ('HomePageHeader',))
            self.assertNotPageContent(response, ('Home Pge Header',))
            self.assertNotPageContent(response, ('Home PageHeader</h1>',))
            self.assertNotPageContent(response, ('<h1>HomePage Header',))
            self.assertNotPageContent(response, ('<h2>Home Page Header</h2>',))

            # Ensure other content is consistently NOT found.
            self.assertNotPageContent(response, ('Wrong Content',))
            self.assertNotPageContent(response, ('<h1>Home Page Wrong',))
            self.assertNotPageContent(response, ('Wrong Page Header</h1>',))

            # Ensure multiple values are also all not found.
            # Above values, but all in a single list. All should fail to be found.
            self.assertNotPageContent(
                response,
                (
                    '<h1>HomePage Header</h1>',
                    '<h1>Home PageHeader</h1>',
                    '<h1>HomePageHeader</h1>',
                    '<h1>Home Pge Header</h1>',
                    'HomePage Header',
                    'Home PageHeader',
                    'HomePageHeader',
                    'Home Pge Header',
                    'Home PageHeader</h1>',
                    '<h1>HomePage Header',
                    '<h2>Home Page Header</h2>',
                ),
            )
            # Multiple values that should not be present.
            self.assertNotPageContent(
                response,
                (
                    'Wrong Content',
                    'Wrong text',
                    '<h1>Home Page Wrong',
                    '<h1>Wrong Header</h1>',
                    'Wrong Page Header</h1>',
                ),
            )

    def test__assertNotPageContent__failure(self):
        """
        Tests assertNotPageContent() function, in cases when it should fail.
        """
        err_msg = 'Found content in response. Expected content to not be present. Content was:\n{0}'

        with self.subTest('Minimal Response - Exact Match'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, '<h1>Test Title</h1>')
            self.assertText(err_msg.format('<h1>Test Title</h1>'), str(err.exception))

        with self.subTest('Minimal Response - Sub-Matches'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, 'Test')
            self.assertText(err_msg.format('Test'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, 'Title')
            self.assertText(err_msg.format('Title'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, '<h1>')
            self.assertText(err_msg.format('<h1>'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, '</h1>')
            self.assertText(err_msg.format('</h1>'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, '<h1>Test')
            self.assertText(err_msg.format('<h1>Test'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(response, 'Title</h1>')
            self.assertText(err_msg.format('Title</h1>'), str(err.exception))

        with self.subTest('Minimal Response - Outer whitespace'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('&nbsp; <h1>Test Title</h1> &nbsp; ')
                self.assertNotPageContent(response, '<h1>Test Title</h1>')
            self.assertText(err_msg.format('<h1>Test Title</h1>'), str(err.exception))

        with self.subTest('Minimal Response - Inner whitespace'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
                self.assertNotPageContent(response, '<h1>Test Title</h1>')
            self.assertText(err_msg.format('<h1>Test Title</h1>'), str(err.exception))

        with self.subTest('Minimal Response - Inner whitespace'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
                self.assertNotPageContent(response, '<h1>Test Title</h1>')
            self.assertText(err_msg.format('<h1>Test Title</h1>'), str(err.exception))

        with self.subTest('Minimal Response - With Newlines'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test  \n  Title</h1>')
                self.assertNotPageContent(response, '<h1>Test Title</h1>')
            self.assertText(err_msg.format('<h1>Test Title</h1>'), str(err.exception))

        with self.subTest('Minimal Response - With additional error info provided.'):
            # First verify as standard not-found in array.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertNotPageContent(
                    response,
                    [
                        '<h1>Test Title</h1>',
                    ],
                )
            self.assertText(err_msg.format('<h1>Test Title</h1>'), str(err.exception))

        # Now actually verify same thing, but with extra error info (as list).
        with self.assertRaises(AssertionError) as err:
            response = HttpResponse('<h1>Test Title</h1>')
            self.assertNotPageContent(
                response,
                [
                    ['<h1>Test Title</h1>', 'Extra error stuff here!'],
                ],
            )
        self.assertText(
            err_msg.format('<h1>Test Title</h1>\n\nExtra error stuff here!'),
            str(err.exception),
        )

        # Now actually verify same thing, but with extra error info (as tuple).
        with self.assertRaises(AssertionError) as err:
            response = HttpResponse('<h1>Test Title</h1>')
            self.assertNotPageContent(
                response,
                [
                    ('<h1>Test Title</h1>', 'Extra error stuff here!'),
                ],
            )
        self.assertText(
            err_msg.format('<h1>Test Title</h1>\n\nExtra error stuff here!'),
            str(err.exception),
        )

        with self.subTest('Standard Response - Set of items where one or more items is found (none should be found)'):
            response = self._get_page_response('django_expanded_test_cases:home')

            # First item is found.
            with self.assertRaises(AssertionError) as err:
                self.assertNotPageContent(
                    response,
                    (
                        '<h1>Home Page Header</h1>',
                        'Wrong Content',
                        'Wrong text',
                        '<h1>Home Page Wrong',
                        '<h1>Wrong Header</h1>',
                        'Wrong Page Header</h1>',
                    ),
                )
            self.assertText(err_msg.format('<h1>Home Page Header</h1>'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertNotPageContent(
                    response,
                    (
                        'Home Page Header',
                        'Wrong Content',
                        'Wrong text',
                        '<h1>Home Page Wrong',
                        '<h1>Wrong Header</h1>',
                        'Wrong Page Header</h1>',
                    ),
                )
            self.assertText(err_msg.format('Home Page Header'), str(err.exception))

            # Middle item is found.
            with self.assertRaises(AssertionError) as err:
                self.assertNotPageContent(
                    response,
                    (
                        'Wrong Content',
                        'Wrong text',
                        '<h1>Home Page Header</h1>',
                        '<h1>Home Page Wrong',
                        '<h1>Wrong Header</h1>',
                        'Wrong Page Header</h1>',
                    ),
                )
            self.assertText(err_msg.format('<h1>Home Page Header</h1>'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertNotPageContent(
                    response,
                    (
                        'Wrong Content',
                        'Wrong text',
                        'Home Page Header',
                        '<h1>Home Page Wrong',
                        '<h1>Wrong Header</h1>',
                        'Wrong Page Header</h1>',
                    ),
                )
            self.assertText(err_msg.format('Home Page Header'), str(err.exception))

            # Last item is found.
            with self.assertRaises(AssertionError) as err:
                self.assertNotPageContent(
                    response,
                    (
                        'Wrong Content',
                        'Wrong text',
                        '<h1>Home Page Wrong',
                        '<h1>Wrong Header</h1>',
                        'Wrong Page Header</h1>',
                        '<h1>Home Page Header</h1>',
                    ),
                )
            self.assertText(err_msg.format('<h1>Home Page Header</h1>'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertNotPageContent(
                    response,
                    (
                        'Wrong Content',
                        'Wrong text',
                        '<h1>Home Page Wrong',
                        '<h1>Wrong Header</h1>',
                        'Wrong Page Header</h1>',
                        'Home Page Header',
                    ),
                )
            self.assertText(err_msg.format('Home Page Header'), str(err.exception))

    def test__assertRepeatingElement__success__standard_elements__basic(self):
        """
        Tests assertPageContent() function, in cases when it should succeed on "standard" (non-void) elements.
        """
        with self.subTest('Response with one item, when one item is expected'):
            response = HttpResponse('<li></li>')
            self.assertRepeatingElement(response, 'li', 1)
            self.assertRepeatingElement(response, '<li>', 1)

        with self.subTest('Response with two items, when two items are expected'):
            # No spaces.
            response = HttpResponse('<li></li><li></li>')
            self.assertRepeatingElement(response, 'li', 2)
            self.assertRepeatingElement(response, '<li>', 2)
            # With spaces.
            response = HttpResponse('<li></li> <li></li>')
            self.assertRepeatingElement(response, 'li', 2)
            self.assertRepeatingElement(response, '<li>', 2)

        with self.subTest('Response with three items, when three items are expected'):
            # No spaces.
            response = HttpResponse('<li></li><li></li><li></li>')
            self.assertRepeatingElement(response, 'li', 3)
            self.assertRepeatingElement(response, '<li>', 3)
            # With spaces.
            response = HttpResponse('<li></li> <li></li> <li></li>')
            self.assertRepeatingElement(response, 'li', 3)
            self.assertRepeatingElement(response, '<li>', 3)

        with self.subTest('Response with four items, when four items are expected'):
            # No spaces.
            response = HttpResponse('<li></li><li></li><li></li><li></li>')
            self.assertRepeatingElement(response, 'li', 4)
            self.assertRepeatingElement(response, '<li>', 4)
            # With spaces.
            response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
            self.assertRepeatingElement(response, 'li', 4)
            self.assertRepeatingElement(response, '<li>', 4)

    def test__assertRepeatingElement__success__standard_elements__with_noise(self):
        """
        Tests assertPageContent() function, in cases when it should succeed on "standard" (non-void) elements that
        are mixed with various unrelated "noise" elements.
        """
        with self.subTest('Response with one item, when one item is expected'):
            # No spaces.
            response = HttpResponse('<br><li><p>Test</p></li><hr>')
            self.assertRepeatingElement(response, '<li>', 1)
            # With spaces.
            response = HttpResponse('<br> <li><p>Test</p></li> <hr>')
            self.assertRepeatingElement(response, '<li>', 1)

        with self.subTest('Response with two items, when two items are expected'):
            # No spaces.
            response = HttpResponse('<ul><li><p>Test</p></li><br><li><p>Test</p></li></ul>')
            self.assertRepeatingElement(response, 'li', 2)
            self.assertRepeatingElement(response, '<li>', 2)
            # With spaces.
            response = HttpResponse('<ul> <li><p>Test</p></li> <br> <li><p>Test</p></li> </ul>')
            self.assertRepeatingElement(response, 'li', 2)
            self.assertRepeatingElement(response, '<li>', 2)

        with self.subTest('Response with three items, when three items are expected'):
            # No spaces.
            response = HttpResponse('<ul><li><p>Test</p></li><br><li><p>Test</p></li><br><li><p>Test</p></li></ul>')
            self.assertRepeatingElement(response, 'li', 3)
            self.assertRepeatingElement(response, '<li>', 3)
            # With spaces.
            response = HttpResponse(
                """
                <ul>
                <li><p>Test</p></li> <br>
                <li><p>Test</p></li> <br>
                <li><p>Test</p></li>
                </ul>
                """
            )
            self.assertRepeatingElement(response, 'li', 3)
            self.assertRepeatingElement(response, '<li>', 3)

        with self.subTest('Response with four items, when four items are expected'):
            # No spaces.
            response = HttpResponse(
                """
                <ul><li><p>Test</p></li><br><li><p>Test</p></li><br><li><p>Test</p></li><br><li><p>Test</p></li></ul>
                """
            )
            self.assertRepeatingElement(response, 'li', 4)
            self.assertRepeatingElement(response, '<li>', 4)
            # With spaces.
            response = HttpResponse(
                """
                <ul>
                <li><p>Test</p></li> <br>
                <li><p>Test</p></li> <br>
                <li><p>Test</p></li> <br>
                <li><p>Test</p></li>
                </ul>
                """
            )
            self.assertRepeatingElement(response, 'li', 4)
            self.assertRepeatingElement(response, '<li>', 4)

    def test__assertRepeatingElement__success__void_elements(self):
        """
        Tests assertPageContent() function, in cases when it should succeed on "void" elements.
        Aka, elements that do not have closing tags.
        """
        with self.subTest('Response with one item, when one item is expected'):
            response = HttpResponse('<hr>')
            self.assertRepeatingElement(response, '<hr>', 1)

        with self.subTest('Response with two items, when two items are expected'):
            # No spaces.
            response = HttpResponse('<hr><hr>')
            self.assertRepeatingElement(response, '<hr>', 2)
            # With spaces.
            response = HttpResponse('<hr> <hr>')
            self.assertRepeatingElement(response, '<hr>', 2)

        with self.subTest('Response with three items, when three items are expected'):
            # No spaces.
            response = HttpResponse('<hr><hr><hr>')
            self.assertRepeatingElement(response, '<hr>', 3)
            # With spaces.
            response = HttpResponse('<hr> <hr> <hr>')
            self.assertRepeatingElement(response, '<hr>', 3)

        with self.subTest('Response with four items, when four items are expected'):
            # No spaces.
            response = HttpResponse('<hr><hr><hr><hr>')
            self.assertRepeatingElement(response, '<hr>', 4)
            # With spaces.
            response = HttpResponse('<hr> <hr> <hr> <hr>')
            self.assertRepeatingElement(response, '<hr>', 4)

    def test__assertRepeatingElement__fail__incorrect_count(self):
        exception_msg = 'Expected {0} element opening tags. Found {1}.'

        with self.subTest('Providing an expected of less than 1'):
            with self.assertRaises(ValueError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 0)
            self.assertText(
                'The assertRepeatingElement() function requires an element occurs one or more times.',
                str(err.exception),
            )

        # Empty response tests.
        with self.subTest('Empty response, when one item is expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 0), str(err.exception))

        with self.subTest('Empty response, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(exception_msg.format(2, 0), str(err.exception))

        with self.subTest('Empty response, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(exception_msg.format(3, 0), str(err.exception))

        with self.subTest('Empty response, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(exception_msg.format(4, 0), str(err.exception))

        # Single item response tests.
        with self.subTest('Response with one item, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(exception_msg.format(2, 1), str(err.exception))

        with self.subTest('Response with one item, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(exception_msg.format(3, 1), str(err.exception))

        with self.subTest('Response with one item, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(exception_msg.format(4, 1), str(err.exception))

        # Two item response tests.
        with self.subTest('Response with two items, when one item is expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 2), str(err.exception))
            # With spaces
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 2), str(err.exception))

        with self.subTest('Response with two items, when three items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(exception_msg.format(3, 2), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(exception_msg.format(3, 2), str(err.exception))

        with self.subTest('Response with two items, when four items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(exception_msg.format(4, 2), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(exception_msg.format(4, 2), str(err.exception))

        # Three item response tests.
        with self.subTest('Response with three items, when one item is expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 3), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 3), str(err.exception))

        with self.subTest('Response with three items, when two items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(exception_msg.format(2, 3), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(exception_msg.format(2, 3), str(err.exception))

        with self.subTest('Response with three items, when four items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(exception_msg.format(4, 3), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(exception_msg.format(4, 3), str(err.exception))

        # Four item response tests.
        with self.subTest('Response with four items, when one item is expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 4), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(exception_msg.format(1, 4), str(err.exception))

        with self.subTest('Response with four items, when two items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(exception_msg.format(2, 4), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(exception_msg.format(2, 4), str(err.exception))

        with self.subTest('Response with four items, when three items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(exception_msg.format(3, 4), str(err.exception))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(exception_msg.format(3, 4), str(err.exception))

    def test__assertRepeatingElement__fail__incomplete_items(self):
        open_exception_msg = 'Expected {0} element opening tags. Found {1}.'
        close_exception_msg = 'Expected {0} element closing tags. Found {1}.'

        with self.subTest('Response with one plus partial items, when one item is expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(open_exception_msg.format(1, 2), str(err.exception))

        with self.subTest('Response with one plus partial items, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(close_exception_msg.format(2, 1), str(err.exception))

        with self.subTest('Response with two plus partial items, when one item is expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertText(open_exception_msg.format(1, 3), str(err.exception))

        with self.subTest('Response with two plus partial items, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(open_exception_msg.format(2, 3), str(err.exception))

        with self.subTest('Response with two plus partial items, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(close_exception_msg.format(3, 2), str(err.exception))

        with self.subTest('Response with three plus partial items, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertText(open_exception_msg.format(2, 4), str(err.exception))

        with self.subTest('Response with three plus partial items, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(open_exception_msg.format(3, 4), str(err.exception))

        with self.subTest('Response with three plus partial items, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(close_exception_msg.format(4, 3), str(err.exception))

        with self.subTest('Response with four plus partial items, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertText(open_exception_msg.format(3, 5), str(err.exception))

        with self.subTest('Response with four plus partial items, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertText(open_exception_msg.format(4, 5), str(err.exception))

        with self.subTest('Response with four plus partial items, when five items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 5)
            self.assertText(close_exception_msg.format(5, 4), str(err.exception))

    # endregion Element Assertion Tests


class TestIntegrationAssertions(IntegrationTestCase, IntegrationAssertionTestCase):
    """Runtime test execution of IntegrationTestCase class custom assertions, when using default project settings."""

    pass
