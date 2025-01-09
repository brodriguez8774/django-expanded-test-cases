General Setting Configuration
*****************************

The following
`Django settings <https://docs.djangoproject.com/en/dev/topics/settings/>`_
allow configuration of the **ExpandedTestCases** package.

All of these settings are optional, and will fall back to a default value if
not defined.


Configuring Client State
========================

This section documents controls for handling test client state, which
is directly relevant to "retaining user login between client requests"
as well as "retaining session data between client requests".

Note that if you need to test for session data in your project, then the
default settings are probably inadequate, and you will need to adjust
the below values.


RESET_CLIENT_STATE_ON_REQUEST
-----------------------------

Originally, DjangoETC would force the Django test client to "reset" at the
start of each ``assertResponse()`` statement.
The idea was that it would ensure no user accidentally remains logged in
between assertions, which could unexpectedly lead to tests being incorrect.

However, due to how Django logs out test users, this had the side-effect of
also clearing session data between assertions.
Therefore, concurrent assertions could not share session data, and thus
some test scenarios were not possible.

This setting keeps the original behavior if set to True (the default).
Set to false to skip client reset between assertions for all project tests.


.. note::

    Alternatively, if you don't want to use a project-wide setting, then you
    can set the ``self._reset_client_state_on_request`` class-level variable.

    This will default to the value defined by ``RESET_CLIENT_STATE_ON_REQUEST``
    for your project.

    The ``self._reset_client_state_on_request`` is a class-level boolean that
    lets you override the setting on a per-test basis.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_RESET_CLIENT_STATE_ON_REQUEST = False


Configuring Content Areas for Assertions
========================================

SKIP_CONTENT_BEFORE
-------------------

Only applicable to ``assertResponse`` statements,
when using ``expected_content``.

Effectively an "upper" html content value to strip out of both search space
and debug output.
Anything above this value will be removed.

In most projects, there is a set of content (such as header data) at the start
of the page, which tests generally won't target.
If the project has a consistent element or string value that defines where
content starts being relevant, that value can be defined here, to then exclude
all start-of-page content above it, for all tests within project.

Defining this setting can help significantly reduce redundant/"useless" debug
output for integration tests, as long as the content is universally exclude-able
project-wide.

For similar logic on a per-test basis, see
:ref:`the content_starts_after parameter<test_cases/integration_test_case/response_assertions:Misc Parameters>`.


:Type: ``string`` (Either regex or literal)
:Default: ``None``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE = '<h1>My Header</h1>'


SKIP_CONTENT_AFTER
------------------

Only applicable to ``assertResponse`` statements,
when using ``expected_content``.

Effectively an "lower" html content value to strip out of both search space
and debug output.
Anything below this value will be removed.

Similar to above ``SKIP_CONTENT_BEFORE`` setting.

For similar logic on a per-test basis, see
:ref:`the content_starts_before parameter<test_cases/integration_test_case/response_assertions:Misc Parameters>`.


:Type: ``string`` (Either regex or literal)
:Default: ``None``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER = '<footer>My Footer</footer>'


SKIP_CONTENT_HEAD
-----------------

Similar to above ``SKIP_CONTENT_BEFORE`` setting, except in boolean form.
Can use this if the project should simply ignore content in the
``<head>`` tag.

If set to false or if ``SKIP_CONTENT_BEFORE`` is defined, then has no effect.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_HEAD = True


Configuring Assertion Functionality
===================================

Some of the provided assertions can be configured to be more or less strict,
using the following settings.


ALLOW_TITLE_PARTIALS
--------------------

When running the
:ref:`test_cases/integration_test_case/other_functionality:assertPageTitle`
assertion, this setting can optionally allow partial title matching.
If partial is allowed, then checks for title partials/substrings will pass.
Otherwise, the title string must match the full provided test value,
or it will fail.


:Type: ``bool``
:Default: ``False``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_ALLOW_TITLE_PARTIALS = True


ALLOW_MESSAGE_PARTIALS
----------------------

When running the
:ref:`test_cases/integration_test_case/other_functionality:assertContextMessages`
assertion, this setting can optionally allow partial message matching.
If partial is allowed, then checks for message partials/substrings will pass.
Otherwise, the message string must match the full provided test value,
or it will fail.


:Type: ``bool``
:Default: ``False``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS = True


MATCH_ALL_CONTEXT_MESSAGES
--------------------------

When running the
:ref:`test_cases/integration_test_case/other_functionality:assertContextMessages`
assertion, this setting optionally tell tests to fail when there are messages in
the response that were not explicitly tested for.

Only applies in ``assertResponse`` if any ``expected_messages`` were provided
at all.
Otherwise, the ``assertResponse`` will still pass in the case when
no ``expected_messages`` were provided, and context messages were returned
with the response.


:Type: ``bool``
:Default: ``False``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES = True
