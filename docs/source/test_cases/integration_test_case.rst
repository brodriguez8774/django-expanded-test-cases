IntegrationTestCase
*******************


The **IntegrationTestCase** class provides additional wrapper functionality for
checking request/response logic WITHOUT using a browser window instance.

This class is able to quickly test request/response generation, as long as the
view logic does not require interactive elements, such as JavaScript.


.. tip::

   We recommend using this class as the general default, for a majority of
   Django site UnitTests.

   This class is extremely versatile, and strikes a good balance between
   performance and capabilities.

   For the few things this class cannot test (such as JavaScript logic),
   consider using the :ref:`LiveServerTestCase` class.


----


Custom Response Assertions
==========================

The **Response Assertions** are utility assertions that can check for multiple
of the below :ref:`custom element assertions` at once, in a single function
call.


.. note::

   If your project requires additional User authentication setup, in order to
   access pages (such as requiring two-factor), then override the
   ``_extra_user_auth_setup()`` function and add your logic there.

   This ``_extra_user_auth_setup()`` function is an empty hook into
   **Response Assertion** User login logic, that runs in the after the user
   is grabbed, but before the response is rendered.


assertResponse
--------------

.. code::

    assertResponse()

The core **Response Assertion**.

Pulls a response from the provided URL location (either a literal URL, or a
`reverse url <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_
located within the project), and then checks for various attributes.

At minimum, checks that the response ``status_code`` value (after any
redirects) matches the provided ``expected_status`` param.

Only "expected" params that are provided will be checked, with the exception
of ``status_code``, which will assume a default of ``200`` if not provided.

Both ``assertGetResponse()`` and ``assertPostResponse()`` technically call
this.

For clarity, it's recommended to instead call the above
``assertGetResponse()`` or ``assertPostResponse()`` assertions, to make it
explicitly visible what the expected response type is that's being checked.

:param url: The url to grab the response from.
:param get: Bool indicating if response is GET or POST. True means GET.
:param data: Dictionary of values to pass to response, if response is POST.
:param expected_redirect_url: Expected url that response should end at, after
                             any redirections that occur.
:param expected_status: Expected status code response should have, after any
                       redirections.
:param expected_title: Expected response title (``<title>`` tag) response
                      should have.
:param expected_header: Expected page header (``<h1>`` tag) response should
                       have.
:param expected_messages: Expected messages response should contain. Usually
                         generated with the
                         `Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.
:param expected_content: Expected page content response should contain.
:param auto_login: Bool indicating if user should be auto-logged-in, before
                  trying to render response. Useful for verifying behavior
                  of views with login/permission requirements.
:param user: User to log in with, if ``auto_login`` is True. Defaults to
            ``test_user`` if not provided.
:param user_permissions: Optional permissions to provide User, before
                        attempting to render response.
:param user_groups: Optional groups to provide User, before attempting to
                   render response.
:param ignore_content_ordering: Bool indicating if ordering of
                               ``expected_content`` is important or not.
                               Defaults to assuming ordering matters.

:return: The generated response object, in case tests need to run additional
        logic on it.


assertGetResponse
-----------------

.. code::

    assertGetResponse()

A wrapper for above ``assertResponse()``, that has minimal extra logic for
assuming a page is a GET response.

All above params are applicable, except for ``get``.


assertPostResponse
------------------

.. code::

    assertPostResponse()

A wrapper for above ``assertResponse()``, that has minimal extra logic for
assuming a page is a POST response.

All above params are applicable, except for ``get`` and ``data``.


----


Custom Element Assertions
=========================

The **Element Assertions** check for the existence and state of a specific
element within a `Django Response Object
<https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_.

They then each return the verified element, in case further testing is required
that the assertion cannot handle.


assertRedirects
---------------

.. code::

    assertRedirects()

Asserts that a response is redirected to a specific URL.

Most functionality comes from Django's default assertRedirects() function.

However, this adds additional wrapper logic to:
* Check that provided response param is a valid Response object, and attempts
to generate one if not.
* Attempts to grab URL as a
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
                       any redirections.

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

:return: The found response content, in case tests need to run additional
        logic on it.


assertPageHeader
----------------

.. code::

    assertPageHeader()

Asserts that a response has a given page header value. Aka, the ``<h1>`` tag
contents.

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

   It will NOT fail if messages exist in the response, but are not checked.

   For example, if we have a response containing messages of
   ["Message #1", "Message #2", "Message #3"], then the following will check
   for a single message, find it, and then ignore the remaining other two
   messages pass:

   ``self.assertContextMessages(response, 'Message #2')``

   In the future, there will likely be an option to change this behavior, so
   that if there are messages on the page that are NOT checked via the
   ``expected_messages`` param, then the ``assertContextMessages()`` assertion
   will fail.


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

:return Found message elements.
