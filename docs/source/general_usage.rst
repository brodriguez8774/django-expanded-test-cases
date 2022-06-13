General Usage
*************


Functionality Overview
======================

The `Django Expanded TestCases` library is meant to be a set of utility
classes and functions, which expands upon those defined in Django's default
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
class and UnitTesting logic.

A majority of logic provided in this library amounts to helper wrappers around
sets of commonly used testing statements. So what might normally take 5 or 10
lines of testing logic is condensed down to a single assertion.

For a large project with many thousands of tests, this can add up fast.


Functionality Example
---------------------

For example, if you wanted a basic response test to check that a given
`url reverse <https://docs.djangoproject.com/en/4.0/ref/urlresolvers/#reverse>`_,
renders the expected page, you might need to:

* Log in with a specific testing user, if the url is behind a login wall.
* Generate the reverse of a provided url string.
* Fetch the response that generates at that url.
* Decode and parse the ``response.content`` for some uniquely identifiable
  attribute, such as the <h1> tag.
* Verify the located <h1> tag contents match the expected value.

In standard Python code, this may look roughly like:

.. code:: python

    """Standard test, using Django's base testing functionality."""

    import re
    from django.contrib.auth import get_user_model
    from django.test import TestCase
    from django.urls import reverse


    class TestProjectViews(TestCase):

        def test_response_header():
            user = get_user_model().objects.get(username='john')
            self.client.force_login(user)
            url = reverse('my-url-string', args=(url_args))
            response = self.client.get(url, follow=True)
            content = response.content.decode('utf-8')
            response_header = re.search(r'<h1>([\S\s]+)</h1>', response)
            self.assertEqual('Expected H1 Value', response_header)


Alternatively, using the `Django Expanded TestCases` library, we can use the
``assertHeader()`` function to simplify the same check down to:

.. code:: python

    """Slightly simplified test, using provided assertHeader() function."""

    from django.urls import reverse
    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_response_header():
            self.client.force_login(self.get_user('john'))
            url = reverse('my-url-string', args=(url_args))
            response = self.client.get(url, follow=True)
            self.assertHeader(assertPageHeader, 'Expected H1 Value')

We can then use the ``assertResponse()`` check to simplify even further:

.. code:: python

    """Extremely simplified test, using provided assertResponse() function."""

    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_response_header():
            self.test_user = self.get_user('john')
            self.assertResponse('my-url-string', url_args, expected_header='Expected H1 Value')


The three above code snippets are effectively equivalent in what they
accomplish.

As you can see, the `Django Expanded TestCases` library isn't doing anything
groundbreaking, per say. Yet it makes the same test significantly easier and
faster to write, allowing the developer to focus on the actual meat and bones
of the test, rather than wasting significant time writing repeated code to
simply generate response objects and pull values from them.

Writing tests in such a way will also generally reduce the amount of visual
clutter in a test, resulting in a project tests that are generally more
immediately obvious as to exactly what is being tested.


Debug Output Overview
=====================

.. warning::

    While this project can function with ``manage.py test``, the debug output
    functionality will be effectively unavailable. Instead, we strongly
    recommend considering using PyTest to run project UnitTests.

    See :doc:`quickstart` for details.


Any testing responses that were generated via the `Django Expanded TestCases`
assertions and classes can automatically output response debug information, in
an attempt to make it faster to troubleshoot failing tests (This functionality
can be toggled via the ``DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT`` setting. See
:doc:`configuration` for details.)


As result, helpful information is immediately visible in the console, after any
test failure, allowing immediate feedback as to what actually rendered during
the testing assertions. This can make troubleshooting and cleaning up tests
take significantly less time, and be overall less cumbersome to troubleshoot
when they inevitably do fail.


Debug Output Example
--------------------

TODO: Give example of debug output.