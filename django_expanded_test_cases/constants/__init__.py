"""
Imports to make this folder behave like a single file.
"""

# Constants related to testing users and test user auth logic.
from .auth_constants import (
    ETC_AUTO_GENERATE_USERS,
    ETC_DEFAULT_ADMIN_USER_IDENTIFIER,
    ETC_DEFAULT_INACTIVE_USER_IDENTIFIER,
    ETC_DEFAULT_STANDARD_USER_IDENTIFIER,
    ETC_DEFAULT_SUPER_USER_IDENTIFIER,
    ETC_DEFAULT_USER_PASSWORD,
    ETC_GENERATE_USERS_WITH_REAL_NAMES,
    ETC_REQUEST_USER_STRICTNESS,
    ETC_USER_MODEL_IDENTIFIER,
)


# Constants that don't necessarily fit under any other categories.
from .general_handling_constants import (
    ETC_ALLOW_MESSAGE_PARTIALS,
    ETC_ALLOW_TITLE_PARTIALS,
    ETC_MATCH_ALL_CONTEXT_MESSAGES,
    ETC_RESPONSE_DEBUG_LOGGING_LEVEL,
    ETC_VIEWS_SHOULD_REDIRECT,
    VOID_ELEMENT_LIST,
)


# Constants related to end-user debug/testing output.
from .debug_output_constants import (
    COLORAMA_PRESENT,
    ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH,
    ETC_DEBUG_PRINT,
    ETC_DEBUG_PRINT__LOGGING_SEPARATOR,
    ETC_DEBUG_PRINT__RESPONSE_SEPARATOR,
    ETC_DEBUG_PRINT__STD_OUT_SEPARATOR,
    ETC_DEBUG_PRINT__SKIP_DISPLAY,
    ETC_INCLUDE_RESPONSE_DEBUG_URL,
    ETC_INCLUDE_RESPONSE_DEBUG_CONTENT,
    ETC_INCLUDE_RESPONSE_DEBUG_CONTEXT,
    ETC_INCLUDE_RESPONSE_DEBUG_FORMS,
    ETC_INCLUDE_RESPONSE_DEBUG_HEADER,
    ETC_INCLUDE_RESPONSE_DEBUG_MESSAGES,
    ETC_INCLUDE_RESPONSE_DEBUG_SESSION,
    ETC_INCLUDE_RESPONSE_DEBUG_USER_INFO,
    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_EMPHASIS_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_RESET_COLOR,
    ETC_RESPONSE_DEBUG_CONTENT_COLOR,
    ETC_RESPONSE_DEBUG_CONTEXT_COLOR,
    ETC_RESPONSE_DEBUG_FORM_COLOR,
    ETC_RESPONSE_DEBUG_HEADER_COLOR,
    ETC_RESPONSE_DEBUG_USER_INFO_COLOR,
    ETC_RESPONSE_DEBUG_MESSAGE_COLOR,
    ETC_RESPONSE_DEBUG_SESSION_COLOR,
    ETC_RESPONSE_DEBUG_URL_COLOR,
    UNDERLINE,
    UNDERLINE_RESET,
)


# Constants related to selenium usage.
from .selenium_constants import (
    ETC_SELENIUM_BROWSER,
    ETC_SELENIUM_DEBUG_PORT_START_VALUE,
    ETC_SELENIUM_DISABLE_CACHE,
    ETC_SELENIUM_DRIVER_LEVEL,
    ETC_SELENIUM_EXTRA_BROWSER_OPTIONS,
    ETC_SELENIUM_HEADLESS,
    ETC_SELENIUM_IMPLICIT_WAIT_DEFAULT,
    ETC_SELENIUM_PAGE_TIMEOUT_DEFAULT,
    ETC_SELENIUM_WINDOW_POSITIONS,
)
