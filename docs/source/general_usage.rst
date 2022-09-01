General Usage
*************

Reminder that the **Django-Expanded-Test-Cases** package is meant to expand the
existing Django
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
class and
`UnitTesting <https://docs.python.org/3/library/unittest.html>`_
logic with some extra functionality.

Below are examples using this in practice:


Functionality Example #1 - Minimal Test
=======================================

In any given web framework, the most common use case is to generate some page
response from a url. So if you wanted a basic test to check that a given
`url reverse <https://docs.djangoproject.com/en/4.0/ref/urlresolvers/#reverse>`_
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
            user = get_user_model().objects.get(username='john1234')
            self.client.force_login(user)
            url = reverse('my-url-reverse-string', args=(url_args,))
            response = self.client.get(url, follow=True)
            content = response.content.decode('utf-8')
            response_header = re.search(r'<h1>([\S\s]+)</h1>', response)
            self.assertEqual('Expected H1 Value', response_header)


Alternatively, using the **Django-Expanded-Test-Cases** package, we can use the
``assertPageHeader()`` function to simplify that same check down to:

.. code:: python

    """Slightly simplified test, using provided assertPageHeader() function."""

    from django.urls import reverse
    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_response_header():
            self.client.force_login(self.get_user('john1234'))
            url = reverse('my-url-reverse-string', args=(url_args,))
            response = self.client.get(url, follow=True)
            self.assertPageHeader(response, 'Expected H1 Value')

As you can see, we were able to eliminate quite a bit of setup. But, we can
then use the ``assertResponse()`` check to simplify this even further:

.. code:: python

    """Extremely simplified test, using provided assertResponse() function."""

    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_response_header():
            self.test_user = self.get_user('john1234')
            self.assertResponse('my-url-reverse-string', url_args, expected_header='Expected H1 Value')


.. note::

    The three above code snippets are effectively equivalent in what they
    accomplish.

As you can see, the **Django-Expanded-Test-Cases** package isn't doing anything
groundbreaking, per say. Yet it makes the same test significantly easier and
faster to write, allowing the developer to focus on the actual meat and bones
of the test, rather than wasting significant time writing repeated code to
simply generate response objects and pull values from them.

Writing tests in such a way will also generally reduce the amount of visual
clutter in a test, resulting in project tests that are generally more
immediately obvious as to exactly what is being tested.


Functionality Example #2 - Ordered Content Check
================================================

This is a more complicated example than above. Here, we:

* Log in with a specific testing user.
* Generate the reverse of a given url string.
* Fetch a response at the url.
* Check the response for a set of page content, expected to be in a specific
  order.

For formatting and readability purposes, this is a single assertion that's
broken into multiple lines.


.. code:: python

    """Ordered page content test, using provided assertGetResponse() function."""

    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_page_contents():
            self.assertGetResponse(
                'my_project:todo-list',
                expected_content=[
                    'TODO List',
                    '<ul>',
                    '<li><p>Wake up</p></li>',
                    '<li><p>Have breakfast</p></li>',
                    '<li><p>Go to work</p></li>',
                    '<li><p>Fix my Django tests</p></li>',
                    '<li><p>Have dinner</p></li>',
                    '</ul>',
                ],
                user='john1234',
            )


Functionality Example #3 - Form Submission Check
================================================

We can also test POST responses, to check that a page handles data submission as
expected. In this example, we:

* Log in with a specific testing user.
* Generate the reverse of a given url string.
* Fetch a response at the url, after providing mock form data as part of a POST
  request.
* Check the rendered page response for:

    * A page title, to ensure we're at the page we expect.
    * A page header, to further ensure we're at the page we expect.
    * Context page messages that we expect to return on form submission success.
    * A few content strings we expect to see on the page.

For formatting and readability purposes, this is a single assertion that's
broken into multiple lines.


.. code:: python

    """Form submission test, using provided assertPostResponse() function."""

    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_form_submission():
            self.assertPostResponse(
                'my_project:survey',
                data={'favorite_color': 1, 'additional_comments': 'I like stuff'}
                expected_title='Home | My Site',
                expected_header='Welcome to my Project Home',
                expected_messages=[
                    'Form submitted!',
                    'We thank you for taking our survey.',
                ],
                expected_content=[
                    'Welcome to our site!',
                    'Please try our products',
                ],
                user='john1234',
            )


Functionality Example #4 - Repeating HTML Element Check
=======================================================

In cases where we expect an html element to repeat a number of times, we can
call the ``assertRepeatingElement()`` function. In this example, we:

* Call the ``assertGetResponse()`` function to initially generate a response.

    * Within this assertion, we only check the page title and header, to verify
    we're loading the page we expect.
    * We save the return value (aka the page content) to a variable.

* Call the ``assertRepeatingElement()`` function, to actually do the work we
want. In this case, we check for a total of 10 <li> elements, within a specific
subsection of page content.


For formatting and readability purposes, this is two separate assertions, with
each one broken into multiple lines.


.. code:: python

    """
    Using the assertRepeatingElement() function to check that multiple instances
    of a given element exist.
    """

    from django_expanded_test_cases import IntegrationTestCase


    class TestProjectViews(IntegrationTestCase):

        def test_response_header():
            page_content = self.assertGetResponse(
                'my_project:lists-page',
                expected_title='My Lists | My Site',
                expected_header='Header for Lists Page',
                user='john1234',
            )
            assertRepeatingElement(
                page_content,
                '<li>',
                10,
                content_starts_after="<h3>John's List</h3>",
                content_ends_before='<footer>',
            )


.. note::
    There are many ways to call/generate the initial response content. We don't
    necessarily have to call any of ETC's ``assertResponse()`` functions here.
    We only do so out of convenience, as it's a quick and easy way to get
    response content output for any given page in our project.


Debug Output Overview
=====================

.. warning::

    While this project can function with ``manage.py test``, the debug output
    functionality will send content to the console on every test, regardless of
    pass or fail, leading to an overwhelming amount of output. Instead, we
    **strongly** recommend that you consider using PyTest to run tests, as
    it tends to handle this debug output better.

    For an explanation of why this is, see our note on
    :doc:`Testing Environments <quickstart>`.


Any testing responses that were generated via the **Django-Expanded-Test-Cases**
assertions and classes can automatically output response debug information, in
an attempt to make it faster to troubleshoot failing tests (This functionality
can be toggled via the ``DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT`` setting. See
:doc:`configuration` for details.)


As result, helpful information is immediately visible in the console, after any
test failure, allowing immediate feedback as to what actually rendered during
the testing assertions. This can make test troubleshooting and cleaning up
take significantly less time, and be overall less cumbersome to troubleshoot
when they inevitably do fail.


Debug Output Example
--------------------

TODO: Give example of debug output.
