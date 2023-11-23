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
   consider using the :doc:`live_server_test_case` class.


----


Custom Response Assertions
==========================

The **Response Assertions** are utility functions that can generate a page
response according to provided URL parameters, and then check for one or more
properties upon the generated response object.

See the below :ref:`test_cases/integration_test_case:custom element assertions` section for further
documentation of the possible individual property assertions.


.. note::

   If your project requires additional User authentication setup, in order to
   access pages (such as requiring two-factor), then override the
   ``_extra_user_auth_setup()`` function and add your logic there.

   This ``_extra_user_auth_setup()`` function is an empty hook into
   **Response Assertion** User login logic, that runs after the user
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

.. note::

    This assertion is the base for two others assertions that are much
    more explicit.
    :ref:`test_cases/integration_test_case:assertGetResponse` and
    :ref:`test_cases/integration_test_case:assertPostResponse`.
    It is recommended that you use these more explicit versions so that your
    test expresses clarity as to what the expected request type should be.

:param url: The url to grab the response from.
:param get: Bool indicating if the response should be created with a GET or POST
           request. True means GET.
:param data: Dictionary of values to pass for request generation, if method is
            POST.
:param expected_status: Expected status code the response should have, after all
                       redirections have completed.
:param expected_redirect_url: Expected url that response should end at, after
                             any redirections have completed.
:param url_args: Values to provide for URL population, in "arg" format.
:param url_kwargs: Values to provide for URL population, in "kwarg" format.
:param redirect_args: Values to provide for URL population, in "arg" format.
:param redirect_kwargs: Values to provide for URL population, in "kwarg" format.
:param expected_title: Expected title (``<title>`` tag) the response should
                      include.
:param expected_header: Expected page header (``<h1>`` tag) response should
                       have.
:param expected_messages: Expected messages that the response should contain.
                         Usually these are generated with the
                         `Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.
:param expected_content: Expected page content that the response should contain.
                         See also ``ignore_content_ordering`` param.
:param expected_not_content: Content that should NOT show up in the page response.
:param auto_login: Bool indicating if user should be auto-logged-in, before
                  trying to render the response. Useful for verifying behavior
                  of views with login/permission requirements.
:param user: User to log in with, if ``auto_login`` is set to True. Defaults to
            ``test_user`` if not provided.
:param user_permissions: Optional permissions to provide to the User before
                        attempting to render the response.
:param user_groups: Optional groups to provide to the User, before attempting to
                   render the response.
:param ignore_content_ordering: Bool indicating if ordering of the
                               ``expected_content`` is important or not.
                               Defaults to assuming that ordering matters.
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

:return: The generated response object, in case tests need to run additional
        logic on it.


assertGetResponse
-----------------

.. code::

    assertGetResponse()

A wrapper for the above ``assertResponse()``, that has minimal extra logic for
ensuring that the response is generated from a GET request.

All above params are applicable, except for ``get`` and ``data``.


assertPostResponse
------------------

.. code::

    assertPostResponse()

A wrapper for the above ``assertResponse()``, that has minimal extra logic for
ensuring that the response is generated from a POST request.

All above params are applicable, except for ``get``.


----


Custom Element Assertions
=========================

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
