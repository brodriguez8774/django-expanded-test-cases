"""
Tests for test_cases/integration_test_case.py "helper function" utilities and logic.
"""

# System Imports.
import logging

# Third-Party Imports.
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

# Internal Imports.
from django_expanded_test_cases import IntegrationTestCase


class IntegrationHelperTestCase:
    """Tests for IntegrationTestCase class "helper function" utilities and logic.

    This class is a parent class that should not run by itself.
    It needs to be imported into other classes to execute.
    """

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
            self.assertEqual(return_val, AnonymousUser())

            # Verify user is still not logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

        # Reset login state.
        self.client.logout()

        with self.subTest('No login as test admin'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should not log in provided user.
            return_val = self._get_login_user('test_admin', auto_login=False)
            self.assertEqual(return_val, AnonymousUser())

            # Verify user is still not logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

        # Reset login state.
        self.client.logout()

        with self.subTest('No login as test superuser'):
            # Verify no user is logged in.
            self.assertNotIn('_auth_user_id', self.client.session.keys())

            # Run _get_login_user() function. Should not log in provided user.
            return_val = self._get_login_user('test_superuser', auto_login=False)
            self.assertEqual(return_val, AnonymousUser())

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
            self.assertText('', self.get_page_title(response))
            self.assertText('', self.get_page_title(response.content))
            self.assertText('', self.get_page_title(response.content.decode('utf-8')))

        with self.subTest('Title exists, but is empty'):
            response = HttpResponse('<title></title>')
            self.assertText('', self.get_page_title(response))
            self.assertText('', self.get_page_title(response.content))
            self.assertText('', self.get_page_title(response.content.decode('utf-8')))

        with self.subTest('Title exists, but is whitespace'):
            response = HttpResponse('<title>   </title>')
            self.assertText('', self.get_page_title(response))
            self.assertText('', self.get_page_title(response.content))
            self.assertText('', self.get_page_title(response.content.decode('utf-8')))

    def test__get_page_title__populated_title(self):
        """
        Tests get_page_title() function, when page title is populated.
        """
        with self.subTest('Basic title'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertText('Test Title', self.get_page_title(response))
            self.assertText('Test Title', self.get_page_title(response.content))
            self.assertText('Test Title', self.get_page_title(response.content.decode('utf-8')))

        with self.subTest('Basic title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<title>   Test    Title   </title>')
            self.assertText('Test Title', self.get_page_title(response))
            self.assertText('Test Title', self.get_page_title(response.content))
            self.assertText('Test Title', self.get_page_title(response.content.decode('utf-8')))

        with self.subTest('Complex title'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertText(
                'Test Title | My Custom App | My Really Cool Site',
                self.get_page_title(response),
            )
            self.assertText(
                'Test Title | My Custom App | My Really Cool Site',
                self.get_page_title(response.content),
            )
            self.assertText(
                'Test Title | My Custom App | My Really Cool Site',
                self.get_page_title(response.content.decode('utf-8')),
            )

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertText(
                'Test Title | My Custom App | My Really Cool Site',
                self.get_page_title(response),
            )
            self.assertText(
                'Test Title | My Custom App | My Really Cool Site',
                self.get_page_title(response.content),
            )
            self.assertText(
                'Test Title | My Custom App | My Really Cool Site',
                self.get_page_title(response.content.decode('utf-8')),
            )

    def test__get_page_header__empty_header(self):
        """
        Tests get_page_header() function, when page H1 header is empty.
        """
        with self.subTest('No header element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertText('', self.get_page_header(response))
            self.assertText('', self.get_page_header(response.content))
            self.assertText('', self.get_page_header(response.content.decode('utf-8')))

        with self.subTest('Header exists, but is empty'):
            response = HttpResponse('<h1></h1>')
            self.assertText('', self.get_page_header(response))
            self.assertText('', self.get_page_header(response.content))
            self.assertText('', self.get_page_header(response.content.decode('utf-8')))

        with self.subTest('Header exists, but is whitespace'):
            response = HttpResponse('<h1>   </h1>')
            self.assertText('', self.get_page_header(response))
            self.assertText('', self.get_page_header(response.content))
            self.assertText('', self.get_page_header(response.content.decode('utf-8')))

    def test__get_page_header__populated_header(self):
        """
        Tests get_page_header() function, when page H1 header is populated.
        """
        with self.subTest('Basic header'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertText('Test Header', self.get_page_header(response))
            self.assertText('Test Header', self.get_page_header(response.content))
            self.assertText('Test Header', self.get_page_header(response.content.decode('utf-8')))

        with self.subTest('Basic header, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<h1>   Test    Header   </h1>')
            self.assertText('Test Header', self.get_page_header(response))
            self.assertText('Test Header', self.get_page_header(response.content))
            self.assertText('Test Header', self.get_page_header(response.content.decode('utf-8')))

    def test__get_context_messages(self):
        """
        Tests get_context_messages() function.
        """
        with self.subTest('No messages'):
            response = self._get_page_response('django_expanded_test_cases:home')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 0)

        with self.subTest('Single message'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 1)
            self.assertIn('This is a test message.', messages)

        with self.subTest('Two messages'):
            response = self._get_page_response('django_expanded_test_cases:response-with-two-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 2)
            self.assertIn('Test message #1.', messages)
            self.assertIn('Test message #2.', messages)

        with self.subTest('Three messages'):
            response = self._get_page_response('django_expanded_test_cases:response-with-three-messages')
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
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - Outer whitespace'):
            response = HttpResponse('&nbsp; <h1>Test Title</h1> &nbsp; ')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - With Newlines'):
            response = HttpResponse('<h1>Test  \n  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Standard Response - Login Page'):
            response = self._get_page_response('django_expanded_test_cases:login')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText(
                (
                    '<head><meta charset="utf-8"><title>Login Page | Test Views</title></head>'
                    '<body>'
                    '<h1>Login Page Header</h1><p>Pretend this is a login page.</p>'
                    '</body>'
                ),
                response,
            )

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('django_expanded_test_cases:home')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText(
                (
                    '<head><meta charset="utf-8"><title>Home Page | Test Views</title></head>'
                    '<body>'
                    '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>'
                    '</body>'
                ),
                response,
            )

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('django_expanded_test_cases:template-response-home')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText(
                (
                    '<head><meta charset="utf-8"><title>Home Page | Test Views</title></head>'
                    '<body>'
                    '<h1>Home Page Header</h1><p>Pretend this is the project landing page.</p>'
                    '</body>'
                ),
                response,
            )

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            response = self.get_minimized_response_content(response, strip_newlines=True)
            self.assertText(
                (
                    '<head><meta charset="utf-8"><title>View with One Message | Test Views</title></head>'
                    '<body>'
                    '<ul><li><p>This is a test message.</p></li></ul>'
                    '<h1>View with One Message Header</h1>'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>'
                    '</body>'
                ),
                response,
            )

    def test__get_minimized_response_content__strip_newlines_is_false(self):
        """
        Tests get_minimized_response_content() function.
        """
        with self.subTest('Minimal Response - No change'):
            response = HttpResponse('<h1>Test Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - Outer whitespace'):
            response = HttpResponse('&nbsp; <h1>Test Title</h1> &nbsp; ')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - Inner whitespace'):
            response = HttpResponse('<h1>Test  &nbsp;  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText('<h1>Test Title</h1>', response)

        with self.subTest('Minimal Response - With Newlines'):
            response = HttpResponse('<h1>Test  \n  Title</h1>')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText('<h1>Test \n Title</h1>', response)

        with self.subTest('Standard Response - Login Page'):
            response = self._get_page_response('django_expanded_test_cases:login')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText(
                (
                    '<head>\n<meta charset="utf-8">\n<title>Login Page | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<h1>Login Page Header</h1>\n<p>Pretend this is a login page.</p>\n'
                    '</body>'
                ),
                response,
            )

        with self.subTest('Standard Response - Render() Home Page'):
            response = self._get_page_response('django_expanded_test_cases:home')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText(
                (
                    '<head>\n<meta charset="utf-8">\n<title>Home Page | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<h1>Home Page Header</h1>\n<p>Pretend this is the project landing page.</p>\n'
                    '</body>'
                ),
                response,
            )

        with self.subTest('Standard Response - TemplateResponse Home Page'):
            response = self._get_page_response('django_expanded_test_cases:template-response-home')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText(
                (
                    '<head>\n<meta charset="utf-8">\n<title>Home Page | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<h1>Home Page Header</h1>\n<p>Pretend this is the project landing page.</p>\n'
                    '</body>'
                ),
                response,
            )

        with self.subTest('Standard Response - One Message Page'):
            response = self._get_page_response('django_expanded_test_cases:response-with-one-message')
            response = self.get_minimized_response_content(response, strip_newlines=False)
            self.assertText(
                (
                    '<head>\n<meta charset="utf-8">\n<title>View with One Message | Test Views</title>\n</head>\n'
                    '<body>\n'
                    '<ul>\n<li><p>\n This is a test message.\n</p></li>\n</ul>\n'
                    '<h1>View with One Message Header</h1>\n'
                    '<p>Pretend useful stuff is displayed here, for one-message render() view.</p>\n'
                    '</body>'
                ),
                response,
            )

    def test__standardize_url__success(self):
        """
        Tests standardize_url() function, in situations when it should succeed.
        """

        with self.subTest('Emtpy url'):
            # Base url.
            url = self.standardize_url(
                '',
                append_root=False,
            )
            self.assertText('/', url)

            # With site root.
            url = self.standardize_url(
                '',
                append_root=True,
            )
            self.assertText('127.0.0.1/', url)

        with self.subTest('Basic url - No outer slashes'):
            # Base url.
            url = self.standardize_url(
                'login',
                append_root=False,
            )
            self.assertText('/login/', url)

            # With site root.
            url = self.standardize_url(
                'login',
                append_root=True,
            )
            self.assertText('127.0.0.1/login/', url)

        with self.subTest('Basic url - With outer slashes'):
            # Base url.
            url = self.standardize_url(
                '/login/',
                append_root=False,
            )
            self.assertText('/login/', url)

            # With site root.
            url = self.standardize_url(
                '/login/',
                append_root=True,
            )
            self.assertText('127.0.0.1/login/', url)

        with self.subTest('Longer url - No outer slashes'):
            # Base url.
            url = self.standardize_url(
                'this/is/a/test/url',
                append_root=False,
            )
            self.assertText('/this/is/a/test/url/', url)

            # With site root.
            url = self.standardize_url(
                '/this/is/a/test/url/',
                append_root=True,
            )
            self.assertText('127.0.0.1/this/is/a/test/url/', url)

        with self.subTest('With GET args - Provided in url'):
            # Base url.
            url = self.standardize_url(
                '/my/url/?arg1=testing&arg2=aaa',
                append_root=False,
            )
            self.assertText('/my/url/?arg1=testing&arg2=aaa', url)

            # With site root.
            url = self.standardize_url(
                '/my/url/?arg1=testing&arg2=aaa',
                append_root=True,
            )
            self.assertText('127.0.0.1/my/url/?arg1=testing&arg2=aaa', url)

        with self.subTest('With GET args - Provided via generate_get_url()'):
            # Base url.
            url = self.standardize_url(
                self.generate_get_url('/my/url/', arg1='testing', arg2='aaa'),
                append_root=False,
            )
            self.assertText('/my/url/?arg1=testing&arg2=aaa', url)

            # With site root.
            url = self.standardize_url(
                self.generate_get_url('/my/url/', arg1='testing', arg2='aaa'),
                append_root=True,
            )
            self.assertText('127.0.0.1/my/url/?arg1=testing&arg2=aaa', url)

        with self.subTest('With GET args - Provided in url with mixed characters'):
            # Base url.
            url = self.standardize_url(
                '/my/url/?arg1=testing stuff?<blah>weird_values-aaa',
                append_root=False,
            )
            self.assertText('/my/url/?arg1=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

            # With site root.
            url = self.standardize_url(
                '/my/url/?arg1=testing stuff?<blah>weird_values-aaa',
                append_root=True,
            )
            self.assertText('127.0.0.1/my/url/?arg1=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

        with self.subTest('With GET args - Provided in generate_get_url() with mixed characters'):
            # Base url.
            url = self.standardize_url(
                self.generate_get_url('/my/url/?', test='testing stuff?<blah>weird_values-aaa'),
                append_root=False,
            )
            self.assertText('/my/url/?test=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

            # With site root.
            url = self.standardize_url(
                self.generate_get_url('/my/url/?', test='testing stuff?<blah>weird_values-aaa'),
                append_root=True,
            )
            self.assertText('127.0.0.1/my/url/?test=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

        with self.subTest('Basic resolve url'):
            # Base url.
            url = self.standardize_url(
                'django_expanded_test_cases:login',
                append_root=False,
            )
            self.assertText('/login/', url)

            # With site root.
            url = self.standardize_url(
                'django_expanded_test_cases:login',
                append_root=True,
            )
            self.assertText('127.0.0.1/login/', url)

        with self.subTest('Resolve url with params as args'):
            # Base url.
            url = self.standardize_url(
                'django_expanded_test_cases:response-with-args',
                url_args=(11, 'args_test_1'),
                append_root=False,
            )
            self.assertText('/views/11/args_test_1/', url)

            # With site root.
            url = self.standardize_url(
                'django_expanded_test_cases:response-with-args',
                url_args=(12, 'args_test_2'),
                append_root=True,
            )
            self.assertText('127.0.0.1/views/12/args_test_2/', url)

        with self.subTest('Resolve url with params as kwargs'):
            # Base url.
            url = self.standardize_url(
                'django_expanded_test_cases:response-with-args',
                url_kwargs={'id': 21, 'name': 'kwargs_test_1'},
                append_root=False,
            )
            self.assertText('/views/21/kwargs_test_1/', url)

            # With site root.
            url = self.standardize_url(
                'django_expanded_test_cases:response-with-args',
                url_kwargs={'id': 22, 'name': 'kwargs_test_2'},
                append_root=True,
            )
            self.assertText('127.0.0.1/views/22/kwargs_test_2/', url)

    def test__standardize_url__failure(self):
        """
        Tests standardize_url() function, in situations when it should fail.
        """
        with self.subTest('Resolve url with with args and kwargs'):
            # Base url.
            with self.assertRaises(ValueError):
                url = self.standardize_url(
                    'django_expanded_test_cases:response-with-args',
                    url_args=(31, 'testing'),
                    url_kwargs={'id': 31, 'name': 'testing'},
                    append_root=False,
                )

            # With site root.
            with self.assertRaises(ValueError):
                url = self.standardize_url(
                    'django_expanded_test_cases:response-with-args',
                    url_args=(31, 'testing'),
                    url_kwargs={'id': 31, 'name': 'testing'},
                    append_root=True,
                )

    def test__standardize_html_tags(self):
        """
        Tests letters in standardize_html_tags() functions.
        """
        with self.subTest('Test html tag - No spaces'):
            value = self.standardize_html_tags('<h1>Test Header</h1><p>Aaa</p>')
            self.assertText('<h1>Test Header</h1><p>Aaa</p>', value)

        with self.subTest('Test html tag - With spaces'):
            value = self.standardize_html_tags('  <h1>  Test Header  </h1> <p> Aaa </p>  ')
            self.assertText('<h1>Test Header</h1><p>Aaa</p>', value)

        with self.subTest('Test array - No spaces'):
            value = self.standardize_html_tags('[1, 2, 3]')
            self.assertText('[1, 2, 3]', value)

        with self.subTest('Test array - with spaces'):
            value = self.standardize_html_tags('  [  1, 2, 3  ]  ')
            self.assertText('[1, 2, 3]', value)

        with self.subTest('Test dict - No spaces'):
            value = self.standardize_html_tags('{"one": 1, "two": 2}')
            self.assertText('{"one": 1, "two": 2}', value)

        with self.subTest('Test dict - With spaces'):
            value = self.standardize_html_tags('{  "one": 1, "two": 2  }  ')
            self.assertText('{"one": 1, "two": 2}', value)

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
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is not present - Single-item response'):
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find element "<li>" in content. Provided content was:\n<p></p>'

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is not present - Single-item response'):
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find element "<li>" in content. Provided content was:\n<p></p>'

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is present multiple times'):
            response = HttpResponse('<li></li><li></li>')
            err_msg = (
                'Found multiple instances of "<li>" element. Expected only one instance. Content was:\n'
                '<li></li><li></li>'
            )

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(response, '</li>')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is not present - Single-item response'):
            response = HttpResponse('<p id="test"></p>')
            err_msg = 'Unable to find id "test_id" in content. Provided content was:\n<p id="test"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(response, 'test_id')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is not present - Single-item response'):
            response = HttpResponse('<p id="some_id"></p>')
            err_msg = 'Unable to find id "test_id" in content. Provided content was:\n<p id="some_id"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(response, 'test_id')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            response = HttpResponse('<p id="test_id"></p><p id="test_id"></p>')
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<p id="test_id"></p><p id="test_id"></p>'
            )
            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(response, 'test_id')
            self.assertText(err_msg, str(err.exception))

            # As mixed tags.
            response = HttpResponse('<li id="test_id"><p id="test_id">Test</p></li>')
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<li id="test_id"><p id="test_id">Test</p></li>'
            )
            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(response, 'test_id')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is not present - Single-item response'):
            response = HttpResponse('<p class="some_class"></p>')
            err_msg = 'Unable to find class "test_class" in content. Provided content was:\n<p class="some_class"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(response, 'test_class')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is not present - Single-item response'):
            response = HttpResponse('<p class="some_class"></p>')
            err_msg = 'Unable to find class "test_class" in content. Provided content was:\n<p class="some_class"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li class="test_class"></li><li class="test_class"></li>')
            err_msg = (
                'Found multiple instances of "test_class" class. Expected only one instance. Content was:\n'
                '<li class="test_class"></li><li class="test_class"></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            response = HttpResponse('<p class="test_class"></p><p class="test_class"></p>')
            err_msg = (
                'Found multiple instances of "test_class" class. Expected only one instance. Content was:\n'
                '<p class="test_class"></p><p class="test_class"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(response, 'test_class')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is not present - Single-item response'):
            # Missing all parts.
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<p></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing two parts.
            response = HttpResponse('<li></li>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<li></li>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing one part.
            response = HttpResponse('<li><p class="test_class"></p></li>')
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n<li><p class="test_class"></p></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(response, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is not present - Single-item response'):
            # Missing all parts.
            response = HttpResponse('<p></p>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<p></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing two parts.
            response = HttpResponse('<li></li>')
            err_msg = 'Unable to find css selector "li .test_class > a" in content. Provided content was:\n<li></li>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing one parts.
            response = HttpResponse('<li><p class="test_class"></p></li>')
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n<li><p class="test_class"></p></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(response, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute is not present - Single-item response'):
            response = HttpResponse('<p some_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute key is not present - Single-item response'):
            response = HttpResponse('<p some_attr="my_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="my_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute value is not present - Single-item response'):
            response = HttpResponse('<p my_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p my_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute is not present - Single-item response'):
            response = HttpResponse('<p some_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute key is not present - Single-item response'):
            response = HttpResponse('<p some_attr="my_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p some_attr="my_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute value is not present - Single-item response'):
            response = HttpResponse('<p my_attr="some_val"></p>')
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n<p my_attr="some_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li my_attr="my_val"></li><li my_attr="my_val"></li>')
            err_msg = (
                'Found multiple instances of "my_attr" data attribute with value "my_val". Expected only one instance. '
                'Content was:\n<li my_attr="my_val"></li><li my_attr="my_val"></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            response = HttpResponse('<p my_attr="my_val"></p><p my_attr="my_val"></p>')
            err_msg = (
                'Found multiple instances of "my_attr" data attribute with value "my_val". Expected only one instance. '
                'Content was:\n<p my_attr="my_val"></p><p my_attr="my_val"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(response, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected name is not present - Single-item response'):
            response = HttpResponse('<p name="other_name"></p>')
            err_msg = 'Unable to find name "test_name" in content. Provided content was:\n<p name="other_name"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(response, 'test_name')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected name is not present - Single-item response'):
            response = HttpResponse('<p name="other_name"></p>')
            err_msg = 'Unable to find name "test_name" in content. Provided content was:\n<p name="other_name"></p>'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is present multiple times'):
            # As <li> tag.
            response = HttpResponse('<li name="test_name"></li><li name="test_name"></li>')
            err_msg = (
                'Found multiple instances of "test_name" name. Expected only one instance. Content was:\n'
                '<li name="test_name"></li><li name="test_name"></li>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            response = HttpResponse('<p name="test_name"></p><p name="test_name"></p>')
            err_msg = (
                'Found multiple instances of "test_name" name. Expected only one instance. Content was:\n'
                '<p name="test_name"></p><p name="test_name"></p>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(response, 'test_name')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is not present - Single-item response'):
            response = HttpResponse('<a href="other_link_text"></a>')
            err_msg = (
                'Unable to find link text "test_link_text" in content. '
                'Provided content was:\n<a href="other_link_text"></a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(response, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is not present - Single-item response'):
            response = HttpResponse('<a href="other_link_text"></a>')
            err_msg = (
                'Unable to find link text "test_link_text" in content. '
                'Provided content was:\n<a href="other_link_text"></a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(response, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

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
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is present multiple times'):
            response = HttpResponse('<a href="test_link_text"></a><a href="test_link_text"></a>')
            err_msg = (
                'Found multiple instances of "test_link_text" link text. Expected only one instance. Content was:\n'
                '<a href="test_link_text"></a><a href="test_link_text"></a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(response, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_text__success(self):
        """
        Tests find_elements_by_text() function, in cases when it should succeed.
        """
        with self.subTest('When expected text is the only item, with standard element'):
            response = HttpResponse('<p>This are words test_element_text test test test.</p>')

            results = self.find_elements_by_text(response, 'test_element_text')
            self.assertEqual(len(results), 1)
            self.assertIn('<p>\n This are words test_element_text test test test.\n</p>', results)

        with self.subTest('When expected text exists multiple times - Two instances'):
            response = HttpResponse('<li>test_element_text One</li><li>test_element_text Two</li>')

            # By base element tag.
            results = self.find_elements_by_text(response, 'test_element_text')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n test_element_text One\n</li>', results)
            self.assertIn('<li>\n test_element_text Two\n</li>', results)

        with self.subTest('When expected text exists multiple times - Three instances plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><a href="">test_element_text One</a></li>
                        <li><a href="">test_element_text Two</a></li>
                        <li><a href="">other_element_textThree</a></li>
                    </ul>
                    <ul>
                        <li><a href="">test_element_text Four</a></li>
                        <li><a href="">another_element_text Five</a></li>
                        <li><a href="">test Six</a></li>
                    </ul>
                    <ul>
                        <li><a href="test_element_text">Seven</a></li>
                        <li><a data="test_element_text">Eight</a></li>
                        <li><a test_element_text="">Nine</a></li>
                    </ul>
                </div>
                """
            )
            results = self.find_elements_by_text(response, 'test_element_text')
            self.assertEqual(len(results), 3)
            self.assertIn('<a href="">\n test_element_text One\n</a>', results)
            self.assertIn('<a href="">\n test_element_text Two\n</a>', results)
            self.assertIn('<a href="">\n test_element_text Four\n</a>', results)

        with self.subTest('When expected text exists - Filtered by type'):
            response = HttpResponse(
                '<h1>test_element_text</h1>'
                '<h2>test_element_text</h2>'
                '<h3>test_element_text</h3>'
                '<h4>test_element_text</h4>'
                '<h5>test_element_text</h5>'
                '<h6>test_element_text</h6>'
                '<p>test_element_text</p>'
                '<span>test_element_text</span>'
                '<li>test_element_text</li>'
            )

            # Verify full results when not limiting by element type.
            results = self.find_elements_by_text(response, 'test_element_text')
            self.assertEqual(len(results), 9)

            # Verify results when limiting by each type.
            # Type h1.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h1')
            self.assertEqual(len(results), 1)
            self.assertIn('<h1>\n test_element_text\n</h1>', results)
            # Type h2.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h2')
            self.assertEqual(len(results), 1)
            self.assertIn('<h2>\n test_element_text\n</h2>', results)
            # Type h3.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h3')
            self.assertEqual(len(results), 1)
            self.assertIn('<h3>\n test_element_text\n</h3>', results)
            # Type h4.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h4')
            self.assertEqual(len(results), 1)
            self.assertIn('<h4>\n test_element_text\n</h4>', results)
            # Type h5.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h5')
            self.assertEqual(len(results), 1)
            self.assertIn('<h5>\n test_element_text\n</h5>', results)
            # Type h6.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h6')
            self.assertEqual(len(results), 1)
            self.assertIn('<h6>\n test_element_text\n</h6>', results)
            # Type p.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='p')
            self.assertEqual(len(results), 1)
            self.assertIn('<p>\n test_element_text\n</p>', results)
            # Type span.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='span')
            self.assertEqual(len(results), 1)
            self.assertIn('<span>\n test_element_text\n</span>', results)
            # Type li.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n test_element_text\n</li>', results)

        with self.subTest('When expected text exists - Filtered by type and multiple matches'):
            response = HttpResponse(
                '<h1>test_element_text One</h1>'
                '<h2>test_element_text One</h2>'
                '<h2>test_element_text Two</h2>'
                '<h3>test_element_text One</h3>'
                '<h3>test_element_text Two</h3>'
                '<h3>test_element_text Three</h3>'
            )

            # Verify full results when not limiting by element type.
            results = self.find_elements_by_text(response, 'test_element_text')
            self.assertEqual(len(results), 6)

            # Verify results when limiting by each type.
            # Type h1.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h1')
            self.assertEqual(len(results), 1)
            self.assertIn('<h1>\n test_element_text One\n</h1>', results)
            # Type h2.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h2')
            self.assertEqual(len(results), 2)
            self.assertIn('<h2>\n test_element_text One\n</h2>', results)
            self.assertIn('<h2>\n test_element_text Two\n</h2>', results)
            # Type h3.
            results = self.find_elements_by_text(response, 'test_element_text', element_type='h3')
            self.assertEqual(len(results), 3)
            self.assertIn('<h3>\n test_element_text One\n</h3>', results)
            self.assertIn('<h3>\n test_element_text Two\n</h3>', results)
            self.assertIn('<h3>\n test_element_text Three\n</h3>', results)

    def test__find_elements_by_text__failure(self):
        """
        Tests find_elements_by_text() function, in cases when it should fail.
        """
        with self.subTest('When expected text is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find element text "test_element_text" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Single-item response'):
            response = HttpResponse('<a href="">other_element_text</a>')
            err_msg = (
                'Unable to find element text "test_element_text" in content. '
                'Provided content was:\n<a href="">other_element_text</a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <a href="">other_element_text Some text.</a>
                    <a href="">another_element_text Some more text.</a>
                    <a href="">test Some text with the str "element_text" in it.</a>
                </div>
                """
            )
            err_msg = (
                'Unable to find element text "test_element_text" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="">other_element_text Some text.</a>\n'
                '<a href="">another_element_text Some more text.</a>\n'
                '<a href="">test Some text with the str "element_text" in it.</a>\n'
                '</div>\n'
            )
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text exists - But filtered by type that is not found'):
            response = HttpResponse(
                """
                <div>
                    <h1>test_element_text</h1>
                    <h2>test_element_text</h2>
                    <p>test_element_text</p>
                    <li>test_element_text</li>
                </div>
                """
            )

            # Verify full results when not limiting by element type.
            results = self.find_elements_by_text(response, 'test_element_text')
            self.assertEqual(len(results), 4)

            # Verify non-results when limiting by each non-present type.
            # Type h3.
            err_msg = (
                'Unable to find element text "test_element_text" in content under element type of "h3". '
                'Provided content was:\n'
                '<div>\n'
                '<h1>test_element_text</h1>\n'
                '<h2>test_element_text</h2>\n'
                '<p>test_element_text</p>\n'
                '<li>test_element_text</li>\n'
                '</div>\n'
            )
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(response, 'test_element_text', element_type='h3')
            self.assertText(err_msg, str(err.exception))
            # Type span.
            err_msg = (
                'Unable to find element text "test_element_text" in content under element type of "span". '
                'Provided content was:\n'
                '<div>\n'
                '<h1>test_element_text</h1>\n'
                '<h2>test_element_text</h2>\n'
                '<p>test_element_text</p>\n'
                '<li>test_element_text</li>\n'
                '</div>\n'
            )
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(response, 'test_element_text', element_type='span')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_text__success(self):
        """
        Tests find_element_by_text() function, in cases when it should succeed.
        """
        with self.subTest('When expected element is the only item, with standard element'):
            response = HttpResponse('<p>test_element_text</p>')

            results = self.find_element_by_text(response, 'test_element_text')
            self.assertText('<p>\n test_element_text\n</p>', results)

        with self.subTest('When expected element exists plus extra'):
            response = HttpResponse(
                """
                <div>
                    <ul>
                        <li><a href="">test_element_text One</a></li>
                    </ul>
                    <ul></ul>
                </div>
                <div>
                    <ul></ul>
                </div>
                """
            )
            results = self.find_element_by_text(response, 'test_element_text')
            self.assertText('<a href="">\n test_element_text One\n</a>', results)

    def test__find_element_by_text__failure(self):
        """
        Tests find_element_by_text() function, in cases when it should fail.
        """
        with self.subTest('When expected text is not present - Blank response'):
            response = HttpResponse('')
            err_msg = 'Unable to find element text "test_element_text" in content. Provided content was:\n'

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element_text is not present - Single-item response'):
            response = HttpResponse('<a href="">other_element_text</a>')
            err_msg = (
                'Unable to find element text "test_element_text" in content. '
                'Provided content was:\n<a href="">other_element_text</a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Multi-item response'):
            response = HttpResponse(
                """
                <div>
                    <h1>Page Header</h1>
                    <a href="">other_element_text Some text.</a>
                    <a href="">another_element_text Some more text.</a>
                    <a href="">test Some text with the str "element_text" in it.</a>
                </div>
                """
            )
            err_msg = (
                'Unable to find element text "test_element_text" in content. Provided content was:\n'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="">other_element_text Some text.</a>\n'
                '<a href="">another_element_text Some more text.</a>\n'
                '<a href="">test Some text with the str "element_text" in it.</a>\n'
                '</div>\n'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element_text is present multiple times'):
            response = HttpResponse('<a href="">test_element_text</a><a href="">test_element_text</a>')
            err_msg = (
                'Found multiple instances of "test_element_text" element text. Expected only one instance. '
                'Content was:\n'
                '<a href="">test_element_text</a><a href="">test_element_text</a>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(response, 'test_element_text')
            self.assertText(err_msg, str(err.exception))


class TestIntegrationHelpers(IntegrationTestCase, IntegrationHelperTestCase):
    """Runtime test execution of IntegrationTestCase class "helper function" logic,
    when using default project settings.
    """
    pass
