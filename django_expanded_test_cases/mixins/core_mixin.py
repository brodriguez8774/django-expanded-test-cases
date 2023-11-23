"""
Core testing logic, universal to all test cases.
"""

# System Imports.
import re
from functools import wraps
from types import FunctionType

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.utils.http import urlencode

# Internal Imports.
from django_expanded_test_cases.constants import (
    ETC_DEBUG_PRINT,
    ETC_AUTO_GENERATE_USERS,
    ETC_REQUEST_USER_STRICTNESS,
    ETC_USER_MODEL_IDENTIFIER,
    ETC_DEFAULT_SUPER_USER_IDENTIFIER,
    ETC_DEFAULT_ADMIN_USER_IDENTIFIER,
    ETC_DEFAULT_STANDARD_USER_IDENTIFIER,
    ETC_DEFAULT_INACTIVE_USER_IDENTIFIER,
    ETC_DEFAULT_USER_PASSWORD,
    ETC_GENERATE_USERS_WITH_REAL_NAMES,
    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_RESET_COLOR,
)


# region Debug Print Wrapper Logic

def wrapper(method):
    """Wrapper logic to intercept all functions on AssertionError and print error at bottom of output."""
    @wraps(method)
    def wrapped(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except AssertionError as err:
            if ETC_DEBUG_PRINT:
                print('\n')
                print('{0}{1}{2}'.format(ETC_OUTPUT_ERROR_COLOR, err, ETC_OUTPUT_RESET_COLOR))
                print('')
            raise err
    return wrapped


class DebugPrintMetaClass(type):
    """Courtesy of https://stackoverflow.com/a/11350487"""
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if isinstance(attribute, FunctionType):
                # Replace function with a DebugPrint-wrapped version.
                attribute = wrapper(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(meta, classname, bases, newClassDict)

# endregion Debug Print Wrapper Logic


class BaseMixin:
    """Base mixin that all other project classes should inherit from in some way.

    Basically only exists to guarantee certain expected functions exist during inheritance chain, unconditionally.
    Helps prevent MethodNotFound errors and make inheritance/super() calls easier to handle.
    """

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        """Test logic setup run at the start of class creation.

        Function is empty, but provided to prevent MethodNotFound errors
        in case super() is called from an inheriting child.
        """
        pass

    @classmethod
    def setUpTestData(cls, *args, **kwargs):
        """Test logic setup run at the start of class creation, specifically for data setup.

        Function is empty, but provided to prevent MethodNotFound errors
        in case super() is called from an inheriting child.
        """
        pass

    def setUp(self, *args, **kwargs):
        """Test logic setup run at the start of function/method execution.

        Function is empty, but provided to prevent MethodNotFound errors
        in case super() is called from an inheriting child.
        """
        pass

    def subTest(self, *args, **kwargs):
        """Test logic setup run every time we enter a subtest.

        Function is empty, but provided to prevent MethodNotFound errors
        in case super() is called from an inheriting child.
        """
        pass

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        """Test logic setup run at the end of class execution, as part of termination/clean up.

        Function is empty, but provided to prevent MethodNotFound errors
        in case super() is called from an inheriting child.
        """
        pass

    def tearDown(self, *args, **kwargs):
        """Test logic setup run at the end of function/method execution, as part of termination/clean up.

        Function is empty, but provided to prevent MethodNotFound errors
        in case super() is called from an inheriting child.
        """
        pass


class CoreTestCaseMixin(BaseMixin):
    """Core testing logic, used in all other expanded TestCase classes.

    For compatibility, does not inherit from
        django.test.TestCase
        channels.testing.ChannelsLiveServerTestCase

    Inheriting from either (seems to) make it incompatible with the other.
    Therefore we treat this as a separate mixin that inherits from nothing, and is included in all.
    """

    # region Class Functions

    @classmethod
    def setUpClass(cls, *args, debug_print=None, **kwargs):
        """Test logic setup run at the start of class creation.

        :param debug_print: Optional bool that indicates if debug output should print to console.
                            Param overrides setting value if both param and setting are set.
        """

        # Call parent logic.
        super().setUpClass(*args, **kwargs)

        # Check user debug_print option.
        if debug_print is not None:
            cls._debug_print_bool = bool(debug_print)
        else:
            cls._debug_print_bool = ETC_DEBUG_PRINT

        cls._site_root_url = None

    @classmethod
    def setUpTestData(cls, *args, extra_usergen_kwargs=None, **kwargs):
        """Test logic setup run at the start of class creation, specifically for data setup.

        :param extra_usergen_kwargs: Optional extra kwargs to pass into the get_user_model().objects.create_user()
                                     function.
        """

        # Call parent logic.
        super().setUpTestData(*args, **kwargs)

        if ETC_AUTO_GENERATE_USERS:
            # Run logic to auto-generate test users. Setting is on by default.
            if extra_usergen_kwargs is None:
                extra_usergen_kwargs = {}
            elif not isinstance(extra_usergen_kwargs, dict):
                raise ValueError(
                    'The extra_usergen_kwargs value must be a dictionary of additional args used in the '
                    'get_user_model().objects.create_user() function.'
                )

            cls._auto_generate_test_users(extra_usergen_kwargs=extra_usergen_kwargs)

    def subTest(self, *args, **kwargs):
        """Test logic setup run every time we enter a subtest.
        """

        # Call parent logic.
        super().subTest(*args, **kwargs)

        # Reset display error, in case multiple subtests run and fail in a given test.
        self._error_displayed = False

    @classmethod
    def _auto_generate_test_users(cls, extra_usergen_kwargs=None):
        """Logic to automatically generate test users.

        Only run if DJANGO_EXPANDED_TESTCASES_AUTO_GENERATE_USERS setting is true.
        """
        # Django imports here to avoid situational "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser

        if extra_usergen_kwargs is None:
            extra_usergen_kwargs = {}
        elif not isinstance(extra_usergen_kwargs, dict):
            raise ValueError(
                'The extra_usergen_kwargs value must be a dictionary of additional args used in the '
                'get_user_model().objects.create_user() function.'
            )

        # Generate "special case" test user instances.
        # Guarantees that there will always be at least some default User models when tests are run.

        # Superuser model. Can access/see everything, regardless of permissions.
        cls.test_superuser = get_user_model().objects.create_user(
            **{ETC_USER_MODEL_IDENTIFIER: ETC_DEFAULT_SUPER_USER_IDENTIFIER},
            password=ETC_DEFAULT_USER_PASSWORD,
            is_superuser=True,
            **extra_usergen_kwargs,
        )
        # Attempt to set fields and then save. If fields exist, then they will populate. Else are ignored.
        if ETC_GENERATE_USERS_WITH_REAL_NAMES:
            cls.test_superuser.first_name = 'John'
            cls.test_superuser.last_name = 'Doe'
            cls.test_superuser.name = 'John'
        else:
            cls.test_superuser.first_name = 'SuperUserFirst'
            cls.test_superuser.last_name = 'SuperUserLast'
            cls.test_superuser.name = 'SuperUserName'
        if ETC_USER_MODEL_IDENTIFIER.lower() != 'email':
            cls.test_superuser.email = 'super_user@example.com'
        cls.test_superuser.save()
        cls.test_superuser = cls.get_user(cls, ETC_DEFAULT_SUPER_USER_IDENTIFIER)

        # Admin user model. Can access Django admin.
        cls.test_admin = get_user_model().objects.create_user(
            **{ETC_USER_MODEL_IDENTIFIER: ETC_DEFAULT_ADMIN_USER_IDENTIFIER},
            password=ETC_DEFAULT_USER_PASSWORD,
            is_staff=True,
            **extra_usergen_kwargs,
        )
        # Attempt to set fields and then save. If fields exist, then they will populate. Else are ignored.
        if ETC_GENERATE_USERS_WITH_REAL_NAMES:
            cls.test_admin.first_name = 'Jenny'
            cls.test_admin.last_name = 'Johnson'
            cls.test_admin.name = 'Jenny'
        else:
            cls.test_admin.first_name = 'AdminUserFirst'
            cls.test_admin.last_name = 'AdminUserLast'
            cls.test_admin.name = 'AdminUserName'
        if ETC_USER_MODEL_IDENTIFIER.lower() != 'email':
            cls.test_admin.email = 'admin_user@example.com'
        cls.test_admin.save()
        cls.test_admin = cls.get_user(cls, ETC_DEFAULT_ADMIN_USER_IDENTIFIER)

        # Inactive user model. Has "is_active" set to false, and cannot login.
        cls.test_inactive_user = get_user_model().objects.create_user(
            **{ETC_USER_MODEL_IDENTIFIER: ETC_DEFAULT_INACTIVE_USER_IDENTIFIER},
            password=ETC_DEFAULT_USER_PASSWORD,
            is_active=False,
            **extra_usergen_kwargs,
        )
        # Attempt to set fields and then save. If fields exist, then they will populate. Else are ignored.
        if ETC_GENERATE_USERS_WITH_REAL_NAMES:
            cls.test_inactive_user.first_name = 'Clang'
            cls.test_inactive_user.last_name = 'Zythor'
            cls.test_inactive_user.name = 'Clang'
        else:
            cls.test_inactive_user.first_name = 'InactiveUserFirst'
            cls.test_inactive_user.last_name = 'InactiveUserLast'
            cls.test_inactive_user.name = 'InactiveUserName'
        if ETC_USER_MODEL_IDENTIFIER.lower() != 'email':
            cls.test_inactive_user.email = 'inactive_user@example.com'
        cls.test_inactive_user.save()
        cls.test_inactive_user = cls.get_user(cls, ETC_DEFAULT_INACTIVE_USER_IDENTIFIER)

        # Standard user model.
        cls.test_user = get_user_model().objects.create_user(
            **{ETC_USER_MODEL_IDENTIFIER: ETC_DEFAULT_STANDARD_USER_IDENTIFIER},
            password=ETC_DEFAULT_USER_PASSWORD,
            **extra_usergen_kwargs,
        )
        # Attempt to set fields and then save. If fields exist, then they will populate. Else are ignored.
        if ETC_GENERATE_USERS_WITH_REAL_NAMES:
            cls.test_user.first_name = 'Sammy'
            cls.test_user.last_name = 'Smith'
            cls.test_user.name = 'Sammy'
        else:
            cls.test_user.first_name = 'UserFirst'
            cls.test_user.last_name = 'UserLast'
            cls.test_user.name = 'StandardUserName'
        if ETC_USER_MODEL_IDENTIFIER.lower() != 'email':
            cls.test_user.email = 'user@example.com'
        cls.test_user.save()
        cls.test_user = cls.get_user(cls, ETC_DEFAULT_STANDARD_USER_IDENTIFIER)

        # Set actual default "class user" for tests based on settings.
        if ETC_REQUEST_USER_STRICTNESS == 'anonymous':
            # Default user to run tests with an anonymous user.
            cls.user = AnonymousUser()

        elif ETC_REQUEST_USER_STRICTNESS == 'relaxed':
            # Default user to run tests with above "test_user".
            cls.user = cls.test_user

        elif ETC_REQUEST_USER_STRICTNESS == 'strict':
            # No default user to run tests with.
            cls.user = None

        else:
            raise ValueError(
                'Invalid value provided for EXPANDED_TEST_CASES_REQUEST_USER_STRICTNESS setting. '
                'Must be one of: ["anonymous", "relaxed", "strict"].'
            )

    def _debug_print(self, *args, fore='', back='', style='', **kwargs):
        """Prints or suppresses output, based on DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT settings variable.

        Variable defaults to display output, if not provided.
        Mostly used for internal testcase logic.
        """
        if self._debug_print_bool:
            print(fore, end='')
            print(back, end='')
            print(style, end='')
            print(*args, **kwargs, end='')
            print(ETC_OUTPUT_RESET_COLOR)

    # region Custom Assertions

    def assertText(self, expected_text, actual_text, compare_index=None, strip=True):
        """Wrapper for assertEqual(), that prints full values to console on mismatch.

        :param expected_text: Expected text value to check against.
        :param actual_text: Actual text value to compare.
        :param strip: Bool indicating if outer whitespace should be stripped. Defaults to True.
        """
        # Enforce str type.
        expected_text = str(expected_text)
        actual_text = str(actual_text)

        # Handle optional cleaning params.
        if strip:
            expected_text = expected_text.strip()
            actual_text = actual_text.strip()

        # Sanitize compare_index, used for startsWith() and endsWith() versions.
        if compare_index is not None:
            compare_index = int(compare_index)
            if compare_index == 0:
                compare_index = None

        # Attempt assertion.
        try:
            self.assertEqual(expected_text, actual_text)
        except AssertionError as err:
            # Assertion failed. Provide debug output.

            # Loop through to calculate color output differences.
            # First split on newlines.
            split_expected = expected_text.split('\n')
            split_actual = actual_text.split('\n')
            append_newline = False

            # Handle if either is empty.
            if len(split_expected) == 1 and split_expected[0].strip() == '':
                split_expected = []
            if len(split_actual) == 1 and split_actual[0].strip() == '':
                split_actual = []

            # Determine which one is longer.
            if len(split_actual) > len(split_expected):
                max_lines = len(split_actual)
            else:
                max_lines = len(split_expected)

            formatted_expected_output = ''
            formatted_actual_output = ''
            total_actual_count_thus_far = 0
            total_actual_index = None
            actual_text_total_len = len(actual_text)
            if compare_index is not None:
                if compare_index > 0:
                    # Is positive, so starstWith().
                    total_actual_index = 0
                else:
                    # Is negative, so endsWith().
                    total_actual_index = actual_text_total_len

            # Loop through all lines.
            for line_index in range(max_lines):

                # Check if expected/actual each have lines up to this index.
                try:
                    curr_expected_line = split_expected[line_index]
                    if append_newline:
                        curr_expected_line = '\n{0}'.format(curr_expected_line)
                except IndexError:
                    curr_expected_line = None
                try:
                    curr_actual_line = split_actual[line_index]
                    if append_newline:
                        curr_actual_line = '\n{0}'.format(curr_actual_line)
                except IndexError:
                    curr_actual_line = None
                append_newline = False

                # Handle if compare_index value is provided.
                if compare_index is not None and line_index > 0:
                    if compare_index > 0:
                        # Is positive, so startsWith. Count from start of text.
                        total_actual_index = total_actual_count_thus_far
                    else:
                        # Is negative, so endsWith(). Count from end of text.
                        total_actual_index = actual_text_total_len - total_actual_count_thus_far

                if curr_expected_line == curr_actual_line:
                    # Line is full match and correct.
                    curr_expected_line = '{0}{1}{2}\n'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, curr_expected_line, ETC_OUTPUT_RESET_COLOR)
                    curr_actual_line = '{0}{1}{2}\n'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, curr_actual_line, ETC_OUTPUT_RESET_COLOR)
                elif curr_expected_line is None:
                    # "Actual" output is longer than "expected" output. Impossible to match current line.
                    curr_expected_line = ''
                    curr_actual_line = '{0}{1}{2}\n'.format(
                        ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                        curr_actual_line,
                        ETC_OUTPUT_RESET_COLOR,
                    )
                elif curr_actual_line is None:
                    # "Expected" output is longer than "actual" output. Impossible to match current line.
                    curr_expected_line = '{0}{1}{2}\n'.format(
                        ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                        curr_expected_line,
                        ETC_OUTPUT_RESET_COLOR,
                    )
                    curr_actual_line = ''
                else:
                    # Both lines are populated but do not match.
                    # Determine which one is longer.
                    if len(curr_actual_line) > len(curr_expected_line):
                        max_chars = len(curr_actual_line)
                    else:
                        max_chars = len(curr_expected_line)

                    # Check each character and determine where non-match happens.
                    curr_expected_color = ETC_OUTPUT_RESET_COLOR
                    curr_actual_color = ETC_OUTPUT_RESET_COLOR
                    curr_expected_char_line = ''
                    curr_actual_char_line = ''
                    for char_index in range(max_chars):

                        # Handle if starstWith() or endsWith().
                        do_char_compare = True
                        if compare_index is not None:
                            if compare_index > 0:
                                # Is positive, so startsWith()
                                total_actual_index += 1

                                # Skip comparison if actual_index is past compare_index.
                                if total_actual_index > compare_index:
                                    do_char_compare = False
                            else:
                                # Is negative, so endsWith().
                                total_actual_index -= 1

                                # Skip comparison if actual_index is before compare_index.
                                if total_actual_index > - compare_index:
                                    do_char_compare = False

                        # Grab current character.
                        try:
                            expected_char = curr_expected_line[char_index]
                        except IndexError:
                            expected_char = ''
                        try:
                            actual_char = curr_actual_line[char_index]
                        except IndexError:
                            actual_char = ''

                        # Format based on match.
                        if not do_char_compare:
                            # Skip comparison, for either startsWith() or endsWith() assertions.
                            if curr_expected_color != ETC_OUTPUT_RESET_COLOR:
                                curr_expected_color = ETC_OUTPUT_RESET_COLOR
                                curr_expected_char_line += curr_expected_color
                            if curr_actual_color != ETC_OUTPUT_RESET_COLOR:
                                curr_actual_color = ETC_OUTPUT_RESET_COLOR
                                curr_actual_char_line += curr_actual_color

                        elif expected_char == actual_char:
                            # Match.
                            if curr_expected_color != ETC_OUTPUT_EXPECTED_MATCH_COLOR:
                                curr_expected_color = ETC_OUTPUT_EXPECTED_MATCH_COLOR
                                curr_expected_char_line += curr_expected_color
                            if curr_actual_color != ETC_OUTPUT_ACTUALS_MATCH_COLOR:
                                curr_actual_color = ETC_OUTPUT_ACTUALS_MATCH_COLOR
                                curr_actual_char_line += curr_actual_color

                        else:
                            # Non-match.
                            if curr_expected_color != ETC_OUTPUT_EXPECTED_ERROR_COLOR:
                                curr_expected_color = ETC_OUTPUT_EXPECTED_ERROR_COLOR
                                curr_expected_char_line += curr_expected_color
                            if curr_actual_color != ETC_OUTPUT_ACTUALS_ERROR_COLOR:
                                curr_actual_color = ETC_OUTPUT_ACTUALS_ERROR_COLOR
                                curr_actual_char_line += curr_actual_color

                        curr_expected_char_line += '{0}'.format(expected_char)
                        curr_actual_char_line += '{0}'.format(actual_char)

                    # Update output strings.
                    append_newline = True
                    formatted_expected_output += curr_expected_char_line
                    formatted_actual_output += curr_actual_char_line
                    continue

                # Update output strings.
                formatted_expected_output += curr_expected_line
                formatted_actual_output += curr_actual_line

                # Update total actual length.
                total_actual_count_thus_far += len(curr_actual_line)

            # Finally print actual debug output.
            self._debug_print('')
            self._debug_print('')
            self._debug_print('EXPECTED:', fore=ETC_OUTPUT_EXPECTED_MATCH_COLOR)
            self._debug_print(formatted_expected_output)
            self._debug_print('')
            self._debug_print('')
            self._debug_print('ACTUAL:', fore=ETC_OUTPUT_ACTUALS_MATCH_COLOR)
            self._debug_print(formatted_actual_output)
            self._debug_print('')
            self._debug_print('')

            # Raise original error.
            raise err

    def assertTextStartsWith(self, expected_text, actual_text, strip=True):
        """Modiefied wrapper for assertEqual(), that prints full values to console on mismatch.

        Considered a pass if entire string of "expected_text" is at the beginning of "actual_text" variable.
        """
        # Enforce str type.
        expected_text = str(expected_text)
        actual_text = str(actual_text)

        # Handle optional cleaning params.
        if strip:
            expected_text = expected_text.strip()
            actual_text = actual_text.strip()

        # Check if start matches.
        if not str(actual_text).startswith(expected_text):
            # Failed to match. Call original assertText for output handling.
            text_length = len(expected_text)
            return self.assertText(expected_text, actual_text, text_length, strip=strip)

        # Passed.
        return True

    def assertTextEndsWith(self, expected_text, actual_text, strip=True):
        """Modified wrapper for assertEqual(), that prints full values to console on mismatch.

        Considered a pass if entire string of "expected_text" is at the beginning of "actual_text" variable.
        """
        # Enforce str type.
        expected_text = str(expected_text)
        actual_text = str(actual_text)

        # Handle optional cleaning params.
        if strip:
            expected_text = expected_text.strip()
            actual_text = actual_text.strip()

        # Check if ending matches.
        if not str(actual_text).endswith(expected_text):
            # Failed to match. Call original assertText for output handling.
            text_length = len(expected_text)
            return self.assertText(expected_text, actual_text, compare_index=-text_length, strip=strip)

        # Passed.
        return True

    # endregion Custom Assertions

    # region User Management Functions

    def get_user(self, user, password=ETC_DEFAULT_USER_PASSWORD, extra_usergen_kwargs=None):
        """Returns user matching provided value.

        :param user: User model, or corresponding user identifier, to use.
        :param password: Password str to assign to user.
        :param extra_usergen_kwargs: Optional extra kwargs to pass into the get_user_model().objects.create_user()
                                     function.
        :return: User object
        """

        # Check if instance is User model.
        if isinstance(user, get_user_model()):
            # Already User model. This is fine.
            pass

        # Handle all "special cases" for testing logic.
        elif ETC_AUTO_GENERATE_USERS is True and user == ETC_DEFAULT_SUPER_USER_IDENTIFIER:
            user = self.test_superuser
        elif ETC_AUTO_GENERATE_USERS is True and user == ETC_DEFAULT_ADMIN_USER_IDENTIFIER:
            user = self.test_admin
        elif ETC_AUTO_GENERATE_USERS is True and user == ETC_DEFAULT_INACTIVE_USER_IDENTIFIER:
            user = self.test_inactive_user
        elif ETC_AUTO_GENERATE_USERS is True and user == ETC_DEFAULT_STANDARD_USER_IDENTIFIER:
            user = self.test_user
        else:
            # Is not User model. Get or create.

            # First validate optional extra kwargs.
            if extra_usergen_kwargs is None:
                extra_usergen_kwargs = {}
            elif not isinstance(extra_usergen_kwargs, dict):
                raise ValueError(
                    'The extra_usergen_kwargs value must be a dictionary of additional args used in the '
                    'get_user_model().objects.create_user() function.'
                )

            try:
                user = get_user_model().objects.get(
                    **{ETC_USER_MODEL_IDENTIFIER: str(user)},
                    **extra_usergen_kwargs,
                )
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create(
                    **{ETC_USER_MODEL_IDENTIFIER: str(user)},
                    **extra_usergen_kwargs,
                )

        # Handle passwords.
        if not hasattr(user, 'unhashed_password') or user.unhashed_password != password:
            password = str(password).strip()
            if len(password) == 0:
                # Empty password. Reset back to default settings value.
                password = ETC_DEFAULT_USER_PASSWORD
            user.set_password(password)
            user.unhashed_password = password
            user.save()

        return user

    def add_user_permission(self, user_permission, user=None):
        """Adds Permission to given user.

        :param user_permission: Permission to add.
        :param user: User to add Permission to. If not provided, defaults to test_user model.
        :return: Updated user object.
        """
        # Django imports here to avoid situational "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser, Permission

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
                except Permission.DoesNotExist as pde:
                    raise ValueError('Failed to find permission of "{0}".'.format(user_permission)) from pde

        # If we made it this far, then valid Permission was found. Apply to user.
        # But first determine what user we're applying to.
        if user is not None:
            # Actual user arg provided to function. Use that.
            user = self.get_user(user)
        elif self.user and not isinstance(self.user, AnonymousUser):
            # No arg provided to function. Fall back to class user, if provided.
            user = self.get_user(self.user)
        else:
            # No arg provided to function AND no class user defined.
            # Resort to "default standard user" as final fallback.
            user = self.get_user(ETC_DEFAULT_STANDARD_USER_IDENTIFIER)

        # Actually add permission.
        user.user_permissions.add(permission)

        # Return user object in case user wants to run additional checks.
        return user

    def add_user_group(self, user_group, user=None):
        """Adds Group to given user.

        :param user_group: Group to add.
        :param user: User to add Group to. If not provided, defaults to test_user model.
        :return: Updated user object.
        """
        # Django imports here to avoid situational "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser, Group

        # Check if instance is a Group model.
        if isinstance(user_group, Group):
            # Already Group model. This is fine.
            group = user_group

        else:
            # Is not Group model. Attempt to get.
            user_group = str(user_group)
            try:
                group = Group.objects.get(name=user_group)
            except Group.DoesNotExist as gde:
                raise ValueError('Failed to find Group of "{0}".'.format(user_group)) from gde

        # If we made it this far, then valid Group was found. Apply to user.
        # But first determine what user we're applying to.
        if user is not None:
            # Actual user arg provided to function. Use that.
            user = self.get_user(user)
        elif self.user and not isinstance(self.user, AnonymousUser):
            # No arg provided to function. Fall back to class user, if provided.
            user = self.get_user(self.user)
        else:
            # No arg provided to function AND no class user defined.
            # Resort to "default standard user" as final fallback.
            user = self.get_user(ETC_DEFAULT_STANDARD_USER_IDENTIFIER)

        # Actually add groups.
        user.groups.add(group)

        # Return user object in case user wants to run additional checks.
        return user

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

        # If kwargs were provided, trim final slash if url ends with such.
        while url.endswith('/'):
            url = url[:-1]

        # Trim final ? if url ends with such.
        while url.endswith('?'):
            url = url[:-1]

        # If kwargs were provided, trim final slash if url ends with such.
        # Makes sure handling is consistent, even if ordering of ? and / are weird.
        while url.endswith('/'):
            url = url[:-1]

        # Finally, generate actual url and return.
        get_params = urlencode(kwargs)
        get_url = '{0}/{1}'.format(
            url,
            ('' if get_params == '' else '?' + get_params)
        )

        self._debug_print('URL: {0}'.format(get_url))
        return get_url

    def standardize_characters(self, value):
        """Standardizes various characters in provided str.

        Helps make testing easier.
        As generally tests only care that the character exists, not so much how it's written.

        Ex: Brackets have multiple ways to be written, and this will "standardize" them to a literal bracket.
        Ex: Django form errors seem to auto-escape apostrophe (') characters to the html code. Which isn't intuitive.
        Ex: Django seems to like converting values the hex version, so we convert them back during testing.

        Note: If passing the return into regex, further sanitation is required. $ and ^ characters will break regex.

        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = self.standardize_symbols(value)
        value = self.standardize_numbers(value)
        value = self.standardize_letters(value)

        return value

    def standardize_symbols(self, value):
        """Standardizes various symbol-based characters in provided str.

        Helps make testing easier.
        As generally tests only care that the character exists, not so much how it's written.
        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Regex Format: ( decimal_equivalent | hex_equivalent | english_equivalent )
        value = re.sub(r'(&#32;|&#x20;)', ' ', value)  # Standard space character.
        value = re.sub(r'(&#160;|&#x[Aa]0;|&nbsp;)', ' ', value)  # Non-breaking space character.

        value = re.sub(r'(&#33;|&#x21;|&excl;)', '!', value)  # Exclamation mark character.
        value = re.sub(r'(&#34;|&#x22;|&quot;)', '"', value)  # Quotation character.
        value = re.sub(r'(&#35;|&#x23;|&num;)', '#', value)  # Number sign character.
        value = re.sub(r'(&#36;|&#x24;|&dollar;)', '$', value)  # Dollar sign character.
        value = re.sub(r'(&#37;|&#x25;|&percnt;)', '%', value)  # Percent sign character.
        value = re.sub(r'(&#38;|&#x26;|&amp;)', '&', value)  # Ampersand character.
        value = re.sub(r'(&#39;|&#x27;|&apos;)', "'", value)  # Apostrophe character.
        value = re.sub(r'(&#40;|&#x28;|&lpar;)', '(', value)  # Opening parenthesis character.
        value = re.sub(r'(&#41;|&#x29;|&rpar;)', ')', value)  # Closing parenthesis character.
        value = re.sub(r'(&#42;|&#x2[Aa];|&ast;)', '*', value)  # Asterisk character.
        value = re.sub(r'(&#43;|&#x2[Bb];|&plus;)', '+', value)  # Plus character.
        value = re.sub(r'(&#44;|&#x2[Cc];|&comma;)', ',', value)  # Comma character.
        value = re.sub(r'(&#45;|&#8722;|&#x2[Dd];|&minus;)', '-', value)  # Minus character.
        value = re.sub(r'(&#46;|&#x2[Ee];|&period;)', '.', value)  # Period character.
        value = re.sub(r'(&#47;|&#x2[Ff];|&sol;)', '/', value)  # Slash character.

        value = re.sub(r'(&#58;|&#x3[Aa];|&colon;)', ':', value)  # Colon character.
        value = re.sub(r'(&#59;|&#x3[Bb];|&semi;)', ';', value)  # Semicolon character.
        value = re.sub(r'(&#60;|&#x3[Cc];|&lt;)', '<', value)  # Less than character.
        value = re.sub(r'(&#61;|&#x3[Dd];|&equals;)', '=', value)  # Equals character.
        value = re.sub(r'(&#62;|&#x3[Ee];|&gt;)', '>', value)  # Greater than character.
        value = re.sub(r'(&#63;|&#x3[Ff];|&quest;)', '?', value)  # Question mark character.
        value = re.sub(r'(&#64;|&#x40;|&commat;)', '@', value)  # At sign character.

        value = re.sub(r'(&#91;|&#x5[Bb];|&lbrack;)', '[', value)  # Opening square bracket character.
        value = re.sub(r'(&#92;|&#x5[Cc];|&bsol;)', '\\\\', value)  # Backslash character.
        value = re.sub(r'(&#93;|&#x5[Dd];|&rbrack;)', ']', value)  # Closing square bracket character.
        value = re.sub(r'(&#94;|&#x5[Ee];|&Hat;)', '^', value)  # UpArrow/Hat character.
        value = re.sub(r'(&#95;|&#x5[Ff];|&lowbar;)', '_', value)  # Underscore character.
        value = re.sub(r'(&#96;|&#x60;|&grave;)', '`', value)  # Grave accent character.

        value = re.sub(r'(&#123;|&#x7[Bb];|&lbrace;)', '{', value)  # Opening dict bracket character.
        value = re.sub(r'(&#124;|&#x7[Cc];|&vert;)', '|', value)  # Pipe character.
        value = re.sub(r'(&#125;|&#x7[Dd];|&rbrace;)', '}', value)  # Closing dict bracket character.
        value = re.sub(r'(&#126;|&#x7[Ee];|&tilde;)', '~', value)  # Tilde character.

        return value

    def standardize_numbers(self, value):
        """Standardizes various number-based characters in provided str.

        Helps make testing easier.
        As generally tests only care that the character exists, not so much how it's written.
        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Regex Format: ( decimal_equivalent | hex_equivalent | english_equivalent )
        value = re.sub(r'(&#48;|&#x30;)', '0', value)  # Number 0 character.
        value = re.sub(r'(&#49;|&#x31;)', '1', value)  # Number 1 character.
        value = re.sub(r'(&#50;|&#x32;)', '2', value)  # Number 2 character.
        value = re.sub(r'(&#51;|&#x33;)', '3', value)  # Number 3 character.
        value = re.sub(r'(&#52;|&#x34;)', '4', value)  # Number 4 character.
        value = re.sub(r'(&#53;|&#x35;)', '5', value)  # Number 5 character.
        value = re.sub(r'(&#54;|&#x36;)', '6', value)  # Number 6 character.
        value = re.sub(r'(&#55;|&#x37;)', '7', value)  # Number 7 character.
        value = re.sub(r'(&#56;|&#x38;)', '8', value)  # Number 8 character.
        value = re.sub(r'(&#57;|&#x39;)', '9', value)  # Number 9 character.

        return value

    def standardize_letters(self, value):
        """Standardizes various letter-based characters in provided str.

        Helps make testing easier.
        As generally tests only care that the character exists, not so much how it's written.
        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Regex Format: ( decimal_equivalent | hex_equivalent)
        value = re.sub(r'(&#65;|&#x41;)', 'A', value)  # Upper a character.
        value = re.sub(r'(&#66;|&#x42;)', 'B', value)  # Upper b character.
        value = re.sub(r'(&#67;|&#x43;)', 'C', value)  # Upper c character.
        value = re.sub(r'(&#68;|&#x44;)', 'D', value)  # Upper d character.
        value = re.sub(r'(&#69;|&#x45;)', 'E', value)  # Upper e character.
        value = re.sub(r'(&#70;|&#x46;)', 'F', value)  # Upper f character.
        value = re.sub(r'(&#71;|&#x47;)', 'G', value)  # Upper g character.
        value = re.sub(r'(&#72;|&#x48;)', 'H', value)  # Upper h character.
        value = re.sub(r'(&#73;|&#x49;)', 'I', value)  # Upper i character.
        value = re.sub(r'(&#74;|&#x4[Aa];)', 'J', value)  # Upper j character.
        value = re.sub(r'(&#75;|&#x4[Bb];)', 'K', value)  # Upper k character.
        value = re.sub(r'(&#76;|&#x4[Cc];)', 'L', value)  # Upper l character.
        value = re.sub(r'(&#77;|&#x4[Dd];)', 'M', value)  # Upper m character.
        value = re.sub(r'(&#78;|&#x4[Ee];)', 'N', value)  # Upper n character.
        value = re.sub(r'(&#79;|&#x4[Ff];)', 'O', value)  # Upper o character.
        value = re.sub(r'(&#80;|&#x50;)', 'P', value)  # Upper p character.
        value = re.sub(r'(&#81;|&#x51;)', 'Q', value)  # Upper q character.
        value = re.sub(r'(&#82;|&#x52;)', 'R', value)  # Upper r character.
        value = re.sub(r'(&#83;|&#x53;)', 'S', value)  # Upper s character.
        value = re.sub(r'(&#84;|&#x54;)', 'T', value)  # Upper t character.
        value = re.sub(r'(&#85;|&#x55;)', 'U', value)  # Upper u character.
        value = re.sub(r'(&#86;|&#x56;)', 'V', value)  # Upper v character.
        value = re.sub(r'(&#87;|&#x57;)', 'W', value)  # Upper w character.
        value = re.sub(r'(&#88;|&#x58;)', 'X', value)  # Upper x character.
        value = re.sub(r'(&#89;|&#x59;)', 'Y', value)  # Upper y character.
        value = re.sub(r'(&#90;|&#x5[Aa];)', 'Z', value)  # Upper z character.

        value = re.sub(r'(&#97;|&#x61;)', 'a', value)  # Lower a character.
        value = re.sub(r'(&#98;|&#x62;)', 'b', value)  # Lower b character.
        value = re.sub(r'(&#99;|&#x63;)', 'c', value)  # Lower c character.
        value = re.sub(r'(&#100;|&#x64;)', 'd', value)  # Lower d character.
        value = re.sub(r'(&#101;|&#x65;)', 'e', value)  # Lower e character.
        value = re.sub(r'(&#102;|&#x66;)', 'f', value)  # Lower f character.
        value = re.sub(r'(&#103;|&#x67;)', 'g', value)  # Lower g character.
        value = re.sub(r'(&#104;|&#x68;)', 'h', value)  # Lower h character.
        value = re.sub(r'(&#105;|&#x69;)', 'i', value)  # Lower i character.
        value = re.sub(r'(&#106;|&#x6[Aa];)', 'j', value)  # Lower j character.
        value = re.sub(r'(&#107;|&#x6[Bb];)', 'k', value)  # Lower k character.
        value = re.sub(r'(&#108;|&#x6[Cc];)', 'l', value)  # Lower l character.
        value = re.sub(r'(&#109;|&#x6[Dd];)', 'm', value)  # Lower m character.
        value = re.sub(r'(&#110;|&#x6[Ee];)', 'n', value)  # Lower n character.
        value = re.sub(r'(&#111;|&#x6[Ff];)', 'o', value)  # Lower o character.
        value = re.sub(r'(&#112;|&#x70;)', 'p', value)  # Lower p character.
        value = re.sub(r'(&#113;|&#x71;)', 'q', value)  # Lower q character.
        value = re.sub(r'(&#114;|&#x72;)', 'r', value)  # Lower r character.
        value = re.sub(r'(&#115;|&#x73;)', 's', value)  # Lower s character.
        value = re.sub(r'(&#116;|&#x74;)', 't', value)  # Lower t character.
        value = re.sub(r'(&#117;|&#x75;)', 'u', value)  # Lower u character.
        value = re.sub(r'(&#118;|&#x76;)', 'v', value)  # Lower v character.
        value = re.sub(r'(&#119;|&#x77;)', 'w', value)  # Lower w character.
        value = re.sub(r'(&#120;|&#x78;)', 'x', value)  # Lower x character.
        value = re.sub(r'(&#121;|&#x79;)', 'y', value)  # Lower y character.
        value = re.sub(r'(&#122;|&#x7[Aa];)', 'z', value)  # Lower z character.

        return value

    def standardize_newlines(self, value):
        """Standardizes newline instances in provided variable.

        Will reduce possible newline character types to the \n character.
        Also, whitespace between newlines is removed, and outer newlines/whitespace is removed.

        Note: Handles similar to standardize_whitespace(), except that newlines are preserved.

        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Replace html linebreak with actual newline character.
        value = re.sub('<br>|</br>|<br/>|<br />', '\n', value)

        # Replace non-breaking space with actual space character.
        value = re.sub('(&nbsp;)+', ' ', value)

        # Replace any carriage return characters with newline character.
        value = re.sub(r'\r+', '\n', value)

        # Replace any whitespace trapped between newline characters.
        # This is empty/dead space, likely generated by how Django handles templating.
        value = re.sub(r'\n\s+\n', '\n', value)

        # Replace any repeating linebreaks.
        value = re.sub(r'\n\n+', '\n', value)

        # Reduce any repeating whitespace instances.
        value = re.sub(r' ( )+', ' ', value)

        # Strip final calculated string of extra outer whitespace.
        value = str(value).strip()

        return value

    def standardize_whitespace(self, value):
        """Standardizes whitespace in provided variable.

        When possible, all whitespace and whitespace-esque characters (including newlines)
        are reduced down to a single space.

        Note: Handles similar to standardize_newlines(), except that all newlines are removed.

        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Replace html linebreak with space character.
        value = re.sub('<br>|</br>|<br/>|<br />', ' ', value)

        # Replace non-breaking space with actual space character.
        value = re.sub('(&nbsp;)+', ' ', value)

        # Remove any newline characters.
        value = re.sub(r'(\r)+|(\n)+', ' ', value)

        # Reduce any repeating whitespace instances.
        value = re.sub(r' ( )+', ' ', value)

        # Strip final calculated string of extra outer whitespace.
        value = str(value).strip()

        return value

    # endregion Helper Functions

    # endregion Class Functions

    # region Properties

    @property
    def site_root_url(self):
        """"""
        if (
            self._site_root_url is None
            or self._site_root_url == ''
        ):
            # No site root populated. Check for "live_server_url", which is auto-populated for Selenium tests.
            if (
                hasattr(self, 'live_server_url')
                and self.live_server_url is not None
                and self.live_server_url != ''
            ):
                return self.live_server_url

            # Failed to get auto-populated Selenium url.
            # Return default (will apply in most cases).
            return '127.0.0.1'
        else:
            # Site root is populated. Return value.
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


# Define acceptable imports on file.
__all__ = [
    'CoreTestCaseMixin',
]
