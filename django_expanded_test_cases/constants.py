"""Constants for ExpandedTestCases package."""

# Third-Party Imports.
from django.conf import settings


# Imports that may not be accessible, depending on local python environment setup.
try:
    from colorama import Back, Fore, Style
    COLORAMA_PRESENT = True
except ImportError:
    COLORAMA_PRESENT = False


# Underline style definition for debug printing.
UNDERLINE = '\u001b[4m'
UNDERLINE_RESET = '\u001b[0m'


# General output format settings.
OUTPUT_ERROR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_ERROR_HEADER',
    '{0}{1}{2}'.format(Fore.RED, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
))
OUTPUT_EXPECTED_MATCH = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_MATCH',
    '{0}{1}{2}'.format(Fore.CYAN, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
))
OUTPUT_EXPECTED_ERROR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_ERROR',
    '{0}{1}{2}'.format(Fore.BLACK, Back.CYAN, Style.NORMAL) if COLORAMA_PRESENT else '',
))
OUTPUT_ACTUALS_MATCH = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_MATCH',
    '{0}{1}{2}'.format(Fore.MAGENTA, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
))
OUTPUT_ACTUALS_ERROR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_ERROR',
    '{0}{1}{2}'.format(Fore.BLACK, Back.MAGENTA, Style.NORMAL) if COLORAMA_PRESENT else '',
))
OUTPUT_EMPHASIS = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_EMPHASIS',
    (Style.BRIGHT if COLORAMA_PRESENT else '') + UNDERLINE,
))
OUTPUT_RESET = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_RESET',
    Style.RESET_ALL if COLORAMA_PRESENT else UNDERLINE_RESET,
))

# Output formatting for response sections.
RESPONSE_DEBUG_URL = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_URL',
    Fore.YELLOW if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_CONTENT = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTENT',
    Fore.WHITE if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_HEADERS = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_HEADERS',
    Fore.CYAN if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_CONTEXT = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTEXT',
    Fore.BLUE if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_SESSION = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_SESSION',
    Fore.MAGENTA if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_MESSAGES = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_MESSAGES',
    Fore.CYAN if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_FORMS = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_FORMS',
    Fore.BLUE if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_USER_INFO = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_USER_INFO',
    Fore.MAGENTA if COLORAMA_PRESENT else '',
))


# Void element list as defined at:
# https://www.w3.org/TR/2011/WD-html-markup-20110113/syntax.html#void-element
# TLDR: A "void element" is an HTML element that does not require a closing tag.
# Used in the "repeating element" logic.
VOID_ELEMENT_LIST = [
    'area',
    'base',
    'br',
    'col',
    'command',
    'embed',
    'hr',
    'img',
    'input',
    'keygen',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr',
]


# Indicates whether the additional debug information should be output.
ETC_DEBUG_PRINT = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT',
    True,
))
# Indicates whether partial matches are allowed for messages.
ETC_ALLOW_MESSAGE_PARTIALS = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS',
    True,
))
# Indicates whether tests fail when there are messages in the response that were not explicitly tested for.
ETC_MATCH_ALL_CONTEXT_MESSAGES = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES',
    False,
))


# Controls if test-users should be automatically generated or not.
ETC_AUTO_GENERATE_USERS = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_AUTO_GENERATE_USERS',
    True,
))
# Controls what level of strictness UnitTest requests have for users.
ETC_REQUEST_USER_STRICTNESS = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_REQUEST_USER_STRICTNESS',
    'anonymous',
)).strip().lower()
# Allows incorporating package with non-standard user identifiers.
# Such as the common case of using a user email as an identifier, instead of a username.
ETC_USER_MODEL_IDENTIFIER = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER',
    'username',
))
# The identifier used for the auto-generated "superuser" user.
ETC_DEFAULT_SUPER_USER_IDENTIFIER = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEFAULT_SUPER_USER_IDENTIFIER',
    None,
)
# The identifier used for the auto-generated "admin" user.
ETC_DEFAULT_ADMIN_USER_IDENTIFIER = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEFAULT_ADMIN_USER_IDENTIFIER',
    None,
)
# The identifier used for the auto-generated "standard" user.
ETC_DEFAULT_STANDARD_USER_IDENTIFIER = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEFAULT_STANDARD_USER_IDENTIFIER',
    None,
)
# The identifier used for the auto-generated "inactive" user.
ETC_DEFAULT_INACTIVE_USER_IDENTIFIER = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEFAULT_INACTIVE_USER_IDENTIFIER',
    None,
)
# The default password used for auto-generated users.
ETC_DEFAULT_USER_PASSWORD = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD',
    'password',
))
# Indicates if auto-generated users should get pretend "real" first/last name values.
ETC_GENERATE_USERS_WITH_REAL_NAMES = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_GENERATE_USERS_WITH_REAL_NAMES',
    False,
))


# region User Identifiers

# Validate ETC_REQUEST_USER_STRICTNESS setting.
if ETC_REQUEST_USER_STRICTNESS not in ['anonymous', 'relaxed', 'strict']:
    raise ValueError(
        'Invalid value provided for EXPANDED_TEST_CASES_REQUEST_USER_STRICTNESS setting. '
        'Must be one of: ["anonymous", "relaxed", "strict"].'
    )
# Validate combination of ETC_REQUEST_USER_STRICTNESS and ETC_AUTO_GENERATE_USERS settings.
elif ETC_REQUEST_USER_STRICTNESS == 'relaxed' and not ETC_AUTO_GENERATE_USERS:
    raise ValueError('When ETC_REQUEST_USER_STRICTNESS is set to "relaxed", ETC_AUTO_GENERATE_USERS must be True.')

# Set default identifier value, based on either provided value or common user identifier types.
default_superuser_identifier = None
default_admin_identifier = None
default_inactive_identifier = None
default_user_identifier = None

if ETC_USER_MODEL_IDENTIFIER == 'username':
    # Set default identifiers in username format.
    if ETC_DEFAULT_SUPER_USER_IDENTIFIER is None:
        default_superuser_identifier = 'test_superuser'
    if ETC_DEFAULT_ADMIN_USER_IDENTIFIER is None:
        default_admin_identifier = 'test_admin'
    if ETC_DEFAULT_INACTIVE_USER_IDENTIFIER is None:
        default_inactive_identifier = 'test_inactive'
    if ETC_DEFAULT_STANDARD_USER_IDENTIFIER is None:
        default_user_identifier = 'test_user'

elif ETC_USER_MODEL_IDENTIFIER == 'email':
    # Set default identifiers in email format.
    if ETC_DEFAULT_SUPER_USER_IDENTIFIER is None:
        default_superuser_identifier = 'test_superuser@example.com'
    if ETC_DEFAULT_ADMIN_USER_IDENTIFIER is None:
        default_admin_identifier = 'test_admin@example.com'
    if ETC_DEFAULT_INACTIVE_USER_IDENTIFIER is None:
        default_inactive_identifier = 'test_inactive@example.com'
    if ETC_DEFAULT_STANDARD_USER_IDENTIFIER is None:
        default_user_identifier = 'test_user@example.com'

# Handle any identifiers that have not yet been set by this point.
if default_superuser_identifier is None:
    default_superuser_identifier = str(ETC_DEFAULT_SUPER_USER_IDENTIFIER)
if default_admin_identifier is None:
    default_admin_identifier = str(ETC_DEFAULT_ADMIN_USER_IDENTIFIER)
if default_inactive_identifier is None:
    default_inactive_identifier = str(ETC_DEFAULT_INACTIVE_USER_IDENTIFIER)
if default_user_identifier is None:
    default_user_identifier = str(ETC_DEFAULT_STANDARD_USER_IDENTIFIER)

ETC_DEFAULT_SUPER_USER_IDENTIFIER = default_superuser_identifier
ETC_DEFAULT_ADMIN_USER_IDENTIFIER = default_admin_identifier
ETC_DEFAULT_INACTIVE_USER_IDENTIFIER = default_inactive_identifier
ETC_DEFAULT_STANDARD_USER_IDENTIFIER = default_user_identifier

# endregion User Identifiers
