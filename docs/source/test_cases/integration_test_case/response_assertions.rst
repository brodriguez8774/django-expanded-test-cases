IntegrationTestCase - Response Assertions
*****************************************


This page documents the specs for **IntegrationTestCase** class functionality.

Specifically, the **Response Assertions**, which make up the bulk of this class.


----


Available Assertions
====================

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

    This assertion is the base for other assertions that are more explicit.
    :ref:`test_cases/integration_test_case/response_assertions:assertGetResponse`,
    :ref:`test_cases/integration_test_case/response_assertions:assertPostResponse`, and
    :ref:`test_cases/integration_test_case/response_assertions:assertJsonResponse`.
    It is recommended that you use these more explicit versions so that your
    test expresses clarity as to what the expected request type should be.

All of these assertions return the generated response object,
in case tests need to run additional logic on it.
Such as further assertions or additional debugging.


assertGetResponse
-----------------

.. code::

    assertGetResponse(*args, **kwargs)

A wrapper for the above ``assertResponse()``, that has minimal extra logic for
ensuring that the response is generated from a GET request.

See below for available parameters.


assertPostResponse
------------------

.. code::

    assertPostResponse(*args, **kwargs)

A wrapper for the above ``assertResponse()``, that has minimal extra logic for
ensuring that the response is generated from a POST request.

See below for available parameters.


assertJsonResponse
------------------

.. code::

    assertJsonResponse(*args, **kwargs)


A wrapper for the above ``assertResponse()``, that has minimal extra logic for
handling a request that returns a JSON object.

Can process as either a GET or POST request.
To process as a POST request provide the `data` attribute (dictionary format).

See below for available parameters.


----


Available Parameters
====================

Due to the functionality that the various ``assertResponse`` functions need to
handle for, there are quite a few possible parameters that can be provided.

Aside from the required `url` arg, all parameters are optional.

Any extra args/kwargs are passed on to the inner
:ref:`test_cases/integration_test_case/other_functionality:Hook Functions`
to allow maximum flexibility and customization.

Otherwise, available parameters are defined below.


----


Request Processing Parameters
-----------------------------

Parameters to allow customization of what view is fetched, and how the initial
request is formed.

Url Generation Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^

Parameters to determine url to use.
See :doc:`url_handling` for further details.

* ``url`` - The only required url.
  This is the url to generate the response with.

* ``url_args`` - Values to provide for URL population, in "arg" format.
  Should be provided in list/tuple/array format.

* ``url_kwargs`` - Values to provide for URL population, in "kwarg" format.
  Should be provided in key->value dictionary format.

* ``url_query_params`` - Query parameters to append to URL during url
  population.
  Should be provided in key->value dictionary format.

General Request Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameters to affect what response is fetched using above url parameters.

* ``get`` - Bool indicating if the response should be created with a GET or
  POST request.
  True means GET.

* ``data`` - Dictionary of values to pass for request generation, if method is
  POST.

* ``secure`` - Bool indicating if request should be retrieved as HTTP or HTTPS.

* ``return_format`` - Format to parse for assertion checks.
  Currently accepted values are ``Html`` for standard webpage.
  ``Json`` for json.

* ``headers`` - Additional test client headers, if any.
  Such as those needed to format a proper Json response.


----


User Processing Parameters
--------------------------

Parameters to allow customization of what user object is used during page
request.

* ``auto_login`` - Bool indicating if user should be auto-logged-in,
  before trying to render the response.
  Useful for verifying behavior of views with login/permission requirements.

  If set to False, then view does not try to authenticate with a new user
  instance, and instead keeps the previously logged in user.
  Which in most instances, will default to
  `Django's Anonymous Django user <https://docs.djangoproject.com/en/5.1/ref/contrib/auth/#anonymoususer-object>`_.

* ``user`` - User to log in with, if ``auto_login`` is set to True.
  Defaults to ``test_user`` if not provided. Also see
  :doc:`package user settings<../../configuration/auth>`
  to customize test user behavior.

* ``user_permissions`` - Optional permissions to provide to the User before
  attempting to render the response.

* ``user_groups`` - Optional groups to provide to the User, before
  attempting to render the response.


----


Assertion Check Parameters
--------------------------

The **Response Assertion** have the ability to, well, assert properties upon
the generated response, and raise errors on failure.

Available assertion parameters are as follows:


Url Assertion Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

* ``expected_url`` - Expected url that response should hit, prior to any
  potential redirections.

* ``expected_redirect_url`` - Expected url that response should end at, after
  any redirections have completed.
  Should be None if no redirects are expected.

* ``redirect_args`` - Values to provide for redirect_url population,
  in "arg" format.
  Used exclusively for processing the **expected_redirect_url** value.
  See :ref:`test_cases/integration_test_case/url_handling:Expected Redirect Url Processing`.

* ``redirect_kwargs`` - Values to provide for redirect_url population,
  in "kwarg" format.
  Used exclusively for processing the **expected_redirect_url** value.
  See :ref:`test_cases/integration_test_case/url_handling:Expected Redirect Url Processing`.

* ``redirect_query_params`` - Query parameters to append to redirect_url
  during url population.
  Used exclusively for processing the **expected_redirect_url** value.
  See :ref:`test_cases/integration_test_case/url_handling:Expected Redirect Url Processing`.

* ``expected_final_url`` - Expected url that response should end at, including
  if any redirects occurred.

* ``view_should_redirect`` - Bool indicating if a redirect was expected or not
  during request handling.
  Leave none if you don't care whether a redirect occurred or not.


Response Assertion Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``expected_status`` - Expected status code the response should have,
  after all redirections have completed.

* ``expected_title`` - Expected title (``<title>`` tag) the response
  should have.

* ``expected_header`` - Expected page header (``<h1>`` tag) response
  should have.

* ``expected_messages`` - Expected messages that the response should contain.
  Usually these are generated with the
  `Django Messages Framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_.

* ``expected_not_messages`` - The negation of `expected_messages`.
  Verifies messages that should NOT be contained within the response.

* ``expected_content`` - Expected page content that the response
  should contain.
  See also ``ignore_content_ordering`` param.

* ``expected_not_content`` - The negation of `expected_content`.
  Verifies content that should NOT show up in the page response.

* ``expected_json`` - Expected JSON content that the response should contain.
  Only applicable to `assertJsonResponse()` assertion.


----


Misc Parameters
---------------

Most of these parameters further customize how assertion checks function.

* ``ignore_content_ordering`` - Bool indicating if ordering of the
  ``expected_content`` is important or not.
  Defaults to True, assuming that ordering matters.
  That is, if all `expected_content`` is found on page, but are not in the
  correct order, then the assertion will still fail.

* ``content_starts_after`` - Optional "upper" html content value to strip
  out of both search space and debug output.
  This value and anything above will be removed.
  If multiple instances exist on page, then the first found instance
  (from top of HTML output) is selected.

* ``content_ends_before`` - Optional "lower" html content value to strip
  out of both search space and debug output.
  This value and anything below will be removed.
  If multiple instances exist on page, then the first found instance
  (from bottom of HTML output) is selected.

* ``debug_logging_level`` - Optionally set a logging level to help reduce
  debug output on test failure.
  Any logging of this level or lower is disabled.
  Note: Adjusting logging only lasts for the duration of the single
  `assertResponse`, and is restored to pior state once the assertion ends.
