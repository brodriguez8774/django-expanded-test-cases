"""
Constants that don't necessarily fit under any other categories.
If this file gets too long, values should be split into their own file when possible.
"""

# Third-Party Imports.
from django.conf import settings


# Imports that may not be accessible, depending on local python environment setup.
try:
    from colorama import Back, Fore, Style

    COLORAMA_PRESENT = True
except ImportError:
    COLORAMA_PRESENT = False


# In most projects, there is a set of content (such as header data) at the start of the page,
# which tests generally won't target. That content can safely be excluded from testing output, similar to
# the assertContent() content_starts_after value.
# If the project has a consistent element or string value that defines where content starts being relevant,
# it can be defined here, to then exclude all start-of-page content above it, for all tests within project.
# Defining this project can help significantly reduce redundant/"useless" debug output for integration tests,
# as long as the content is universally not helpful for testing in regards to the project.
ETC_SKIP_CONTENT_BEFORE = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE',
    None,
)


# Similar to above SKIP_CONTENT_BEFORE, except used to define content at the end-of-page that is to be skipped.
ETC_SKIP_CONTENT_AFTER = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER',
    None,
)


# Similar to SKIP_CONTENT_BEFORE, except is a boolean.
# If true and SKIP_CONTENT_BEFORE is not defined, then automatically skips the site <head></head> tag.
# If false or if SKIP_CONTENT_BEFORE is defined, then has no effect.
ETC_SKIP_CONTENT_HEAD = bool(getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_HEAD',
    False,
))


# Indicates whether partial matches are allowed for site title assertions.
# IE: Will pass as long as provided text appears as a subsection of the full site title.
# Defaults to needing exact match.
ETC_ALLOW_TITLE_PARTIALS = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_ALLOW_TITLE_PARTIALS',
        False,
    )
)


# Indicates whether partial matches are allowed for message assertions.
# IE: Will pass as long as provided text appears as a subsection of one or more messages.
# Defaults to needing exact match.
ETC_ALLOW_MESSAGE_PARTIALS = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS',
        False,
    )
)


# Indicates whether tests fail when there are messages in the response that were not explicitly tested for.
# Aka, when doing ANY message assertion, if this is True, then ALL messages in response need to be checked.
ETC_MATCH_ALL_CONTEXT_MESSAGES = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES',
        False,
    )
)


# Either set logging to only show provided value (or higher) during tests. Or leave as default logging behavior.
ETC_RESPONSE_DEBUG_LOGGING_LEVEL = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_RESPONSE_DEBUG_LOGGING_LEVEL',
    None,
)
if str(ETC_RESPONSE_DEBUG_LOGGING_LEVEL).strip().upper() in ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    # Known value provided. Sanitize and save to attribute.
    ETC_RESPONSE_DEBUG_LOGGING_LEVEL = str(ETC_RESPONSE_DEBUG_LOGGING_LEVEL).strip().upper()
else:
    # Unrecognized value, or value was not provided. Use default behavior.
    ETC_RESPONSE_DEBUG_LOGGING_LEVEL = None


# Indicates whether tests should implicitly check for page redirects on every assertResponse statement.
# None: Default behavior (does nothing, user must explicitly check via 404 status or url assertions).
# True: Implicitly checks for page redirect on every assertResponse statement, unless explicitly told otherwise.
# False: Implicitly checks for NO page redirect on every assertResponse statement, unless explicitly told otherwise.
# This setting probably doesn't have much value in normal testing. But
# can be useful for testing packages with specific niche functionality.
ETC_VIEWS_SHOULD_REDIRECT = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_VIEWS_SHOULD_REDIRECT',
    None,
)
if ETC_VIEWS_SHOULD_REDIRECT is not None:
    ETC_VIEWS_SHOULD_REDIRECT = bool(ETC_VIEWS_SHOULD_REDIRECT)


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
