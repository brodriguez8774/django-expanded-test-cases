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


# region Console Color Options

# General output/color format settings.
ETC_OUTPUT_ERROR_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_ERROR_HEADER_COLOR',
    '{0}{1}{2}'.format(Fore.RED, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
))
ETC_OUTPUT_EXPECTED_MATCH_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_MATCH_COLOR',
    '{0}{1}{2}'.format(Fore.CYAN, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
))
ETC_OUTPUT_EXPECTED_ERROR_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_ERROR_COLOR',
    '{0}{1}{2}'.format(Fore.BLACK, Back.CYAN, Style.NORMAL) if COLORAMA_PRESENT else '',
))
ETC_OUTPUT_ACTUALS_MATCH_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_MATCH_COLOR',
    '{0}{1}{2}'.format(Fore.MAGENTA, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
))
ETC_OUTPUT_ACTUALS_ERROR_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_ERROR_COLOR',
    '{0}{1}{2}'.format(Fore.BLACK, Back.MAGENTA, Style.NORMAL) if COLORAMA_PRESENT else '',
))
ETC_OUTPUT_EMPHASIS_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_EMPHASIS_COLOR',
    (Style.BRIGHT if COLORAMA_PRESENT else '') + UNDERLINE,
))
ETC_OUTPUT_RESET_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_OUTPUT_RESET_COLOR',
    Style.RESET_ALL if COLORAMA_PRESENT else UNDERLINE_RESET,
))

# Output/color formatting for response sections.
ETC_RESPONSE_DEBUG_URL_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_URL_COLOR',
    Fore.YELLOW if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_CONTENT_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTENT_COLOR',
    Fore.WHITE if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_HEADER_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_HEADER_COLOR',
    Fore.CYAN if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_CONTEXT_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTEXT_COLOR',
    Fore.BLUE if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_SESSION_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_SESSION_COLOR',
    Fore.MAGENTA if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_MESSAGE_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_MESSAGES_COLOR',
    Fore.CYAN if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_FORM_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_FORMS_COLOR',
    Fore.BLUE if COLORAMA_PRESENT else '',
))
ETC_RESPONSE_DEBUG_USER_INFO_COLOR = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_USER_INFO_COLOR',
    Fore.MAGENTA if COLORAMA_PRESENT else '',
))

# endregion Console Color Options


# region Console Region Show/Hide Options

# Enabling/disabling output of specific sections.
ETC_INCLUDE_RESPONSE_DEBUG_URL = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_URL',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_CONTENT = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTENT',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_HEADER = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_HEADER',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_CONTEXT = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTEXT',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_SESSION = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_SESSION',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_MESSAGES = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_MESSAGES',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_FORMS = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_FORMS',
    True,
))
ETC_INCLUDE_RESPONSE_DEBUG_USER_INFO = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_USER_INFO',
    True,
))

# endregion Console Region Show/Hide Options


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


# region General Options

# Indicates whether the additional debug information should be output.
ETC_DEBUG_PRINT = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT',
    True,
))
# Indicates whether partial matches are allowed for site title assertions.
# IE: Will pass as long as provided text appears as a subsection of the full site title.
# Defaults to needing exact match.
ETC_ALLOW_TITLE_PARTIALS = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_ALLOW_TITLE_PARTIALS',
    False,
))
# Indicates whether partial matches are allowed for message assertions.
# IE: Will pass as long as provided text appears as a subsection of one or more messages.
# Defaults to needing exact match.
ETC_ALLOW_MESSAGE_PARTIALS = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS',
    False,
))
# Indicates whether tests fail when there are messages in the response that were not explicitly tested for.
# Aka, when doing ANY message assertion, if this is True, then ALL messages in response need to be checked.
ETC_MATCH_ALL_CONTEXT_MESSAGES = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES',
    False,
))

# endregion General Options


# region Selenium Options

# Browser to launch for selenium testing. Options of 'chrome'/'firefox' are good defaults.
ETC_SELENIUM_BROWSER = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_BROWSER',
    'chrome',
))
# Run Selenium tests in "headless" mode.
# Default is to visually show browser. "Headless" will skipp visually rendering the browser while still running tests.
# Good for speed but bad for debugging issues.
ETC_SELENIUM_HEADLESS = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_HEADLESS',
    False,
))
# Set browser/selenium cache to be ignored.
# Using the cache can sometimes lead to incorrect/failing tests when running selenium in a multi-threaded environment.
ETC_SELENIUM_DISABLE_CACHE = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_DISABLE_CACHE',
    False,
))
# Starting debug port, to get around remote-debugging-port option using the same value for all generated drivers,
# Using the same port seems to cause issues with allowing proper switching between drivers.
# Each generated driver increments this value by one, to guarantee all tests among all files should have unique ports.
ETC_SELENIUM_DEBUG_PORT_START_VALUE = int(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_DEBUG_PORT_START_VALUE',
    9221,
))
# A list of lists, comprised of desired (x, y) window positions to spawn selenium browsers at.
# If not provided, then defaults to however the OS spawns windows in.
# Ex: [(0, 0), (960, 0)] for a standard 1920 x 1080 landscape display.
ETC_SELENIUM_WINDOW_POSITIONS = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_WINDOW_POSITIONS',
    None,
)
# Extra options to pass into browser. Should be some iterable, such as a list or tuple of strings.
ETC_SELENIUM_EXTRA_BROWSER_OPTIONS = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_EXTRA_BROWSER_OPTIONS',
    None,
)
# Number of seconds to wait on selenium page load before giving up.
# Refers to the full page itself loading. As in getting any page response at all. Default of 30 seconds.
ETC_SELENIUM_PAGE_TIMEOUT_DEFAULT = int(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_PAGE_TIMEOUT_DEFAULT',
    30,
))
# Number of seconds to wait on selenium page element (constantly checking for existence) before giving up.
# Refers to a specific element loading within a page. Default of 5 seconds.
ETC_SELENIUM_IMPLICIT_WAIT_DEFAULT = int(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_IMPLICIT_WAIT_DEFAULT',
    5,
))
# Location to auto-create drivers for tests. Should be either "class" or "method".
# The "class" option will create drivers on test class startup, that all test methods will share.
# The "method" option will create drivers on each test method instance.
ETC_SELENIUM_DRIVER_LEVEL = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SELENIUM_DRIVER_LEVEL',
    'method',
)).strip().lower()

# endregion Selenium Options


# region User Handling Options

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

# endregion User Handling Options


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
