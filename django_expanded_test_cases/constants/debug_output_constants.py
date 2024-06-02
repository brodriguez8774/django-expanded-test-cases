"""
Constants related to end-user debug/testing output.
"""

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


# region General Debug Handling

# Indicates whether the additional debug information should be output.
ETC_DEBUG_PRINT = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT',
        True,
    )
)


# A set of regex-matching strings to skip displaying during debug output.
# Useful such as when importing third-party libraries with front-end elements, if you don't expect to ever
# need to test for said elements.
ETC_DEBUG_PRINT__SKIP_DISPLAY = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT__SKIP_DISPLAY',
    [],
)

# endregion General Debug Handling


# region Console Region Show/Hide Options

# Enabling/disabling output of specific sections.
ETC_INCLUDE_RESPONSE_DEBUG_URL = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_URL',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_CONTENT = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTENT',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_HEADER = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_HEADER',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_CONTEXT = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTEXT',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_SESSION = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_SESSION',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_MESSAGES = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_MESSAGES',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_FORMS = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_FORMS',
        True,
    )
)
ETC_INCLUDE_RESPONSE_DEBUG_USER_INFO = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_USER_INFO',
        True,
    )
)

# endregion Console Region Show/Hide Options


# region Console Color Options

# General output/color format settings.
ETC_OUTPUT_ERROR_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_ERROR_HEADER_COLOR',
        '{0}{1}{2}'.format(Fore.RED, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
    )
)
ETC_OUTPUT_EXPECTED_MATCH_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_MATCH_COLOR',
        '{0}{1}{2}'.format(Fore.CYAN, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
    )
)
ETC_OUTPUT_EXPECTED_ERROR_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_ERROR_COLOR',
        '{0}{1}{2}'.format(Fore.BLACK, Back.CYAN, Style.NORMAL) if COLORAMA_PRESENT else '',
    )
)
ETC_OUTPUT_ACTUALS_MATCH_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_MATCH_COLOR',
        '{0}{1}{2}'.format(Fore.MAGENTA, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else '',
    )
)
ETC_OUTPUT_ACTUALS_ERROR_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_ERROR_COLOR',
        '{0}{1}{2}'.format(Fore.BLACK, Back.MAGENTA, Style.NORMAL) if COLORAMA_PRESENT else '',
    )
)
ETC_OUTPUT_EMPHASIS_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_EMPHASIS_COLOR',
        (Style.BRIGHT if COLORAMA_PRESENT else '') + UNDERLINE,
    )
)
ETC_OUTPUT_RESET_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_OUTPUT_RESET_COLOR',
        Style.RESET_ALL if COLORAMA_PRESENT else UNDERLINE_RESET,
    )
)

# Output/color formatting for response sections.
ETC_RESPONSE_DEBUG_URL_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_URL_COLOR',
        Fore.YELLOW if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_CONTENT_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTENT_COLOR',
        Fore.WHITE if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_HEADER_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_HEADER_COLOR',
        Fore.CYAN if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_CONTEXT_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTEXT_COLOR',
        Fore.BLUE if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_SESSION_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_SESSION_COLOR',
        Fore.MAGENTA if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_MESSAGE_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_MESSAGES_COLOR',
        Fore.CYAN if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_FORM_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_FORMS_COLOR',
        Fore.BLUE if COLORAMA_PRESENT else '',
    )
)
ETC_RESPONSE_DEBUG_USER_INFO_COLOR = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_USER_INFO_COLOR',
        Fore.MAGENTA if COLORAMA_PRESENT else '',
    )
)

# endregion Console Color Options
