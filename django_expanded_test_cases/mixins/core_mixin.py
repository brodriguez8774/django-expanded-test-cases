"""
Core testing logic, universal to all test cases.
"""

# System Imports.
import re
from colorama import Fore, Style
from functools import wraps
from types import FunctionType

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.http import urlencode

# User Imports.
from django_expanded_test_cases.constants import DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT

# region Debug Print Wrapper Logic

def wrapper(method):
    """Wrapper logic to intercept all functions on AssertionError and print error at bottom of output."""
    @wraps(method)
    def wrapped(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except AssertionError as err:
            if DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT:
                print('\n')
                print('{0}{1}{2}'.format(Fore.RED, err, Style.RESET_ALL))
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


class CoreTestCaseMixin:
    """Core testing logic, used in all other expanded TestCase classes.

    For compatibility, does not inherit from
        django.test.TestCase
        channels.testing.ChannelsLiveServerTestCase

    Inheriting from either (seems to) make it incompatible with the other.
    Therefore we treat this as a separate mixin that inherits from nothing, and is included in all.
    """

    # region Class Functions

    @classmethod
    def set_up_class(cls, debug_print=None):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase, calling the literal function
        here would override instead.

        :param debug_print: Optional bool that indicates if debug output should print to console.
                            Param overrides setting value if both param and setting are set.
        """
        # Generate "special case" test user instances.
        # Guarantees that there will always be at least some default User models when tests are run.
        cls.test_superuser = get_user_model().objects.create_user(
            username='test_superuser',
            password='password',
            is_superuser=True,
        )
        cls.test_admin = get_user_model().objects.create_user(
            username='test_admin',
            password='password',
            is_staff=True,
        )
        cls.test_user = get_user_model().objects.create_user(username='test_user', password='password')
        cls.test_inactive_user = get_user_model().objects.create_user(
            username='test_inactive',
            password='password',
            is_active=False,
        )

        # Check user debug_print option.
        if debug_print is not None:
            cls._debug_print_bool = bool(debug_print)
        else:
            cls._debug_print_bool = DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT

    def _debug_print(self, *args, fore='', back='', style='', **kwargs):
        """Prints or suppresses output, based on DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT settings variable.

        Variable defaults to display output, if not provided.
        Mostly used for internal testcase logic.
        """
        if self._debug_print_bool:
            print(fore, end="")
            print(back, end="")
            print(style, end="")
            print(*args, **kwargs, end="")
            print(Style.RESET_ALL)

    # region Custom Assertions

    def assertText(self, actual_text, expected_text, strip=True):
        """Wrapper for assertEqual(), that prints full values to console on mismatch.

        NOTE: Outer whitespace is stripped if either strip or standardize params are set to True.

        :param actual_text: Actual text value to compare.
        :param expected_text: Expected text value to check against.
        :param strip: Bool indicating if outer whitespace should be stripped. Defaults to True.
        """
        # Enforce str type.
        actual_text = str(actual_text)
        expected_text = str(expected_text)

        # Handle optional cleaning params.
        if strip:
            actual_text = actual_text.strip()
            expected_text = expected_text.strip()

        # Attempt assertion.
        try:
            self.assertEqual(actual_text, expected_text)
        except AssertionError as err:
            # Assertion failed. Provide debug output.
            self._debug_print('')
            self._debug_print('')
            self._debug_print('')
            self._debug_print('')
            self._debug_print('')
            self._debug_print('ACTUAL:', fore=Fore.RED)
            self._debug_print(actual_text, fore=Fore.RED)
            self._debug_print('')
            self._debug_print('')
            self._debug_print('EXPECTED:', fore=Fore.GREEN)
            self._debug_print(expected_text, fore=Fore.GREEN)
            self._debug_print('')
            self._debug_print('')
            self._debug_print('')
            self._debug_print('')
            self._debug_print('')

            # Raise original error.
            raise AssertionError(err) from err

    # endregion Custom Assertions

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
        elif user == 'test_inactive':
            user = self.test_inactive_user

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
        :return: Updated user object.
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
                except Permission.DoesNotExist as pde:
                    raise ValueError('Failed to find permission of "{0}".'.format(user_permission)) from pde

        # If we made it this far, then valid Permission was found. Apply to user.
        user = self.get_user(user)
        user.user_permissions.add(permission)

        # Return user object in case user wants to run additional checks.
        return user

    def add_user_group(self, user_group, user='test_user'):
        """Adds Group to given user.

        :param user_group: Group to add.
        :param user: User to add Group to. If not provided, defaults to test_user model.
        :return: Updated user object.
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
            except Group.DoesNotExist as gde:
                raise ValueError('Failed to find Group of "{0}".'.format(user_group)) from gde

        # If we made it this far, then valid Group was found. Apply to user.
        user = self.get_user(user)
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

        # Finally, generate actual url and return.
        get_params = urlencode(kwargs)
        get_url = url + ('' if get_params == '' else '?' + get_params)
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
