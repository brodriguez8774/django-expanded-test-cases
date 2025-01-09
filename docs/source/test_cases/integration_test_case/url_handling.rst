IntegrationTestCase - Url Handling
**********************************


The **IntegrationTestCase** class is built to generate page responses from a
given Url, and then test these responses accordingly.

By nature, that means the IntegrationTestCase class has to handle Urls.
At the moment, there are four separate potential Url concepts:

* **Request Url** - This is the url that is provided to a given
  :doc:`Response Assertion<./response_assertions>`
  in order to process a Django request.

* **Response Urls** - To help facilitate test debugging, all responses generated
  with DjangoExpandedTestCases ``assertResponse()`` functions contain
  information on the urls acquired while generating the response.

  This information can be accessed via ``response.url_data``, and has the
  following subsections:

  * ``url_data.provided`` - The url values that were provided for the initial
    request.
    This is not used in any assertions or debug output, and is provided
    exclusively to help provide additional information while debugging tests.

    * ``url_data.provided.url`` - The url string provided for the request.

    * ``url_data.provided.args`` - The url args provided in addition to the base
      url string.
      Exclusively used if treating the url as a
      `Django reverse url <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_.

    * ``url_data.provided.kwargs`` - The url kwargs provided in addition to the
      base url string.
      Exclusively used if treating the url as a
      `Django reverse url <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_.

    * ``url_data.provided.query_params`` - The url parameters to append to the
      generated url.
      For example, the ending part of ``www.my-url.com?test=5``.

  * ``url_data.computed`` - The resulting url values that were found during
    processing of the request.
    These values are used for assertions, but can also provide useful additional
    information while debugging tests.

    * ``url_data.computed.initial_url`` - This is the result of the above
      "Request Url", after all internal url processing has occurred, but
      before any potential redirects.

    * ``url_data.computed.redirect_url`` - This is the result of the above
      "Request Url", after all internal url processing has occurred, including
      after processing any potential redirects.

      If no redirects occurred while processing the response, then this value is
      ``None`` instead.

    * ``url_data.computed.final_url`` - This is the final result of the above
      "Request Url".

      This is technically redundant with the above two url values.
      However, if you want to always have the "final" url, regardless of redirects
      or not, then this is a safe value to use.


----


Assertion Url Processing
========================

The **DjangoExpandedTestCases** package tries to be as robust and flexible as
possible, to fit the needs of any project.

Thus, url processing attempts to be flexible and dynamic.

In the below documentation, all urls can be processed with or without the
fully qualified domain url as a prefix.
The package attempts handle domain values intelligently, so that url handling
does not need domains (as per standard Django testing), but so that urls will
not break if domains are provided for any reason.

If using a domain other than either of the standard ``127.0.0.1`` or
``localhost``, then please set the ``site_root_url`` class variable prior to
running any assertions.


----


Request Url Processing
----------------------

When processing a request in any ``assertResponse`` statement, the request url
is processed in multiple stages:

First, the package attempts to read it as a literal url string.

* For example, if trying to access an endpoint of
  ``www.mysite.com/merchandise/shirts/`` with a url name of
  ``merchandise:shirts``, then the literal url string would be
  ``/merchandise/shirts/``.

If the url fails to resolve successfully as a literal url string, then
the package attempts to resolve the url as a
`Django reverse url <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_.
This includes processing of the ``url_args`` and ``url_kwargs`` values,
if either was provided.
These ``url_args``/``url_kwargs`` function the same as args/kwargs for a Django
reverse url, and should be formatted accordingly.

* For example, if trying to access an endpoint of
  ``www.mysite.com/merchandise/shirts/`` with a url name of
  ``merchandise:shirts``, then the reverse url string would be
  ``merchandise:shirts``.

At this point, any ``url_query_params`` are appended in the traditional format,
and then the actual page response is generated.


----


Expected Url Processing
-----------------------

The ``expected_url`` value is only taken as a literal url.

ETC does not attempt to do any fancy internal processing to the
``expected_url``.
The logic is that it's used for assertions, which should be more
explicit and have less magic going on.

If you want to use things like reverse, you should use built-in Django logic
to calculate the url prior to passing it into the ``assertResponse`` assertion.

For example, something like:

.. code::

    expected_url=reverse("merchandise:shirts")


----


Expected Redirect Url Processing
--------------------------------

For the moment, the ``expected_redirect_url`` DOES NOT follow the same logic
as the other two "expected" values. It instead has the same dynamic processing
as the original "request url".

This directly goes against the logic discussed in ``expected_url``, and honestly
I don't remember why this one was implemented differently.

Fixing this inconsistency is going to be a breaking change, but it probably
needs to be resolved prior to a 1.0 release.

Further discussion and input is welcome at
https://github.com/brodriguez8774/django-expanded-test-cases/issues/22 ,
if anyone has opinions on how to handle this.

Ultimately all three of these "expected" urls should probably be handled the
same.
But for now this one is the odd child out, sorry.


----


Expected Final Url Processing
-----------------------------

Handled effectively the same as ``expected_url``.
See :ref:`test_cases/integration_test_case/url_handling:Expected Url Processing`
