General Setting Configuration
*****************************

The following
`Django settings <https://docs.djangoproject.com/en/dev/topics/settings/>`_
allow configuration of the **ExpandedTestCases** package.

All of these settings are optional, and will fall back to a default value if
not defined.


DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT
=====================================
Django ETC can optionally provide additional debug testing output, to help with
trying to troubleshoot test errors. See
:ref:`general_usage:Debug Output Overview` for more details.

This setting enables or disables debug output.

:Type: ``bool``
:Default: ``True``

Example::

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = False


DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS
================================================
When running the
:ref:`test_cases/integration_test_case:assertContextMessages`
assertion, this setting can optionally allow partial message matching. If
partial is allowed, then checking for message substrings will pass. Otherwise,
the message string must match the full provided test value, or it will fail.

:Type: ``bool``
:Default: ``True``

Example::

    DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS = False


DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES
====================================================

.. warning::
    Not yet implemented.

    Planned for a future release.

When running the
:ref:`test_cases/integration_test_case:assertContextMessages`
assertion, this setting optionally tell tests to fail when there are messages in
the response that were not explicitly tested for.

:Type: ``bool``
:Default: ``False``

Example::

    DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES = True


SELENIUM_TEST_BROWSER
=====================
When using the :doc:`../test_cases/live_server_test_case` classes
for `Selenium <https://www.selenium.dev/>`_ tests, this setting specifies which browser to use.

Currently, supported test browsers are as follows:
 * chrome
 * chromium
 * firefox

:Type: ``string``
:Default: ``chrome``

Example::

    SELENIUM_TEST_BROWSER = 'firefox'
