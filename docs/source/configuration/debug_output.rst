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

    That is, the "expected" should always come first, and the "actual" should
    come later.

    This ordering affects:

    * General assertion error messages.
      If ordering is wrong, then some error output might be slightly misleading.
      This is sometimes the case even in default Django test assertions.

    * Color debug output, if
      `Colorama <https://pypi.org/project/colorama/>`_ is installed.


General Debug Output Handling
=============================

General configurations for handling of debug output on test errors.

For many of these settings, they allow customizing to personal preference for
readability.
Thus, we recommend setting up a project ``.env`` file (or equivalent)
so that these settings can be set per-developer, for whatever allows them
the most optimal individual workflow.


DEBUG_PRINT
-----------

Django ETC can optionally provide additional debug testing output, to help with
trying to troubleshoot test errors. See
:ref:`general_usage:Debug Output Overview` for more details.

This setting enables or disables debug output.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = False


DEBUG_PRINT__SKIP_DISPLAY
-------------------------

A set of regex-matching strings to skip displaying during debug output.
Since it's regex, it can match arbitrary values in the middle of html.

Useful such as when importing third-party libraries with front-end elements,
if you don't expect to ever need to test for said elements.

Should be a list containing strings of one or more regex values to skip.


:Type: ``list``
:Default: ``[]``,

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT__SKIP_DISPLAY = [
        'regex1',
        'regex2',
    ]


DEBUG_PRINT__TEST_SEPARATOR
-------------------------------

Optionally customize the visual separator between UnitTest error output.
This is displayed at the top of every failing UnitTest output, to help
add visual distinction of where one test ends and the next begins.

Can be used to add extra newlines or other formatting to debugging output.

.. note::

    Must manually insert newlines at the end of each line where desired.
    Can optionally also insert color formatting if desired.


:Type: ``str``
:Default: ``''``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT__TEST_SEPARATOR = (
        '\n'
        '\n'
        '=========================**********=========================\n'
        '=========================**********=========================\n'
        '\n'
        '\n'
    )


DEBUG_PRINT__RESPONSE_SEPARATOR
-------------------------------

Optionally customize the visual separator between
:doc:`Response Assertions<../test_cases/integration_test_case/response_assertions>`.
This is displayed at the bottom of the assertResponse debug output.

Can be used to add extra newlines or other formatting between
``assertResponse`` debugging output.

.. note::

    Must manually insert newlines at the end of each line where desired.
    Can optionally also insert color formatting if desired.


:Type: ``str``
:Default: ``''``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT__RESPONSE_SEPARATOR = (
        '\n'
        '\n'
        '=========================**********=========================\n'
        '=========================**********=========================\n'
        '\n'
        '\n'
    )


DEBUG_PRINT__STD_OUT_SEPARATOR
------------------------------

Optionally customize the visual separator at the end of test std_out (print)
output, during debug output for a failing
:doc:`Response Assertion<../test_cases/integration_test_case/response_assertions>`.

Aside adding visual separation in a separate location, handles generally the
same as the above
``DEBUG_PRINT__RESPONSE_SEPARATOR``.


:Type: ``str``
:Default: ``''``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT__STD_OUT_SEPARATOR = (
        '\n'
        '\n'
        '=========================**********=========================\n'
        '=========================**********=========================\n'
        '\n'
        '\n'
    )


DEBUG_PRINT__LOGGING_SEPARATOR
------------------------------

Optionally customize the visual separator at the end of test logging output,
during debug output for a failing
:doc:`Response Assertion<../test_cases/integration_test_case/response_assertions>`.

Aside adding visual separation in a separate location, handles generally the
same as the above
``DEBUG_PRINT__RESPONSE_SEPARATOR``.


:Type: ``str``
:Default: ``''``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT__LOGGING_SEPARATOR = (
        '\n'
        '\n'
        '=========================**********=========================\n'
        '=========================**********=========================\n'
        '\n'
        '\n'
    )


ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH
-----------------------------------------------

Controls how many "contextual values" are shown on ``assertContent`` test error.

This setting specifically only applies when the ``assertContent`` is given
multiple values to test for in a single assertion.

The default value (of 2) shows the two statements before and the two after the
failing value, if possible.

Then for example, setting to this to 3 will attempt to show 3 statements before
and after.
While setting this to 0 will skip the assertion trying to output context on
failure.


:Type: ``int``
:Default: ``2``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH = 3


Showing/Hiding Output Regions
=============================

On a UnitTest response failure, ETC will attempt to display debug output for
any requests that were triggered prior to the failure, when using
:doc:`Response Assertion<../test_cases/integration_test_case/response_assertions>`.

This output can provide quite a bit of information.

In some projects, this is helpful.
In others, it ends up being overkill with some of it turning into white noise.

To help account for both ends of this spectrum, many of the debug output
sections can be customized to be shown/hidden as needed.


INCLUDE_RESPONSE_DEBUG_URL
--------------------------

Indicates if the "url" section of debug output should be shown or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_URL = True


INCLUDE_RESPONSE_DEBUG_CONTENT
------------------------------

Indicates if the "html content" section of debug output should be shown
or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTENT = True


INCLUDE_RESPONSE_DEBUG_HEADER
-----------------------------

Indicates if the "header" section of debug output should be shown or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_HEADER = True


INCLUDE_RESPONSE_DEBUG_CONTEXT
------------------------------

Indicates if the "context data" section of debug output should be shown
or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_CONTEXT = True


INCLUDE_RESPONSE_DEBUG_SESSION
------------------------------

Indicates if the "session data" section of debug output should be shown
or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_SESSION = True


INCLUDE_RESPONSE_DEBUG_MESSAGES
-------------------------------

Indicates if the "page messages" section of debug output should be
shown or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_MESSAGES = True


INCLUDE_RESPONSE_DEBUG_FORMS
----------------------------

Indicates if the "form" section of debug output should be shown or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_FORMS = True


INCLUDE_RESPONSE_DEBUG_USER_INFO
--------------------------------

Indicates if the "login user" section of debug output should be shown
or hidden.

True means show, False means hide.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_INCLUDE_RESPONSE_DEBUG_USER_INFO = True


Debug Output Color Handling
===========================

If the `Colorama <https://pypi.org/project/colorama/>`_ Python package is
installed, then ETC will colorize debug output out of the box.

To adjust this default coloring with
`Colorama <https://pypi.org/project/colorama/>`_,
or to provide custom debug colorization if ``Colorama`` is not installed,
use the following settings.


OUTPUT_ERROR_HEADER_COLOR
-------------------------

Color formatting used for displaying the header section at the top of a new
error output.


:Type: ``str``
:Default: Colorama ``Fore.RED``, ``Back.RESET``, ``Style.NORMAL``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_ERROR_HEADER_COLOR = 'CustomHeaderColor'


OUTPUT_EXPECTED_MATCH_COLOR
---------------------------

Color formatting used for displaying a matching character for the "expected"
value of a comparison test.


:Type: ``str``
:Default: Colorama ``Fore.CYAN``, ``Back.RESET``, ``Style.NORMAL``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_MATCH_COLOR = 'CustomExpectedMatchColor'


OUTPUT_EXPECTED_ERROR_COLOR
---------------------------

Color formatting used for displaying a mismatched character for the "expected"
value of a comparison test.


:Type: ``str``
:Default: Colorama ``Fore.BLACK``, ``Back.CYAN``, ``Style.NORMAL``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_ERROR_COLOR = 'CustomExpectedErrorColor'


OUTPUT_ACTUALS_MATCH_COLOR
--------------------------

Color formatting used for displaying a matching character for the "actual"
value of a comparison test.


:Type: ``str``
:Default: Colorama ``Fore.MAGENTA``, ``Back.RESET``, ``Style.NORMAL``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_MATCH_COLOR = 'CustomActualMatchColor'


OUTPUT_ACTUALS_ERROR_COLOR
--------------------------

Color formatting used for displaying a mismatched character for the "actual"
value of a comparison test.


:Type: ``str``
:Default: Colorama ``Fore.BLACK``, ``Back.MAGENTA``, ``Style.NORMAL``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_ERROR_COLOR = 'CustomActualErrorColor'


OUTPUT_EMPHASIS_COLOR
---------------------

Color formatting used for "emphasis" logic.


:Type: ``str``
:Default: Colorama ``Style.BRIGHT``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_EMPHASIS_COLOR = 'CustomEmphasis'


OUTPUT_RESET_COLOR
------------------

Color formatting used for "reset color" logic.
Used as part of string terminators, to prevent colors bleeding into other
console output.


:Type: ``str``
:Default: Colorama ``Style.RESET_ALL`` or '\u001b[0m'

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_OUTPUT_RESET_COLOR = 'CustomReset'


RESPONSE_OUTPUT_URL_COLOR
-------------------------

Color formatting used for the response "debug URL output" section.


:Type: ``str``
:Default: Colorama ``Fore.YELLOW``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_URL_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_CONTENT_COLOR
-----------------------------

Color formatting used for the response "debug content output" section.


:Type: ``str``
:Default: Colorama ``Fore.WHITE``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTENT_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_HEADER_COLOR
----------------------------

Color formatting used for the response "debug header output" section.

:Type: ``str``
:Default: Colorama ``Fore.CYAN``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_HEADER_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_CONTEXT_COLOR
-----------------------------

Color formatting used for the response "debug context output" section.


:Type: ``str``
:Default: Colorama ``Fore.BLUE``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_CONTEXT_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_SESSION_COLOR
-----------------------------

Color formatting used for the response "debug session output" section.


:Type: ``str``
:Default: Colorama ``Fore.MAGENTA``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_SESSION_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_MESSAGES_COLOR
------------------------------

Color formatting used for the response "debug messages output" section.


:Type: ``str``
:Default: Colorama ``Fore.CYAN``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_MESSAGES_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_FORMS_COLOR
---------------------------

Color formatting used for the response "debug messages output" section.


:Type: ``str``
:Default: Colorama ``Fore.BLUE``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_FORMS_COLOR = 'CustomOutputColor'


RESPONSE_OUTPUT_USER_INFO_COLOR
-------------------------------

Color formatting used for the response "debug user info output" section.


:Type: ``str``
:Default: Colorama ``Fore.MAGENTA``, or empty str.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESPONSE_OUTPUT_USER_INFO_COLOR = 'CustomOutputColor'
