"""
Constants related to selenium usage.
"""

# Third-Party Imports.
from django.conf import settings


# Imports that may not be accessible, depending on local python environment setup.
try:
    from colorama import Back, Fore, Style

    COLORAMA_PRESENT = True
except ImportError:
    COLORAMA_PRESENT = False


# region Selenium Options

# Browser to launch for selenium testing. Options of 'chrome'/'firefox' are good defaults.
ETC_SELENIUM_BROWSER = str(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_SELENIUM_BROWSER',
        'chrome',
    )
)
# Run Selenium tests in "headless" mode.
# Default is to visually show browser. "Headless" will skipp visually rendering the browser while still running tests.
# Good for speed but bad for debugging issues.
ETC_SELENIUM_HEADLESS = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_SELENIUM_HEADLESS',
        False,
    )
)
# Set browser/selenium cache to be ignored.
# Using the cache can sometimes lead to incorrect/failing tests when running selenium in a multi-threaded environment.
ETC_SELENIUM_DISABLE_CACHE = bool(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_SELENIUM_DISABLE_CACHE',
        False,
    )
)
# Starting debug port, to get around remote-debugging-port option using the same value for all generated drivers,
# Using the same port seems to cause issues with allowing proper switching between drivers.
# Each generated driver increments this value by one, to guarantee all tests among all files should have unique ports.
ETC_SELENIUM_DEBUG_PORT_START_VALUE = int(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_SELENIUM_DEBUG_PORT_START_VALUE',
        9221,
    )
)
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
ETC_SELENIUM_PAGE_TIMEOUT_DEFAULT = int(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_SELENIUM_PAGE_TIMEOUT_DEFAULT',
        30,
    )
)
# Number of seconds to wait on selenium page element (constantly checking for existence) before giving up.
# Refers to a specific element loading within a page. Default of 5 seconds.
ETC_SELENIUM_IMPLICIT_WAIT_DEFAULT = int(
    getattr(
        settings,
        'DJANGO_EXPANDED_TESTCASES_SELENIUM_IMPLICIT_WAIT_DEFAULT',
        5,
    )
)
# Location to auto-create drivers for tests. Should be either "class" or "method".
# The "class" option will create drivers on test class startup, that all test methods will share.
# The "method" option will create drivers on each test method instance.
ETC_SELENIUM_DRIVER_LEVEL = (
    str(
        getattr(
            settings,
            'DJANGO_EXPANDED_TESTCASES_SELENIUM_DRIVER_LEVEL',
            'method',
        )
    )
    .strip()
    .lower()
)

# endregion Selenium Options
