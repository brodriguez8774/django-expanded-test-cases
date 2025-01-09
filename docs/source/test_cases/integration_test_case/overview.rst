IntegrationTestCase - Overview
******************************


The **IntegrationTestCase** class provides additional wrapper functionality for
checking request/response logic WITHOUT using a browser window instance.

This class is able to quickly test request/response generation, as long as the
view logic does not require interactive elements, such as JavaScript.
It has the added benefit of providing detailed debug output on assertion
failure, so it's much clearer to see what was returned, vs what was expected.


The primary purpose of this class is to speed up test creation while enabling
more thorough page tests, with less templating and less repeating code.
The idea is that tests themselves should contain only the elements being tested
for, whenever possible.
Any extra templating logic (to acquire specific page elements, etc) only slows
down the creation of actual test writing, and generally reduced readability
of the tests themselves.
Whenever possible, tests should be as direct and at-a-glance legible as can be.


.. tip::

   We recommend using this class as the general default, for a majority of
   Django site UnitTests.

   This class is extremely versatile, and strikes a good balance between
   performance and testing capabilities.

   For the things this class cannot test (such as JavaScript logic),
   consider using the :doc:`../live_server_test_case` class.


----


Overview
========

Implement this by inheriting the ``IntegrationTestCase`` class.
This class can be imported via:

.. code::

    from django_expanded_test_cases import IntegrationTestCase


All of the default
`Django assertions <https://docs.djangoproject.com/en/5.1/topics/testing/tools/#assertions>`_
are available while using this class.
When in doubt, you can always fall back to the testing assertions provided
by the standard Django testing suite.

This class also implements all the assertions and logic contained in the
:doc:`../base_test_case`.


Overview -  Response Assertions
-------------------------------

The main functionality provided by the IntegrationTestCase class are various
:doc:`Response Assertions<./response_assertions>`,
which do a good deal of heavy lifting in
an attempt to make testing easier, more thorough, and faster to write.

These **Response Assertions** are utility functions that can generate a page
response according to provided URL parameters, and then optionally verify one
or more properties within the generated response object.


.. note::

    If your site uses session data, then please also see the section on
    :ref:`configuration/general:Configuring Client State`.


Overview - Element Assertions
-----------------------------

The above **Response Assertions** internally implement a handful of various
**Element Assertions**, which are also exposed for use in writing tests.

These **Element Assertions** each check for a specific page content value,
such as verifying the page title or page header.
All of these checks can be (and certainly have been) done manually in tests
to check for content.

By bundling logic into these **Element Assertions**, the same checks are now
callable as single-line statements, with less templating code to do the same
check.


Overview - Helper Functions
---------------------------

To make all of above work, there are various helper functions,
which are also all exposed to the end-user to help facilitate an enhanced
testing experience.


Overview - Hook Functions
-------------------------

Finally, different projects have different needs, when it comes to testing.

To try to ensure the DjangoExpandedTestCases package fits all projects, there
are "hook" functions provided, which allow the injection of additional logic
during the testing request-response cycle.


----


Response Assertions
===================

**Response Assertions** are the primary functionality provided by the
IntegrationTestCase class.

The available **Response Assertions** are as follows:

* :ref:`test_cases/integration_test_case/response_assertions:assertGetResponse`
  - Follows a Url, gets a GET page response, and then
  optionally checks one or more values to verify expected response.

* :ref:`test_cases/integration_test_case/response_assertions:assertPostResponse`
  - Same as above, but for a POST response.
  Expects to be provided a dictionary of POST data process.

* :ref:`test_cases/integration_test_case/response_assertions:assertJsonResponse`
  - Similar to above assertions, but expects a JSON
  file response, instead of an html response.
  Can optionally take in POST data, but does not need it.

All of these custom response assertions:

* Have :doc:`url handling<./url_handling>`
  for determining and fetching the page response.

* Return the acquired response object, for further testing, examination,
  debugging, if desired.

* Call smaller
  :ref:`test_cases/integration_test_case/overview:Element Assertions`,
  all of which can be invoked separately if desired (see below).


.. tip::

    When using any of these response assertions, we highly recommend providing
    checks to ensure the correct page was fetched.
    Never blindly trust that a url authenticates and resolves to the expected
    page.

    For example, when calling an ``assertGetResponse``, it's a good idea to
    always check the page title (using the ``expected_title`` kwarg), check the
    page header (using the ``expected_header`` kwarg), or check for some
    expected unique section of page content (using the ``expected_content``
    kwarg).

    Once there is some logic to verify the correct page was fetched, only then
    should you test for the actual page logic you want the test to verify.

    If nothing else, this makes it much easier to debug in the future, if
    project authentication changes in a way that leads to some (or all) tests
    to acquire a different page than expected.


----


Element Assertions
==================

The **Element Assertions** check for the existence and state of a specific
element within a `Django Response Object
<https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_.

Each assertion returns the verified element. This ensures the programmer
can easily perform additional testing and debugging, if desired.

Provided assertions are as follows:

* :ref:`test_cases/integration_test_case/other_functionality:assertRedirects`
  - Asserts the request is redirected to a specific URL.

* :ref:`test_cases/integration_test_case/other_functionality:assertStatusCode`
  - Asserts the response contains a given status code value.

* :ref:`test_cases/integration_test_case/other_functionality:assertPageTitle`
  - Asserts the response contains a given title value.
  (Aka, the ``<title>`` tag contents).

* :ref:`test_cases/integration_test_case/other_functionality:assertPageHeader`
  - Asserts the response contains a given page header value
  (Aka, the ``<h1>`` tag contents).

* :ref:`test_cases/integration_test_case/other_functionality:assertContextMessages`
  - Asserts the response contains the given context message values.
  These are usually generated with the
  `Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.

* :ref:`test_cases/integration_test_case/other_functionality:assertNotContextMessages`
  - The negation of above. Asserts the given
  message ARE NOT found in the response.

* :ref:`test_cases/integration_test_case/other_functionality:assertPageContent`
  - Asserts the response contains the given page content html.

  By default, provided values are ordering-sensitive.
  That is, if given values A, B, and C to detect on page, each item must be
  present on the page, AND each item must be found in that order.

* :ref:`test_cases/integration_test_case/other_functionality:assertNotPageContent`
  - The negation of above ``assertPageContent``.
  Asserts the given content html IS NOT found in the response.

  However, ordering is not relevant, since items should not exist to begin with.

* :ref:`test_cases/integration_test_case/other_functionality:assertRepeatingElement`
  - Asserts the response contains the given HTMl
  element, and that it repeats a specified number of times (or more).


All of these **Element Assertions** also return the corresponding page element,
for further testing, examination, debugging, if desired.


----


Helper Functions
================

The IntegrationTestCase class also provides additional helper functions,
to help further speed up the creation of tests.

* :ref:`test_cases/integration_test_case/other_functionality:get_page_title`
  - Parses out the page title element (aka the ``<title>``
  tag) from response object.

* :ref:`test_cases/integration_test_case/other_functionality:get_page_header`
  - Parses out page header element (aka the ``<h1>`` tag) from response object.

* :ref:`test_cases/integration_test_case/other_functionality:get_context_messages`
  - Parses out message elements from response object.
  These are usually generated with the
  `Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.


----


Hook Functions
==============

Finally, the IntegrationTestCase provides "hook" functions to enable additional
setup and configuration for any project, regardless of individual project needs.

We acknowledge that test writing is never a "one size fits all" situation, and
every project is different.
Thus, hook functions provide additional points in which further logic can be
injected.

By default, these functions do nothing on their own and are fully safe to
override.

* ``_get_login_user__extra_user_auth_setup()`` - This function is called after
  getting the
  :doc:`corresponding User object<../../managing_test_users>`
  for authentication, but prior to attempting to process the
  request-response cycle.

* ``_assertResponse__pre_builtin_tests()`` - This function is called after getting
  the page response, but prior to calling any assertion checks on it.

* ``_assertResponse__post_builtin_tests()`` - This function is called after
  getting the page response, and after calling all provided assertion checks
  on it.

For further details on these hook functions, see
:ref:`Hook Function Specs<test_cases/integration_test_case/other_functionality:Hook Functions>`.
