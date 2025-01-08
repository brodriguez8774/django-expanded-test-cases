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


assertRedirects
---------------

.. code::

    assertRedirects()

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


assertStatusCode
----------------

.. code::

    assertStatusCode()

Asserts that a response has a given status code value.

:param response: Response object to check against.
:param expected_status: Expected status code that response should have, after
                       any redirections are completed.

:return: The found status code value, in case tests need to run additional
        logic on it.


assertPageTitle
---------------

.. code::

    assertPageTitle()

Asserts that a response has a given title value. Aka, the ``<title>`` tag
contents.

:param response: Response object to check against.
:param expected_title: Expected title text that response should have.
:param exact_match: Bool indicating if title needs to match exactly, or is
                   allowed partial matches. Useful when site title is long,
                   and tests only care about a specific subsection of the
                   title.

:return: The found title value, in case tests need to run additional logic
        on it.


assertPageHeader
----------------

.. code::

    assertPageHeader()

Asserts that a response has a given page header value. Aka, the ``<h1>`` tag
contents.

Technically, each page is only meant to have a single ``<h1>`` header.
However, not all sites follow this rule, and this assertion does not work
reliably in cases when there are multiple ``<h1>`` header tags on a page.

:param response: Response object to check against.
:param expected_title: Expected page header text that response should have.

:return: The found page header value, in case tests need to run additional
        logic on it.


assertContextMessages
---------------------

.. code::

    assertContextMessages()

Asserts that a response has the given context message values. These are
usually generated with the
`Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.

Expected messages can be provided as a single string, or a list of multiple
expected strings.

:param response: Response object to check against.
:param expected_messages: Expected messages that response should contain.
:param allow_partials: Bool indicating if messages must match exactly, or
                      are allowed partial matches. Useful for messages that
                      are extra long, and tests only care about a specific
                      subsection of the message.

:return: None.


.. important::

   Currently, the ``assertContextMessages()`` assertion only cares if a value
   is provided into the ``expected_messages`` param, and then not found in the
   page response.

   It will **NOT** fail if messages exist in the response, but are not checked.

   For example, if we have a response containing messages of
   ["Message #1", "Message #2", "Message #3"] and use the following code to
   check for a single message, the unchecked messages (#1 and #3) will be
   ignored and the assertion will pass:

   ``self.assertContextMessages(response, 'Message #2')``

   In the future, there will likely be an option to change this behavior, so
   that if there are messages on the page that are **NOT** checked via the
   ``expected_messages`` param, then the ``assertContextMessages()`` assertion
   will fail.


assertPageContent
-----------------

.. code::

    assertPageContent()

Asserts that a response has the given page content html.

Expected content can be provided as a single string, or a list of multiple
expected strings.

Optionally can also verify ordering of expected elements, with the assertion
failing if elements are not found in order on the page. Default is to assume
that ordering is important.

:param response: Response object to check against.
:param expected_content: Expected content that response should contain.
:param ignore_ordering: Bool indicating if content ordering matters. Defaults
                        to assuming ordering should be obeyed.
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


assertRepeatingElement
----------------------

.. code::

    assertRepeatingElement()

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

get_page_title
--------------

.. code::

    get_page_title(response)

Parses out title element (aka ``<title>`` tag) from response object.

:param response: Response object to pull title from.

:return: Found title element.


get_page_header
---------------

.. code::

    get_page_header(response)

Parses out page header element (aka ``<h1>`` tag) from response object.

:param response: Response object to pull header from.

:return: Found page header element.


get_page_messages
-----------------

.. code::

    get_page_messages(response)

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

* ``_get_login_user__extra_user_auth_setup()`` - This function is called after
  getting the corresponding User object for authentication LINK HERE, but prior to
  attempting to process the request-response cycle.

  This is critical for projects with additional authentication logic.
  If a project has additional authentication logic to process (such as
  authentication keys or custom Auth backend logic), then it should be done
  here.

  This hook receives only known args/kwargs that are related to user
  authentication and request processing.

* ``_assertResponse__pre_builtin_tests()`` - This function is called after getting
  the page response, but prior to calling any assertion checks on it.

  If a project requires any additional pre-check setup, or should have any
  custom checks to run prior to those built into ETC, then it should be done
  here.

  This hook receives all known args/kwargs that the response assertion receives.

* ``_assertResponse__post_builtin_tests()`` - This function is called after
  getting the page response, and after calling all provided assertion checks
  on it.

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

