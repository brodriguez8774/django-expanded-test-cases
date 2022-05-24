"""
Tests for test_cases/base_test_case.py.
"""

# System Imports.

# User Imports.
from django_expanded_test_cases.test_cases import BaseTestCase


class BaseClassTest(BaseTestCase):
    """Tests for BaseTestCase class."""

    def setUp(self):
        # Run parent setup logic.
        super().setUp()
        # Also call CoreMixin setup logic.
        self.set_up()

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
