"""
Core testing logic, universal to all test cases.
"""

# System Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.http.response import HttpResponseBase
from django.utils.http import urlencode


class CoreTestCaseMixin:
    """Core testing logic, used in all other expanded TestCase classes.

    For compatibility, does not inherit from
        django.test.TestCase
        channels.testing.ChannelsLiveServerTestCase

    Inheriting from either (seems to) make it incompatible with the other.
    Therefore we treat this as a separate mixin that inherits from nothing, and is included in all.
    """

    # region Class Functions

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

    # region Helper Functions

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

    # endregion Helper Functions

    # region Debug Output Functions

    def print_debug_content(self, response_content):
        """Prints debug response page output."""

        # Handle for potential param types.
        if isinstance(response_content, HttpResponseBase):
            response_content = response_content.content.decode('utf-8')
        elif isinstance(response_content, bytes):
            response_content = response_content.decode('utf-8')

        # Print out data, if present.
        if response_content:
            self._debug_print()
            self._debug_print(('{0} {1} {0}'.format('=' * 10, 'response.content')))
            self._debug_print(response_content)
            self._debug_print()

    def print_debug_headers(self, response_headers):
        """Prints debug response header data."""

        # Handle for potential param types.
        if isinstance(response_headers, HttpResponseBase):
            # Actual attr name seemed to change based on settings definitions.
            # Unsure of why though? May want to figure out details at later date.
            # This should account for both instances I'm pretty sure I encountered, though.
            if hasattr(response_headers, 'headers'):
                response_headers = response_headers.headers
            elif hasattr(response_headers, '_headers'):
                response_headers = response_headers._headers
            else:
                response_headers = None

        self._debug_print()
        self._debug_print(('{0} {1} {0}'.format('=' * 10, 'response.headers')))

        # Print out data, if present.
        if response_headers is not None and len(response_headers) > 0:
            for key, value in response_headers.items():
                self._debug_print('    * "{0}": "{1}"'.format(key, value))
        else:
            self._debug_print('    No response headers found.')
        self._debug_print()

    def print_debug_context(self, response_context):
        """Prints debug response context data."""
        raise NotImplemented()

    def print_debug_session_data(self, client):
        """Prints debug response session data."""

        # Handle for potential param types.
        if isinstance(client, HttpResponseBase):
            client = client.client

        self._debug_print()
        self._debug_print('{0} {1} {0}'.format('=' * 10, 'client.session'))

        if client is not None and len(client.session.items()) > 0:
            for key, value in client.session.items():
                self._debug_print('    * {0}: {1}'.format(key, value))
        else:
            self._debug_print('    No session data found.')
        self._debug_print('')

    def print_debug_form_data(self, response_context):
        """Prints debug response form data."""
        raise NotImplemented()

    def print_debug_messages(self, response_context):
        """Prints debug response message data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            response_context = response_context.context

        self._debug_print()
        self._debug_print(('{0} {1} {0}'.format('=' * 10, 'response.context["messages"]')))

        # Print out data, if present.
        if response_context is not None and 'messages' in response_context:
            messages = response_context['messages']
            if len(messages) > 0:
                for message in messages:
                    self._debug_print('    * "{0}"'.format(message))
            else:
                self._debug_print('    No context messages found.')
        self._debug_print()

    def print_debug_user_info(self, user):
        """Prints debug user data."""

        self._debug_print()
        self._debug_print('{0} {1} {0}'.format('=' * 10, 'User Info'))

        # Only proceed if we got a proper user model.
        if isinstance(user, get_user_model()):

            # General user information.
            self._debug_print('    * Username: "{0}"'.format(user.username))
            self._debug_print('    * First: "{0}"'.format(user.first_name))
            self._debug_print('    * Last: "{0}"'.format(user.last_name))
            self._debug_print('    * Email: "{0}"'.format(user.email))

            # User auth data.
            self._debug_print('    * is_authenticated: {0}'.format(user.is_authenticated))

            # User groups.
            self._debug_print('    * User Groups: {0}'.format(user.groups.all()))

            # User permissions.
            self._debug_print('    * User Permissions: {0}'.format(user.user_permissions.all()))

            self._debug_print()

        else:
            self._debug_print('    * Invalid user "{0}" of type "{1}". Expected "{2}".'.format(
                user,
                type(user),
                type(get_user_model()),
            ))

    # endregion Debug Output Functions.

    # endregion Class Functions

    # region Properties

    @property
    def site_root_url(self):
        """"""
        return self._site_root_url

    @site_root_url.setter
    def site_root_url(self, value):
        """"""
        # Validate.
        value = str(value).strip()
        while len(value) > 0 and value[-1] == '/':
            value = value[:-1]

        # Save.
        self._site_root_url = value

    # endregion Properties
