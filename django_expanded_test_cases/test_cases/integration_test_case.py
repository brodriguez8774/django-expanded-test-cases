"""
Testing logic for views and other multi-part components.
"""

# System Imports.
from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

# User Imports.
from .base_test_case import BaseTestCase


class IntegrationTestCase(BaseTestCase):
    """Testing functionality for views and other multi-part components."""

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize url variables.
        cls.login_url = reverse(settings.LOGIN_URL)
        cls._site_root_url = None

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

    def assertResponse(self, url, *args, expected_status=200, **kwargs):
        """Asserts that view response object at given URL matches various parameters.

        :param url: Url to get response object from.
        :param expected_status: Expected status code, after any redirections. Default code of 200.
        """
        # Preprocess all potential url values.
        url = str(url).strip()
        current_site = '127.0.0.1'
        url_args = ()
        url_kwargs = {}

        # Handle site_root_url value.
        if self.site_root_url is not None:
            current_site = self.site_root_url

        # Standardize if literal site url was provided and user included site_root.
        if url.startswith(current_site):
            url = url[len(current_site):]

        # If "args" key or "kwargs" key exists in function kwargs param, assume is meant for url reverse.
        if 'args' in kwargs.keys():
            url_args = kwargs['args']
        if 'kwargs' in kwargs.keys():
            url_kwargs = kwargs['kwargs']

        # Attempt to get reverse of provided url.
        try:
            url = reverse(url, args=url_args, kwargs=url_kwargs)
        except NoReverseMatch:
            # Could not find as reverse. Assume is literal url.
            if len(url) > 0 and url[-1] != '/':
                url += '/'

        # Make sure exactly one slash is prepended to the url value.
        url = url.lstrip('/').rstrip('/')
        if len(url) == 0:
            url = '/'
        else:
            url = '/{0}/'.format(url)

        # Log url we're attempting to access.
        if self.site_root_url is not None:
            current_site = '{0}{1}'.format(self.site_root_url, url)
        else:
            current_site = '127.0.0.1{0}'.format(url)
        self._debug_print('Attempting to access url "{0}"'.format(current_site))

        # Get response object.
        response = self.client.get(url, follow=True)
        response.url = current_site

        # Verify page status code.
        self.assertEqual(
            response.status_code,
            expected_status,
            'Expected status code (after potential redirects) of "{0}". Actual code was "{1}"'.format(
                expected_status,
                response.status_code,
            ),
        )

        # All assertions passed so far. Return response in case user wants to do further checks.
        return response
