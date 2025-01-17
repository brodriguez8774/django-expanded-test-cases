IntegrationTestCase - Other Functionality
*****************************************


This page documents the specs for remaining **IntegrationTestCase** class
functionality.


----


Element Assertions
==================

The **Element Assertions** check for the existence and state of a specific
element within a `Django Response Object
<https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_.

Each assertion returns the verified element. This is so that any further
required testing that the assertion didn't handle can be easily performed on
the element.


assertRedirects()
-----------------

.. code::

    self.assertRedirects(response, expected_redirect_url)

Asserts that a request is redirected to a specific URL.

Most functionality comes from Django's default assertRedirects() function.

However, this adds additional wrapper logic to:

* Check that provided response param is a valid Response object, and attempts
  to generate one if not.
* Attempts to grab the URL as a
  `reverse <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_.

:param response: Response object to check against.
:param expected_redirect_url: Expected path that response should redirect to.

:return: Return value of parent Django assertRedirects() function.


assertStatusCode()
------------------

.. code::

    self.assertStatusCode(response, expected_status)

Asserts that a response has a given status code value.

:param response: Response object to check against.
:param expected_status: Expected status code that response should have, after
                       any redirections are completed.

:return: The found status code value, in case tests need to run additional
        logic on it.


assertPageTitle()
-----------------

.. code::

    self.assertPageTitle(response, expected_title, allow_partials=True)

Asserts that a response has a given title value. Aka, the ``<title>`` tag
contents.

:param response: Response object to check against.
:param expected_title: Expected title text that response should have.
:param allow_partials: Bool indicating if title needs to match exactly, or is
                   allowed partial matches.
                   Useful when site title is long, and tests only care about
                   a specific subsection of the title.
                   Defaults to False, aka must be an exact match.
                   For a site-wide version of this param, see
                   :ref:`configuration/general:ALLOW_TITLE_PARTIALS`

:return: The found title value, in case tests need to run additional logic
        on it.


assertPageHeader()
------------------

.. code::

    self.assertPageHeader(response, expected_header)

Asserts that a response has a given page header value. Aka, the ``<h1>`` tag
contents.

Technically, each page is only meant to have a single ``<h1>`` header.
However, not all sites follow this rule, and this assertion does not work
reliably in cases when there are multiple ``<h1>`` header tags on a page.

:param response: Response object to check against.
:param expected_header: Expected page header text that response should have.

:return: The found page header value, in case tests need to run additional
        logic on it.


assertContextMessages()
-----------------------

.. code::

    self.assertContextMessages(response, expected_messages, allow_partials=True)

Asserts that a response has the given context message values. These are
usually generated with the
`Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.

Expected messages can be provided as a single string, or a list of multiple
expected strings.

:param response: Response object to check against.
:param expected_messages: Expected messages that response should contain.
:param allow_partials: Bool indicating if message needs to match exactly, or is
                   allowed partial matches.
                   Useful when messages are long, and tests only care about
                   a specific subsection of the messages.
                   Defaults to False, aka must be an exact match.
                   For a project-wide version of this param, see
                   :ref:`configuration/general:ALLOW_MESSAGE_PARTIALS`

:return: None.


.. important::

   Currently, the ``assertContextMessages()`` assertion only cares if a value
   is provided into the ``expected_messages`` param, and then not found in the
   page response.

   It will **NOT** fail if messages exist in the response, but are not checked
   for.

   For example, if we have a response containing messages of
   ["Message #1", "Message #2", "Message #3"] and use the following code to
   check for a single message, the unchecked messages (#1 and #3) will be
   ignored and the assertion will pass:

   ``self.assertContextMessages(response, 'Message #2')``

   In the future, there will likely be an option to change this behavior, so
   that if desired, the assertion will only pass when all present messages are
   checked for.


assertNotContextMessages()
--------------------------

.. code::

    self.assertNotContextMessages(response, expected_not_messages, allow_partials=True)

The negation of
:ref:`test_cases/integration_test_case/other_functionality:assertContextMessages()`
Asserts that a response does not contain the given context message values.
These are usually generated with the
`Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.

Expected messages can be provided as a single string, or a list of multiple
expected strings.

:param response: Response object to check against.
:param expected_not_messages: Expected messages that response should NOT
                              contain.
:param allow_partials: Bool indicating if message needs to match exactly, or is
                   allowed partial matches.
                   Useful when messages are long, and tests only care about
                   a specific subsection of the messages.
                   Defaults to False, aka must be an exact match.
                   For a project-wide version of this param, see
                   :ref:`configuration/general:ALLOW_MESSAGE_PARTIALS`

:return: None.


assertPageContent()
-------------------

.. code::

    self.assertPageContent(response, expected_content, ignore_ordering=True)

Asserts that a response has the given page content html.

Expected content can be provided as a single string, or a list of multiple
expected strings.

:param response: Response object to check against.
:param expected_content: Expected content that response should contain.
:param ignore_ordering: Bool indicating if content ordering matters.
                        Defaults to assuming ordering should be obeyed.
:param content_starts_after: Optional content value to strip out of search
                             space. This value and anything above will be
                             removed. If multiple instances exist on page, then
                             the first found instance (from top of HTML output)
                             is selected.
:param content_ends_before: Optional content value to strip out of search space.
                            This value and anything below will be removed. If
                            multiple instances exist on page, then the first
                            found instance (from bottom of HTML output) is
                            selected.

:return: The found response content, in case tests need to run additional
         logic on it.


assertNotPageContent()
----------------------

.. code::

    self.assertNotPageContent(response, expected_not_content, ignore_ordering=True)

The negation of
:ref:`test_cases/integration_test_case/other_functionality:assertPageContent()`
Asserts that a response does not contain the given page content html.

Expected content can be provided as a single string, or a list of multiple
expected strings.

Optionally can also verify ordering of expected elements, with the assertion
failing if elements are not found in order on the page. Default is to assume
that ordering is important.

:param response: Response object to check against.
:param expected_not_content: Expected content that response should NOT contain.

:return: The found response content, in case tests need to run additional
         logic on it.


assertRepeatingElement()
------------------------

.. code::

    self.assertRepeatingElement(response, expected_repeating_element, repeat_count)

:param response: Response object to check against.
:param expected_repeating_element: The expected repeating HTML element.
                                   Ex: <li>, <p>, etc.
:param repeat_count: Integer indicating how many times the HTML element should
                     repeat.
:param content_starts_after: Optional content value to strip out of search
                             space. This value and anything above will be
                             removed. If multiple instances exist on page, then
                             the first found instance (from top of HTML output)
                             is selected.
:param content_ends_before: Optional content value to strip out of search space.
                            This value and anything below will be removed. If
                            multiple instances exist on page, then the first
                            found instance (from bottom of HTML output) is
                            selected.

:return: The found response content, in case tests need to run additional
         logic on it.

----


Helper Functions
================

get_page_title()
----------------

.. code::

    self.get_page_title(response)

Parses out title element (aka ``<title>`` tag) from response object.

:param response: Response object to pull title from.

:return: Found title element.


get_page_header()
-----------------

.. code::

    self.get_page_header(response)

Parses out page header element (aka ``<h1>`` tag) from response object.

:param response: Response object to pull header from.

:return: Found page header element.


get_context_messages()
----------------------

.. code::

    self.get_context_messages(response)

Parses out message elements from response object. These are
usually generated with the
`Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.

:param response: Response object to pull messages from.

:return: Found message elements.


Hook Functions
==============

Finally, the IntegrationTestCase provides "hook" functions to enable additional
setup and configuration for any project, regardless of individual project needs.

We acknowledge that test writing is never a "one size fits all" situation, and
every project is different.
Thus, hook functions provide additional points in which further logic can be
inject.

By default, these functions do nothing on their own and are fully safe to
override.

_get_login_user__extra_user_auth_setup()
----------------------------------------

.. code::

    self._get_login_user__extra_user_auth_setup(*args, **kwargs)

This function is called after getting the corresponding
:doc:`User object for authentication<../../managing_test_users>`, but prior
to attempting to process the
`request-response <https://docs.djangoproject.com/en/dev/ref/request-response/>`_
cycle.

This is critical for projects with additional authentication logic.
If a project has additional authentication logic to process (such as
authentication keys or custom Auth backend logic), then it should be done
here to ensure test users can authenticate.

This hook receives only known args/kwargs that are related to user
authentication and request processing.


_assertResponse__pre_builtin_tests()
------------------------------------

.. code::

    self._assertResponse__pre_builtin_tests(*args, **kwargs)

This function is called after getting the
`page response <https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_,
but prior to calling any assertion checks on it.

If a project requires any additional pre-check setup, or should have any
custom checks to run prior to those built into ETC, then it should be done here.

This hook receives all known args/kwargs that the response assertion receives.


_assertResponse__post_builtin_tests()
-------------------------------------

.. code::

    self._assertResponse__post_builtin_tests(*args, **kwargs)


This function is called after getting the
`page response <https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_,
and after calling all provided assertion checks on it.

If a project requires any additional clean-up processing, or should have any
custom checks to run after those built into ETC, then it should be done here.

This hook receives all known args/kwargs that the response assertion receives.


Implementing Hooks
------------------

These hook functions only apply when using the **Response Assertion**
functionality.
If not calling any **Response Assertions**, then these hooks do nothing.

To use these hooks, implement a custom class that inherits from the
**IntegrationTestCase** class.
Then overwrite the corresponding hook and add the desired additional logic.

If any additional args/kwargs are provided to a **Response Assertion**
(above and beyond what the response assertion already expects), these
are passed on to all hooks, so that the end-user can provide any additional
data their project needs to function.


Hook Warnings and Warning Customization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If any supplemental args/kwargs are passed into any of the
:doc:`Response Assertions<./response_assertions>` (beyond those the package
is aware of), then they are assumed to be needed for one or more of the built-in
hook functions.

However, the hook functions do nothing by default, and are meant to be
overridden.
Thus, if supplemental args/kwargs are provided and no hooks functions are
overridden, the package will raise warnings indicating such, to alert the
programmer that one or more provided values are probably not
working as expected.

To customize how these warnings behave, override either
``_hook_function_warning_check()`` (which displays the warning messages),
or ``_hook_function_warning_check_if_statement()`` (which controls the
if-statement that determines if the warnings should display).

See source code for these functions for more details.
They're both towards the bottom of the file
`django_expanded_test_cases/test_cases/integration_test_case.py <https://github.com/brodriguez8774/django-expanded-test-cases/blob/main/django_expanded_test_cases/test_cases/integration_test_case.py>`_.
