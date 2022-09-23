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
RESPONSE_DEBUG_SESSION = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_SESSION',
    Fore.MAGENTA if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_MESSAGES = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_MESSAGES',
    Fore.BLUE if COLORAMA_PRESENT else '',
))
RESPONSE_DEBUG_USER_INFO = str(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_USER_INFO',
    Fore.CYAN if COLORAMA_PRESENT else '',
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
