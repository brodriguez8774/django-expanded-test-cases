"""
Tests for test_cases/base_test_case.py.
"""

# System Imports.

# User Imports.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django_expanded_test_cases.test_cases import BaseTestCase


class BaseClassTest(BaseTestCase):
    """Tests for BaseTestCase class."""

    def setUp(self):
        # Run parent setup logic.
        super().setUp()
        # Also call CoreMixin setup logic.
        self.set_up()

    # region User Management Function Tests

    def test__get_user(self):
        """
        Tests get_user() function.
        """
        with self.subTest('Test "test_superuser" user - Default password'):
            test_superuser = self.get_user('test_superuser')

            self.assertEqual(test_superuser, self.test_superuser)
            self.assertEqual(test_superuser.username, 'test_superuser')
            self.assertTrue(test_superuser.check_password('password'))
            self.assertEqual(test_superuser.unhashed_password, 'password')
            self.assertEqual(test_superuser.is_superuser, True)
            self.assertEqual(test_superuser.is_staff, False)

        with self.subTest('Test "test_admin" user - Default password'):
            test_admin = self.get_user('test_admin')

            self.assertEqual(test_admin, self.test_admin)
            self.assertEqual(test_admin.username, 'test_admin')
            self.assertTrue(test_admin.check_password('password'))
            self.assertEqual(test_admin.unhashed_password, 'password')
            self.assertEqual(test_admin.is_superuser, False)
            self.assertEqual(test_admin.is_staff, True)

        with self.subTest('Test "test_user" user - Default password'):
            test_user = self.get_user('test_user')

            self.assertEqual(test_user, self.test_user)
            self.assertEqual(test_user.username, 'test_user')
            self.assertTrue(test_user.check_password('password'))
            self.assertEqual(test_user.unhashed_password, 'password')
            self.assertEqual(test_user.is_superuser, False)
            self.assertEqual(test_user.is_staff, False)

    def test__add_user_permission(self):
        """
        Tests add_user_permission() function.
        """
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

        # Verify initial user Permissions.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add perm by codename'):
            # Test adding permission.
            self.add_user_permission('test_perm_1', user='test_user')
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Test adding different permission.
            self.add_user_permission('test_perm_2', user='test_admin')
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

        with self.subTest('Test add perm by name'):
            # Test adding permission.
            self.add_user_permission('Test Perm 1', user='test_user')
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Test adding different permission.
            self.add_user_permission('Test Perm 2', user='test_admin')
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

    def test__add_user_group(self):
        """
        Tests add_user_group() function.
        """
        # Initialize Group models.
        group_1 = Group.objects.create(name='group_1')
        group_2 = Group.objects.create(name='group_2')

        # Verify initial user Groups.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        # Test adding group.
        self.add_user_group('group_1', user='test_user')
        self.assertEqual(self.test_user.groups.all().count(), 1)
        self.assertEqual(self.test_user.groups.all()[0], group_1)

        # Test adding different group.
        self.add_user_group('group_2', user='test_admin')
        self.assertEqual(self.test_admin.groups.all().count(), 1)
        self.assertEqual(self.test_admin.groups.all()[0], group_2)

        # Verify other users are unaffected.
        self.assertFalse(self.test_superuser.groups.all().exists())

    # endregion User Management Function Tests

    def test__generate_get_url(self):
        """
        Tests generate_get_url() function.
        """
        with self.subTest('Generate from passed "url" param'):
            # Test no params.
            url = self.generate_get_url('http://127.0.0.1/')
            self.assertEqual(url, 'http://127.0.0.1/')

            # Test one str param.
            url = self.generate_get_url('http://127.0.0.1/', test_1='one')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one')

            # Test two str params.
            url = self.generate_get_url('http://127.0.0.1/', test_1='one', test_2='two')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one&test_2=two')

            # Test one non-str simple param.
            url = self.generate_get_url('http://127.0.0.1/', test_1=1)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1')

            # Test two non-str simple params.
            url = self.generate_get_url('http://127.0.0.1/', test_1=1, test_2=True)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1&test_2=True')

            # Test one non-str complex param.
            url = self.generate_get_url('http://127.0.0.1/', test_1=['a', 'b', 'c'])
            self.assertEqual(url, 'http://127.0.0.1/?test_1=%5B%27a%27%2C+%27b%27%2C+%27c%27%5D')

            # Test two non-str complex params.
            url = self.generate_get_url('http://127.0.0.1/', test_1=['foo', 'bar'], test_2={'cat': 'Tabby', 'dog': 'Spot'})
            self.assertEqual(
                url,
                (
                    'http://127.0.0.1/?test_1=%5B%27foo%27%2C+%27bar%27%5D&test_2=%7B%27cat%27%3A+'
                    '%27Tabby%27%2C+%27dog%27%3A+%27Spot%27%7D'
                ),
            )

        with self.subTest('Generate from class "self.url" variable'):
            # Set class variable.
            self.url = 'http://127.0.0.1/'

            # Test no params.
            url = self.generate_get_url()
            self.assertEqual(url, 'http://127.0.0.1/')

            # Test one str param.
            url = self.generate_get_url(test_1='one')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one')

            # Test two str params.
            url = self.generate_get_url(test_1='one', test_2='two')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one&test_2=two')

            # Test one non-str simple param.
            url = self.generate_get_url(test_1=1)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1')

            # Test two non-str simple params.
            url = self.generate_get_url(test_1=1, test_2=True)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1&test_2=True')

            # Test one non-str complex param.
            url = self.generate_get_url(test_1=['a', 'b', 'c'])
            self.assertEqual(url, 'http://127.0.0.1/?test_1=%5B%27a%27%2C+%27b%27%2C+%27c%27%5D')

            # Test two non-str complex params.
            url = self.generate_get_url(test_1=['foo', 'bar'], test_2={'cat': 'Tabby', 'dog': 'Spot'})
            self.assertEqual(
                url,
                (
                    'http://127.0.0.1/?test_1=%5B%27foo%27%2C+%27bar%27%5D&test_2=%7B%27cat%27%3A+'
                    '%27Tabby%27%2C+%27dog%27%3A+%27Spot%27%7D'
                ),
            )
