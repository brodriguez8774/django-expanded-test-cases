"""Constants for ExpandedTestCases package."""
from django.conf import settings


# Underline style definition for debug printing.
UNDERLINE = '\u001b[4m'


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
ETC_DEBUG_PRINT = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT',
    True
)
# Indicates whether partial matches are allowed for messages.
ETC_ALLOW_MESSAGE_PARTIALS = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS',
    True
)
# Indicates whether tests fail when there are messages in the response that were not explicitly tested for.
ETC_MATCH_ALL_CONTEXT_MESSAGES = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES',
    False
)
