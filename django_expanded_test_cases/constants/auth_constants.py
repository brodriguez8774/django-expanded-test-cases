"""
Constants related to testing users and test user auth logic.
"""

# Third-Party Imports.
from django.conf import settings


# Imports that may not be accessible, depending on local python environment setup.
try:
    from colorama import Back, Fore, Style

    COLORAMA_PRESENT = True
except ImportError:
    COLORAMA_PRESENT = False


# region User Handling Options

# Controls if test-users should be automatically generated or not.
ETC_AUTO_GENERATE_USERS = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_AUTO_GENERATE_USERS',
        True,
    )
)
# Controls what level of strictness UnitTest requests have for users.
ETC_REQUEST_USER_STRICTNESS = (
    str(
        getattr(
            settings,
            'DJANGO_EXPANDED_TESTCASES_REQUEST_USER_STRICTNESS',
            'anonymous',
        )
    )
    .strip()
    .lower()
)
# Allows incorporating package with non-standard user identifiers.
# Such as the common case of using a user email as an identifier, instead of a username.
ETC_USER_MODEL_IDENTIFIER = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER',
        'username',
    )
)
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
ETC_DEFAULT_USER_PASSWORD = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD',
        'password',
    )
)
# Indicates if auto-generated users should get pretend "real" first/last name values.
ETC_GENERATE_USERS_WITH_REAL_NAMES = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_GENERATE_USERS_WITH_REAL_NAMES',
        False,
    )
)

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
