"""
Tests for test_cases/integration_test_case.py.
"""

# System Imports.
import logging
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

# Internal Imports.
from django_expanded_test_cases import IntegrationTestCase


class IntegrationClassTest(IntegrationTestCase):
    """Tests for IntegrationTestCase class."""

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.test_superuser.first_name = 'TestFirst'
        cls.test_superuser.last_name = 'TestLast'
        cls.test_superuser.save()

    # region Response Tests

    def test__assertGetResponse__with_login(self):
        """Verifies that expected user is logged in during assertGetResponse."""

        with self.subTest('Check login using default user'):
            response = self.assertGetResponse('django_expanded_test_cases:index')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using super user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as arg'):

            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session['_auth_user_id']))
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as arg'):
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as arg'):
            new_user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:index', user=new_user)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest('Check login using super user - Provided as class variable'):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:index')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided as class variable'):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:index')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided as class variable'):
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:index')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session['_auth_user_id']))
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided as class variable'):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:index')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.context['user'])
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using custom new user - Provided as class variable'):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:index')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

        with self.subTest('Check login using super user - Provided with conflicting values (function value should win)'):
            self.user = self.get_user('new_user')
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_superuser')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.context['user'])
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user - Provided with conflicting values (function value should win)'):
            self.user = self.get_user('test_superuser')
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_admin')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.context['user'])
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user - Provided with conflicting values (function value should win)'):
            self.user = self.get_user('test_admin')
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_inactive')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session['_auth_user_id']))
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user - Provided with conflicting values (class value should win)'):
            # This is the exception, because "test_user" technically IS the "default" user.
            # Thus, providing this for the function value when a class value is also provided will result
            # in the class value being used instead.
            self.user = self.get_user('test_inactive')
            response = self.assertGetResponse('django_expanded_test_cases:index', user='test_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session['_auth_user_id']))
            self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertFalse(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, response.wsgi_request.user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using custom new user - Provided with conflicting values (function value should win)'):
            self.user = self.get_user('test_user')
            response = self.assertGetResponse('django_expanded_test_cases:index', user='new_user')

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session['_auth_user_id']))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.context['user'])
            self.assertEqual(new_user, response.user)

    # endregion Response Tests

    # region Assertion Tests

    # region Response Assertion Tests

    def test__assertResponse__url(self):
        """
        Tests URL value returned response object in assertResponse() function.
        """
        with self.subTest('With no site_root_url value defined - Via literal value'):
            # Test 404 page url.
            response = self.assertResponse('bad_url', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')
            response = self.assertResponse('bad_url/', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')
            response = self.assertResponse('127.0.0.1/bad_url/', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')
            response = self.assertResponse('///bad_url///', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')

            # Test "index" page url.
            response = self.assertResponse('')
            self.assertEqual(response.url, '127.0.0.1/')
            response = self.assertResponse('/')
            self.assertEqual(response.url, '127.0.0.1/')
            response = self.assertResponse('127.0.0.1/')
            self.assertEqual(response.url, '127.0.0.1/')

            # Test "login" page url.
            response = self.assertResponse('login/')
            self.assertEqual(response.url, '127.0.0.1/login/')
            response = self.assertResponse('/login/')
            self.assertEqual(response.url, '127.0.0.1/login/')
            response = self.assertResponse('127.0.0.1/login/')
            self.assertEqual(response.url, '127.0.0.1/login/')

            # Test "one message" page url.
            response = self.assertResponse('one-message/')
            self.assertEqual(response.url, '127.0.0.1/one-message/')
            response = self.assertResponse('/one-message/')
            self.assertEqual(response.url, '127.0.0.1/one-message/')
            response = self.assertResponse('127.0.0.1/one-message/')
            self.assertEqual(response.url, '127.0.0.1/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('two-messages/')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')
            response = self.assertResponse('/two-messages/')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')
            response = self.assertResponse('127.0.0.1/two-messages/')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('user/detail/1/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')
            response = self.assertResponse('/user/detail/1/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')
            response = self.assertResponse('127.0.0.1/user/detail/1/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('user/detail/2/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')
            response = self.assertResponse('/user/detail/2/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')
            response = self.assertResponse('127.0.0.1/user/detail/2/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')

        with self.subTest('With no site_root_url value defined - Via reverse()'):
            # Test "index" page url.
            response = self.assertResponse('django_expanded_test_cases:index')
            self.assertEqual(response.url, '127.0.0.1/')

            # Test "login" page url.
            response = self.assertResponse('django_expanded_test_cases:login')
            self.assertEqual(response.url, '127.0.0.1/login/')

            # Test "one message" page url.
            response = self.assertResponse('django_expanded_test_cases:one-message')
            self.assertEqual(response.url, '127.0.0.1/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('django_expanded_test_cases:two-messages')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('django_expanded_test_cases:user-detail', args=(1,))
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('django_expanded_test_cases:user-detail', kwargs={'pk': 2})
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')

        with self.subTest('With custom site_root_url value defined'):
            self.site_root_url = 'https://my_really_cool_site.com/'

            # Test "index" page url.
            response = self.assertResponse('django_expanded_test_cases:index')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/')

            # Test "login" page url.
            response = self.assertResponse('django_expanded_test_cases:login')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/login/')

            # Test "one message" page url.
            response = self.assertResponse('django_expanded_test_cases:one-message')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('django_expanded_test_cases:two-messages')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('django_expanded_test_cases:user-detail', args=(1,))
            self.assertEqual(response.url, 'https://my_really_cool_site.com/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('django_expanded_test_cases:user-detail', kwargs={'pk': 2})
            self.assertEqual(response.url, 'https://my_really_cool_site.com/user/detail/2/')

    def test__assertResponse__url_redirect(self):
        """
        Tests "url_redirect" functionality of assertResponse() function.
        """
        exception_msg = 'Response didn\'t redirect as expected. Response code was 200 (expected 302).'

        with self.subTest('With view that redirects'):
            # Using direct url.
            self.assertResponse('redirect/index/')
            self.assertResponse('redirect/index/', expected_redirect_url='/')
            self.assertResponse('redirect/index/', expected_redirect_url='django_expanded_test_cases:index')

            # Using reverse.
            self.assertResponse('django_expanded_test_cases:redirect-to-index')
            self.assertResponse('django_expanded_test_cases:redirect-to-index', expected_redirect_url='/')
            self.assertResponse(
                'django_expanded_test_cases:redirect-to-index',
                expected_redirect_url='django_expanded_test_cases:index',
            )

        with self.subTest('With view that does not redirect'):
            # Using direct url.
            self.assertResponse('')
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('', expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('', expected_redirect_url='django_expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('login/', expected_redirect_url='django_expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)

            # Using reverse.
            self.assertResponse('django_expanded_test_cases:index')
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_redirect_url='django_expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:login', expected_redirect_url='django_expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)

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

    def test__assertResponse__status_code(self):
        """
        Tests "status_code" functionality of assertResponse() function.
        """
        exception_msg = '{0} != {1} : Expected status code (after potential redirects) of "{1}". Actual code was "{0}".'

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
            self.assertEqual(str(err.exception), exception_msg.format(200, 400))

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
            self.assertEqual(str(err.exception), exception_msg.format(200, 500))

        with self.subTest('With status_code=404'):
            # Test 404 in direct url.
            response = self.assertResponse('bad_url', expected_status=404)
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via args.
            response = self.assertResponse('django_expanded_test_cases:user-detail', args=(234,), expected_status=404)
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via kwargs.
            response = self.assertResponse('django_expanded_test_cases:user-detail', kwargs={'pk': 345}, expected_status=404)
            self.assertEqual(response.status_code, 404)

            # With non-404 code provided.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('bad_url', expected_status=200)
            self.assertEqual(str(err.exception), exception_msg.format(404, 200))

    def test__assertResponse__expected_title(self):
        """
        Tests "expected_title" functionality of assertResponse() function.
        """
        exception_msg = (
            'Expected title HTML contents of "Wrong Title" (using exact matching). '
            'Actual value was "Home Page | Test Views".'
        )

        with self.subTest('Title match'):
            self.assertResponse('django_expanded_test_cases:index', expected_title='Home Page | Test Views')

        with self.subTest('Title mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_title='Wrong Title')
            self.assertEqual(str(err.exception), exception_msg)

    def test__assertResponse__expected_header(self):
        """
        Tests "expected_header" functionality of assertResponse() function.
        """
        exception_msg = 'Expected H1 header HTML contents of "Wrong Header". Actual value was "Home Page Header".'

        with self.subTest('Header match'):
            self.assertResponse('django_expanded_test_cases:index', expected_header='Home Page Header')

        with self.subTest('Header mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_header='Wrong Header')
            self.assertEqual(str(err.exception), exception_msg)

    def test__assertResponse__expected_messages(self):
        """
        Tests "expected_messages" functionality of assertResponse() function.
        """
        exception_msg = 'Failed to find message "{0}" in context (Partial matching {1} allowed).'

        with self.subTest('No messages on page - match'):
            self.assertResponse('django_expanded_test_cases:index', expected_messages='')
            self.assertResponse('django_expanded_test_cases:index', expected_messages=[''])

        with self.subTest('No messages on page - mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_messages='Wrong message.')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:index', expected_messages=['Wrong message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))

        with self.subTest('Multiple messages on page - match'):
            self.assertResponse('django_expanded_test_cases:three-messages', expected_messages='Test info message.')
            self.assertResponse('django_expanded_test_cases:three-messages', expected_messages=['Test warning message.'])
            self.assertResponse(
                'django_expanded_test_cases:three-messages',
                expected_messages=['Test info message.', 'Test warning message.'],
            )
            self.assertResponse(
                'django_expanded_test_cases:three-messages',
                expected_messages=['Test info message.', 'Test warning message.', 'Test error message.'],
            )

        with self.subTest('Multiple messages on page - mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('django_expanded_test_cases:three-messages', expected_messages='Wrong message.')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:three-messages',
                    expected_messages=['Test info message.', 'Wrong message.'],
                )
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))

    def test__assertResponse__expected_content(self):
        """
        Tests "expected_content" functionality of assertResponse() function.
        """
        exception_msg = 'Could not find expected content value in response. Provided value was:\n{0}'

        with self.subTest('Content match - With tags'):
            # With non-repeating values.
            self.assertResponse(
                'django_expanded_test_cases:index',
                expected_content=[
                    '<title>Home Page | Test Views</title>',
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is',
                    'the project landing page.</p>',
                ],
            )

            # With repeated values.
            self.assertResponse(
                'django_expanded_test_cases:index',
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
                'django_expanded_test_cases:index',
                expected_content=[
                    'Home Page | Test Views',
                    'Home Page Header',
                    'Pretend this is',
                    'the project landing page.',
                ],
            )

            # With repeated values.
            self.assertResponse(
                'django_expanded_test_cases:index',
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
                self.assertResponse('django_expanded_test_cases:index', expected_content='Wrong value')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong value'))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'django_expanded_test_cases:index',
                    expected_content=[
                        'Home Page Header',
                        'Pretend this is',
                        'Wrong value'
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg.format('Wrong value'))

        with self.subTest('With search subsections'):
            # Strip start.
            self.assertResponse(
                'django_expanded_test_cases:index',
                expected_content='<p>Pretend this is the project landing page.</p>',
                content_starts_after='<h1>Home Page Header</h1>',
            )
            # Strip end.
            self.assertResponse(
                'django_expanded_test_cases:index',
                expected_content='<title>Home Page | Test Views</title>',
                content_ends_before='<h1>Home Page Header</h1>',
            )
            # Strip both.
            self.assertResponse(
                'django_expanded_test_cases:index',
                expected_content='<h1>Home Page Header</h1>',
                content_starts_after='<title>Home Page | Test Views</title>',
                content_ends_before='<p>Pretend this is the project landing page.</p>',
            )

        with self.subTest('With content blocks'):
            # Entire page as one block.
            self.assertResponse(
                'django_expanded_test_cases:index',
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
                'django_expanded_test_cases:index',
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
                'django_expanded_test_cases:index',
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
                'django_expanded_test_cases:index',
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
                'django_expanded_test_cases:index',
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

    def test__assertGetResponse(self):
        """
        Tests assertGetResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """
        response = self.assertGetResponse('django_expanded_test_cases:index')

        self.assertEqual(response.url, '127.0.0.1/')
        self.assertEqual(response.status_code, 200)

    def test__assertPostResponse(self):
        """
        Tests assertPostResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """
        response = self.assertPostResponse('django_expanded_test_cases:index')

        self.assertEqual(response.url, '127.0.0.1/')
        self.assertEqual(response.status_code, 200)

    # endregion Response Assertion Tests

    # region Element Assertion Tests

    def test__assertResponseRedirects__success(self):
        """
        Tests assertResponseRedirects() function, in cases when it should succeed.
        """
        with self.subTest('With view that redirects'):
            # Using direct url.
            self.assertRedirects('redirect/index/', expected_redirect_url='/')
            self.assertRedirects('redirect/index/', expected_redirect_url='django_expanded_test_cases:index')

            # Using reverse.
            self.assertRedirects('django_expanded_test_cases:redirect-to-index', expected_redirect_url='/')
            self.assertRedirects(
                'django_expanded_test_cases:redirect-to-index',
                expected_redirect_url='django_expanded_test_cases:index',
            )

    def test__assertResponseRedirects__failure(self):
        """
        Tests assertResponseRedirects() function, in cases when it should fail.
        """
        exception_msg = 'Response didn\'t redirect as expected. Response code was {0} (expected 302).'

        with self.subTest('With view that does not redirect - Invalid page'):
            request = self._get_page_response('bad_page/')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='django_expanded_test_cases:invalid')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))

        with self.subTest('With view that does not redirect - Index page'):
            request = self._get_page_response('')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='django_expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))

        with self.subTest('With view that does not redirect - Non-index page'):
            request = self._get_page_response('login/')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='django_expanded_test_cases:login')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))

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
            self.assertEqual(str(err.exception), exception_msg.format('404', '200'))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 200)
            self.assertEqual(str(err.exception), exception_msg.format('404', '200'))

        with self.subTest('Expected 404, got 200'):
            response = HttpResponse(status=200)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 404)
            self.assertEqual(str(err.exception), exception_msg.format('200', '404'))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 404)
            self.assertEqual(str(err.exception), exception_msg.format('200', '404'))

        with self.subTest('Expected 200, got 500'):
            response = HttpResponse(status=500)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 200)
            self.assertEqual(str(err.exception), exception_msg.format('500', '200'))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 200)
            self.assertEqual(str(err.exception), exception_msg.format('500', '200'))

        with self.subTest('Expected 500, got 200'):
            response = HttpResponse(status=200)
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response, 500)
            self.assertEqual(str(err.exception), exception_msg.format('200', '500'))
            with self.assertRaises(AssertionError) as err:
                self.assertStatusCode(response.status_code, 500)
            self.assertEqual(str(err.exception), exception_msg.format('200', '500'))

    def test__assertPageTitle__success(self):
        """
        Tests assertPageTitle() function, in cases when it should succeed.
        """
        with self.subTest('Including title tag in expected'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, '<title>Test Title</title>')

        with self.subTest('Including title tag in expected, with extra whitespace around tag'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, '   <title>    Test Title    </title>   ')

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
            self.assertPageTitle(response, 'Test Title | My Custom App | My Really Cool Site', exact_match=True)

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating) - Exact Match'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertPageTitle(response, 'Test Title | My Custom App | My Really Cool Site', exact_match=True)

        with self.subTest('Complex title - Loose Match'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertPageTitle(response, 'Test Title', exact_match=False)
            self.assertPageTitle(response, 'My Custom App', exact_match=False)
            self.assertPageTitle(response, 'My Really Cool Site', exact_match=False)

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating) - Loose Match'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertPageTitle(response, 'Test Title', exact_match=False)
            self.assertPageTitle(response, 'My Custom App', exact_match=False)
            self.assertPageTitle(response, 'My Really Cool Site', exact_match=False)

    def test__assertPageTitle__failure(self):
        """
        Tests assertPageTitle() function, in cases when it should fail.
        """
        exception_msg = 'Expected title HTML contents of "{0}" (using exact matching). Actual value was "{1}".'

        with self.subTest('Checking for title when none exists'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertPageTitle(response, 'Test Title')
            self.assertEqual(str(err.exception), exception_msg.format('Test Title', ''))

        with self.subTest('Expected value is on page, but not in title tag'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Test Title')
            self.assertEqual(str(err.exception), exception_msg.format('Test Title', ''))
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><p>Test Title</p>')
                self.assertPageTitle(response, 'Test Title')
            self.assertEqual(str(err.exception), exception_msg.format('Test Title', ''))

        with self.subTest('Assuming extra whitespace is still present'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>   Test    Title   </title>')
                self.assertPageTitle(response, '   Test    Title   ')
            self.assertEqual(str(err.exception), exception_msg.format('Test    Title', 'Test Title'))

        with self.subTest('Set to exact match, but only passing in title subsection'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'Test Title')
            self.assertEqual(str(err.exception), exception_msg.format(
                'Test Title',
                'Test Title | My Custom App | My Really Cool Site',
            ))
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'My Custom App')
            self.assertEqual(str(err.exception), exception_msg.format(
                'My Custom App',
                'Test Title | My Custom App | My Really Cool Site',
            ))
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'My Really Cool Site')
            self.assertEqual(str(err.exception), exception_msg.format(
                'My Really Cool Site',
                'Test Title | My Custom App | My Really Cool Site',
            ))

        with self.subTest('Set to partial match, but value is not in title'):
            # Full mismatch.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Wrong Value')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong Value', ''))
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title</title>')
                self.assertPageTitle(response, 'Wrong Value')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong Value', 'Test Title'))

            # Partial match, but also has extra.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Test Title and More')
            self.assertEqual(str(err.exception), exception_msg.format('Test Title and More', ''))
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Test Title</title>')
                self.assertPageTitle(response, 'Test Title and More')
            self.assertEqual(str(err.exception), exception_msg.format('Test Title and More', 'Test Title'))

        with self.subTest('Multiple Titles - Two and no spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Title 1</title><title>Title 2</title>')
                self.assertPageTitle(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple titles (2 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                )
            )

        with self.subTest('Multiple Titles - Two with spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title > Title 1 < /title><title > Title 2 < /title>')
                self.assertPageTitle(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple titles (2 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                )
            )

        with self.subTest('Multiple Titles - Two with line breaks'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Title 1</title>\n<br>\n<title>Title 2</title>')
                self.assertPageTitle(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple titles (2 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                )
            )

        with self.subTest('Multiple Titles - Three'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<title>Title 1</title><title>Title 2</title><title>Title 3</title>')
                self.assertPageTitle(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple titles (3 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                )
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
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple titles (5 total). There should only be one <title> tag per page.\n'
                    'For further reference on <title> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_title.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title'
                )
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
            self.assertEqual(str(err.exception), exception_msg.format('Test Header', ''))

        with self.subTest('Expected value is on page, but not in header tag'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('Test Header')
                self.assertPageHeader(response, 'Test Header')
            self.assertEqual(str(err.exception), exception_msg.format('Test Header', ''))
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h2>Test Header</h2><p>Test Header</p>')
                self.assertPageHeader(response, 'Test Header')
            self.assertEqual(str(err.exception), exception_msg.format('Test Header', ''))

        with self.subTest('Assuming extra whitespace is still present'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>   Test    Header   </h1>')
                self.assertPageHeader(response, '   Test    Header   ')
            self.assertEqual(str(err.exception), exception_msg.format('Test    Header', 'Test Header'))

        with self.subTest('Expected value is present, plus extra'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Header</h1>')
                self.assertPageHeader(response, 'Test Header plus Extra')
            self.assertEqual(str(err.exception), exception_msg.format('Test Header plus Extra', 'Test Header'))

        with self.subTest('Multiple Headers - Two and no spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Header 1</h1><h1>Header 2</h1>')
                self.assertPageHeader(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple headers (2 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                )
            )

        with self.subTest('Multiple Headers - Two with spaces'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1 > Header 1 < /h1><h1 > Header 2 < /h1>')
                self.assertPageHeader(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple headers (2 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                )
            )

        with self.subTest('Multiple Headers - Two with line breaks'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Header 1</h1>\n<br>\n<h1>Header 2</h1>')
                self.assertPageHeader(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple headers (2 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                )
            )

        with self.subTest('Multiple Headers - Three'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Header 1</h1><h1>Header 2</h1><h1>Header 3</h1>')
                self.assertPageHeader(response, '')
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple headers (3 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                )
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
            self.assertEqual(
                str(err.exception),
                (
                    'Found multiple headers (5 total). There should only be one <h1> tag per page.\n'
                    'For further reference on <h1> tags, consider consulting:\n'
                    '    * https://www.w3schools.com/tags/tag_hn.asp\n'
                    '    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements'
                )
            )

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', True)
    def test__assertContextMessages__success__allow_partials(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        We only do a minimal amount of testing for this function here.
        We assume a majority of testing will occur in the "disallow_partials" set.
        """
        with self.subTest('Check for single message partial, single message exists'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            self.assertContextMessages(response, 'This is a test message.')
            self.assertContextMessages(response, 'is a test message')
            self.assertContextMessages(response, 'test')

        with self.subTest('Check for three message partials, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:three-messages')
            self.assertContextMessages(response, ['info', 'warning message', 'Test error'])

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertContextMessages__success__disallow_partials(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        The majority of tests for this function exist here.
        """
        with self.subTest('Check for single message, single message exists'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            self.assertContextMessages(response, 'This is a test message.')

        with self.subTest('Check for single message, two messages exists'):
            response = self._get_page_response('django_expanded_test_cases:two-messages')
            self.assertContextMessages(response, 'Test message #1.')
            self.assertContextMessages(response, 'Test message #2.')

        with self.subTest('Check for single message, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:three-messages')
            self.assertContextMessages(response, 'Test info message.')
            self.assertContextMessages(response, 'Test warning message.')
            self.assertContextMessages(response, 'Test error message.')

        with self.subTest('Check for two messages, two messages exists'):
            response = self._get_page_response('django_expanded_test_cases:two-messages')
            self.assertContextMessages(response, ['Test message #1.', 'Test message #2.'])

        with self.subTest('Check for two messages, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:three-messages')
            self.assertContextMessages(response, ['Test info message.', 'Test warning message.'])
            self.assertContextMessages(response, ['Test info message.', 'Test error message.'])
            self.assertContextMessages(response, ['Test warning message.', 'Test error message.'])

        with self.subTest('Check for three messages, three messages exists'):
            response = self._get_page_response('django_expanded_test_cases:three-messages')
            self.assertContextMessages(response, ['Test info message.', 'Test warning message.', 'Test error message.'])

    @patch('django_expanded_test_cases.test_cases.integration_test_case.ETC_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertContextMessages__failure(self):
        """
        Tests assertContextMessages() function, in cases when it should fail.
        """
        exception_msg = 'Failed to find message "{0}" in context (Partial matching {1} allowed).'

        with self.subTest('Checking for single message, none exist'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:index')
                self.assertContextMessages(response, 'This is a test message.')
            self.assertEqual(str(err.exception), exception_msg.format('This is a test message.', 'is NOT'))

        with self.subTest('Checking for single message, one exists but doesn\'t match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:one-message')
                self.assertContextMessages(response, 'Testing!')
            self.assertEqual(str(err.exception), exception_msg.format('Testing!', 'is NOT'))

        with self.subTest('Checking for single message, but it\'s only a partial match'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, 'This is a test message')
            self.assertEqual(str(err.exception), exception_msg.format('This is a test message', 'is NOT'))
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, 'test message.')
            self.assertEqual(str(err.exception), exception_msg.format('test message.', 'is NOT'))
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, 'test')
            self.assertEqual(str(err.exception), exception_msg.format('test', 'is NOT'))

        with self.subTest('Checking for single message, multiple exist but don\'t match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:three-messages')
                self.assertContextMessages(response, 'Testing!')
            self.assertEqual(str(err.exception), exception_msg.format('Testing!', 'is NOT'))

        with self.subTest('Checking for two messages, none exist'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:index')
                self.assertContextMessages(response, ['This is a test message.', 'Another message.'])
            self.assertEqual(str(err.exception), exception_msg.format('This is a test message.', 'is NOT'))

        with self.subTest('Checking for two messages, but only one exists'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:one-message')
                self.assertContextMessages(response, ['This is a test message.', 'Another message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Another message.', 'is NOT'))

        with self.subTest('Checking for two messages, multiple exist but one doesn\'t match'):
            response = self._get_page_response('django_expanded_test_cases:three-messages')
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, ['Test info message.', 'Another message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Another message.', 'is NOT'))
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, ['Bad message', 'Test info message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Bad message', 'is NOT'))

        with self.subTest('Checking for two messages, multiple exist but none match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:three-messages')
                self.assertContextMessages(response, ['Testing!', 'Testing again!'])
            self.assertEqual(str(err.exception), exception_msg.format('Testing!', 'is NOT'))

    def test__assertPageContent__success(self):
        """
        Tests assertPageContent() function, in cases when it should succeed.
        """
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
            self.assertPageContent(response, '<h1>Login Page Header</h1><p>Pretend this is a login page.</p>')

        with self.subTest('Standard Response, missing part of value'):
            response = self._get_page_response('django_expanded_test_cases:login')
            self.assertPageContent(response, '<h1>Login Page Header</h1>')
            self.assertPageContent(response, '<p>Pretend this is a login page.</p>')

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('django_expanded_test_cases:index')
            self.assertPageContent(response, '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>')

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('django_expanded_test_cases:template-response-index')
            self.assertPageContent(response, '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>')

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            self.assertPageContent(
                response,
                (
                    '<ul><li><p>This is a test message.</p></li></ul>'
                    '<h1>View with One Message Header</h1>'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>'
                ),
            )

        with self.subTest('Standard Response - Set of items on index page'):
            response = self._get_page_response('django_expanded_test_cases:index')
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
            response = self._get_page_response('django_expanded_test_cases:user-detail', args=(1,))

            # Standard, ordered page match.
            self.assertPageContent(
                response,
                [
                    '<h1>User Detail Page Header</h1>',
                    'Username: "test_superuser"',
                    'First Name: "TestFirst"',
                    'Last Name: "TestLast"',
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
                    'First Name: "TestFirst"',
                    'Last Name: "TestLast"',
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                    'TestFirst',
                    'TestLast',
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
                    'First Name: "TestFirst"',
                    'Last Name: "TestLast"',
                    '<h1>User Detail Page Header</h1>',
                ],
                ignore_ordering=True,  # Ignore because unordered.
            )

        with self.subTest('Standard Response - Set of items on user page - As Tuple'):
            response = self._get_page_response('django_expanded_test_cases:user-detail', args=(1,))

            # Standard, ordered page match.
            self.assertPageContent(
                response,
                (
                    '<h1>User Detail Page Header</h1>',
                    'Username: "test_superuser"',
                    'First Name: "TestFirst"',
                    'Last Name: "TestLast"',
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
                    'First Name: "TestFirst"',
                    'Last Name: "TestLast"',
                    'Is Active: "True"',
                    'Is SuperUser: "True"',
                    'Is Staff: "False"',
                    'TestFirst',
                    'TestLast',
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
                    'First Name: "TestFirst"',
                    'Last Name: "TestLast"',
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
            response = self._get_page_response('django_expanded_test_cases:index')
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
            response = self._get_page_response('django_expanded_test_cases:index')

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
            response = self._get_page_response('django_expanded_test_cases:index')

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
            response = self._get_page_response('django_expanded_test_cases:index')

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
            response = self._get_page_response('django_expanded_test_cases:index')

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
            response = self._get_page_response('django_expanded_test_cases:index')

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
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Test Title</h1>'))

        with self.subTest('Minimal Response - Wrong value passed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>Testing</h1>')
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Testing</h1>'))

        with self.subTest('Standard Response - Wrong value passed'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:login')
                self.assertPageContent(response, '<h1>Testing Header</h1><p>Pretend this is a page.</p>')
            self.assertEqual(
                str(err.exception),
                exception_msg_not_found.format('<h1>Testing Header</h1><p>Pretend this is a page.</p>'),
            )

        with self.subTest('Standard Response - Set of items with wrong values'):
            response = self._get_page_response('django_expanded_test_cases:index')

            # Test as list.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ['<h1>Test Page Header</h1>'])
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Test Page Header</h1>'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ['Wrong Content'])
            self.assertEqual(str(err.exception), exception_msg_not_found.format('Wrong Content'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ['<h1>Home Page Wrong'])
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Home Page Wrong'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ['Wrong Page Header</h1>'])
            self.assertEqual(str(err.exception), exception_msg_not_found.format('Wrong Page Header</h1>'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ['<h1>Home Page Header</h1>', 'Wrong text'])
            self.assertEqual(str(err.exception), exception_msg_not_found.format('Wrong text'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ['<h1>Wrong Header</h1>', 'project landing page'])
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Wrong Header</h1>'))
            # Test as tuple.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ('<h1>Test Page Header</h1>',))
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Test Page Header</h1>'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ('Wrong Content',))
            self.assertEqual(str(err.exception), exception_msg_not_found.format('Wrong Content'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ('<h1>Home Page Wrong',))
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Home Page Wrong'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ('Wrong Page Header</h1>',))
            self.assertEqual(str(err.exception), exception_msg_not_found.format('Wrong Page Header</h1>'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ('<h1>Home Page Header</h1>', 'Wrong text'))
            self.assertEqual(str(err.exception), exception_msg_not_found.format('Wrong text'))
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(response, ('<h1>Wrong Header</h1>', 'project landing page'))
            self.assertEqual(str(err.exception), exception_msg_not_found.format('<h1>Wrong Header</h1>'))

        with self.subTest('Standard Response - Wrong ordering'):
            response = self._get_page_response('django_expanded_test_cases:user-detail', args=(1,))

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string at top.
                self.assertPageContent(
                    response,
                    [
                        'First Name: "TestFirst"',
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "TestLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg_bad_order.format('<h1>User Detail Page Header</h1>'))

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after header.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'First Name: "TestFirst"',
                        'Username: "test_superuser"',
                        'Last Name: "TestLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg_bad_order.format('Username: "test_superuser"'))

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after last name.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "TestLast"',
                        'First Name: "TestFirst"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg_bad_order.format('First Name: "TestFirst"'))

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after active.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "TestLast"',
                        'Is Active: "True"',
                        'First Name: "TestFirst"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg_bad_order.format('First Name: "TestFirst"'))

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after superuser.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "TestLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'First Name: "TestFirst"',
                        'Is Staff: "False"',
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg_bad_order.format('First Name: "TestFirst"'))

            with self.assertRaises(AssertionError) as err:
                # Test "first name" string after staff.
                self.assertPageContent(
                    response,
                    [
                        '<h1>User Detail Page Header</h1>',
                        'Username: "test_superuser"',
                        'Last Name: "TestLast"',
                        'Is Active: "True"',
                        'Is SuperUser: "True"',
                        'Is Staff: "False"',
                        'First Name: "TestFirst"',
                    ],
                )
            self.assertEqual(str(err.exception), exception_msg_bad_order.format('First Name: "TestFirst"'))

    def test__assertPageContent__failure__with_bad_search_space(self):
        exception_msg = 'Could not find "{0}" value in content response. Provided value was:\n{1}'
        response = self._get_page_response('django_expanded_test_cases:index')

        # Bad content_starts_after values.
        with self.subTest('With content_starts_after not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_starts_after='Wrong value.',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', 'Wrong value.'))
        with self.subTest('With content_starts_after not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='Wrong content value.',
                    content_starts_after='Wrong value.',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', 'Wrong value.'))
        with self.subTest('With content_starts_after found with extra'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_starts_after='Home Page Header plus Extra',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', 'Home Page Header plus Extra'),
            )

        # Bad content_ends_before values.
        with self.subTest('With content_ends_before not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_ends_before='Wrong value.',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', 'Wrong value.'))
        with self.subTest('With content_ends_before and expected_content not found'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='Wrong content value.',
                    content_ends_before='Wrong value.',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', 'Wrong value.'))
        with self.subTest('With content_ends_before found with extra'):
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_ends_before='Home Page Header plus Extra',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', 'Home Page Header plus Extra'),
            )

    def test__assertPageContent__fail__with_limited_search_space(self):
        exception_msg = 'Expected content value was found, but occurred in "{0}" section. Expected was:\n{1}'
        response = self._get_page_response('django_expanded_test_cases:index')

        with self.subTest('Standard Response - With content_starts_after defined'):
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<head>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '<head>'))
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<meta charset="utf-8">',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '<meta charset="utf-8">'))
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='</head>',
                    content_starts_after='<h1>Home Page Header</h1>',
                    ignore_ordering=True,
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '</head>'))
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<body>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '<body>'))
            # Expected as single value - With exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '<h1>Home Page Header</h1>'))
            # Expected as single value - With partial of exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='h1>',
                    content_starts_after='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', 'h1>'))

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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<title>Home Page | Test Views</title>'),
            )

        with self.subTest('Standard Response - With content_ends_before defined'):
            response = self._get_page_response('django_expanded_test_cases:index')

            # Expected as single value - Exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<h1>Home Page Header</h1>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', '<h1>Home Page Header</h1>'))
            # Expected as single value - Partial of exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='h1>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', 'h1>'))
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<p>Pretend this is the project landing page.</p>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
            )
            # Expected as single value - With ignore_ordering (should have no effect here).
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<p>Pretend this is the project landing page.</p>',
                    ignore_ordering=True,
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
            )
            # Expected as single value.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='</body>',
                    content_ends_before='<h1>Home Page Header</h1>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', '</body>'))

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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
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
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', '</body>'))

        with self.subTest('Standard Response - With both content containers defined'):
            response = self._get_page_response('django_expanded_test_cases:index')

            # Expected as single value - above search area.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<meta charset="utf-8">',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
            )
            # Expected as single value - above search area, exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<title>Home Page | Test Views</title>',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<title>Home Page | Test Views</title>'),
            )
            # Expected as single value - below search area.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='</body>',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', '</body>'))
            # Expected as single value - below search area, exact match.
            with self.assertRaises(AssertionError) as err:
                self.assertPageContent(
                    response,
                    expected_content='<p>Pretend this is the project landing page.</p>',
                    content_starts_after='<title>Home Page | Test Views</title>',
                    content_ends_before='<p>Pretend this is the project landing page.</p>',
                )
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', '<p>Pretend this is the project landing page.</p>'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
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
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '<head>'))
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
            self.assertEqual(str(err.exception), exception_msg.format('content_starts_after', '<head>'))
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_starts_after', '<meta charset="utf-8">'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', 'the project landing page.</p>'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('content_ends_before', 'the project landing page.</p>'),
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
            self.assertEqual(str(err.exception), exception_msg.format('content_ends_before', '</body>'))

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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1> ...'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <div>123456789</div><h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>This is a test p tag.</p></div><h1>Test Title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... est p tag.</p></div><h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>Testing</p><h1>Test Title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <p>Testing</p><h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <div>123456789</div><h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>This is a test p tag.</p></div><h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... est p tag.</p></div><h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>Testing</p><h1>Test Title</h1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <p>Testing</p><h1>Test Title</h1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV>123456789</DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <DIV>123456789</DIV><H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV><P>THIS IS A TEST P TAG.</P></DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... EST P TAG.</P></DIV><H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<P>TESTING</P><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <P>TESTING</P><H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV>123456789</DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <DIV>123456789</DIV><H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<DIV><P>THIS IS A TEST P TAG.</P></DIV><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... EST P TAG.</P></DIV><H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<P>TESTING</P><H1>TEST TITLE</H1>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <P>TESTING</P><H1>TEST TITLE</H1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <div>123456789</div><h1>test title</h1> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>this is a test p tag.</p></div><h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... est p tag.</p></div><h1>test title</h1> ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>testing</p><h1>test title</h1>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <p>testing</p><h1>test title</h1> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div>123456789</div><h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <div>123456789</div><h1>test title</h1> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<div><p>this is a test p tag.</p></div><h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... est p tag.</p></div><h1>test title</h1> ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<p>testing</p><h1>test title</h1>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <p>testing</p><h1>test title</h1> ...'),
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
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1><div>123456789</div> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div><p>This is a test p tag.</p></div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1><div><p>This is a te ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><p>Testing</p>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>Test Title</h1><p>Testing</p> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div>123456789</div>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1><div>123456789</div> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><div><p>This is a test p tag.</p></div>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1><div><p>This is a te ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>Test Title</h1><p>Testing</p>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <h1>Test Title</h1><p>Testing</p> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV>123456789</DIV>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1><DIV>123456789</DIV> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV><P>THIS IS A TEST P TAG.</P></DIV>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1><DIV><P>THIS IS A TE ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><P>TESTING</P>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <H1>TEST TITLE</H1><P>TESTING</P> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV>123456789</DIV>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1><DIV>123456789</DIV> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><DIV><P>THIS IS A TEST P TAG.</P></DIV>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1><DIV><P>THIS IS A TE ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response upper and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<H1>TEST TITLE</H1><P>TESTING</P>')
                self.assertPageContent(response, '<h1>test title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>test title</h1>', '... <H1>TEST TITLE</H1><P>TESTING</P> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div>123456789</div>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1><div>123456789</div> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div><p>this is a test p tag.</p></div>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1><div><p>this is a te ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><p>testing/p>')
                self.assertPageContent(response, '<h1>Test Title</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<h1>Test Title</h1>', '... <h1>test title</h1><p>testing/p> ...'),
            )

        with self.subTest('Minimal Response - Exact Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div>123456789</div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1><div>123456789</div> ...'),
            )

        with self.subTest('Minimal Response - Extra Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><div><p>this is a test p tag.</p></div>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1><div><p>this is a te ...'),
            )

        with self.subTest('Minimal Response - Lesser Match - With response lower and check upper'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<h1>test title</h1><p>testing/p>')
                self.assertPageContent(response, '<H1>TEST TITLE</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format('<H1>TEST TITLE</H1>', '... <h1>test title</h1><p>testing/p> ...'),
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
                response = self._get_page_response('django_expanded_test_cases:index')
                self.assertPageContent(response, '<H1>HOME PAGE HEADER</H1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format(
                    '<H1>HOME PAGE HEADER</H1>',
                    '... /title></head><body><h1>Home Page Header</h1><p>Pretend this is t ...'
                ),
            )

        with self.subTest('Standard Response - With response mixed and check lower'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:index')
                self.assertPageContent(response, '<h1>home page header</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format(
                    '<h1>home page header</h1>',
                    '... /title></head><body><h1>Home Page Header</h1><p>Pretend this is t ...'
                ),
            )

        with self.subTest('Standard Response - With response mixed and check mixed'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('django_expanded_test_cases:index')
                self.assertPageContent(response, '<h1>home Page header</h1>')
            self.assertEqual(
                str(err.exception),
                exception_msg.format(
                    '<h1>home Page header</h1>',
                    '... /title></head><body><h1>Home Page Header</h1><p>Pretend this is t ...'
                ),
            )

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
            self.assertEqual(
                str(err.exception),
                'The assertRepeatingElement() function requires an element occurs one or more times.',
            )

        # Empty response tests.
        with self.subTest('Empty response, when one item is expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 0))

        with self.subTest('Empty response, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), exception_msg.format(2, 0))

        with self.subTest('Empty response, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), exception_msg.format(3, 0))

        with self.subTest('Empty response, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), exception_msg.format(4, 0))

        # Single item response tests.
        with self.subTest('Response with one item, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), exception_msg.format(2, 1))

        with self.subTest('Response with one item, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), exception_msg.format(3, 1))

        with self.subTest('Response with one item, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), exception_msg.format(4, 1))

        # Two item response tests.
        with self.subTest('Response with two items, when one item is expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 2))
            # With spaces
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 2))

        with self.subTest('Response with two items, when three items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), exception_msg.format(3, 2))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), exception_msg.format(3, 2))

        with self.subTest('Response with two items, when four items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), exception_msg.format(4, 2))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), exception_msg.format(4, 2))

        # Three item response tests.
        with self.subTest('Response with three items, when one item is expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 3))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 3))

        with self.subTest('Response with three items, when two items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), exception_msg.format(2, 3))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), exception_msg.format(2, 3))

        with self.subTest('Response with three items, when four items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), exception_msg.format(4, 3))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), exception_msg.format(4, 3))

        # Four item response tests.
        with self.subTest('Response with four items, when one item is expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 4))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), exception_msg.format(1, 4))

        with self.subTest('Response with four items, when two items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), exception_msg.format(2, 4))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), exception_msg.format(2, 4))

        with self.subTest('Response with four items, when three items are expected'):
            # No spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li><li></li><li></li><li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), exception_msg.format(3, 4))
            # With spaces.
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), exception_msg.format(3, 4))

    def test__assertRepeatingElement__fail__incomplete_items(self):
        open_exception_msg = 'Expected {0} element opening tags. Found {1}.'
        close_exception_msg = 'Expected {0} element closing tags. Found {1}.'

        with self.subTest('Response with one plus partial items, when one item is expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), open_exception_msg.format(1, 2))

        with self.subTest('Response with one plus partial items, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), close_exception_msg.format(2, 1))

        with self.subTest('Response with two plus partial items, when one item is expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 1)
            self.assertEqual(str(err.exception), open_exception_msg.format(1, 3))

        with self.subTest('Response with two plus partial items, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), open_exception_msg.format(2, 3))

        with self.subTest('Response with two plus partial items, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), close_exception_msg.format(3, 2))

        with self.subTest('Response with three plus partial items, when two items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 2)
            self.assertEqual(str(err.exception), open_exception_msg.format(2, 4))

        with self.subTest('Response with three plus partial items, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), open_exception_msg.format(3, 4))

        with self.subTest('Response with three plus partial items, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), close_exception_msg.format(4, 3))

        with self.subTest('Response with four plus partial items, when three items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 3)
            self.assertEqual(str(err.exception), open_exception_msg.format(3, 5))

        with self.subTest('Response with four plus partial items, when four items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 4)
            self.assertEqual(str(err.exception), open_exception_msg.format(4, 5))

        with self.subTest('Response with four plus partial items, when five items are expected'):
            with self.assertRaises(AssertionError) as err:
                response = HttpResponse('<li></li> <li></li> <li></li> <li></li> <li>')
                self.assertRepeatingElement(response, '<li>', 5)
            self.assertEqual(str(err.exception), close_exception_msg.format(5, 4))

    # endregion Element Assertion Tests

    # endregion Assertion Tests

    # region Helper Function Tests

    def test___get_login_user__verify_login(self):
        """"""
        with self.subTest('Auto login as test user'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should log in provided user.
            return_val = self._get_login_user('test_user', auto_login=True)
            self.assertEqual(return_val, self.test_user)

            # Verify user is now logged in.
            self.assertIn('_auth_user_id', self.client.session.keys())
            self.assertEqual(str(self.test_user.pk), self.client.session['_auth_user_id'])

        # Reset login state.
        self.client.logout()

        with self.subTest('Auto login as test admin'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should log in provided user.
            return_val = self._get_login_user(self.test_admin, auto_login=True)
            self.assertEqual(return_val, self.test_admin)

            # Verify user is now logged in.
            self.assertIn('_auth_user_id', self.client.session.keys())
            self.assertEqual(str(self.test_admin.pk), self.client.session['_auth_user_id'])

        # Reset login state.
        self.client.logout()

        with self.subTest('Auto login as test superuser'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should log in provided user.
            return_val = self._get_login_user('test_superuser', auto_login=True)
            self.assertEqual(return_val, self.test_superuser)

            # Verify user is now logged in.
            self.assertIn('_auth_user_id', self.client.session.keys())
            self.assertEqual(str(self.test_superuser.pk), self.client.session['_auth_user_id'])

        # Reset login state.
        self.client.logout()

        with self.subTest('No login as test user'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should not log in provided user.
            return_val = self._get_login_user('test_user', auto_login=False)
            self.assertEqual(return_val, self.test_user)

            # Verify user is still not logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

        # Reset login state.
        self.client.logout()

        with self.subTest('No login as test admin'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should not log in provided user.
            return_val = self._get_login_user('test_admin', auto_login=False)
            self.assertEqual(return_val, self.test_admin)

            # Verify user is still not logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

        # Reset login state.
        self.client.logout()

        with self.subTest('No login as test superuser'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should not log in provided user.
            return_val = self._get_login_user('test_superuser', auto_login=False)
            self.assertEqual(return_val, self.test_superuser)

            # Verify user is still not logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

    def test___get_login_user__set_permissions(self):
        """"""
        # Generate dummy content_type.
        test_content_type = ContentType.objects.create(app_label='test_app', model='test_model')

        # Initialize Permission models.
        perm_1 = Permission.objects.create(
            content_type=test_content_type,
            codename='test_perm_1',
            name='Test Perm 1',
        )
        perm_2 = Permission.objects.create(
            content_type=test_content_type,
            codename='test_perm_2',
            name='Test Perm 2',
        )
        perm_3 = Permission.objects.create(
            content_type=test_content_type,
            codename='test_perm_3',
            name='Test Perm 3',
        )

        # Verify initial user Permissions.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test adding single permission'):
            # Test adding permission.
            return_val = self._get_login_user(self.test_user, user_permissions='test_perm_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self._get_login_user('test_admin', user_permissions='test_perm_2')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test adding multiple permissions'):
            # Test adding permission.
            return_val = self._get_login_user('test_user', user_permissions=['test_perm_1', 'Test Perm 2'])
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 2)
            self.assertIn(perm_1, self.test_user.user_permissions.all())
            self.assertIn(perm_2, self.test_user.user_permissions.all())

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self._get_login_user(self.test_admin, user_permissions=[perm_2, 'test_perm_3'])
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 2)
            self.assertIn(perm_1, self.test_user.user_permissions.all())
            self.assertIn(perm_2, self.test_user.user_permissions.all())
            self.assertEqual(self.test_admin.user_permissions.all().count(), 2)
            self.assertIn(perm_2, self.test_admin.user_permissions.all())
            self.assertIn(perm_3, self.test_admin.user_permissions.all())

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

    def test___get_login_user__set_groups(self):
        """"""
        # Initialize Group models.
        group_1 = Group.objects.create(name='group_1')
        group_2 = Group.objects.create(name='group_2')
        group_3 = Group.objects.create(name='group_3')

        with self.subTest('Test adding single group'):
            # Verify initial user Groups.
            self.assertFalse(self.test_superuser.groups.all().exists())
            self.assertFalse(self.test_admin.groups.all().exists())
            self.assertFalse(self.test_user.groups.all().exists())

            # Test adding group.
            return_val = self._get_login_user('test_user', user_groups='group_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.groups.all().exists())
            self.assertFalse(self.test_superuser.groups.all().exists())

            # Test adding different group.
            return_val = self._get_login_user(self.test_admin, user_groups='group_2')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.groups.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test adding multiple group'):
            # Test adding group.
            return_val = self._get_login_user('test_user', user_groups=['group_1', group_2])
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 2)
            self.assertIn(group_1, self.test_user.groups.all())
            self.assertIn(group_2, self.test_user.groups.all())

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.groups.all().exists())
            self.assertFalse(self.test_superuser.groups.all().exists())

            # Test adding different group.
            return_val = self._get_login_user(self.test_admin, user_groups=['group_2', group_3])
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 2)
            self.assertIn(group_1, self.test_user.groups.all())
            self.assertIn(group_2, self.test_user.groups.all())
            self.assertEqual(self.test_admin.groups.all().count(), 2)
            self.assertIn(group_2, self.test_admin.groups.all())
            self.assertIn(group_3, self.test_admin.groups.all())

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.groups.all().exists())

    def test__get_page_title__empty_title(self):
        """
        Tests get_page_title() function, when page title is empty.
        """
        with self.subTest('No title element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertEqual(self.get_page_title(response), '')
            self.assertEqual(self.get_page_title(response.content), '')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), '')

        with self.subTest('Title exists, but is empty'):
            response = HttpResponse('<title></title>')
            self.assertEqual(self.get_page_title(response), '')
            self.assertEqual(self.get_page_title(response.content), '')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), '')

        with self.subTest('Title exists, but is whitespace'):
            response = HttpResponse('<title>   </title>')
            self.assertEqual(self.get_page_title(response), '')
            self.assertEqual(self.get_page_title(response.content), '')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), '')

    def test__get_page_title__populated_title(self):
        """
        Tests get_page_title() function, when page title is populated.
        """
        with self.subTest('Basic title'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertEqual(self.get_page_title(response), 'Test Title')
            self.assertEqual(self.get_page_title(response.content), 'Test Title')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), 'Test Title')

        with self.subTest('Basic title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<title>   Test    Title   </title>')
            self.assertEqual(self.get_page_title(response), 'Test Title')
            self.assertEqual(self.get_page_title(response.content), 'Test Title')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), 'Test Title')

        with self.subTest('Complex title'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertEqual(self.get_page_title(response), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(self.get_page_title(response.content), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(
                self.get_page_title(response.content.decode('utf-8')),
                'Test Title | My Custom App | My Really Cool Site',
            )

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertEqual(self.get_page_title(response), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(self.get_page_title(response.content), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(
                self.get_page_title(response.content.decode('utf-8')),
                'Test Title | My Custom App | My Really Cool Site',
            )

    def test__get_page_header__empty_header(self):
        """
        Tests get_page_header() function, when page H1 header is empty.
        """
        with self.subTest('No header element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertEqual(self.get_page_header(response), '')
            self.assertEqual(self.get_page_header(response.content), '')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), '')

        with self.subTest('Header exists, but is empty'):
            response = HttpResponse('<h1></h1>')
            self.assertEqual(self.get_page_header(response), '')
            self.assertEqual(self.get_page_header(response.content), '')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), '')

        with self.subTest('Header exists, but is whitespace'):
            response = HttpResponse('<h1>   </h1>')
            self.assertEqual(self.get_page_header(response), '')
            self.assertEqual(self.get_page_header(response.content), '')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), '')

    def test__get_page_header__populated_header(self):
        """
        Tests get_page_header() function, when page H1 header is populated.
        """
        with self.subTest('Basic header'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertEqual(self.get_page_header(response), 'Test Header')
            self.assertEqual(self.get_page_header(response.content), 'Test Header')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), 'Test Header')

        with self.subTest('Basic header, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<h1>   Test    Header   </h1>')
            self.assertEqual(self.get_page_header(response), 'Test Header')
            self.assertEqual(self.get_page_header(response.content), 'Test Header')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), 'Test Header')

    def test__get_context_messages(self):
        """
        Tests get_context_messages() function.
        """
        with self.subTest('No messages'):
            response = self._get_page_response('django_expanded_test_cases:index')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 0)

        with self.subTest('Single message'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 1)
            self.assertIn('This is a test message.', messages)

        with self.subTest('Two messages'):
            response = self._get_page_response('django_expanded_test_cases:two-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 2)
            self.assertIn('Test message #1.', messages)
            self.assertIn('Test message #2.', messages)

        with self.subTest('Three messages'):
            response = self._get_page_response('django_expanded_test_cases:three-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 3)
            self.assertIn('Test info message.', messages)
            self.assertIn('Test warning message.', messages)
            self.assertIn('Test error message.', messages)

        with self.subTest('TemplateResponse check'):
            response = self._get_page_response('django_expanded_test_cases:template-response-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 3)
            self.assertIn('Test info message.', messages)
            self.assertIn('Test warning message.', messages)
            self.assertIn('Test error message.', messages)

    def test__get_minimized_response_content__strip_newlines_is_true(self):
        """
        Tests get_minimized_response_content() function.
        """
        with self.subTest('Minimal Response - No change'):
            response = HttpResponse('<h1>Test Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Outer whitespace'):
            response = HttpResponse('&nbsp; <h1>Test Title</h1> &nbsp; ')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - With Newlines'):
            response = HttpResponse('<h1>Test  \n  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Standard Response - Login Page'):
            response = self._get_page_response('django_expanded_test_cases:login')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(
                response,
                (
                    '<head><meta charset="utf-8"><title>Login Page | Test Views</title></head>'
                    '<body>'
                    '<h1>Login Page Header</h1><p>Pretend this is a login page.</p>'
                    '</body>'
                ),
            )

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('django_expanded_test_cases:index')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(
                response,
                (
                    '<head><meta charset="utf-8"><title>Home Page | Test Views</title></head>'
                    '<body>'
                    '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>'
                    '</body>'
                ),
            )

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('django_expanded_test_cases:template-response-index')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(
                response,
                (
                    '<head><meta charset="utf-8"><title>Home Page | Test Views</title></head>'
                    '<body>'
                    '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>'
                    '</body>'
                ),
            )

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertEqual(
                response,
                (
                    '<head><meta charset="utf-8"><title>View with One Message | Test Views</title></head>'
                    '<body>'
                    '<ul><li><p>This is a test message.</p></li></ul>'
                    '<h1>View with One Message Header</h1>'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>'
                    '</body>'
                ),
            )

    def test__get_minimized_response_content__strip_newlines_is_false(self):
        """
        Tests get_minimized_response_content() function.
        """
        with self.subTest('Minimal Response - No change'):
            response = HttpResponse('<h1>Test Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Outer whitespace'):
            response = HttpResponse('&nbsp; <h1>Test Title</h1> &nbsp; ')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(response, '<h1>Test Title</h1>')

        with self.subTest('Minimal Response - With Newlines'):
            response = HttpResponse('<h1>Test  \n  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(response, '<h1>Test \n Title</h1>')

        with self.subTest('Standard Response - Login Page'):
            response = self._get_page_response('django_expanded_test_cases:login')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(
                response,
                (
                    '<head>\n<meta charset="utf-8">\n<title>Login Page | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<h1>Login Page Header</h1>\n<p>Pretend this is a login page.</p>\n'
                    '</body>'
                )
            )

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('django_expanded_test_cases:index')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(
                response,
                (
                    '<head>\n<meta charset="utf-8">\n<title>Home Page | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<h1>Home Page Header</h1>\n<p>Pretend this is the project landing page.</p>\n'
                    '</body>'
                )
            )

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('django_expanded_test_cases:template-response-index')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(
                response,
                (
                    '<head>\n<meta charset="utf-8">\n<title>Home Page | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<h1>Home Page Header</h1>\n<p>Pretend this is the project landing page.</p>\n'
                    '</body>'
                )
            )

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('django_expanded_test_cases:one-message')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertEqual(
                response,
                (
                    '<head>\n<meta charset="utf-8">\n<title>View with One Message | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<ul>\n<li><p>\n This is a test message.\n</p></li>\n</ul>\n'
                    '<h1>View with One Message Header</h1>\n'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>\n'
                    '</body>'
                ),
            )

    def test__standardize_html_tags(self):
        """
        Tests letters in standardize_html_tags() functions.
        """
        with self.subTest('Test html tag - No spaces'):
            value = self.standardize_html_tags('<h1>Test Header</h1><p>Aaa</p>')
            self.assertEqual(value, '<h1>Test Header</h1><p>Aaa</p>')

        with self.subTest('Test html tag - With spaces'):
            value = self.standardize_html_tags('  <h1>  Test Header  </h1> <p> Aaa </p>  ')
            self.assertEqual(value, '<h1>Test Header</h1><p>Aaa</p>')

        with self.subTest('Test array - No spaces'):
            value = self.standardize_html_tags('[1, 2, 3]')
            self.assertEqual(value, '[1, 2, 3]')

        with self.subTest('Test array - with spaces'):
            value = self.standardize_html_tags('  [  1, 2, 3  ]  ')
            self.assertEqual(value, '[1, 2, 3]')

        with self.subTest('Test dict - No spaces'):
            value = self.standardize_html_tags('{"one": 1, "two": 2}')
            self.assertEqual(value, '{"one": 1, "two": 2}')

        with self.subTest('Test dict - With spaces'):
            value = self.standardize_html_tags('{  "one": 1, "two": 2  }  ')
            self.assertEqual(value, '{"one": 1, "two": 2}')

    def test__find_elements_by_tag__success(self):
        """
        Tests find_elements_by_tag() function, in cases when it should succeed.
        """
        with self.subTest('When expected element is the only item, with standard element'):
            response = HttpResponse('<li></li>')

            # By base element tag.
            results = self.find_elements_by_tag(response, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n</li>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(response, '<li>')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n</li>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(response, '</li>')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n</li>', results)

        with self.subTest('When expected element is the only item, with void element - Standard tag'):
            response = HttpResponse('<hr>')

            # By base element tag.
            results = self.find_elements_by_tag(response, 'hr')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(response, '<hr>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(response, '<hr/>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)

        with self.subTest('When expected element is the only item, with void element - Old style tag'):
            response = HttpResponse('<hr/>')

            # By base element tag.
            results = self.find_elements_by_tag(response, 'hr')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(response, '<hr>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(response, '<hr/>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)

        with self.subTest('When expected element exists multiple times - Two instances'):
            response = HttpResponse('<li>One</li><li>Two</li>')

            # By base element tag.
            results = self.find_elements_by_tag(response, 'li')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n One\n</li>', results)
            self.assertIn('<li>\n Two\n</li>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(response, '<li>')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n One\n</li>', results)
            self.assertIn('<li>\n Two\n</li>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(response, '</li>')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n One\n</li>', results)
            self.assertIn('<li>\n Two\n</li>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p>One</p></li>
                        <li><p>Two</p></li>
                        <li><p>Three</p></li>
                    </ul>
                    <ul>
                        <li><p>Four</p></li>
                        <li><p>Five</p></li>
                        <li><p>Six</p></li>
                    </ul>
                </div>
                """
            )

            # By base element tag.
            results = self.find_elements_by_tag(response, 'li')
            self.assertEqual(len(results), 6)
            self.assertIn('<li>\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Three\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Four\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Five\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Six\n</p>\n</li>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(response, '<li>')
            self.assertEqual(len(results), 6)
            self.assertIn('<li>\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Three\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Four\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Five\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Six\n</p>\n</li>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(response, '</li>')
            self.assertEqual(len(results), 6)
            self.assertIn('<li>\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Three\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Four\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Five\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Six\n</p>\n</li>', results)

    def test__find_elements_by_tag__failure(self):
        """
        Tests find_elements_by_tag() function, in cases when it should fail.
        """
        with self.subTest('When expected element is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find element "<li>" in content. Provided content was:\n'

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is not present - Single-item response'):
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find element "<li>" in content. Provided content was:\n<p></p>'

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p>Some text.</p>
                    <p>Some more text.</p>
                    <p>Some text with the str "li" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "li" in it.</p>\n'
                '</div>\n'
            )

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_tag__success(self):
        """
        Tests find_element_by_tag() function, in cases when it should succeed.
        """
        with self.subTest('When expected element is the only item, with standard element'):
            response = HttpResponse('<li></li>')

            # By base element tag.
            results = self.find_element_by_tag(response, 'li')
            self.assertText('<li>\n</li>', results)
            # By standard element open tag.
            results = self.find_element_by_tag(response, '<li>')
            self.assertText('<li>\n</li>', results)
            # By standard element close tag.
            results = self.find_element_by_tag(response, '</li>')
            self.assertText('<li>\n</li>', results)

        with self.subTest('When expected element is the only item, with void element - Standard tag'):
            response = HttpResponse('<hr>')

            # By base element tag.
            results = self.find_element_by_tag(response, 'hr')
            self.assertText('<hr/>\n', results)
            # By standard element open tag.
            results = self.find_element_by_tag(response, '<hr>')
            self.assertText('<hr/>\n', results)
            # By standard element close tag.
            results = self.find_element_by_tag(response, '<hr/>')
            self.assertText('<hr/>\n', results)

        with self.subTest('When expected element is the only item, with void element - Old style tag'):
            response = HttpResponse('<hr/>')

            # By base element tag.
            results = self.find_element_by_tag(response, 'hr')
            self.assertText('<hr/>\n', results)
            # By standard element open tag.
            results = self.find_element_by_tag(response, '<hr>')
            self.assertText('<hr/>\n', results)
            # By standard element close tag.
            results = self.find_element_by_tag(response, '<hr/>')
            self.assertText('<hr/>\n', results)

        with self.subTest('When expected element exists plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p>One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )

            # By base element tag.
            results = self.find_element_by_tag(response, 'li')
            self.assertText('<li>\n<p>\n One\n</p>\n</li>', results)
            # By standard element open tag.
            results = self.find_element_by_tag(response, '<li>')
            self.assertText('<li>\n<p>\n One\n</p>\n</li>', results)
            # By standard element close tag.
            results = self.find_element_by_tag(response, '</li>')
            self.assertText('<li>\n<p>\n One\n</p>\n</li>', results)

    def test__find_element_by_tag__failure(self):
        """
        Tests find_element_by_tag() function, in cases when it should fail.
        """
        with self.subTest('When expected element is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find element "<li>" in content. Provided content was:\n'

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is not present - Single-item response'):
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find element "<li>" in content. Provided content was:\n<p></p>'

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p>Some text.</p>
                    <p>Some more text.</p>
                    <p>Some text with the str "li" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "li" in it.</p>\n'
                '</div>\n'
            )

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is present multiple times'):
            response = HttpResponse('<li></li><li></li>')
            err_msg = (
                'Found multiple instances of "<li>" element. Expected only one instance. Content was:\n'
                '<li></li><li></li>'
            )

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, 'li')
            self.assertText(str(err.exception), err_msg)
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(str(err.exception), err_msg)
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(str(err.exception), err_msg)

    def test__find_elements_by_id__success(self):
        """
        Tests find_elements_by_id() function, in cases when it should succeed.
        """
        with self.subTest('When expected id is the only item'):
            # As <li> tag.
            response = HttpResponse('<li id="test_id"></li>')
            results = self.find_elements_by_id(response, 'test_id')
            self.assertText(len(results), 1)
            self.assertIn('<li id="test_id">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p id="test_id"></p>')
            results = self.find_elements_by_id(response, 'test_id')
            self.assertText(len(results), 1)
            self.assertIn('<p id="test_id">\n</p>', results)

        with self.subTest('When expected id exists multiple times - Two instances'):
            response = HttpResponse('<li id="test_id">One</li><li id="test_id">Two</li>')
            with self.assertLogs(level=logging.WARNING):
                results = self.find_elements_by_id(response, 'test_id')
            self.assertEqual(len(results), 2)
            self.assertIn('<li id="test_id">\n One\n</li>', results)
            self.assertIn('<li id="test_id">\n Two\n</li>', results)

        with self.subTest('When expected id exists multiple times - Three instances plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li id="test_id"><p>One</p></li>
                        <li id="test_id"><p>Two</p></li>
                        <li id="some_value"><p>Three</p></li>
                    </ul>
                    <ul>
                        <li id="test_id"><p>Four</p></li>
                        <li id="another_id"><p>Five</p></li>
                        <li id="test"><p>Six</p></li>
                    </ul>
                </div>
                """
            )
            with self.assertLogs(level=logging.WARNING):
                results = self.find_elements_by_id(response, 'test_id')
            self.assertEqual(len(results), 3)
            self.assertIn('<li id="test_id">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li id="test_id">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li id="test_id">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p id="test_id">One</p></li>
                        <li><p id="test_id">Two</p></li>
                        <li><p id="some_value">Three</p></li>
                    </ul>
                    <ul>
                        <li><p id="test_id">Four</p></li>
                        <li><p id="another_id">Five</p></li>
                        <li><p id="test">Six</p></li>
                    </ul>
                </div>
                """
            )
            with self.assertLogs(level=logging.WARNING):
                results = self.find_elements_by_id(response, 'test_id')
            self.assertEqual(len(results), 3)
            self.assertIn('<p id="test_id">\n One\n</p>', results)
            self.assertIn('<p id="test_id">\n Two\n</p>', results)
            self.assertIn('<p id="test_id">\n Four\n</p>', results)

    def test__find_elements_by_id__failure(self):
        """
        Tests find_elements_by_id() function, in cases when it should fail.
        """
        with self.subTest('When expected id is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find id "test_id" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected id is not present - Single-item response'):
            response = HttpResponse('<p id="test"></p>')
            err_msg = 'Unable to find id "test_id" in content. Provided content was:\n<p id="test"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected id is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p id="some_value">Some text.</p>
                    <p id="another_id">Some more text.</p>
                    <p>Some text with the str "id" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p id="some_value">Some text.</p>\n'
                '<p id="another_id">Some more text.</p>\n'
                '<p>Some text with the str "id" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_id__success(self):
        """
        Tests find_element_by_id() function, in cases when it should succeed.
        """
        with self.subTest('When expected id is the only item'):
            # As <li> tag.
            response = HttpResponse('<li id="test_id"></li>')
            results = self.find_element_by_id(response, 'test_id')
            self.assertText('<li id="test_id">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p id="test_id"></p>')
            results = self.find_element_by_id(response, 'test_id')
            self.assertText('<p id="test_id">\n</p>', results)

        with self.subTest('When expected id exists plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li id=test_id><p>One</p></li>
                        <li><p>Two</p></li>
                        <li id="some_value"><p>Three</p></li>
                    </ul>
                    <ul>
                        <li id="another_id"><p>Four</p></li>
                        <li><p>Five</p></li>
                        <li id="test"><p>Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_element_by_id(response, 'test_id')
            self.assertText('<li id="test_id">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p id=test_id>One</p></li>
                        <li><p>Two</p></li>
                        <li id="some_value"><p>Three</p></li>
                    </ul>
                    <ul>
                        <li id="another_id"><p>Four</p></li>
                        <li><p>Five</p></li>
                        <li id="test"><p>Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_element_by_id(response, 'test_id')
            self.assertText('<p id="test_id">\n One\n</p>', results)

    def test__find_element_by_id__failure(self):
        """
        Tests find_element_by_id() function, in cases when it should fail.
        """
        with self.subTest('When expected id is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find id "test_id" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected id is not present - Single-item response'):
            response = HttpResponse('<p id="some_id"></p>')
            err_msg = 'Unable to find id "test_id" in content. Provided content was:\n<p id="some_id"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected id is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p id="some_value">Some text.</p>
                    <p id="another_id">Some more text.</p>
                    <p>Some text with the str "id" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p id="some_value">Some text.</p>\n'
                '<p id="another_id">Some more text.</p>\n'
                '<p>Some text with the str "id" in it.</p>\n'
                '</div>\n'
            )

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected id is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li id="test_id"></li><li id="test_id"></li>')
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<li id="test_id"></li><li id="test_id"></li>'
            )
            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

            # As <p> tag.
            response = HttpResponse('<p id="test_id"></p><p id="test_id"></p>')
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<p id="test_id"></p><p id="test_id"></p>'
            )
            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

            # As mixed tags.
            response = HttpResponse('<li id="test_id"><p id="test_id">Test</p></li>')
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<li id="test_id"><p id="test_id">Test</p></li>'
            )
            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(response, 'test_id')
            self.assertText(str(err.exception), err_msg)

    def test__find_elements_by_class__success(self):
        """
        Tests find_elements_by_class() function, in cases when it should succeed.
        """
        with self.subTest('When expected class is the only item'):
            # As <li>  tag.
            response = HttpResponse('<li class="test_class"></li>')
            results = self.find_elements_by_class(response, 'test_class')
            self.assertEqual(len(results), 1)
            self.assertIn('<li class="test_class">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p class="test_class"></p>')
            results = self.find_elements_by_class(response, 'test_class')
            self.assertEqual(len(results), 1)
            self.assertIn('<p class="test_class">\n</p>', results)

        with self.subTest('When expected class exists multiple times - Two instances'):
            response = HttpResponse('<li class="test_class">One</li><li class="test_class">Two</li>')

            results = self.find_elements_by_class(response, 'test_class')
            self.assertEqual(len(results), 2)
            self.assertIn('<li class="test_class">\n One\n</li>', results)
            self.assertIn('<li class="test_class">\n Two\n</li>', results)

        with self.subTest('When expected class exists plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li class="test_class"><p>One</p></li>
                        <li class="test_class"><p>Two</p></li>
                        <li class="some_value"><p>Three</p></li>
                    </ul>
                    <ul>
                        <li class="test_class test"><p>Four</p></li>
                        <li class="another_class"><p>Five</p></li>
                        <li class="test"><p>Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_class(response, 'test_class')
            self.assertEqual(len(results), 3)
            self.assertIn('<li class="test_class">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li class="test_class">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li class="test_class test">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p class="test_class">One</p></li>
                        <li><p class="test_class">Two</p></li>
                        <li><p class="some_value">Three</p></li>
                    </ul>
                    <ul>
                        <li><p class="test_class test">Four</p></li>
                        <li><p class="another_class">Five</p></li>
                        <li><p class="test">Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_class(response, 'test_class')
            self.assertEqual(len(results), 3)
            self.assertIn('<p class="test_class">\n One\n</p>', results)
            self.assertIn('<p class="test_class">\n Two\n</p>', results)
            self.assertIn('<p class="test_class test">\n Four\n</p>', results)

    def test__find_elements_by_class__failure(self):
        """
        Tests find_elements_by_class() function, in cases when it should fail.
        """
        with self.subTest('When expected class is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find class "test_class" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected class is not present - Single-item response'):
            response = HttpResponse('<p class="some_class"></p>')
            err_msg = 'Unable to find class "test_class" in content. Provided content was:\n<p class="some_class"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected class is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p>Some text.</p>
                    <p>Some more text.</p>
                    <p>Some text with the str "class" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "class" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_class__success(self):
        """
        Tests find_element_by_class() function, in cases when it should succeed.
        """
        with self.subTest('When expected class is the only item'):
            # As <li> tag.
            response = HttpResponse('<li class="test_class"></li>')
            results = self.find_element_by_class(response, 'test_class')
            self.assertText('<li class="test_class">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p class="test_class"></p>')
            results = self.find_element_by_class(response, 'test_class')
            self.assertText('<p class="test_class">\n</p>', results)

        with self.subTest('When expected class exists plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li class="test_class"><p>One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )
            results = self.find_element_by_class(response, 'test_class')
            self.assertText('<li class="test_class">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p class="test_class">One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )
            results = self.find_element_by_class(response, 'test_class')
            self.assertText('<p class="test_class">\n One\n</p>', results)

    def test__find_element_by_class__failure(self):
        """
        Tests find_element_by_class() function, in cases when it should fail.
        """
        with self.subTest('When expected class is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find class "test_class" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected class is not present - Single-item response'):
            response = HttpResponse('<p class="some_class"></p>')
            err_msg = 'Unable to find class "test_class" in content. Provided content was:\n<p class="some_class"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected class is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p class="some_class">Some text.</p>
                    <p class="another_class">Some more text.</p>
                    <p class="test">Some text with the str "class" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p class="some_class">Some text.</p>\n'
                '<p class="another_class">Some more text.</p>\n'
                '<p class="test">Some text with the str "class" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected class is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li class="test_class"></li><li class="test_class"></li>')
            err_msg = (
                'Found multiple instances of "test_class" class. Expected only one instance. Content was:\n'
                '<li class="test_class"></li><li class="test_class"></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

            # As <p> tag.
            response = HttpResponse('<p class="test_class"></p><p class="test_class"></p>')
            err_msg = (
                'Found multiple instances of "test_class" class. Expected only one instance. Content was:\n'
                '<p class="test_class"></p><p class="test_class"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(str(err.exception), err_msg)

    def test__find_elements_by_css_selector__success(self):
        """
        Tests find_elements_by_css_selector() function, in cases when it should succeed.
        """
        with self.subTest('When expected css_selector is the only item, with standard element'):
            response = HttpResponse('<li><p class="test_class"><a>One</a></p></li>')

            results = self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertEqual(len(results), 1)
            self.assertIn('<a>\n One\n</a>', results)

        with self.subTest('When expected element exists multiple times - Two instances'):
            response = HttpResponse(
                """
                <li><p class="test_class"><a>One</a></p></li>
                <li><p class="test_class"><a>Two</a></p></li>
                """
            )

            results = self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertEqual(len(results), 2)
            self.assertIn('<a>\n One\n</a>', results)
            self.assertIn('<a>\n Two\n</a>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p class="test_class"><a>One</a></p></li>
                        <li><p class="test_class"><a>Two</a></p></li>
                        <li><p class="test_class">Three</p></li>
                    </ul>
                    <ul>
                        <li><p class="test_class"><a>Four</a></p></li>
                        <li><p class="test_class"><div><a>Five</a></div></p></li>
                        <li><p class="other_class"><a>Six</a></p></li>
                    </ul>
                </div>
                """
            )

            # By base element tag.
            results = self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertEqual(len(results), 3)
            self.assertIn('<a>\n One\n</a>', results)
            self.assertIn('<a>\n Two\n</a>', results)
            self.assertIn('<a>\n Four\n</a>', results)

    def test__find_elements_by_css_selector__failure(self):
        """
        Tests find_elements_by_css_selector() function, in cases when it should fail.
        """
        with self.subTest('When expected css_selector is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected css_selector is not present - Single-item response'):
            # Missing all parts.
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<p></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

            # Missing two parts.
            response = HttpResponse('<li></li>')
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n<li></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

            # Missing one part.
            response = HttpResponse('<li><p class="test_class"></p></li>')
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n<li><p class="test_class"></p></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected css_selector is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p>Some text.</p>
                    <p>Some more text.</p>
                    <p>Some text with the str "css_selector" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "css_selector" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_css_selector__success(self):
        """
        Tests find_element_by_css_selector() function, in cases when it should succeed.
        """
        with self.subTest('When expected css_selector is the only item, with standard element'):
            response = HttpResponse('<li><p class="test_class"><a>One</a></p></li>')

            results = self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText('<a>\n One\n</a>', results)

        with self.subTest('When expected css_selector exists plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p class="test_class"><a>One</a></p></li>
                        <li><a>Two</a></li>
                        <li><p class="test_class"><div><a>Three</a></div></p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )

            results = self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText('<a>\n One\n</a>', results)

    def test__find_element_by_css_selector__failure(self):
        """
        Tests find_element_by_css_selector() function, in cases when it should fail.
        """
        with self.subTest('When expected css_selector is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected css_selector is not present - Single-item response'):
            # Missing all parts.
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<p></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

            # Missing two parts.
            response = HttpResponse('<li></li>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<li></li>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

            # Missing one parts.
            response = HttpResponse('<li><p class="test_class"></p></li>')
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n<li><p class="test_class"></p></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected css_selector is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p>Some text.</p>
                    <p>Some more text.</p>
                    <p>Some text with the str "css_selector" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "css_selector" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected css_selector is present multiple times'):
            response = HttpResponse(
                """
                <li><p class="test_class"><a>One</a></p></li>
                <li><p class="test_class"><a>Two</a></p></li>
                """
            )
            err_msg = (
                'Found multiple instances of "li .test_class > a" css selector. Expected only one instance.'
                ' Content was:\n'
                '<li><p class="test_class"><a>One</a></p></li>\n'
                '<li><p class="test_class"><a>Two</a></p></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(str(err.exception), err_msg)

    def test__find_elements_by_data_attribute__success(self):
        """
        Tests find_elements_by_data_attribute() function, in cases when it should succeed.
        """
        with self.subTest('When expected data_attribute is the only item, with standard element'):
            # As <li> tag.
            response = HttpResponse('<li my_attr="my_val"></li>')

            results = self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertEqual(len(results), 1)
            self.assertIn('<li my_attr="my_val">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p my_attr="my_val"></p>')

            results = self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertEqual(len(results), 1)
            self.assertIn('<p my_attr="my_val">\n</p>', results)

        with self.subTest('When expected data_attribute exists multiple times - Two instances'):
            # As <li> tag.
            response = HttpResponse('<li my_attr="my_val">One</li><li my_attr="my_val">Two</li>')

            results = self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertEqual(len(results), 2)
            self.assertIn('<li my_attr="my_val">\n One\n</li>', results)
            self.assertIn('<li my_attr="my_val">\n Two\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p my_attr="my_val">One</p><p my_attr="my_val">Two</p>')

            results = self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertEqual(len(results), 2)
            self.assertIn('<p my_attr="my_val">\n One\n</p>', results)
            self.assertIn('<p my_attr="my_val">\n Two\n</p>', results)

        with self.subTest('When expected data_attribute exists multiple times - Three instances plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li my_attr="my_val"><p>One</p></li>
                        <li my_attr="my_val"><p>Two</p></li>
                        <li other_attr="other_val"><p>Three</p></li>
                    </ul>
                    <ul>
                        <li my_attr="my_val" test_attr="test_val"><p>Four</p></li>
                        <li another_attr="my_val"><p>Five</p></li>
                        <li my_attr="another_val"><p>Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertEqual(len(results), 3)
            self.assertIn('<li my_attr="my_val">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li my_attr="my_val">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li my_attr="my_val" test_attr="test_val">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p my_attr="my_val">One</p></li>
                        <li><p my_attr="my_val">Two</p></li>
                        <li><p other_attr="other_val">Three</p></li>
                    </ul>
                    <ul>
                        <li><p my_attr="my_val" test_attr="test_val">Four</p></li>
                        <li><p another_attr="my_val">Five</p></li>
                        <li><p my_attr="another_val">Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertEqual(len(results), 3)
            self.assertIn('<p my_attr="my_val">\n One\n</p>', results)
            self.assertIn('<p my_attr="my_val">\n Two\n</p>', results)
            self.assertIn('<p my_attr="my_val" test_attr="test_val">\n Four\n</p>', results)

    def test__find_elements_by_data_attribute__failure(self):
        """
        Tests find_elements_by_data_attribute() function, in cases when it should fail.
        """
        with self.subTest('When expected data_attribute is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute is not present - Single-item response'):
            response = HttpResponse('<p some_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute key is not present - Single-item response'):
            response = HttpResponse('<p some_attr="my_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="my_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute value is not present - Single-item response'):
            response = HttpResponse('<p my_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p my_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p some_attr="some_val">Some text.</p>
                    <p another_attr="another_val">Some more text.</p>
                    <p test="test">Some text with the str "data_attribute" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p some_attr="some_val">Some text.</p>\n'
                '<p another_attr="another_val">Some more text.</p>\n'
                '<p test="test">Some text with the str "data_attribute" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_data_attribute__success(self):
        """
        Tests find_element_by_data_attribute() function, in cases when it should succeed.
        """
        with self.subTest('When expected data_attribute is the only item, with standard element'):
            # As <li> tag.
            response = HttpResponse('<li my_attr="my_val"></li>')

            results = self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText('<li my_attr="my_val">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p my_attr="my_val"></p>')

            results = self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText('<p my_attr="my_val">\n</p>', results)

        with self.subTest('When expected data_attribute exists plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li my_attr="my_val"><p>One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )

            # By base element tag.
            results = self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText('<li my_attr="my_val">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p my_attr="my_val">One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )

            # By base element tag.
            results = self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText('<p my_attr="my_val">\n One\n</p>', results)

    def test__find_element_by_data_attribute__failure(self):
        """
        Tests find_element_by_data_attribute() function, in cases when it should fail.
        """
        with self.subTest('When expected data_attribute is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute is not present - Single-item response'):
            response = HttpResponse('<p some_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute key is not present - Single-item response'):
            response = HttpResponse('<p some_attr="my_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="my_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute value is not present - Single-item response'):
            response = HttpResponse('<p my_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p my_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected data_attribute is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p some_attr="some_val">Some text.</p>
                    <p another_attr="another_val">Some more text.</p>
                    <p test="test">Some text with the str "data_attribute" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p some_attr="some_val">Some text.</p>\n'
                '<p another_attr="another_val">Some more text.</p>\n'
                '<p test="test">Some text with the str "data_attribute" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li my_attr="my_val"></li><li my_attr="my_val"></li>')
            err_msg = (
                'Found multiple instances of "my_attr" data attribute with value "my_val". Expected only one instance. '
                'Content was:\n<li my_attr="my_val"></li><li my_attr="my_val"></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

            # As <p> tag.
            response = HttpResponse('<p my_attr="my_val"></p><p my_attr="my_val"></p>')
            err_msg = (
                'Found multiple instances of "my_attr" data attribute with value "my_val". Expected only one instance. '
                'Content was:\n<p my_attr="my_val"></p><p my_attr="my_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(str(err.exception), err_msg)

    def test__find_elements_by_name__success(self):
        """
        Tests find_elements_by_name() function, in cases when it should succeed.
        """
        with self.subTest('When expected name is the only item'):
            # As <li> tag.
            response = HttpResponse('<li name="test_name"></li>')

            results = self.find_elements_by_name(response, 'test_name')
            self.assertEqual(len(results), 1)
            self.assertIn('<li name="test_name">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p name="test_name"></p>')

            results = self.find_elements_by_name(response, 'test_name')
            self.assertEqual(len(results), 1)
            self.assertIn('<p name="test_name">\n</p>', results)

        with self.subTest('When expected name exists multiple times - Two instances'):
            # As <li> tag.
            response = HttpResponse('<li name="test_name">One</li><li name="test_name">Two</li>')

            results = self.find_elements_by_name(response, 'test_name')
            self.assertEqual(len(results), 2)
            self.assertIn('<li name="test_name">\n One\n</li>', results)
            self.assertIn('<li name="test_name">\n Two\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p name="test_name">One</p><p name="test_name">Two</p>')

            results = self.find_elements_by_name(response, 'test_name')
            self.assertEqual(len(results), 2)
            self.assertIn('<p name="test_name">\n One\n</p>', results)
            self.assertIn('<p name="test_name">\n Two\n</p>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li name="test_name"><p>One</p></li>
                        <li name="test_name"><p>Two</p></li>
                        <li name="some_name"><p>Three</p></li>
                    </ul>
                    <ul>
                        <li name="test_name"><p>Four</p></li>
                        <li name="another_name"><p>Five</p></li>
                        <li name="test"><p>Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_name(response, 'test_name')
            self.assertEqual(len(results), 3)
            self.assertIn('<li name="test_name">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li name="test_name">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li name="test_name">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p name="test_name">One</p></li>
                        <li><p name="test_name">Two</p></li>
                        <li><p name="other_name">Three</p></li>
                    </ul>
                    <ul>
                        <li><p name="test_name">Four</p></li>
                        <li><p name="another_name">Five</p></li>
                        <li><p name="test">Six</p></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_name(response, 'test_name')
            self.assertEqual(len(results), 3)
            self.assertIn('<p name="test_name">\n One\n</p>', results)
            self.assertIn('<p name="test_name">\n Two\n</p>', results)
            self.assertIn('<p name="test_name">\n Four\n</p>', results)

    def test__find_elements_by_name__failure(self):
        """
        Tests find_elements_by_name() function, in cases when it should fail.
        """
        with self.subTest('When expected name is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find name "test_name" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected name is not present - Single-item response'):
            response = HttpResponse('<p name="other_name"></p>')
            err_msg = 'Unable to find name "test_name" in content. Provided content was:\n<p name="other_name"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected name is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p name="other_name">Some text.</p>
                    <p name="another_name">Some more text.</p>
                    <p name="test">Some text with the str "name" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p name="other_name">Some text.</p>\n'
                '<p name="another_name">Some more text.</p>\n'
                '<p name="test">Some text with the str "name" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_name__success(self):
        """
        Tests find_element_by_name() function, in cases when it should succeed.
        """
        with self.subTest('When expected name is the only item, with standard element'):
            # As <li> tag.
            response = HttpResponse('<li name="test_name"></li>')

            results = self.find_element_by_name(response, 'test_name')
            self.assertText('<li name="test_name">\n</li>', results)

            # As <p> tag.
            response = HttpResponse('<p name="test_name"></p>')

            results = self.find_element_by_name(response, 'test_name')
            self.assertText('<p name="test_name">\n</p>', results)

        with self.subTest('When expected element exists plus extra'):
            # As <li> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li name="test_name"><p>One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )
            results = self.find_element_by_name(response, 'test_name')
            self.assertText('<li name="test_name">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><p name="test_name">One</p></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )
            results = self.find_element_by_name(response, 'test_name')
            self.assertText('<p name="test_name">\n One\n</p>', results)

    def test__find_element_by_name__failure(self):
        """
        Tests find_element_by_name() function, in cases when it should fail.
        """
        with self.subTest('When expected name is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find name "test_name" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected name is not present - Single-item response'):
            response = HttpResponse('<p name="other_name"></p>')
            err_msg = 'Unable to find name "test_name" in content. Provided content was:\n<p name="other_name"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected name is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <p name="other_name">Some text.</p>
                    <p name="another_name">Some more text.</p>
                    <p name="test">Some text with the str "li" in it.</p>
                </div>
                """
            )
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p name="other_name">Some text.</p>\n'
                '<p name="another_name">Some more text.</p>\n'
                '<p name="test">Some text with the str "li" in it.</p>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected element is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li name="test_name"></li><li name="test_name"></li>')
            err_msg = (
                'Found multiple instances of "test_name" name. Expected only one instance. Content was:\n'
                '<li name="test_name"></li><li name="test_name"></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

            # As <p> tag.
            response = HttpResponse('<p name="test_name"></p><p name="test_name"></p>')
            err_msg = (
                'Found multiple instances of "test_name" name. Expected only one instance. Content was:\n'
                '<p name="test_name"></p><p name="test_name"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(str(err.exception), err_msg)

    def test__find_elements_by_link_text__success(self):
        """
        Tests find_elements_by_link_text() function, in cases when it should succeed.
        """
        with self.subTest('When expected link_text is the only item, with standard element'):
            response = HttpResponse('<a href="test_link_text"></a>')

            results = self.find_elements_by_link_text(response, 'test_link_text')
            self.assertEqual(len(results), 1)
            self.assertIn('<a href="test_link_text">\n</a>', results)

        with self.subTest('When expected link_text exists multiple times - Two instances'):
            response = HttpResponse('<a href="test_link_text">One</a><a href="test_link_text">Two</a>')

            # By base element tag.
            results = self.find_elements_by_link_text(response, 'test_link_text')
            self.assertEqual(len(results), 2)
            self.assertIn('<a href="test_link_text">\n One\n</a>', results)
            self.assertIn('<a href="test_link_text">\n Two\n</a>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><a href="test_link_text">One</a></li>
                        <li><a href="test_link_text">Two</a></li>
                        <li><a href="other_link_text">Three</a></li>
                    </ul>
                    <ul>
                        <li><a href="test_link_text">Four</a></li>
                        <li><a href="another_link_text">Five</a></li>
                        <li><a href="test">Six</a></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_link_text(response, 'test_link_text')
            self.assertEqual(len(results), 3)
            self.assertIn('<a href="test_link_text">\n One\n</a>', results)
            self.assertIn('<a href="test_link_text">\n Two\n</a>', results)
            self.assertIn('<a href="test_link_text">\n Four\n</a>', results)

    def test__find_elements_by_link_text__failure(self):
        """
        Tests find_elements_by_link_text() function, in cases when it should fail.
        """
        with self.subTest('When expected link_text is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find link text "test_link_text" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected link_text is not present - Single-item response'):
            response = HttpResponse('<a href="other_link_text"></a>')
            err_msg = (
                'Unable to find link text "test_link_text" in content. '
                'Provided content was:\n<a href="other_link_text"></a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected link_text is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <a href="other_link_text">Some text.</a>
                    <a href="another_link_text">Some more text.</a>
                    <a href="test">Some text with the str "link_text" in it.</a>
                </div>
                """
            )
            err_msg = (
                'Unable to find link text "test_link_text" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="other_link_text">Some text.</a>\n'
                '<a href="another_link_text">Some more text.</a>\n'
                '<a href="test">Some text with the str "link_text" in it.</a>\n'
                '</div>\n'
            )
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

    def test__find_element_by_link_text__success(self):
        """
        Tests find_element_by_link_text() function, in cases when it should succeed.
        """
        with self.subTest('When expected element is the only item, with standard element'):
            response = HttpResponse('<a href="test_link_text"></a>')

            results = self.find_element_by_link_text(response, 'test_link_text')
            self.assertText('<a href="test_link_text">\n</a>', results)

        with self.subTest('When expected element exists plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><a href="test_link_text">One</a></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )
            results = self.find_element_by_link_text(response, 'test_link_text')
            self.assertText('<a href="test_link_text">\n One\n</a>', results)

    def test__find_element_by_link_text__failure(self):
        """
        Tests find_element_by_link_text() function, in cases when it should fail.
        """
        with self.subTest('When expected link_text is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find link text "test_link_text" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected link_text is not present - Single-item response'):
            response = HttpResponse('<a href="other_link_text"></a>')
            err_msg = (
                'Unable to find link text "test_link_text" in content. '
                'Provided content was:\n<a href="other_link_text"></a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected link_text is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <a href="other_link_text">Some text.</a>
                    <a href="another_link_text">Some more text.</a>
                    <a href="test">Some text with the str "link_text" in it.</a>
                </div>
                """
            )
            err_msg = (
                'Unable to find link text "test_link_text" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="other_link_text">Some text.</a>\n'
                '<a href="another_link_text">Some more text.</a>\n'
                '<a href="test">Some text with the str "link_text" in it.</a>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

        with self.subTest('When expected link_text is present multiple times'):
            response = HttpResponse('<a href="test_link_text"></a><a href="test_link_text"></a>')
            err_msg = (
                'Found multiple instances of "test_link_text" link text. Expected only one instance. Content was:\n'
                '<a href="test_link_text"></a><a href="test_link_text"></a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(response, 'test_link_text')
            self.assertText(str(err.exception), err_msg)

    # endregion Helper Function Tests
