"""
Tests for test_cases/integration_test_case.py.
"""

# System Imports.
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

# User Imports.
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
            response = self.assertResponse('expanded_test_cases:index')
            self.assertEqual(response.url, '127.0.0.1/')

            # Test "login" page url.
            response = self.assertResponse('expanded_test_cases:login')
            self.assertEqual(response.url, '127.0.0.1/login/')

            # Test "one message" page url.
            response = self.assertResponse('expanded_test_cases:one-message')
            self.assertEqual(response.url, '127.0.0.1/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('expanded_test_cases:two-messages')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(1,))
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 2})
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')

        with self.subTest('With custom site_root_url value defined'):
            self.site_root_url = 'https://my_really_cool_site.com/'

            # Test "index" page url.
            response = self.assertResponse('expanded_test_cases:index')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/')

            # Test "login" page url.
            response = self.assertResponse('expanded_test_cases:login')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/login/')

            # Test "one message" page url.
            response = self.assertResponse('expanded_test_cases:one-message')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('expanded_test_cases:two-messages')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(1,))
            self.assertEqual(response.url, 'https://my_really_cool_site.com/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 2})
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
            self.assertResponse('redirect/index/', expected_redirect_url='expanded_test_cases:index')

            # Using reverse.
            self.assertResponse('expanded_test_cases:redirect-to-index')
            self.assertResponse('expanded_test_cases:redirect-to-index', expected_redirect_url='/')
            self.assertResponse(
                'expanded_test_cases:redirect-to-index',
                expected_redirect_url='expanded_test_cases:index',
            )

        with self.subTest('With view that does not redirect'):
            # Using direct url.
            self.assertResponse('')
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('', expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('', expected_redirect_url='expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('login/', expected_redirect_url='expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)

            # Using reverse.
            self.assertResponse('expanded_test_cases:index')
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_redirect_url='expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg)
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:login', expected_redirect_url='expanded_test_cases:index')
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
            response = self.assertResponse('expanded_test_cases:index')
            self.assertEqual(response.status_code, 200)

            # With non-200 code provided.
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_status=400)
            self.assertEqual(str(err.exception), exception_msg.format(200, 400))

        with self.subTest('With status_code=200 - View with params'):
            # Test 200 in direct url.
            response = self.assertResponse('user/detail/1/')
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url, via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(2,))
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url, via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 3})
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
            response = self.assertResponse('expanded_test_cases:user-detail', args=(234,), expected_status=404)
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 345}, expected_status=404)
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
            self.assertResponse('expanded_test_cases:index', expected_title='Home Page | Test Views')

        with self.subTest('Title mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_title='Wrong Title')
            self.assertEqual(str(err.exception), exception_msg)

    def test__assertResponse__expected_header(self):
        """
        Tests "expected_header" functionality of assertResponse() function.
        """
        exception_msg = 'Expected H1 header HTML contents of "Wrong Header". Actual value was "Home Page Header".'

        with self.subTest('Header match'):
            self.assertResponse('expanded_test_cases:index', expected_header='Home Page Header')

        with self.subTest('Header mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_header='Wrong Header')
            self.assertEqual(str(err.exception), exception_msg)

    def test__assertResponse__expected_messages(self):
        """
        Tests "expected_messages" functionality of assertResponse() function.
        """
        exception_msg = 'Failed to find message "{0}" in context (Partial matching {1} allowed).'

        with self.subTest('No messages on page - match'):
            self.assertResponse('expanded_test_cases:index', expected_messages='')
            self.assertResponse('expanded_test_cases:index', expected_messages=[''])

        with self.subTest('No messages on page - mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_messages='Wrong message.')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:index', expected_messages=['Wrong message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))

        with self.subTest('Multiple messages on page - match'):
            self.assertResponse('expanded_test_cases:three-messages', expected_messages='Test info message.')
            self.assertResponse('expanded_test_cases:three-messages', expected_messages=['Test warning message.'])
            self.assertResponse(
                'expanded_test_cases:three-messages',
                expected_messages=['Test info message.', 'Test warning message.'],
            )
            self.assertResponse(
                'expanded_test_cases:three-messages',
                expected_messages=['Test info message.', 'Test warning message.', 'Test error message.'],
            )

        with self.subTest('Multiple messages on page - mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertResponse('expanded_test_cases:three-messages', expected_messages='Wrong message.')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong message.', 'is'))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'expanded_test_cases:three-messages',
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
                'expanded_test_cases:index',
                expected_content=[
                    '<title>Home Page | Test Views</title>',
                    '<h1>Home Page Header</h1>',
                    '<p>Pretend this is',
                    'the project landing page.</p>',
                ],
            )

            # With repeated values.
            self.assertResponse(
                'expanded_test_cases:index',
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
                'expanded_test_cases:index',
                expected_content=[
                    'Home Page | Test Views',
                    'Home Page Header',
                    'Pretend this is',
                    'the project landing page.',
                ],
            )

            # With repeated values.
            self.assertResponse(
                'expanded_test_cases:index',
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
                self.assertResponse('expanded_test_cases:index', expected_content='Wrong value')
            self.assertEqual(str(err.exception), exception_msg.format('Wrong value'))
            with self.assertRaises(AssertionError) as err:
                self.assertResponse(
                    'expanded_test_cases:index',
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
                'expanded_test_cases:index',
                expected_content='<p>Pretend this is the project landing page.</p>',
                content_starts_after='<h1>Home Page Header</h1>',
            )
            # Strip end.
            self.assertResponse(
                'expanded_test_cases:index',
                expected_content='<title>Home Page | Test Views</title>',
                content_ends_before='<h1>Home Page Header</h1>',
            )
            # Strip both.
            self.assertResponse(
                'expanded_test_cases:index',
                expected_content='<h1>Home Page Header</h1>',
                content_starts_after='<title>Home Page | Test Views</title>',
                content_ends_before='<p>Pretend this is the project landing page.</p>',
            )

        with self.subTest('With content blocks'):
            # Entire page as one block.
            self.assertResponse(
                'expanded_test_cases:index',
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
                'expanded_test_cases:index',
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
                'expanded_test_cases:index',
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
                'expanded_test_cases:index',
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
                'expanded_test_cases:index',
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
        response = self.assertGetResponse('expanded_test_cases:index')

        self.assertEqual(response.url, '127.0.0.1/')
        self.assertEqual(response.status_code, 200)

    def test__assertPostResponse(self):
        """
        Tests assertPostResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """
        response = self.assertPostResponse('expanded_test_cases:index')

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
            self.assertRedirects('redirect/index/', expected_redirect_url='expanded_test_cases:index')

            # Using reverse.
            self.assertRedirects('expanded_test_cases:redirect-to-index', expected_redirect_url='/')
            self.assertRedirects(
                'expanded_test_cases:redirect-to-index',
                expected_redirect_url='expanded_test_cases:index',
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
                self.assertRedirects(request, expected_redirect_url='expanded_test_cases:invalid')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))

        with self.subTest('With view that does not redirect - Index page'):
            request = self._get_page_response('')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='expanded_test_cases:index')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))

        with self.subTest('With view that does not redirect - Non-index page'):
            request = self._get_page_response('login/')
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='/')
            self.assertEqual(str(err.exception), exception_msg.format(request.status_code))
            with self.assertRaises(AssertionError) as err:
                self.assertRedirects(request, expected_redirect_url='expanded_test_cases:login')
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

    @patch('django_expanded_test_cases.test_cases.integration_test_case.DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS', True)
    def test__assertContextMessages__success__allow_partials(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        We only do a minimal amount of testing for this function here.
        We assume a majority of testing will occur in the "disallow_partials" set.
        """
        with self.subTest('Check for single message partial, single message exists'):
            response = self._get_page_response('expanded_test_cases:one-message')
            self.assertContextMessages(response, 'This is a test message.')
            self.assertContextMessages(response, 'is a test message')
            self.assertContextMessages(response, 'test')

        with self.subTest('Check for three message partials, three messages exists'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            self.assertContextMessages(response, ['info', 'warning message', 'Test error'])

    @patch('django_expanded_test_cases.test_cases.integration_test_case.DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertContextMessages__success__disallow_partials(self):
        """
        Tests assertContextMessages() function, in cases when it should succeed.

        The majority of tests for this function exist here.
        """
        with self.subTest('Check for single message, single message exists'):
            response = self._get_page_response('expanded_test_cases:one-message')
            self.assertContextMessages(response, 'This is a test message.')

        with self.subTest('Check for single message, two messages exists'):
            response = self._get_page_response('expanded_test_cases:two-messages')
            self.assertContextMessages(response, 'Test message #1.')
            self.assertContextMessages(response, 'Test message #2.')

        with self.subTest('Check for single message, three messages exists'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            self.assertContextMessages(response, 'Test info message.')
            self.assertContextMessages(response, 'Test warning message.')
            self.assertContextMessages(response, 'Test error message.')

        with self.subTest('Check for two messages, two messages exists'):
            response = self._get_page_response('expanded_test_cases:two-messages')
            self.assertContextMessages(response, ['Test message #1.', 'Test message #2.'])

        with self.subTest('Check for two messages, three messages exists'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            self.assertContextMessages(response, ['Test info message.', 'Test warning message.'])
            self.assertContextMessages(response, ['Test info message.', 'Test error message.'])
            self.assertContextMessages(response, ['Test warning message.', 'Test error message.'])

        with self.subTest('Check for three messages, three messages exists'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            self.assertContextMessages(response, ['Test info message.', 'Test warning message.', 'Test error message.'])

    @patch('django_expanded_test_cases.test_cases.integration_test_case.DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS', False)
    def test__assertContextMessages__failure(self):
        """
        Tests assertContextMessages() function, in cases when it should fail.
        """
        exception_msg = 'Failed to find message "{0}" in context (Partial matching {1} allowed).'

        with self.subTest('Checking for single message, none exist'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('expanded_test_cases:index')
                self.assertContextMessages(response, 'This is a test message.')
            self.assertEqual(str(err.exception), exception_msg.format('This is a test message.', 'is NOT'))

        with self.subTest('Checking for single message, one exists but doesn\'t match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('expanded_test_cases:one-message')
                self.assertContextMessages(response, 'Testing!')
            self.assertEqual(str(err.exception), exception_msg.format('Testing!', 'is NOT'))

        with self.subTest('Checking for single message, but it\'s only a partial match'):
            response = self._get_page_response('expanded_test_cases:one-message')
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
                response = self._get_page_response('expanded_test_cases:three-messages')
                self.assertContextMessages(response, 'Testing!')
            self.assertEqual(str(err.exception), exception_msg.format('Testing!', 'is NOT'))

        with self.subTest('Checking for two messages, none exist'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('expanded_test_cases:index')
                self.assertContextMessages(response, ['This is a test message.', 'Another message.'])
            self.assertEqual(str(err.exception), exception_msg.format('This is a test message.', 'is NOT'))

        with self.subTest('Checking for two messages, but only one exists'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('expanded_test_cases:one-message')
                self.assertContextMessages(response, ['This is a test message.', 'Another message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Another message.', 'is NOT'))

        with self.subTest('Checking for two messages, multiple exist but one doesn\'t match'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, ['Test info message.', 'Another message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Another message.', 'is NOT'))
            with self.assertRaises(AssertionError) as err:
                self.assertContextMessages(response, ['Bad message', 'Test info message.'])
            self.assertEqual(str(err.exception), exception_msg.format('Bad message', 'is NOT'))

        with self.subTest('Checking for two messages, multiple exist but none match'):
            with self.assertRaises(AssertionError) as err:
                response = self._get_page_response('expanded_test_cases:three-messages')
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
            response = self._get_page_response('expanded_test_cases:login')
            self.assertPageContent(response, '')

        with self.subTest('Standard Response - Login Page'):
            response = self._get_page_response('expanded_test_cases:login')
            self.assertPageContent(response, '<h1>Login Page Header</h1><p>Pretend this is a login page.</p>')

        with self.subTest('Standard Response, missing part of value'):
            response = self._get_page_response('expanded_test_cases:login')
            self.assertPageContent(response, '<h1>Login Page Header</h1>')
            self.assertPageContent(response, '<p>Pretend this is a login page.</p>')

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('expanded_test_cases:index')
            self.assertPageContent(response, '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>')

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('expanded_test_cases:template-response-index')
            self.assertPageContent(response, '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>')

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('expanded_test_cases:one-message')
            self.assertPageContent(
                response,
                (
                    '<ul><li><p>This is a test message.</p></li></ul>'
                    '<h1>View with One Message Header</h1>'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>'
                ),
            )

        with self.subTest('Standard Response - Set of items on index page'):
            response = self._get_page_response('expanded_test_cases:index')
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
            response = self._get_page_response('expanded_test_cases:user-detail', args=(1,))

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
            response = self._get_page_response('expanded_test_cases:user-detail', args=(1,))

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
            response = self._get_page_response('expanded_test_cases:index')
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
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')

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
                response = self._get_page_response('expanded_test_cases:login')
                self.assertPageContent(response, '<h1>Testing Header</h1><p>Pretend this is a page.</p>')
            self.assertEqual(
                str(err.exception),
                exception_msg_not_found.format('<h1>Testing Header</h1><p>Pretend this is a page.</p>'),
            )

        with self.subTest('Standard Response - Set of items with wrong values'):
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:user-detail', args=(1,))

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
        response = self._get_page_response('expanded_test_cases:index')

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
        response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')

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
            response = self._get_page_response('expanded_test_cases:index')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 0)

        with self.subTest('Single message'):
            response = self._get_page_response('expanded_test_cases:one-message')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 1)
            self.assertIn('This is a test message.', messages)

        with self.subTest('Two messages'):
            response = self._get_page_response('expanded_test_cases:two-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 2)
            self.assertIn('Test message #1.', messages)
            self.assertIn('Test message #2.', messages)

        with self.subTest('Three messages'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 3)
            self.assertIn('Test info message.', messages)
            self.assertIn('Test warning message.', messages)
            self.assertIn('Test error message.', messages)

        with self.subTest('TemplateResponse check'):
            response = self._get_page_response('expanded_test_cases:template-response-messages')
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
            response = self._get_page_response('expanded_test_cases:login')
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
            response = self._get_page_response('expanded_test_cases:index')
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
            response = self._get_page_response('expanded_test_cases:template-response-index')
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
            response = self._get_page_response('expanded_test_cases:one-message')
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
            response = self._get_page_response('expanded_test_cases:login')
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
            response = self._get_page_response('expanded_test_cases:index')
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
            response = self._get_page_response('expanded_test_cases:template-response-index')
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
            response = self._get_page_response('expanded_test_cases:one-message')
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

    # endregion Helper Function Tests
