"""
Core testing logic, universal to all test cases.
"""

# System Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.http import urlencode


class CoreTestCaseMixin:
    """Core testing logic, used in all other expanded TestCase classes.

    For compatibility, does not inherit from
        django.test.TestCase
        channels.testing.ChannelsLiveServerTestCase

    Inheriting from either (seems to) make it incompatible with the other.
    Therefore we treat this as a separate mixin that inherits from nothing, and is included in all.
    """
    def set_up(self, debug_print=None):
        """
        Acts as the equivalent of the UnitTesting "setUp()" function.

        However, since this is not inheriting from a given TestCase, calling the literal function
        here would override instead.
        :param debug_print: Optional bool that indicates if debug output should print to console.
            Overrides setting value if both are present.
        """
        # Generate "special case" test user instances.
        # Guarantees that there will always be at least some default User models when tests are run.
        self.test_superuser = get_user_model().objects.create_user(
            username='test_superuser',
            password='password',
            is_superuser=True,
        )
        self.test_admin = get_user_model().objects.create_user(
            username='test_admin',
            password='password',
            is_staff=True,
        )
        self.test_user = get_user_model().objects.create_user(username='test_user', password='password')

        # Check user debug_print option.
        if debug_print is not None:
            self._debug_print_bool = bool(debug_print)
        else:
            self._debug_print_bool = getattr(settings, 'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT', True)

    def _debug_print(self, *args, **kwargs):
        """Prints or suppresses output, based on DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT settings variable.

        Variable defaults to display output, if not provided.
        Mostly used for internal testcase logic.
        """
        if self._debug_print_bool:
            print(*args, **kwargs)

    # region User Management Functions

    def get_user(self, user, password='password'):
        """Returns user matching provided value.

        :param user: User model, or corresponding username, to use.
        :param password: Password str to assign to user.
        :return: User object
        """
        # Check if instance is User model.
        if isinstance(user, get_user_model()):
            # Already User model. This is fine.
            pass

        # Handle all "special cases" for testing logic.
        elif user == 'test_superuser':
            user = self.test_superuser
        elif user == 'test_admin':
            user = self.test_admin
        elif user == 'test_user':
            user = self.test_user

        else:
            # Is not User model. Get or create.
            try:
                user = get_user_model().objects.get(username=str(user))
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create(username=str(user))

        # Handle passwords.
        password = str(password).strip()
        if len(password) == 0:
            # Empty password. Reset back to default.
            password = 'password'
        user.set_password(password)
        user.unhashed_password = password
        user.save()

        return user

    def add_user_permission(self, user_permission, user='test_user'):
        """Adds Permission to given user.

        :param user_permission: Permission to add.
        :param user: User to add Permission to. If not provided, defaults to test_user model.
        :return: None
        """
        # Check if instance is a Permission model.
        if isinstance(user_permission, Permission):
            # Already Permission model. This is fine.
            permission = user_permission

        else:
            # Is not Permission model. Attempt to get.
            user_permission = str(user_permission)
            try:
                permission = Permission.objects.get(codename=user_permission)
            except Permission.DoesNotExist:
                # Failed to get by codename. Attempt again with name.
                try:
                    permission = Permission.objects.get(name=user_permission)
                except Permission.DoesNotExist:
                    raise ValueError('Failed to find permission of "{0}".'.format(user_permission))

        # If we made it this far, then valid Permission was found. Apply to user.
        self.get_user(user).user_permissions.add(permission)

    def add_user_group(self, user_group, user='test_user'):
        """Adds Group to given user.

        :param user_group: Group to add.
        :param user: User to add Group to. If not provided, defaults to test_user model.
        :return: None
        """
        # Check if instance is a Group model.
        if isinstance(user_group, Group):
            # Already Group model. This is fine.
            group = user_group

        else:
            # Is not Group model. Attempt to get.
            user_group = str(user_group)
            try:
                group = Group.objects.get(name=user_group)
            except Group.DoesNotExist:
                raise ValueError('Failed to find Group of "{0}".'.format(user_group))

        # If we made it this far, then valid Group was found. Apply to user.
        self.get_user(user).groups.add(group)

    # endregion User Management Functions

    def generate_get_url(self, url=None, **kwargs):
        """Generates a full GET request url, passing in the provided args.

        Note: Only kwargs are accepted, as this needs <key: value> pairs.
        Pairs are then written out to url, as query string values.
        :param url: Optional url value to use. If not provided, defaults to "self.url", if set.
        :param kwargs: The set of <key: value> pairs to append to end of GET url string.
        :return: Full GET request url string.
        """
        # Validate url to generate from.
        if url is None:
            # No arg provided. Default to class "self.url" value.
            url = self.url
        # Validate that we have an actual value.
        value_error = 'No url provided. Please provide the "url" param or set the "self.url" class value.'
        if url is None:
            raise ValueError(value_error)
        url = str(url).strip()
        if len(url) == 0:
            raise ValueError(value_error)

        # Finally, generate actual url and return.
        get_params = urlencode(kwargs)
        get_url = url + ('' if get_params == '' else '?' + get_params)
        self._debug_print('URL: {0}'.format(get_url))
        return get_url
