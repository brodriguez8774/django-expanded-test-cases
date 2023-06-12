Debug Output Configuration
**************************

The following
`Django settings <https://docs.djangoproject.com/en/dev/topics/settings/>`_
allow configuration of the **ExpandedTestCases** package, regarding settings
for package debug output on test failure.

All of these settings are optional, and will fall back to a default value if
not defined.

.. note::
    When doing a testing comparison of two values, all logic in ETC assumes
    the format of ``someAssert(<expected_value>, <actual_value>)``.

    That is, the expected should always come first, and the actual should
    come later.

    This really only matters if `Colorama <https://pypi.org/project/colorama/>`_
    is installed and the default colorization is being used.


Colorize General Debug Output
=============================

If the `Colorama <https://pypi.org/project/colorama/>`_ Python package is
installed, then ETC will colorize debug output out of the box.

In order to provide debug colorization if ``Colorama`` is not installed, or to
tweak the default provided debug colors, use the following settings.


OUTPUT_ERROR_HEADER_COLOR
-------------------------

Color formatting used for displaying the header section at the top of a new
error output.

:Type: ``str``
:Default: Colorama ``Fore.RED``, ``Back.RESET``, ``Style.NORMAL``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_ERROR_HEADER_COLOR = 'CustomHeaderColor'


OUTPUT_EXPECTED_MATCH_COLOR
---------------------------

Color formatting used for displaying a matching character for the "expected"
value of a comparison test.

:Type: ``str``
:Default: Colorama ``Fore.CYAN``, ``Back.RESET``, ``Style.NORMAL``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_MATCH_COLOR = 'CustomExpectedMatchColor'


OUTPUT_EXPECTED_ERROR_COLOR
---------------------------

Color formatting used for displaying a mismatched character for the "expected"
value of a comparison test.

:Type: ``str``
:Default: Colorama ``Fore.BLACK``, ``Back.CYAN``, ``Style.NORMAL``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_ERROR_COLOR = 'CustomExpectedErrorColor'


OUTPUT_ACTUALS_MATCH_COLOR
--------------------------

Color formatting used for displaying a matching character for the "actual"
value of a comparison test.

:Type: ``str``
:Default: Colorama ``Fore.MAGENTA``, ``Back.RESET``, ``Style.NORMAL``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_MATCH_COLOR = 'CustomActualMatchColor'


OUTPUT_ACTUALS_ERROR_COLOR
--------------------------

Color formatting used for displaying a mismatched character for the "actual"
value of a comparison test.

:Type: ``str``
:Default: Colorama ``Fore.BLACK``, ``Back.MAGENTA``, ``Style.NORMAL``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_ERROR_COLOR = 'CustomActualErrorColor'


OUTPUT_EMPHASIS_COLOR
---------------------

Color formatting used for "emphasis" logic.

:Type: ``str``
:Default: Colorama ``Style.BRIGHT``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_EMPHASIS_COLOR = 'CustomEmphasis'


OUTPUT_RESET_COLOR
------------------

Color formatting used for "reset color" logic.
Used as part of string terminators, to prevent colors bleeding into other
console output.

:Type: ``str``
:Default: Colorama ``Style.RESET_ALL`` or '\u001b[0m'

Example::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_RESET_COLOR = 'CustomReset'


Enable or Disable Response Debug Sections
=========================================

On a UnitTest response failure, ETC will attempt to display debug output for
any requests that were triggered prior to the failure.

Each section in this debug output can be disabled if it is not desired.


INCLUDE_RESPONSE_DEBUG_URL
--------------------------

Toggles displaying or hiding the response "debug URL output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_URL = False


INCLUDE_RESPONSE_DEBUG_CONTENT
------------------------------

Toggles displaying or hiding the response "debug content output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTENT = False


INCLUDE_RESPONSE_DEBUG_HEADER
-----------------------------

Toggles displaying or hiding the response "debug header output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_HEADER = False


INCLUDE_RESPONSE_DEBUG_CONTEXT
------------------------------

Toggles displaying or hiding the response "debug context output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTEXT = False


INCLUDE_RESPONSE_DEBUG_SESSION
------------------------------

Toggles displaying or hiding the response "debug session output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_SESSION = False


INCLUDE_RESPONSE_DEBUG_MESSAGES
-------------------------------

Toggles displaying or hiding the response "debug message output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_MESSAGES = False


INCLUDE_RESPONSE_DEBUG_FORMS
----------------------------

Toggles displaying or hiding the response "debug form output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_FORMS = False


INCLUDE_RESPONSE_DEBUG_USER_INFO
--------------------------------

Toggles displaying or hiding the response "debug user info output" section.

:Type: ``bool``
:Default: True

Example::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_USER_INFO = False


Colorize Response Debug Output
==============================

If the `Colorama <https://pypi.org/project/colorama/>`_ Python package is
installed, then ETC will colorize debug response output out of the box.

In order to provide debug colorization if ``Colorama`` is not installed, or to
tweak the default provided debug response colors, use the following settings.


RESPONSE_OUTPUT_URL
-------------------

Color formatting used for the response "debug URL output" section.

:Type: ``str``
:Default: Colorama ``Fore.YELLOW``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_URL_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_CONTENT_COLOR
-----------------------------

Color formatting used for the response "debug content output" section.

:Type: ``str``
:Default: Colorama ``Fore.WHITE``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTENT_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_HEADER_COLOR
----------------------------

Color formatting used for the response "debug header output" section.

:Type: ``str``
:Default: Colorama ``Fore.CYAN``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_HEADER_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_CONTEXT_COLOR
-----------------------------

Color formatting used for the response "debug context output" section.

:Type: ``str``
:Default: Colorama ``Fore.BLUE``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTEXT_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_SESSION_COLOR
-----------------------------

Color formatting used for the response "debug session output" section.

:Type: ``str``
:Default: Colorama ``Fore.MAGENTA``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_SESSION_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_MESSAGES_COLOR
------------------------------

Color formatting used for the response "debug messages output" section.

:Type: ``str``
:Default: Colorama ``Fore.CYAN``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_MESSAGES_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_FORMS_COLOR
---------------------------

Color formatting used for the response "debug messages output" section.

:Type: ``str``
:Default: Colorama ``Fore.BLUE``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_FORMS_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_USER_INFO_COLOR
-------------------------------

Color formatting used for the response "debug user info output" section.

:Type: ``str``
:Default: Colorama ``Fore.MAGENTA``, or empty str.

Example::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_USER_INFO_COLOR = 'CustomOutputColor'
