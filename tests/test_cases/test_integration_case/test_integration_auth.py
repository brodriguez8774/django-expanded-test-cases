"""
Tests for test_cases/integration_test_case.py logic under different project authentication settings.
"""

# System Imports.
import logging
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from .test_integration_assertions import IntegrationAssertionTestCase
from .test_integration_helpers import IntegrationHelperTestCase
from django_expanded_test_cases import IntegrationTestCase
from django_expanded_test_cases.constants import (
    COLORAMA_PRESENT,
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_RESET_COLOR,
)


class IntegrationAuthTestCase(IntegrationAssertionTestCase, IntegrationHelperTestCase):
    """Tests for IntegrationTestCase class under different project authentication settings.

    This class collects other IntegrationTestCase classes into one class,
    for easy importing into the below multiple auth classes.

    This class is a parent class that should not run by itself.
    It needs to be imported into other classes to execute.
    """


class TestIntegrationAuth__WithExtraAuthUpdate(IntegrationTestCase, IntegrationAuthTestCase):

    def _get_login_user__extra_user_auth_setup(self, *args, **kwargs):
        """Modified extra_user_auth_setup function, to mimic actually setting additional logic for user auth."""

        # Add some arbitrary session data.
        # Being able to save session data is sometimes required for user auth setup,
        # such as certain 2-factor implementations.
        session = self.client.session
        session['etc_testing_session_variable_1'] = True
        session.save()
        session['etc_testing_session_variable_2'] = False
        session.save()
        session['etc_testing_session_variable_3'] = 'Some Value'
        session.save()

        # Call parent logic.
        user = super()._get_login_user__extra_user_auth_setup(*args, **kwargs)

        # Add more arbitrary data.
        # Ensures we can persist session data both before and after calling parent function logic.
        session = self.client.session
        session['etc_testing_session_variable_4'] = True
        session.save()
        session['etc_testing_session_variable_5'] = False
        session.save()
        session['etc_testing_session_variable_6'] = 'Some Value'
        session.save()

        # Return original user value.
        return user

    def test__can_set_session_data_in__extra_user_auth_setup(self):
        """Verify that we can access our extra session data, set as part of the extra_user_auth function."""

        # Get arbitrary response that has gone through user authentication logic.
        response = self.assertGetResponse('django_expanded_test_cases:home', user='test_user')

        # Grab session object from response.
        session = response.client.session

        # Verify expected session data is present.
        self.assertTrue(session.get('etc_testing_session_variable_1', None))
        self.assertFalse(session.get('etc_testing_session_variable_2', None))
        self.assertText('Some Value', session.get('etc_testing_session_variable_3', None))
        self.assertTrue(session.get('etc_testing_session_variable_4', None))
        self.assertFalse(session.get('etc_testing_session_variable_5', None))
        self.assertText('Some Value', session.get('etc_testing_session_variable_6', None))


class TestIntegrationAuth__StrictnessOfAnonymous(IntegrationTestCase):
    """Tests for IntegrationTestCase class, specifically with user strictness set to "anonymous"."""

    @classmethod
    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'anonymous')
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.test_superuser.first_name = 'TestFirst'
        cls.test_superuser.last_name = 'TestLast'
        cls.test_superuser.save()

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'anonymous')
    def test__assertGetResponse__with_login(self):
        """Verifies that expected user is logged in during assertGetResponse."""

        with self.subTest('Check login using default user'):
            # Default user should be Anonymous, and no actual user is logged in unless explicitly provided.
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertEqual(AnonymousUser(), response.wsgi_request.user)
            self.assertEqual(AnonymousUser(), response.context['user'])
            self.assertEqual(AnonymousUser(), response.user)

        with self.subTest('Check login using super user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as arg'):
            new_user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user=new_user)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest('Check login using super user - Provided as class variable'):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as class variable'):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as class variable'):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as class variable'):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as class variable'):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest(
            'Check login using super user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse(
                'django_expanded_test_cases:home',
                user='test_superuser',
            )

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest(
            'Check login using admin user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse(
                'django_expanded_test_cases:home',
                user='test_admin',
            )

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest(
            'Check login using inactive user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse(
                'django_expanded_test_cases:home',
                user='test_inactive',
            )

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest(
            'Check login using standard user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse(
                'django_expanded_test_cases:home',
                user='test_user',
            )

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest(
            'Check login using custom new user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse(
                'django_expanded_test_cases:home',
                user='new_user',
            )

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'anonymous')
    def test__assertResponse__user(self):
        """
        Tests "user" functionality of assertResponse() function.
        """
        with self.subTest('Without providing a login user'):
            response = self.assertResponse('')
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']

        with self.subTest('With login as test user'):
            response = self.assertResponse('', user=self.test_user)
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_user')
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])

        with self.subTest('With login as admin user'):
            response = self.assertResponse('', user=self.test_admin)
            self.assertEqual(response.user, self.test_admin)
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_admin')
            self.assertEqual(response.user, self.test_admin)
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])

        with self.subTest('With login as superuser'):
            response = self.assertResponse('', user=self.test_superuser)
            self.assertEqual(response.user, self.test_superuser)
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_superuser')
            self.assertEqual(response.user, self.test_superuser)
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])

        with self.subTest('Without login, but test user passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_user, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            response = self.assertResponse('', user='test_user', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']

        with self.subTest('Without login, but admin user passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_admin, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            response = self.assertResponse('', user='test_admin', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']

        with self.subTest('Without login, but superuser passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_superuser, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            response = self.assertResponse('', user='test_superuser', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']


class TestIntegrationAuth__StrictnessOfRelaxed(IntegrationTestCase):
    """Tests for IntegrationTestCase class, specifically with user strictness set to "relaxed"."""

    @classmethod
    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'relaxed')
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.test_superuser.first_name = 'TestFirst'
        cls.test_superuser.last_name = 'TestLast'
        cls.test_superuser.save()

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'relaxed')
    def test__assertGetResponse__with_login(self):
        """Verifies that expected user is logged in during assertGetResponse."""

        with self.subTest('Check login using default user'):
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using super user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as arg'):

            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as arg'):
            new_user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user=new_user)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest('Check login using super user - Provided as class variable'):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as class variable'):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as class variable'):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as class variable'):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as class variable'):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest(
            'Check login using super user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest(
            'Check login using admin user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest(
            'Check login using inactive user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest(
            'Check login using standard user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest(
            'Check login using custom new user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='new_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'relaxed')
    def test__assertResponse__user(self):
        """
        Tests "user" functionality of assertResponse() function.
        """
        with self.subTest('With login as test user'):
            response = self.assertResponse('')
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user=self.test_user)
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_user')
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])

        with self.subTest('With login as admin user'):
            response = self.assertResponse('', user=self.test_admin)
            self.assertEqual(response.user, self.test_admin)
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_admin')
            self.assertEqual(response.user, self.test_admin)
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])

        with self.subTest('With login as superuser'):
            response = self.assertResponse('', user=self.test_superuser)
            self.assertEqual(response.user, self.test_superuser)
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_superuser')
            self.assertEqual(response.user, self.test_superuser)
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])

        with self.subTest('Without login, but test user passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())
            response = self.assertResponse('', user=self.test_user, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())
            response = self.assertResponse('', user='test_user', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())

        with self.subTest('Without login, but admin user passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_admin, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())
            response = self.assertResponse('', user='test_admin', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())

        with self.subTest('Without login, but superuser passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_superuser, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())
            response = self.assertResponse('', user='test_superuser', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            self.assertNotIn('_auth_user_id', self.client.session.keys())


class TestIntegrationAuth__StrictnessOfStrict(IntegrationTestCase):
    """Tests for IntegrationTestCase class, specifically with user strictness set to "strict"."""

    @classmethod
    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'strict')
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.test_superuser.first_name = 'TestFirst'
        cls.test_superuser.last_name = 'TestLast'
        cls.test_superuser.save()

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'strict')
    def test__assertGetResponse__with_login(self):
        """Verifies that expected user is logged in during assertGetResponse."""

        with self.subTest('Check login using default user'):
            # No default user provided. Should error.
            with self.assertRaises(ValidationError):
                self.assertGetResponse('django_expanded_test_cases:home')

        with self.subTest('Check login using super user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as arg'):
            new_user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user=new_user)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest('Check login using super user - Provided as class variable'):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as class variable'):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as class variable'):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as class variable'):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as class variable'):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest(
            'Check login using super user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest(
            'Check login using admin user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest(
            'Check login using inactive user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest(
            'Check login using standard user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest(
            'Check login using custom new user - Provided with conflicting values (function value should win)'
        ):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:home', user='new_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_REQUEST_USER_STRICTNESS', 'strict')
    def test__assertResponse__user(self):
        """
        Tests "user" functionality of assertResponse() function.
        """
        with self.subTest('Without providing a login user'):
            # No default user provided. Should error.
            with self.assertRaises(ValidationError):
                self.assertResponse('')

        with self.subTest('With login as test user'):
            response = self.assertResponse('', user=self.test_user)
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_user')
            self.assertEqual(response.user, self.test_user)
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])

        with self.subTest('With login as admin user'):
            response = self.assertResponse('', user=self.test_admin)
            self.assertEqual(response.user, self.test_admin)
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_admin')
            self.assertEqual(response.user, self.test_admin)
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])

        with self.subTest('With login as superuser'):
            response = self.assertResponse('', user=self.test_superuser)
            self.assertEqual(response.user, self.test_superuser)
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])
            response = self.assertResponse('', user='test_superuser')
            self.assertEqual(response.user, self.test_superuser)
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])

        with self.subTest('Without login, but test user passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_user, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            response = self.assertResponse('', user='test_user', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']

        with self.subTest('Without login, but admin user passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_admin, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            response = self.assertResponse('', user='test_admin', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']

        with self.subTest('Without login, but superuser passed'):
            # Basically, passing a user should not really do anything here.
            response = self.assertResponse('', user=self.test_superuser, auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']
            response = self.assertResponse('', user='test_superuser', auto_login=False)
            self.assertEqual(response.user, AnonymousUser())
            with self.assertRaises(KeyError):
                self.client.session['_auth_user_id']


# class IntegrationClassTest__NoAutoGeneratedUser(IntegrationTestCase):
#     """Tests for IntegrationTestCase class, specifically with no auto-generated users."""
#
#     @classmethod
#     @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS', 'False')
#     def setUpClass(cls):
#         # Run parent setup logic.
#         super().setUpClass()
#
#     @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS', 'False')
#     def test__class_users(self):
#         # Since no users were auto-generated, all of these class attributes should come back as None.
#         self.assertFalse(hasattr(self, 'test_superuser'))
#         self.assertFalse(hasattr(self, 'test_admin_user'))
#         self.assertFalse(hasattr(self, 'test_user'))
#         self.assertFalse(hasattr(self, 'test_inactive_user'))
