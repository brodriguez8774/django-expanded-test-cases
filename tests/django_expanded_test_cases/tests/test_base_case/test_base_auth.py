"""
Tests for tests/base_test_case.py under different project authentication settings.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Internal Imports.
from django_expanded_test_cases import BaseTestCase


class TestBaseClassAuth__Base(BaseTestCase):

    # region User Management Function Tests

    def test__get_user__with_project_defaults(self):
        """
        Tests get_user() function.
        """
        with self.subTest('Test "test_superuser" user - With project defaults'):
            test_superuser = self.get_user('test_superuser')

            self.assertEqual(test_superuser, self.test_superuser)
            self.assertEqual(test_superuser.username, 'test_superuser')
            self.assertTrue(test_superuser.check_password('password'))
            self.assertEqual(test_superuser.unhashed_password, 'password')
            self.assertEqual(test_superuser.first_name, 'SuperUserFirst')
            self.assertEqual(test_superuser.last_name, 'SuperUserLast')
            self.assertEqual(test_superuser.email, 'super_user@example.com')
            self.assertEqual(test_superuser.is_superuser, True)
            self.assertEqual(test_superuser.is_staff, False)
            self.assertEqual(test_superuser.is_active, True)

        with self.subTest('Test "test_admin" user - With project defaults'):
            test_admin = self.get_user('test_admin')

            self.assertEqual(test_admin, self.test_admin)
            self.assertEqual(test_admin.username, 'test_admin')
            self.assertTrue(test_admin.check_password('password'))
            self.assertEqual(test_admin.unhashed_password, 'password')
            self.assertEqual(test_admin.first_name, 'AdminUserFirst')
            self.assertEqual(test_admin.last_name, 'AdminUserLast')
            self.assertEqual(test_admin.email, 'admin_user@example.com')
            self.assertEqual(test_admin.is_superuser, False)
            self.assertEqual(test_admin.is_staff, True)
            self.assertEqual(test_admin.is_active, True)

        with self.subTest('Test "test_inactive" user - With project defaults'):
            test_inactive = self.get_user('test_inactive')

            self.assertEqual(test_inactive, self.test_inactive_user)
            self.assertEqual(test_inactive.username, 'test_inactive')
            self.assertTrue(test_inactive.check_password('password'))
            self.assertEqual(test_inactive.unhashed_password, 'password')
            self.assertEqual(test_inactive.first_name, 'InactiveUserFirst')
            self.assertEqual(test_inactive.last_name, 'InactiveUserLast')
            self.assertEqual(test_inactive.email, 'inactive_user@example.com')
            self.assertEqual(test_inactive.is_superuser, False)
            self.assertEqual(test_inactive.is_staff, False)
            self.assertEqual(test_inactive.is_active, False)

        with self.subTest('Test "test_user" user - With project defaults'):
            test_user = self.get_user('test_user')

            self.assertEqual(test_user, self.test_user)
            self.assertEqual(test_user.username, 'test_user')
            self.assertTrue(test_user.check_password('password'))
            self.assertEqual(test_user.unhashed_password, 'password')
            self.assertEqual(test_user.first_name, 'UserFirst')
            self.assertEqual(test_user.last_name, 'UserLast')
            self.assertEqual(test_user.email, 'user@example.com')
            self.assertEqual(test_user.is_superuser, False)
            self.assertEqual(test_user.is_staff, False)
            self.assertEqual(test_user.is_active, True)

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

        with self.subTest('Test add permission to default user'):
            # In context of this test, the "default user" is test_user.

            # Test adding permission.
            return_val = self.add_user_permission('test_perm_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add permission by direct model'):
            # Test adding permission.
            return_val = self.add_user_permission(perm_1, user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self.add_user_permission(perm_2, user='test_admin')
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

        with self.subTest('Test add permission by codename'):
            # Test adding permission.
            return_val = self.add_user_permission('test_perm_1', user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self.add_user_permission('test_perm_2', user='test_admin')
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

        with self.subTest('Test add permission by name'):
            # Test adding permission.
            return_val = self.add_user_permission('Test Perm 1', user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self.add_user_permission('Test Perm 2', user='test_admin')
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

        with self.subTest('Test add permission by class user'):
            # Test adding permission.
            self.user = 'test_user'
            return_val = self.add_user_permission('test_perm_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            self.user = 'test_admin'
            return_val = self.add_user_permission('test_perm_2')
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

        with self.subTest('Test add group to default user'):
            # In context of this test, the "default user" is test_user.

            # Test adding group.
            return_val = self.add_user_group('group_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add group to user by direct model'):
            # Test adding group.
            return_val = self.add_user_group(group_1, user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different group.
            return_val = self.add_user_group(group_2, user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add permission to user by name'):
            # Test adding group.
            return_val = self.add_user_group('group_1', user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different group.
            return_val = self.add_user_group('group_2', user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add group by class user'):
            # Test adding group.
            self.user = self.test_user
            return_val = self.add_user_group('group_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different group.
            self.user = self.test_admin
            return_val = self.add_user_group('group_2')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

    # endregion User Management Function Tests


# TODO: For now, patching doesn't seem to work. Unsure why because the "real name" test works fine.
#   Figure out later.
# @override_settings(DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD='changed_value')
# class BaseClassTest_WithModifiedPassword(BaseTestCase):
#     """Tests for BaseTestCase class, when using settings to generate users with different passwords.
#
#     Required as a separate class, since user generation is handled on class initialization.
#     """
#     @classmethod
#     @patch('django_expanded_test_cases.mixins.core_mixin.ETC_DEFAULT_USER_PASSWORD', 'changed_value')
#     def setUpTestData(cls):
#         # Call parent logic.
#         super().setUpTestData()
#
#     # @patch('django_expanded_test_cases.mixins.core_mixin.ETC_DEFAULT_USER_PASSWORD', 'changed_value')
#     # def get_user(self, *args, **kwargs):
#     #     # Call parent logic.
#     #     return super().get_user(*args, **kwargs)
#
#     def test__get_user__with_modified_password(self):
#         """
#         Tests get_user() function.
#
#         Note: We test all expected model attributes, to ensure that the setting doesn't change anything unexpected.
#         """
#
#         with self.subTest('Test "test_superuser" user - With modified password'):
#             test_superuser = self.get_user('test_superuser')
#
#             print('password: "{0}"'.format(test_superuser.unhashed_password))
#
#             self.assertEqual(test_superuser, self.test_superuser)
#             self.assertEqual(test_superuser.username, 'test_superuser')
#             self.assertTrue(test_superuser.check_password('changed_value'))
#             self.assertEqual(test_superuser.unhashed_password, 'changed_value')
#             self.assertEqual(test_superuser.first_name, 'SuperUserFirst')
#             self.assertEqual(test_superuser.last_name, 'SuperUserLast')
#             self.assertEqual(test_superuser.email, 'super_user@example.com')
#             self.assertEqual(test_superuser.is_superuser, True)
#             self.assertEqual(test_superuser.is_staff, False)
#             self.assertEqual(test_superuser.is_active, True)
#
#         with self.subTest('Test "test_admin" user - With modified password'):
#             test_admin = self.get_user('test_admin')
#
#             self.assertEqual(test_admin, self.test_admin)
#             self.assertEqual(test_admin.username, 'test_admin')
#             self.assertTrue(test_admin.check_password('changed_value'))
#             self.assertEqual(test_admin.unhashed_password, 'changed_value')
#             self.assertEqual(test_admin.first_name, 'AdminUserFirst')
#             self.assertEqual(test_admin.last_name, 'AdminUserLast')
#             self.assertEqual(test_admin.email, 'admin_user@example.com')
#             self.assertEqual(test_admin.is_superuser, False)
#             self.assertEqual(test_admin.is_staff, True)
#             self.assertEqual(test_admin.is_active, True)
#
#         with self.subTest('Test "test_inactive" user - With modified password'):
#             test_inactive = self.get_user('test_inactive')
#
#             self.assertEqual(test_inactive, self.test_inactive_user)
#             self.assertEqual(test_inactive.username, 'test_inactive')
#             self.assertTrue(test_inactive.check_password('changed_value'))
#             self.assertEqual(test_inactive.unhashed_password, 'changed_value')
#             self.assertEqual(test_inactive.first_name, 'InactiveUserFirst')
#             self.assertEqual(test_inactive.last_name, 'InactiveUserLast')
#             self.assertEqual(test_inactive.email, 'inactive_user@example.com')
#             self.assertEqual(test_inactive.is_superuser, False)
#             self.assertEqual(test_inactive.is_staff, False)
#             self.assertEqual(test_inactive.is_active, False)
#
#         with self.subTest('Test "test_user" user - With modified password'):
#             test_user = self.get_user('test_user')
#
#             self.assertEqual(test_user, self.test_user)
#             self.assertEqual(test_user.username, 'test_user')
#             self.assertTrue(test_user.check_password('changed_value'))
#             self.assertEqual(test_user.unhashed_password, 'changed_value')
#             self.assertEqual(test_user.first_name, 'UserFirst')
#             self.assertEqual(test_user.last_name, 'UserLast')
#             self.assertEqual(test_user.email, 'user@example.com')
#             self.assertEqual(test_user.is_superuser, False)
#             self.assertEqual(test_user.is_staff, False)
#             self.assertEqual(test_user.is_active, True)


class TestBaseClassAuth_WithRealNames(BaseTestCase):
    """Tests for BaseTestCase class, when using settings to generate users with real names.

    Required as a separate class, since user generation is handled on class initialization.
    """

    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_GENERATE_USERS_WITH_REAL_NAMES', True)
    def setUp(cls):
        # Call parent logic.
        super().setUp()

    def test__get_user__with_real_names(self):
        """
        Tests get_user() function.

        Note: We test all expected model attributes, to ensure that the setting doesn't change anything unexpected.
        """
        with self.subTest('Test "test_superuser" user - With real names'):
            test_superuser = self.get_user('test_superuser')

            self.assertEqual(test_superuser, self.test_superuser)
            self.assertEqual(test_superuser.username, 'test_superuser')
            self.assertTrue(test_superuser.check_password('password'))
            self.assertEqual(test_superuser.unhashed_password, 'password')
            self.assertEqual(test_superuser.first_name, 'John')
            self.assertEqual(test_superuser.last_name, 'Doe')
            self.assertEqual(test_superuser.email, 'super_user@example.com')
            self.assertEqual(test_superuser.is_superuser, True)
            self.assertEqual(test_superuser.is_staff, False)
            self.assertEqual(test_superuser.is_active, True)

        with self.subTest('Test "test_admin" user - With real names'):
            test_admin = self.get_user('test_admin')

            self.assertEqual(test_admin, self.test_admin)
            self.assertEqual(test_admin.username, 'test_admin')
            self.assertTrue(test_admin.check_password('password'))
            self.assertEqual(test_admin.unhashed_password, 'password')
            self.assertEqual(test_admin.first_name, 'Jenny')
            self.assertEqual(test_admin.last_name, 'Johnson')
            self.assertEqual(test_admin.email, 'admin_user@example.com')
            self.assertEqual(test_admin.is_superuser, False)
            self.assertEqual(test_admin.is_staff, True)
            self.assertEqual(test_admin.is_active, True)

        with self.subTest('Test "test_inactive" user - With real names'):
            test_inactive = self.get_user('test_inactive')

            self.assertEqual(test_inactive, self.test_inactive_user)
            self.assertEqual(test_inactive.username, 'test_inactive')
            self.assertTrue(test_inactive.check_password('password'))
            self.assertEqual(test_inactive.unhashed_password, 'password')
            self.assertEqual(test_inactive.first_name, 'Clang')
            self.assertEqual(test_inactive.last_name, 'Zythor')
            self.assertEqual(test_inactive.email, 'inactive_user@example.com')
            self.assertEqual(test_inactive.is_superuser, False)
            self.assertEqual(test_inactive.is_staff, False)
            self.assertEqual(test_inactive.is_active, False)

        with self.subTest('Test "test_user" user - With real names'):
            test_user = self.get_user('test_user')

            self.assertEqual(test_user, self.test_user)
            self.assertEqual(test_user.username, 'test_user')
            self.assertTrue(test_user.check_password('password'))
            self.assertEqual(test_user.unhashed_password, 'password')
            self.assertEqual(test_user.first_name, 'Sammy')
            self.assertEqual(test_user.last_name, 'Smith')
            self.assertEqual(test_user.email, 'user@example.com')
            self.assertEqual(test_user.is_superuser, False)
            self.assertEqual(test_user.is_staff, False)
            self.assertEqual(test_user.is_active, True)
