"""
Testing logic for views and other multi-part components.
"""

# System Imports.
import json
import logging
import re
import textwrap
import warnings

# Third-Party Imports.
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseBase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

# Internal Imports.
from .base_test_case import BaseTestCase
from django_expanded_test_cases.constants import (
    ETC_ALLOW_MESSAGE_PARTIALS,
    ETC_ALLOW_TITLE_PARTIALS,
    ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH,
    ETC_DEFAULT_STANDARD_USER_IDENTIFIER,
    ETC_INCLUDE_RESPONSE_DEBUG_URL,
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_RESET_COLOR,
    ETC_REQUEST_USER_STRICTNESS,
    ETC_RESET_CLIENT_STATE_ON_REQUEST,
    ETC_RESPONSE_DEBUG_LOGGING_LEVEL,
    ETC_SKIP_CONTENT_AFTER,
    ETC_SKIP_CONTENT_BEFORE,
    ETC_VIEWS_SHOULD_REDIRECT,
    VOID_ELEMENT_LIST,
)
from django_expanded_test_cases.mixins import ResponseTestCaseMixin


# Initialize logging.
logger = logging.getLogger(__name__)


class ProvidedUrlData:
    """Helper class to hold url data that was input to generate response."""

    def __init__(self, base_url, url_args, url_kwargs, url_query_params):

        # Url value that was initially provided to calulate url.
        self.url = base_url

        # Additional url args that were provided to calculate url.
        self.args = url_args

        # Additional url kwargs that were provided to calculate url.
        self.kwargs = url_kwargs

        # Additional url query params that were provided to calculate url.
        self.query_params = url_query_params


class ComputedUrlData:
    """Helper class to hold url data that was computed during processing of response."""

    # Initial computed url, prior to any redirects and view processing.
    initial_url = None
    full_initial_url = None

    # Final computed url at end of response.
    final_url = None
    full_final_url = None

    # If redirect occurred, url of such.
    redirect_url = None
    full_redirect_url = None


class ResponseUrlData:
    """Helper class to hold and maintain url information, for easier debugging."""

    def __init__(self, base_url, url_args, url_kwargs, url_query_params):

        self.provided = ProvidedUrlData(
            base_url,
            url_args,
            url_kwargs,
            url_query_params,
        )
        self.computed = ComputedUrlData()


class IntegrationTestCase(BaseTestCase, ResponseTestCaseMixin):
    """Testing functionality for views and other multi-part components."""

    def __init__(self, *args, **kwargs):
        # Call parent logic.
        super().__init__(*args, **kwargs)

        # Initialize some check values.
        # Initialize these to true. Then the default implementation of each hook function sets to False.
        # Presumably if at least one hook is implemented, then it will stay True.

        class HookClass:
            auth_setup_is_okay = True
            pre_assert_is_okay = True
            post_assert_is_okay = True

        self.hook_checks = HookClass()

    @classmethod
    def setUpClass(cls, *args, debug_print=None, **kwargs):
        """Test logic setup run at the start of class creation."""

        # Call parent logic.
        return_val = super().setUpClass()

        # Initialize url variables.
        try:
            cls.login_url = reverse(settings.LOGIN_URL)
        except NoReverseMatch:
            # Login url is not defined.
            cls.login_url = None

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    @classmethod
    def setUpTestData(cls, *args, **kwargs):
        """Test logic setup run at the start of class creation, specifically for data setup."""

        # Call parent logic.
        return_val = super().setUpTestData()

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def setUp(self, *args, **kwargs):
        """Test logic setup run at the start of function/method execution."""

        # Call parent logic.
        return_val = super().setUp()

        self._error_displayed = False
        self._reset_client_state_on_request = ETC_RESET_CLIENT_STATE_ON_REQUEST

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def subTest(self, *args, **kwargs):
        """Test logic setup run every time we enter a subtest."""

        # Call parent logic.
        return_val = super().subTest()

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        """Test logic setup run at the end of class execution, as part of termination/clean up."""

        # Call parent logic.
        return_val = super().tearDownClass()

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def tearDown(self, *args, **kwargs):
        """Test logic setup run at the end of function/method execution, as part of termination/clean up."""

        # Call parent logic.
        return_val = super().tearDown()

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    # region Custom Assertions

    def assertResponse(
        self,
        url,
        *args,
        get=True,
        data=None,
        secure=True,
        return_format='html',
        headers=None,
        expected_status=200,
        expected_url=None,
        expected_redirect_url=None,
        expected_final_url=None,
        view_should_redirect=None,
        url_args=None,
        url_kwargs=None,
        url_query_params=None,
        redirect_args=None,
        redirect_kwargs=None,
        redirect_query_params=None,
        expected_title=None,
        expected_header=None,
        expected_messages=None,
        expected_not_messages=None,
        expected_content=None,
        expected_not_content=None,
        expected_json=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        extra_usergen_kwargs=None,
        ignore_content_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        debug_logging_level=None,
        **kwargs,
    ):
        """Verifies the view response object at given URL matches provided parameters.

        At minimum, gets a response object from parsing provided url, then asserts the status code matches.
        Optionally also allows testing:
            * Title - The expected title, aka what displays in the browser tab text at the top of the browser.
            * Header (H1 tag) - The expected H1 header tag on the page.
            * Messages - One or more messages, generated from the Django messages framework.
            * Content - One or more values that should physically appear within html rendering.

        :param url: Url to get response object from.
        :param get: Bool indicating if response is GET or POST. Defaults to GET.
        :param data: Optional dict of items to pass into response generation.
        :param secure: Bool indicating if request should be retrieved as HTTP or HTTPS.
        :param return_format: Format to parse for assertion checks. `Html` for standard webpage. `Json` for json.
        :param headers: Additional test client headers, if any.
        :param expected_url: Expected url, before any redirections.
        :param expected_redirect_url: Expected url, after any redirections.
        :param view_should_redirect: True to make sure view has redirected. False to make sure it didn't. None to skip.
        :param url_args: Values to provide for URL population, in "arg" format.
        :param url_kwargs: Values to provide for URL population, in "kwarg" format.
        :param url_query_params: Query parameter values to provide for URL population.
        :param redirect_args: Values to provide for redirect URL population, in "arg" format.
        :param redirect_kwargs: Values to provide for redirect URL population, in "kwarg" format.
        :param redirect_query_params: Query parameter values to provide for redirect URL population.
        :param expected_status: Expected status code, after any redirections. Default code of 200.
        :param expected_title: Expected page title to verify. Skips title test if left as None.
        :param expected_header: Expected page h1 to verify. Skips header test if left as None.
        :param expected_messages: Expected context messages to verify. Skips message test if left as None.
        :param expected_not_messages: Inverse of expected_messages. Skips test if left as None.
        :param expected_content: Expected page content elements to verify. Skips content test if left as None.
        :param expected_not_content: Inverse of expected_content. Skips test if left as None.
        :param expected_json: If expecting JSON formatted response, then the JSON value to check for.
                              Currently requires the full JSON value. Does not do partials.
        :param auto_login: Bool indicating if user should be auto-logged-in.
        :param user: User to log in with, if auto_login is True. Defaults to `test_user`.
        :param user_permissions: Optional permissions to provide to login user.
        :param user_groups: Optional groups to provide to login user.
        :param extra_usergen_kwargs: Optional dictionary of values to pass to _get_login_user__extra_user_auth_setup().
        :param ignore_content_ordering: Bool indicating if ordering should be verified. Defaults to checking ordering.
        :param content_starts_after: The HTML that expected_content should occur after. This HTML and everything
                                     preceding is stripped out of the "search space" for the expected_content value.
        :param content_ends_before: The HTML that expected_content should occur before. This HTML and everything
                                    following is stripped out of the "search space" for the expected_content value.
        :param debug_logging_level: Optionally set a logging level. Any logging of this level or lower is disabled.
        """

        # Configure logging for this specific assertion run.
        # Can be used to disable logging output for views with many logging statements.
        orig_logging_level = None
        if debug_logging_level or ETC_RESPONSE_DEBUG_LOGGING_LEVEL:
            # Try to use the value passed method, use settings value as fallback.
            logging_level = debug_logging_level or ETC_RESPONSE_DEBUG_LOGGING_LEVEL
            orig_logging_level = logging.getLevelName(logging.root.level)

            # Set logging level, which configures logging to only show messages of set level or higher.
            # If CRITICAL is provided, then all logging is effectively disabled.
            # If NOTSET is provided, then all logging is effectively enabled.
            logging.disable(getattr(logging, logging_level))

        # Handle mutable data defaults.
        data = data or {}
        headers = headers or {}
        url_args = (*kwargs.pop('args', []), *(url_args or []))
        url_query_params = url_query_params or {}
        redirect_args = (*(redirect_args or []),)
        redirect_kwargs = {
            **(redirect_kwargs or {}),
        }
        redirect_query_params = redirect_query_params or {}
        url_kwargs = {**kwargs.pop('kwargs', {}), **(url_kwargs or {})}
        extra_usergen_kwargs = extra_usergen_kwargs or {}

        # Sanitize required values.
        return_format = str(return_format).lower().strip()
        if return_format not in ['html', 'json']:
            raise ValueError(
                'Invalid return_format arg. Currently supported return_format values are `html` or `json`.'
            )

        if self._reset_client_state_on_request:
            # Reset client "user login" state for new response generation.
            # Note that this also clears out the current session.
            # If wanting to retain session across requests, then this should be set to False first.
            self.client.logout()

        # Handle getting user.
        user = self._get_default_request_user(user, auto_login)

        # Run logic to get corresponding response object.
        response = self._get_page_response(
            url,
            get=get,
            data=data,
            secure=secure,
            headers=headers,
            url_args=url_args,
            url_kwargs=url_kwargs,
            query_params=url_query_params,
            auto_login=auto_login,
            user=user,
            user_permissions=user_permissions,
            user_groups=user_groups,
            extra_usergen_kwargs=extra_usergen_kwargs,
        )

        # If response is json format, then save actual python-i-fied json data to response as well.
        # Note: Django seems to have built-in processing for `response.content`, so we have to save to
        #   a different variable. This has the added benefit that tests can see what the original json output was,
        #   as well as the python-i-fied version.
        if return_format == 'json':
            response.json_content = json.loads(response.content.decode('utf-8'))
        else:
            # Handle for any return format that is NOT json.
            if expected_json is not None:
                raise ValueError(
                    'Assertion was not expecting a JSON return object, yet expected_json arg was provided. '
                    'Either provide a return_format arg of `json`, or consider using the assertJsonResponse assertion.'
                )

        # Optionally output all debug info for found response.
        if self._debug_print_bool:
            if return_format == 'json':
                # Extra args for json debug output handling.
                self.full_debug_print(
                    response,
                    return_format=return_format,
                    post_data=data,
                    expected_json=expected_json,
                )
            else:
                # Standard debug output handling.
                self.full_debug_print(response, return_format=return_format, post_data=data)

        # Optional hook for running custom pre-builtin-test logic.
        self._assertResponse__pre_builtin_tests(
            url,
            *args,
            response=response,
            get=get,
            data=data,
            secure=secure,
            return_format=return_format,
            headers=headers,
            expected_status=expected_status,
            expected_url=expected_url,
            expected_redirect_url=expected_redirect_url,
            view_should_redirect=view_should_redirect,
            url_args=url_args,
            url_kwargs=url_kwargs,
            url_query_params=url_query_params,
            redirect_args=redirect_args,
            redirect_kwargs=redirect_kwargs,
            redirect_query_params=redirect_query_params,
            expected_title=expected_title,
            expected_header=expected_header,
            expected_messages=expected_messages,
            expected_not_messages=expected_not_messages,
            expected_content=expected_content,
            expected_not_content=expected_not_content,
            auto_login=auto_login,
            user=user,
            user_permissions=user_permissions,
            user_groups=user_groups,
            extra_usergen_kwargs=extra_usergen_kwargs,
            ignore_content_ordering=ignore_content_ordering,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
            debug_logging_level=None,
            **kwargs,
        )

        # Verify page status code.
        self.assertStatusCode(response, expected_status)

        # Verify initial url.
        # TODO: Inconsistent expected_x_url handling.
        #  See project issue 22 (https://github.com/brodriguez8774/django-expanded-test-cases/issues/22).
        if expected_url is not None and response.url_data.computed.initial_url != expected_url:
            self.fail(
                (
                    'Expected Url and actual Url do not match. \n'
                    'Expected Url: \n'
                    '"{0}" \n'
                    'Actual Url: \n'
                    '"{1}" \n'
                ).format(
                    expected_url,
                    response.url_data.computed.initial_url,
                )
            )

        # Verify if redirecting or not. Is a general assertion to verify a redirect happened,
        # if the user perhaps does not care about further details of the redirect.
        #
        # Set to True to make sure view redirected (accomplishes similar to above expected_redirect_url) logic.
        # Set to False to make sure view did NOT redirect.
        # Leave None to skip this assertion.
        if view_should_redirect is None:
            # No value provided for this assertion. Fall back to settings value.
            view_should_redirect = ETC_VIEWS_SHOULD_REDIRECT
        if view_should_redirect is not None and not (
            bool(response.url_data.computed.redirect_url) == view_should_redirect
        ):
            if view_should_redirect:
                self.fail('Expected a page redirect, but response did not redirect.')
            else:
                self.fail('Expected no page redirects, but response processed one or more redirects.')

        # Verify final url.
        # TODO: Inconsistent expected_x_url handling.
        #  See project issue 22 (https://github.com/brodriguez8774/django-expanded-test-cases/issues/22).
        if expected_final_url is not None and response.url_data.computed.final_url != expected_final_url:
            self.fail(
                (
                    'Expected final_url and actual final_url do not match. \n'
                    'Expected final_url: \n'
                    '"{0}" \n'
                    'Actual final_url: \n'
                    '"{1}" \n'
                ).format(
                    expected_final_url,
                    response.url_data.computed.final_url,
                )
            )

        # Verify page redirect.
        # This is more specific than the above "view_should_redirect" assertion, so intentionally done second.
        # TODO: Inconsistent expected_x_url handling.
        #  See project issue 22 (https://github.com/brodriguez8774/django-expanded-test-cases/issues/22).
        if expected_redirect_url is not None:
            self.assertRedirects(
                response,
                expected_redirect_url,
                redirect_args=redirect_args,
                redirect_kwargs=redirect_kwargs,
                redirect_query_params=redirect_query_params,
            )

        # Verify page title.
        if expected_title is not None:
            self.assertPageTitle(response, expected_title)

        # Verify page header.
        if expected_header is not None:
            self.assertPageHeader(response, expected_header)

        # Verify page messages.
        if expected_messages is not None:
            self.assertContextMessages(response, expected_messages, debug_output=False)

        if expected_not_messages is not None:
            self.assertNotContextMessages(response, expected_not_messages, debug_output=False)

        # Verify page content.
        if expected_content is not None:
            self.assertPageContent(
                response,
                expected_content,
                ignore_ordering=ignore_content_ordering,
                content_starts_after=content_starts_after,
                content_ends_before=content_ends_before,
                debug_output=False,
            )

        if expected_not_content is not None:
            self.assertNotPageContent(
                response,
                expected_not_content,
                debug_output=True,
                # debug_output=False,
            )

        if expected_json is not None:
            if expected_json != response.json_content:
                self.fail(
                    'Could not find expected json value in response. Provided value was:\n{0}'.format(
                        expected_json,
                    )
                )

        # Optional hook for running custom post-builtin-test logic.
        self._assertResponse__post_builtin_tests(
            url,
            *args,
            response=response,
            get=get,
            data=data,
            secure=secure,
            headers=headers,
            return_format=return_format,
            expected_status=expected_status,
            expected_url=expected_url,
            expected_redirect_url=expected_redirect_url,
            view_should_redirect=view_should_redirect,
            url_args=url_args,
            url_kwargs=url_kwargs,
            url_query_params=url_query_params,
            redirect_args=redirect_args,
            redirect_kwargs=redirect_kwargs,
            redirect_query_params=redirect_query_params,
            expected_title=expected_title,
            expected_header=expected_header,
            expected_messages=expected_messages,
            expected_not_messages=expected_not_messages,
            expected_content=expected_content,
            expected_not_content=expected_not_content,
            auto_login=auto_login,
            user=user,
            user_permissions=user_permissions,
            user_groups=user_groups,
            extra_usergen_kwargs=extra_usergen_kwargs,
            ignore_content_ordering=ignore_content_ordering,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
            debug_logging_level=None,
            **kwargs,
        )

        # Reset logging level for post-assertion, if it was set earlier.
        if orig_logging_level:
            logging.disable(getattr(logging, orig_logging_level))

        # Handle potential warning if no hook functions have been implemented.
        self._hook_function_warning_check(user, *args, **kwargs)

        # All assertions passed so far. Return response in case user wants to do further checks.
        return response

    def assertGetResponse(
        self,
        url,
        *args,
        data=None,
        secure=True,
        headers=None,
        expected_status=200,
        expected_url=None,
        expected_redirect_url=None,
        expected_final_url=None,
        view_should_redirect=None,
        url_args=None,
        url_kwargs=None,
        url_query_params=None,
        redirect_args=None,
        redirect_kwargs=None,
        redirect_query_params=None,
        expected_title=None,
        expected_header=None,
        expected_messages=None,
        expected_not_messages=None,
        expected_content=None,
        expected_not_content=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        extra_usergen_kwargs=None,
        ignore_content_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        debug_logging_level=None,
        **kwargs,
    ):
        """Verifies a GET response was found at given URL, and matches provided parameters."""

        # Handle mutable data defaults.
        data = data or {}
        headers = headers or {}
        url_args = url_args or []
        url_kwargs = url_kwargs or {}
        url_query_params = url_query_params or []
        redirect_args = redirect_args or []
        redirect_kwargs = redirect_kwargs or {}
        redirect_query_params = redirect_query_params or {}
        extra_usergen_kwargs = extra_usergen_kwargs or {}

        # Call base function to handle actual logic.
        return self.assertResponse(
            url,
            *args,
            get=True,
            data=data,
            secure=secure,
            headers=headers,
            expected_status=expected_status,
            expected_url=expected_url,
            expected_redirect_url=expected_redirect_url,
            expected_final_url=expected_final_url,
            view_should_redirect=view_should_redirect,
            url_args=url_args,
            url_kwargs=url_kwargs,
            url_query_params=url_query_params,
            redirect_args=redirect_args,
            redirect_kwargs=redirect_kwargs,
            redirect_query_params=redirect_query_params,
            expected_title=expected_title,
            expected_header=expected_header,
            expected_messages=expected_messages,
            expected_not_messages=expected_not_messages,
            expected_content=expected_content,
            expected_not_content=expected_not_content,
            expected_json=None,
            auto_login=auto_login,
            user=user,
            user_permissions=user_permissions,
            user_groups=user_groups,
            extra_usergen_kwargs=extra_usergen_kwargs,
            ignore_content_ordering=ignore_content_ordering,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
            debug_logging_level=debug_logging_level,
            **kwargs,
        )

    def assertPostResponse(
        self,
        url,
        *args,
        data=None,
        secure=True,
        headers=None,
        expected_status=200,
        expected_url=None,
        expected_redirect_url=None,
        expected_final_url=None,
        view_should_redirect=None,
        url_args=None,
        url_kwargs=None,
        url_query_params=None,
        redirect_args=None,
        redirect_kwargs=None,
        redirect_query_params=None,
        expected_title=None,
        expected_header=None,
        expected_messages=None,
        expected_not_messages=None,
        expected_content=None,
        expected_not_content=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        extra_usergen_kwargs=None,
        ignore_content_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        debug_logging_level=None,
        **kwargs,
    ):
        """Verifies a GET response was found at given URL, and matches provided parameters."""

        # Handle mutable data defaults.
        data = data or {}
        headers = headers or {}
        url_args = url_args or []
        url_kwargs = url_kwargs or {}
        url_query_params = url_query_params or {}
        redirect_args = redirect_args or []
        redirect_kwargs = redirect_kwargs or {}
        redirect_query_params = redirect_query_params or {}
        extra_usergen_kwargs = extra_usergen_kwargs or {}

        # Forcibly add values to "data" dict, so that POST doesn't validate to empty in view.
        # This guarantees that view serves as POST, like this specific assertion expects.
        if data == {}:
            # Has no values. Forcibly add a single key-value pair.
            data = {'UnitTest': True}

        # Call base function to handle actual logic.
        return self.assertResponse(
            url,
            *args,
            get=False,
            data=data,
            secure=secure,
            headers=headers,
            expected_status=expected_status,
            expected_url=expected_url,
            expected_redirect_url=expected_redirect_url,
            expected_final_url=expected_final_url,
            view_should_redirect=view_should_redirect,
            url_args=url_args,
            url_kwargs=url_kwargs,
            url_query_params=url_query_params,
            redirect_args=redirect_args,
            redirect_kwargs=redirect_kwargs,
            redirect_query_params=redirect_query_params,
            expected_title=expected_title,
            expected_header=expected_header,
            expected_messages=expected_messages,
            expected_not_messages=expected_not_messages,
            expected_content=expected_content,
            expected_not_content=expected_not_content,
            expected_json=None,
            auto_login=auto_login,
            user=user,
            user_permissions=user_permissions,
            user_groups=user_groups,
            extra_usergen_kwargs=extra_usergen_kwargs,
            ignore_content_ordering=ignore_content_ordering,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
            debug_logging_level=debug_logging_level,
            **kwargs,
        )

    def assertJsonResponse(
        self,
        url,
        *args,
        get=None,
        data=None,
        secure=True,
        return_format='json',
        headers=None,
        expected_status=200,
        expected_url=None,
        expected_redirect_url=None,
        expected_final_url=None,
        view_should_redirect=None,
        url_args=None,
        url_kwargs=None,
        url_query_params=None,
        redirect_args=None,
        redirect_kwargs=None,
        redirect_query_params=None,
        expected_title=None,
        expected_messages=None,
        expected_not_messages=None,
        expected_content=None,
        expected_not_content=None,
        expected_json=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        extra_usergen_kwargs=None,
        ignore_content_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        debug_logging_level=None,
        **kwargs,
    ):
        """Verifies a JSON response was found at given URL, and matches provided parameters."""

        # Handle mutable data defaults.
        data = data or {}
        headers = headers or {}
        url_args = url_args or []
        url_kwargs = url_kwargs or {}
        url_query_params = url_query_params or {}
        redirect_args = redirect_args or []
        redirect_kwargs = redirect_kwargs or {}
        redirect_query_params = redirect_query_params or {}
        extra_usergen_kwargs = extra_usergen_kwargs or {}

        # Forcibly add values to "headers" dict, so that we indicate it's a JSON request as per world web standards.
        # NOTE: This logic will only define the corresponding header values if they are not already defined.
        #       If they are defined, then the user provided value takes priority.
        content_type_header_defined = False
        accept_header_defined = False
        try:
            # Reminder: `Content-Type` indicates the format of the request sent from the client to the server.
            #   A value of `application/json` indicates that it should be interpreted as a JsonRequest.
            content_type_header = str(headers['Content-Type']).strip()
            if content_type_header != '':
                content_type_header_defined = True
        except KeyError:
            # Not defined. Prevent error and continue.
            pass

        try:
            # Reminder: `Accept` indicates the format of the response that is expected by the client.
            #   A value of `application/json` indicates that it sent as a JsonRequest.
            accept_header = str(headers['Accept']).strip()
            if accept_header != '':
                accept_header_defined = True
        except KeyError:
            # Not defined. Prevent error and continue.
            pass

        if not content_type_header_defined:
            headers['Content-Type'] = 'application/json'
        if not accept_header_defined:
            headers['Accept'] = 'application/json'

        # Handle if GET or POST.
        if get is not None:
            # `get` explicitly provided. Use that.
            pass
        else:
            # `get` not explicitly provided. Determine from `data` arg.
            if data:
                # Has data. Assume POST response.
                get = False
            else:
                # No data. Assume GET response.
                get = True

        # Call base function to handle actual logic.
        return self.assertResponse(
            url,
            *args,
            get=get,
            data=data,
            secure=secure,
            headers=headers,
            return_format=return_format,
            expected_status=expected_status,
            expected_url=expected_url,
            expected_redirect_url=expected_redirect_url,
            expected_final_url=expected_final_url,
            view_should_redirect=view_should_redirect,
            url_args=url_args,
            url_kwargs=url_kwargs,
            url_query_params=url_query_params,
            redirect_args=redirect_args,
            redirect_kwargs=redirect_kwargs,
            redirect_query_params=redirect_query_params,
            expected_title=expected_title,
            expected_header=None,
            expected_messages=expected_messages,
            expected_not_messages=expected_not_messages,
            expected_content=expected_content,
            expected_not_content=expected_not_content,
            expected_json=expected_json,
            auto_login=auto_login,
            user=user,
            user_permissions=user_permissions,
            user_groups=user_groups,
            extra_usergen_kwargs=extra_usergen_kwargs,
            ignore_content_ordering=ignore_content_ordering,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
            debug_logging_level=debug_logging_level,
            **kwargs,
        )

    def assertRedirects(
        self,
        response,
        expected_redirect_url,
        *args,
        redirect_args=None,
        redirect_kwargs=None,
        redirect_query_params=None,
        **kwargs,
    ):
        """Assert that a response redirected to a specific URL and that the redirect URL can be loaded.

        Most functionality is in the default Django assertRedirects() function.
        However, this acts as a wrapper to also:
            * Check that provided response param is a valid Response object. Attempts to generate one if not.
            * Attempt url as reverse, before trying assertion.
        """
        # Handle mutable data defaults.
        redirect_args = redirect_args or []
        redirect_kwargs = redirect_kwargs or {}
        redirect_query_params = redirect_query_params or {}

        # Ensure provided response is actual response.
        if isinstance(response, HttpResponseBase):
            # Is literal response.
            pass
        else:
            # Is not response. Attempt to get.
            response = self._get_page_response(response)

        # Sanitize redirect url.
        expected_redirect_url = self.standardize_url(
            expected_redirect_url,
            url_args=redirect_args,
            url_kwargs=redirect_kwargs,
            url_query_params=redirect_query_params,
            append_root=False,
        )

        # Run assertion on provided value.
        try:
            return super().assertRedirects(response, expected_redirect_url, *args, **kwargs)
        except AssertionError as err:
            err_str = str(err)

            if (
                # Comment to prevent "black" formatting.
                "expected" in err_str
                and "to equal" in err_str
            ):
                self.fail(
                    (
                        # Comment to prevent "black" formatting.
                        'Response expected_redirect_url didn\'t match. '
                        'Expected url was "{0}". Actual url was "{1}".'
                    ).format(
                        expected_redirect_url,
                        response.url_data.computed.redirect_url,
                    )
                )
            else:
                self.fail(
                    'Response didn\'t redirect as expected. Response code was {0} (expected 302).'.format(
                        response.status_code
                    )
                )

    def assertStatusCode(self, response, expected_status):
        """Verifies the page status code value.

        :param response: Response object to check against.
        :param expected_status: Expected status code, after any redirections.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            actual_status = response.status_code
        else:
            actual_status = int(response)

        # Check status.
        self.assertEqual(
            actual_status,
            expected_status,
            'Expected status code (after potential redirects) of "{0}". Actual code was "{1}".'.format(
                expected_status,
                actual_status,
            ),
        )

        # Return status in case user wants to run additional logic on it.
        return actual_status

    def assertPageTitle(self, response, expected_title, allow_partials=None):
        """Verifies the page title HTML element.

        Note: Some sites have titles with nested elements.
            Ex: "<title><page> | <app> | <website></title>"

        Thus the "exact_match" bool exists, to allow only testing for a specific unit in the title, instead of
        always having to type the full title for every test.

        :param response: Response object to check against.
        :param expected_title: Expected full string in title HTML element.
        :param allow_partials: Bool indicating if title should be exact match, or partial.
        :return: Parsed out title string.
        """
        # Parse out settings values.
        if allow_partials is None:
            allow_partials = ETC_ALLOW_TITLE_PARTIALS
        else:
            allow_partials = bool(allow_partials)

        # Parse out title element from response.
        actual_title = self.get_page_title(response)

        # Remove title tag from expected value, if present.
        expected_title = str(expected_title).strip()
        if expected_title.startswith('<title>'):
            expected_title = expected_title[7:]
        if expected_title.endswith('</title>'):
            expected_title = expected_title[:-8]
        expected_title = expected_title.strip()

        # Check element.
        err_msg = 'Expected title HTML contents of "{0}" ({1}). Actual value was "{2}".'
        if not allow_partials:
            # Check using exact match.
            if expected_title != actual_title:
                self.fail(
                    err_msg.format(
                        expected_title,
                        'using exact matching',
                        actual_title,
                    )
                )
        else:
            # Check using partial match.
            if expected_title not in actual_title:
                self.fail(
                    err_msg.format(
                        expected_title,
                        'using partial matching',
                        actual_title,
                    )
                )

        # Return title in case user wants to run additional logic on it.
        return actual_title

    def assertPageHeader(self, response, expected_header):
        """Verifies the page H1 header HTML element.

        :param response: Response object to check against.
        :param expected_header: Expected full string in H1 header HTML element.
        :return: Parsed out header string.
        """
        # Parse out H1 header element from response.
        actual_header = self.get_page_header(response)

        # Remove H1 tag from expected value, if present.
        expected_header = str(expected_header).strip()
        if expected_header.startswith('<h1>'):
            expected_header = expected_header[4:]
        if expected_header.endswith('</h1>'):
            expected_header = expected_header[:-5]
        expected_header = expected_header.strip()

        # Check element.
        if expected_header != actual_header:
            self.fail(
                'Expected H1 header HTML contents of "{0}". Actual value was "{1}".'.format(
                    expected_header,
                    actual_header,
                )
            )

        # Return header in case user wants to run additional logic on it.
        return actual_header

    def assertContextMessages(self, response, expected_messages, allow_partials=None, debug_output=True):
        """Verifies the context messages.

        :param response: Response object to check against.
        :param expected_messages: Expected message(s) to be found in response.
        :param allow_partials: Bool indicating if messages should fully match or allow partial matches.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out header string.
        """
        if debug_output:
            # Print out actual messages, for debug output.
            self.show_debug_messages(response)

        # Parse out settings values.
        if allow_partials is None:
            allow_partials = ETC_ALLOW_MESSAGE_PARTIALS
        else:
            allow_partials = bool(allow_partials)

        # Parse out message data from response.
        actual_messages = self.get_context_messages(response)

        # Check format of expected value.
        if isinstance(expected_messages, list) or isinstance(expected_messages, tuple):
            # Array of messages passed. Verify each inner value is a str.
            temp_messages = []
            for message in expected_messages:
                message = str(message).strip()
                if len(message) > 0:
                    temp_messages.append(message)
            expected_messages = temp_messages

        elif expected_messages is None:
            # Handle for none type. Not sure why anyone would pass this into the test though.
            expected_messages = []

        elif isinstance(expected_messages, str):
            # For everything else, assume is intended to be a single message.
            message = str(expected_messages).strip()
            expected_messages = []
            if len(message) > 0:
                expected_messages.append(message)

        if len(expected_messages) > 0:
            # For now, we only care about values passed for expected_messages.
            # We ignore any cases where a message exists in the context, but is not explicitly
            # checked by the user in the expected_messages param.

            # One or more messages are expected. Verify they are found.
            for expected_message in expected_messages:
                message_found = False

                # Handle based on partials allowed or not.
                if allow_partials:
                    # Partial message matching is allowed.
                    # Expected value must match or be a substring of a message in context.
                    index = 0
                    while message_found is False and index < len(actual_messages):
                        if expected_message in actual_messages[index]:
                            message_found = True
                        index += 1

                else:
                    # Partial message matching is NOT allowed.
                    # Expected value must exactly match message in context.

                    # Loop through all context messages until found, or all are checked.
                    if expected_message in actual_messages:
                        message_found = True

                # Raise assertion error if not found.
                if not message_found:
                    self.fail(
                        'Failed to find message "{0}" in context (using {1} matching).'.format(
                            expected_message,
                            'partial' if allow_partials else 'exact',
                        )
                    )

    def assertNotContextMessages(self, response, expected_not_messages, allow_partials=None, debug_output=True):
        """Verifies the non-existence context messages.

        :param response: Response object to check against.
        :param expected_not_messages: Expected message(s) to not be present in response.
        :param allow_partials: Bool indicating if messages should fully match or allow partial matches.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out header string.
        """

        if debug_output:
            # Print out actual messages, for debug output.
            self.show_debug_messages(response)

        # Parse out settings values.
        if allow_partials is None:
            allow_partials = ETC_ALLOW_MESSAGE_PARTIALS
        else:
            allow_partials = bool(allow_partials)

        # Parse out message data from response.
        actual_messages = self.get_context_messages(response)

        # Check format of expected value.
        if isinstance(expected_not_messages, list) or isinstance(expected_not_messages, tuple):
            # Array of messages passed. Verify each inner value is a str.
            temp_messages = []
            for message in expected_not_messages:
                message = str(message).strip()
                if len(message) > 0:
                    temp_messages.append(message)
            expected_not_messages = temp_messages

        elif expected_not_messages is None:
            # Handle for none type. Not sure why anyone would pass this into the test though.
            expected_not_messages = []

        elif isinstance(expected_not_messages, str):
            # For everything else, assume is intended to be a single message.
            message = str(expected_not_messages).strip()
            expected_not_messages = []
            if len(message) > 0:
                expected_not_messages.append(message)

        if len(expected_not_messages) > 0:
            # One or more messages are expected to not be present. Verify they do not exist.
            for expected_not_message in expected_not_messages:
                message_found = False

                # Handle based on partials allowed or not.
                if allow_partials:
                    # Partial message matching is allowed.
                    # Expected value must match or be a substring of a message in context.
                    index = 0
                    while message_found is False and index < len(actual_messages):
                        if expected_not_message in actual_messages[index]:
                            message_found = True
                        index += 1

                else:
                    # Partial message matching is NOT allowed.
                    # Expected value must exactly match message in context.

                    # Loop through all context messages until found, or all are checked.
                    if expected_not_message in actual_messages:
                        message_found = True

                # Raise assertion error if found.
                if message_found:
                    self.fail(
                        'Expected to not find message. Found message "{0}" in context (using {1} matching).'.format(
                            expected_not_message,
                            'partial' if allow_partials else 'exact',
                        )
                    )

    def assertPageContent(
        self,
        response,
        expected_content,
        ignore_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        debug_output=True,
    ):
        """Verifies the page content html, similar to the built-in assertContains() function.
        The main difference is that Django templating may create large amounts of whitespace in response html,
        often in places where we wouldn't intuitively expect it, when running tests.
        Technically, the built-in assertHTMLEqual() and assertInHTML() functions exist, and probably could accomplish
        the same assertions. But we still need to parse and format full response object, to display for test failure
        debugging. So I'm not sure if it's helpful at that point to use those or use separate assertions like here.
        Perhaps examine more closely at a later date.

        :param response: Response object to check against.
        :param expected_content: Expected full string (or set of strings) of HTML content.
        :param ignore_ordering: Bool indicating if ordering should be verified. Defaults to checking ordering.
        :param content_starts_after: The HTML that expected_content should occur after. This HTML and everything
                                     preceding is stripped out of the "search space" for the expected_content value.
        :param content_ends_before: The HTML that expected_content should occur before. This HTML and everything
                                    following is stripped out of the "search space" for the expected_content value.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out and formatted content string.
        """
        if debug_output:
            # Print out actual response content, for debug output.
            self.show_debug_content(response)

        main_err_msg = (
            # To prevent Black single-lining this.
            'Could not find expected content value in response. Provided value was:\n'
            '{0}\n'
        )
        checked_content_str_addon = (
            # To prevent Black single-lining this.
            '\n'
            '\n'
            'Surrounding Checks:\n'
            '{0}'
            '{1}'
            '{2}'
        )
        ordering_err_msg = 'Expected content value was found, but ordering of values do not match. Problem value:\n{0}'
        casing_err_msg = (
            'Expected content value was found, but letter capitalization did not match. Expected was:\n'
            '{0}\n'
            '\n'
            'Found was:\n'
            '... {1} ...'
        )

        # Handle settings values for content_starts_before/content_starts_after.
        # TODO: Naming for these is gross, ugh. Must be a better way.
        if content_starts_after is None and ETC_SKIP_CONTENT_BEFORE:
            content_starts_after = ETC_SKIP_CONTENT_BEFORE
        if content_ends_before is None and ETC_SKIP_CONTENT_AFTER:
            content_ends_before = ETC_SKIP_CONTENT_AFTER

        # Extra setup logic, to sanitize and handle if content_starts_after/content_ends_before variables are defined.
        content_dict = self._trim_response_content(
            response,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
        )
        sanitized_original_content = content_dict['minimized_content']
        trimmed_original_content = content_dict['truncated_content']

        # Handle possible types.
        if expected_content is None:
            expected_content = ''
        if isinstance(expected_content, list) or isinstance(expected_content, tuple):
            # The expected_content param is an array of items. Verify they all exist on page.
            trimmed_content = trimmed_original_content
            for index in range(len(expected_content)):
                expected = expected_content[index]

                if len(expected_content) > 1:
                    # Update str in event of error.
                    before_debug_output = ''
                    before_debug_output_statements = ''
                    after_debug_output = ''
                    after_debug_output_statements = ''

                    # Handle "before" output.
                    if ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH > 0:
                        before_debug_output = '{0}Content Checks Before:{1}\n'.format(
                            ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                            ETC_OUTPUT_RESET_COLOR,
                        )

                        for surrounding_check_index in reversed(
                            range(ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH + 1)
                        ):
                            if surrounding_check_index == 0:
                                continue

                            before_debug_output_statements += (
                                '{1}    * {0}{2}\n'.format(
                                    expected_content[index - surrounding_check_index],
                                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                                    ETC_OUTPUT_RESET_COLOR,
                                )
                                if 0 < ((index + 1) - surrounding_check_index) < len(expected_content)
                                else ''
                            )

                        if before_debug_output_statements != '':
                            before_debug_output += before_debug_output_statements
                        else:
                            before_debug_output = ''

                    # Handle "after" output.
                    if ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH > 0:
                        after_debug_output = '{0}Content Checks After:{1}\n'.format(
                            ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                            ETC_OUTPUT_RESET_COLOR,
                        )

                        for surrounding_check_index in range(ETC_ASSERT_CONTENT__SURROUNDING_CHECK_OUTPUT_LENGTH + 1):
                            if surrounding_check_index == 0:
                                continue

                            after_debug_output_statements += (
                                '{1}    * {0}{2}\n'.format(
                                    expected_content[index + surrounding_check_index],
                                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                                    ETC_OUTPUT_RESET_COLOR,
                                )
                                if (len(expected_content) - index) > surrounding_check_index
                                else ''
                            )

                        if after_debug_output_statements != '':
                            after_debug_output += after_debug_output_statements
                        else:
                            after_debug_output = ''

                    updated_checked_content_str_addon = checked_content_str_addon.format(
                        before_debug_output,
                        ('{1}Failed Check:{2}\n' '{1}  > * {0}{2}\n').format(
                            expected_content[index],
                            ETC_OUTPUT_ERROR_COLOR,
                            ETC_OUTPUT_RESET_COLOR,
                        ),
                        after_debug_output,
                    )

                else:
                    updated_checked_content_str_addon = ''

                # Handle if expected is a list or tuple.
                additional_error_info = ''
                if (isinstance(expected, list) or isinstance(expected, tuple)) and len(expected) == 2:
                    # Nested array or tuple.
                    # Assuming first value is the value to check for, and second is error message if not found.
                    additional_error_info = expected[1]
                    expected = expected[0]

                stripped_expected = self.get_minimized_response_content(expected, strip_newlines=True)
                if ignore_ordering:
                    # Ignoring ordering. Check as-is.
                    if stripped_expected not in trimmed_original_content:
                        # Expected value not found in provided content section.
                        display_expected = self.get_minimized_response_content(expected, strip_newlines=False)

                        # Check if due to casing mismatch.
                        if stripped_expected.casefold() in trimmed_original_content.casefold():
                            # Match found when ignoring casing.

                            # Get regex match of actual value, plus 20 characters on each side.
                            search_val = r'((?:[\S\s]{0,20})' + re.escape(stripped_expected) + r'(?:[\S\s]{0,20}))'
                            trimmed_actual = re.search(
                                search_val,
                                trimmed_original_content,
                                flags=re.IGNORECASE,
                            )

                            # Display corresponding error message.
                            self.fail(casing_err_msg.format(display_expected, trimmed_actual.group(0)))

                        else:
                            # Value doesn't exist even after ignoring casing.
                            # Raise message based on content_starts_after/content_ends_before variables.
                            self._assertPageContent(
                                sanitized_original_content,
                                stripped_expected,
                                display_expected,
                                content_starts_after,
                                content_ends_before,
                                main_err_msg,
                                updated_checked_content_str_addon,
                                additional_error_info=additional_error_info,
                            )
                else:
                    # Verifying ordering.
                    # Attempt initial assertion in provided subsection.
                    if stripped_expected not in trimmed_content:
                        # Failed to find content in subsection. Check full content set.
                        if stripped_expected not in trimmed_original_content:
                            # Expected value not found in provided content section.
                            display_expected = self.get_minimized_response_content(expected, strip_newlines=False)

                            # Check if due to casing mismatch.
                            if stripped_expected.casefold() in trimmed_original_content.casefold():
                                # Match found when ignoring casing.

                                # Get regex match of actual value, plus 20 characters on each side.
                                search_val = r'((?:[\S\s]{0,20})' + re.escape(stripped_expected) + r'(?:[\S\s]{0,20}))'
                                trimmed_actual = re.search(
                                    search_val,
                                    trimmed_original_content,
                                    flags=re.IGNORECASE,
                                )

                                # Display corresponding error message.
                                self.fail(casing_err_msg.format(display_expected, trimmed_actual.group(0)))

                            else:
                                # Value doesn't exist even after ignoring casing.
                                # Raise message based on content_starts_after/content_ends_before variables.
                                self._assertPageContent(
                                    sanitized_original_content,
                                    stripped_expected,
                                    display_expected,
                                    content_starts_after,
                                    content_ends_before,
                                    main_err_msg,
                                    updated_checked_content_str_addon,
                                    additional_error_info=additional_error_info,
                                )

                        # If we made it this far, then item was found in full content, but came after a previous
                        # expected value. Raise error.
                        if updated_checked_content_str_addon:
                            ordering_err_msg += updated_checked_content_str_addon
                        self.fail(ordering_err_msg.format(expected))

                # If we made it this far, then value was found. Handle for ordering.
                if not ignore_ordering:
                    # Ordering is being checked. Strip off first section of matching.
                    trimmed_content = stripped_expected.join(
                        trimmed_content.split(stripped_expected)[1:],
                    )

        else:
            # Not an array of items. Assume is a single str value.
            stripped_expected = self.get_minimized_response_content(expected_content, strip_newlines=True)
            if stripped_expected not in trimmed_original_content:
                # Expected value not found in provided content section. Raise Error.
                display_expected = self.get_minimized_response_content(expected_content, strip_newlines=False)

                # Check if due to casing mismatch.
                if stripped_expected.casefold() in trimmed_original_content.casefold():
                    # Match found when ignoring casing.

                    # Get regex match of actual value, plus 20 characters on each side.
                    search_val = r'((?:[\S\s]{0,20})' + re.escape(stripped_expected) + r'(?:[\S\s]{0,20}))'
                    trimmed_actual = re.search(
                        search_val,
                        trimmed_original_content,
                        flags=re.IGNORECASE,
                    )

                    # Display corresponding error message.
                    self.fail(casing_err_msg.format(display_expected, trimmed_actual.group(0)))

                else:
                    # Value doesn't exist even after ignoring casing.
                    # Raise message based on content_starts_after/content_ends_before variables.
                    self._assertPageContent(
                        sanitized_original_content,
                        stripped_expected,
                        display_expected,
                        content_starts_after,
                        content_ends_before,
                        main_err_msg,
                        '',
                    )

        # Return page content in case user wants to run additional logic on it.
        return trimmed_original_content

    def _assertPageContent(
        self,
        actual_content,
        minimized_expected,
        display_expected,
        strip_actual_start,
        strip_actual_end,
        err_msg,
        checked_content_str_addon,
        additional_error_info='',
    ):
        """Internal sub-assertion for assertPageContent() function."""
        strip_err_msg = 'Expected content value was found, but occurred in "{0}" section. Expected was:\n{1}'

        # Check if error was due to content_starts_after/content_ends_before variables.
        found_expected = False
        if strip_actual_start:
            stripped_start_section = str(actual_content.split(strip_actual_start)[0] + strip_actual_start)
            if minimized_expected in stripped_start_section:
                found_expected = 'content_starts_after'

        if strip_actual_end:
            stripped_end_section = str(strip_actual_end + actual_content.split(strip_actual_end)[-1])
            if minimized_expected in stripped_end_section:
                found_expected = 'content_ends_before'

        # Output message based on above searches.
        if found_expected:
            # Content value was in stripped section. Raise corresponding strip message.
            if checked_content_str_addon:
                strip_err_msg += checked_content_str_addon
            self.fail(strip_err_msg.format(found_expected, display_expected))

        else:
            # Content value was physically not present at all. Raise "main" message.
            updated_err_msg = err_msg.format(display_expected)
            if checked_content_str_addon:
                updated_err_msg += checked_content_str_addon
            if additional_error_info:
                updated_err_msg += '\n{0}'.format(additional_error_info)
            self.fail(updated_err_msg)

    def assertNotPageContent(
        self,
        response,
        expected_not_content,
        debug_output=True,
    ):
        """Verifies the non-existence of page content html.
        Django templating may create large amounts of whitespace in response html, often in places where we wouldn't
        intuitively expect it, when running tests. This converts output to a more normalized/predictable format,
        and then verifies the normalized content is not present. Results in more consistent and predictable testing.

        :param response: Response object to check against.
        :param expected_not_content: Expected full string (or set of strings) of HTML content.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out and formatted content string.
        """
        if debug_output:
            # Print out actual response content, for debug output.
            self.show_debug_content(response)

        # Extra setup logic, to sanitize and handle if content_starts_after/content_ends_before variables are defined.
        content_dict = self._trim_response_content(response)
        sanitized_original_content = content_dict['minimized_content']
        trimmed_original_content = content_dict['truncated_content']

        # Handle possible types.
        if expected_not_content is None:
            expected_not_content = ''
        if isinstance(expected_not_content, list) or isinstance(expected_not_content, tuple):
            # Is an array of items. Verify none of them exist on page.
            for content_item in expected_not_content:

                # Handle if expected is a list or tuple.
                additional_error_info = ''
                if (isinstance(content_item, list) or isinstance(content_item, tuple)) and len(content_item) == 2:
                    # Nested array or tuple.
                    # Assuming first value is the value to check for, and second is error message if not found.
                    additional_error_info = content_item[1]
                    content_item = content_item[0]

                # Not an array of items. Assume is a single str value.
                stripped_expected = self.get_minimized_response_content(content_item, strip_newlines=True)
                if stripped_expected != '' and stripped_expected in trimmed_original_content:
                    # Expected value found in provided content section. Raise Error.
                    err_msg = (
                        'Found content in response. Expected content to not be present. Content was:\n'
                        '{0}'.format(content_item)
                    )
                    if additional_error_info:
                        err_msg += '\n\n{0}'.format(additional_error_info)
                    self.fail(err_msg)
        else:
            # Not an array of items. Assume is a single str value.
            stripped_expected = self.get_minimized_response_content(expected_not_content, strip_newlines=True)
            if stripped_expected != '' and stripped_expected in trimmed_original_content:
                # Expected value found in provided content section. Raise Error.
                self.fail(
                    'Found content in response. Expected content to not be present. Content was:\n'
                    '{0}'.format(expected_not_content)
                )

    def assertRepeatingElement(
        self,
        response,
        expected_repeating_element,
        repeat_count,
        content_starts_after=None,
        content_ends_before=None,
        debug_output=True,
    ):
        """Verifies that a given HTMl element repeats, within a given section of content.

        Note: This expects a full HTML element, including both opening and closing tags.

        :param response: Response object to check against.
        :param expected_repeating_element: The expected repeating HTML element. Ex: <li>, <p>, etc.
        :param repeat_count: Integer indicating how many times the HTML element should repeat.
        :param content_starts_after: The HTML that the element should occur after. This HTML and everything
                                     preceding is stripped out of the "search space" for the expected_content value.
        :param content_ends_before: The HTML that the element should occur before. This HTML and everything
                                    following is stripped out of the "search space" for the expected_content value.
        :param debug_output: Bool indicating if debug output should be shown or not. Used for debugging test failures.
        :return: Parsed out and formatted content string.
        """
        # Standardize provided repeating value.
        expected_repeating_element = self.standardize_characters(expected_repeating_element)

        # Sanitize initial content element.
        repeat_count = int(repeat_count)
        if repeat_count < 1:
            raise ValueError('The assertRepeatingElement() function requires an element occurs one or more times.')
        expected_repeating_element = str(expected_repeating_element).strip().lstrip('<').rstrip('>').rstrip('/').strip()
        expected_repeating_element = expected_repeating_element.lower()
        is_void_element = False
        if expected_repeating_element in VOID_ELEMENT_LIST:
            is_void_element = True

        # Generate expected content set.
        # This is what we pass from this wrapper function to the actual assertion function.
        expected_content = []
        for index in range(repeat_count):
            expected_content.append('<{0}>'.format(expected_repeating_element))

            # Add closing tag if not a void element.
            if not is_void_element:
                expected_content.append('</{0}>'.format(expected_repeating_element))

        # Pass our sanitized values into assertPageContent().
        content_dict = self._trim_response_content(
            response,
            content_starts_after=content_starts_after,
            content_ends_before=content_ends_before,
        )
        truncated_content = content_dict['truncated_content']

        # Check element counts within desired section.
        open_tag_err_msg = 'Expected {0} element{1} tags. Found {2}.'
        close_tag_err_msg = 'Expected {0} element closing tags. Found {1}.'
        open_tag_count = truncated_content.count('<{0}>'.format(expected_repeating_element))

        # Check count of element opening tags.
        try:
            self.assertEqual(open_tag_count, repeat_count)
        except AssertionError:
            self.fail(open_tag_err_msg.format(repeat_count, '' if is_void_element else ' opening', open_tag_count))

        # Check count of element closing tags.
        if not is_void_element:
            close_tag_count = truncated_content.count('</{0}>'.format(expected_repeating_element))
            try:
                self.assertEqual(close_tag_count, repeat_count)
            except AssertionError:
                self.fail(close_tag_err_msg.format(repeat_count, close_tag_count))

        # Run full assertPageContent() to make sure we're thorough (unsure of if this part is needed?).
        return self.assertPageContent(truncated_content, expected_content, debug_output=debug_output)

    # endregion Custom Assertions

    # region Helper Functions

    def _get_default_request_user(self, user, auto_login):
        """
        # We first prioritize a direct value passed into this function (if not the default).
        # Then we prioritize a user saved to the class "self.user" variable (if not the default).
        :param user:
        :param auto_login:
        :return:
        """
        # Django imports here to avoid situational "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser

        # If user is None, attempt to fallback to class-user.
        if user is None:
            class_user = getattr(self, 'user', None)
            if class_user != AnonymousUser and class_user != AnonymousUser():
                user = class_user

        # Proceed if user still None.
        if user is None:
            # Handle if default mode is "anonymous" and no user provided.
            if ETC_REQUEST_USER_STRICTNESS == 'anonymous':
                user = AnonymousUser()

            # Handle if default mode is "relaxed" and no user provided.
            elif ETC_REQUEST_USER_STRICTNESS == 'relaxed':
                user = ETC_DEFAULT_STANDARD_USER_IDENTIFIER

            # Handle if default mode is "strict" and no user provided.
            elif ETC_REQUEST_USER_STRICTNESS == 'strict':
                # Handle for logging in a user.
                if auto_login:
                    raise ValidationError(
                        'ETC_REQUEST_USER_STRICTNESS is set to "strict" but auto_login is True and no user was provided. '
                        'Please either set auto_login to False OR explicitly provide a user to authenticate with.'
                    )

            else:
                raise ValueError(
                    'Invalid value provided for EXPANDED_TEST_CASES_REQUEST_USER_STRICTNESS setting. '
                    'Must be one of: ["anonymous", "relaxed", "strict"].'
                )

        # Use anonymous user if not set to auto-login.
        if not auto_login:
            user = AnonymousUser()

        # Return calculated user.
        return user

    def _get_page_response(
        self,
        url,
        *args,
        get=True,
        data=None,
        secure=True,
        headers=None,
        url_args=None,
        url_kwargs=None,
        query_params=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        extra_usergen_kwargs=None,
        **kwargs,
    ):
        """Helper function for assertResponse().

        Fully parses provided user url, and returns corresponding response object.

        :param url: Url to get response object from.
        :param get: Bool indicating if response is GET or POST. Defaults to GET.
        :param data: Optional dict of items to pass into response generation.
        :param secure: Bool indicating if request should be retrieved as HTTP or HTTPS.
        :param headers: Additional test client headers, if any.
        :param url_args: Values to provide for URL population, in "arg" format.
        :param url_kwargs: Values to provide for URL population, in "kwarg" format.
        :param auto_login: Bool indicating if User should be "logged in" to client or not.
        :param user_permissions: Set of Django Permissions to give to test user before accessing page.
        :param user_groups: Set of Django PermissionGroups to give to test user before accessing page.
        :param extra_usergen_kwargs: Optional dictionary of values to pass to _get_login_user__extra_user_auth_setup().
        :return: Django response object for provided url.
        """

        # Handle mutable data defaults.
        data = data or {}
        headers = headers or {}
        url_args = (*kwargs.pop('args', []), *(url_args or []))
        url_kwargs = {**kwargs.pop('kwargs', {}), **(url_kwargs or {})}
        query_params = query_params or {}
        extra_usergen_kwargs = {
            **(extra_usergen_kwargs or {}),
        }

        # Save provided values for user post-test debugging.
        response_url_data = ResponseUrlData(
            url,
            url_args,
            url_kwargs,
            query_params,
        )

        # Validate data types.
        if not isinstance(data, dict):
            raise TypeError('Provided "data" arg must be a dict, for passing into POST requests.')

        # Handle getting user.
        user = self._get_default_request_user(user, auto_login)
        user = self._get_login_user(
            user,
            *args,
            auto_login=auto_login,
            user_permissions=user_permissions,
            user_groups=user_groups,
            **extra_usergen_kwargs,
        )

        # Handle url sanitization.
        url = self.standardize_url(
            url,
            url_args=url_args,
            url_kwargs=url_kwargs,
            url_query_params=query_params,
            append_root=False,
            display_warning=True,
        )
        full_url = '{0}{1}'.format(self.site_root_url, url)
        if ETC_INCLUDE_RESPONSE_DEBUG_URL:
            self.show_debug_url(full_url)

        # Get response object.
        if bool(get):
            response = self.client.get(url, data=data, secure=secure, follow=True, headers=headers)
        else:
            response = self.client.post(url, data=data, secure=secure, follow=True, headers=headers)

        # Update response object with additional useful values for further testing/analysis.

        # The fully computed url after standardizing with provided args/kwargs/query params.
        # But before actually attempting to get response and process in any way.
        response_url_data.computed.initial_url = url
        # The same as above, but with an attempt to prepend the project site root to it.
        response_url_data.computed.full_initial_url = full_url

        # If redirects occurred, then the final url at the end of the redirect chain.
        redirect_url = None
        if hasattr(response, 'redirect_chain') and len(response.redirect_chain) > 0:
            redirect_data = response.redirect_chain[-1]
            if redirect_data[1] == 302 and redirect_data[0] != response_url_data.computed.initial_url:
                redirect_url = redirect_data[0]
                response_url_data.computed.redirect_url = redirect_url
                response_url_data.computed.full_redirect_url = '{0}{1}'.format(self.site_root_url, redirect_url)

        # The fully computed url after processing all view data.
        # The same as the `initial_url` value, unless a redirect occurs.
        # In most instances, will match `initial_url` unless the project is very redirect-heavy.
        if redirect_url is not None:
            final_url = redirect_url
        else:
            final_url = url
        response_url_data.computed.final_url = final_url
        response_url_data.computed.full_final_url = '{0}{1}'.format(self.site_root_url, final_url)

        # Save calculated set of url data to response.
        response.url_data = response_url_data
        # Save user data to response.
        response.user = user

        # Return generated response.
        return response

    def _get_login_user(self, user, *args, auto_login=True, user_permissions=None, user_groups=None, **kwargs):
        """Handles simulating user login with corresponding permissions/groups/etc.

        :param user: User to manipulate.
        :param auto_login: Bool indicating if User should be "logged in" to client or not.
        :param user_permissions: Django Permissions to give to User.
        :param user_groups: Django Groups to give to User.
        :return: Updated User object.
        """

        # Django imports here to avoid situational "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser, Group, Permission

        # If not an anonymous user, attempt to get corresponding actual user object.
        if not isinstance(user, AnonymousUser):
            user = self.get_user(user)

        # Use anonymous user if either not set to auto-login, or provided user is inactive.
        if not auto_login or not hasattr(user, 'is_active') or not user.is_active:
            user = AnonymousUser()

        # If user is provided and is anonymous user object, then skip attempting any other login logic.
        if isinstance(user, AnonymousUser):
            return user

        # Handle mutable data defaults.
        user_permissions = user_permissions or []
        user_groups = user_groups or []

        # Handle possible types for Permissions.
        if isinstance(user_permissions, list) or isinstance(user_permissions, tuple):
            # Is array. This is expected.
            pass
        elif isinstance(user_permissions, str) or isinstance(user_permissions, Permission):
            # Is str or model instance. So assume single permission value.
            user_permissions = [user_permissions]
        else:
            # Invalid/unknown type. Raise error.
            raise TypeError('Provided Django Permissions must be either a str, array, or model format.')

        # Add all Permissions to provided user.
        for permission in user_permissions:
            user = self.add_user_permission(permission, user=user)

        # Handle possible types for Groups.
        if isinstance(user_groups, list) or isinstance(user_groups, tuple):
            # Is array. This is expected.
            pass
        elif isinstance(user_groups, str) or isinstance(user_groups, Group):
            # Is str or model instance. So assume single permission value.
            user_groups = [user_groups]
        else:
            # Invalid/unknown type. Raise error.
            raise TypeError('Provided Django Groups must be either a str, array, or model format.')

        # Add all Groups to provided user.
        for group in user_groups:
            user = self.add_user_group(group, user=user)

        # Optional hook to run additional authentication logic/setup on User.
        # For example, if project has 2-Factor setup that needs to be run.
        user = self._get_login_user__extra_user_auth_setup(
            user,
            *args,
            auto_login=True,
            user_permissions=None,
            user_groups=None,
            **kwargs,
        )

        # Ensure by this point that we have a proper instance of the User object.
        # Accounts for if wonky logic was used in extra_auth_setup, which is defined by the project importing
        # this package, so we have no control over.
        user = self.get_user(user)

        # Handle logging in with user.
        # This forces all response objects to act like this user is logged in for all page accesses.
        # Otherwise, it will act like an anonymous user is navigating the site.
        if auto_login:
            self.client.force_login(user)

        # Return modified user instance.
        return user

    def get_page_title(self, response):
        """Parses out title HTML element from provided response.

        :param response: Response object or response content to get title from.
        :return: Parsed out response title, formatted to have extra whitespace removed.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            response = response.content.decode('utf-8')
        elif isinstance(response, bytes):
            response = response.decode('utf-8')

        # Find title element.
        response_title = re.findall(r'<title(?:>| )([\S\s]+?)(?:</|</ |< /)title>', response)

        # Check that some value was found.
        # Certain response types may have no title, such as file download responses.
        if response_title is None:
            # No tags found. Convert to empty string.
            response_title = ''

        elif response_title is not None:
            # Tag was found.

            # Check how many title tags were found.
            if len(response_title) > 1:
                # Multiple headers were found. Raise error and direct user to helper h1 documentation.
                raise AssertionError(
                    textwrap.dedent(
                        """
                    Found multiple titles ({0} total). There should only be one <title> tag per page.
                    For further reference on <title> tags, consider consulting:
                        * https://www.w3schools.com/tags/tag_title.asp
                        * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title
                    """.format(
                            len(response_title)
                        )
                    ).strip()
                )

            elif len(response_title) == 0:
                # No title text was found. Return empty string.
                response_title = ''

            elif len(response_title) == 1:

                # Pull from capture group.
                response_title = response_title[0]

                # Strip any newlines, if present.
                response_title = re.sub(r'(\n|\r)+', '', response_title)

                # Remove any repeating whitespace, plus any outer whitespace.
                response_title = re.sub(r'(\s)+', ' ', response_title).strip()

                # Ensure title values are actually standardized.
                response_title = self.standardize_characters(response_title)

        # Return formatted title value.
        return response_title

    def get_page_header(self, response):
        """Parses out H1 header HTML element from provided response.

        :param response: Response object or response content to get H1 header from.
        :return: Parsed out response header, formatted to have extra whitespace removed.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            response = response.content.decode('utf-8')
        elif isinstance(response, bytes):
            response = response.decode('utf-8')

        # Find header element.
        response_header = re.findall(r'<h1(?:>| )([\S\s]+?)(?:</|</ |< /)h1>', response)

        # Check that some value was found.
        # Handles if response did not have the H1 header element defined for some reason.
        # For example, likely to occur in responses that provide file downloads.
        if response_header is None:
            # No tags found. Convert to empty string.
            response_header = ''

        elif response_header is not None:
            # Tag was found.

            # Check how many header tags were found.
            if len(response_header) > 1:
                # Multiple headers were found. Raise error and direct user to helper h1 documentation.
                raise AssertionError(
                    textwrap.dedent(
                        """
                    Found multiple headers ({0} total). There should only be one <h1> tag per page.
                    For further reference on <h1> tags, consider consulting:
                        * https://www.w3schools.com/tags/tag_hn.asp
                        * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements
                    """.format(
                            len(response_header)
                        )
                    ).strip()
                )

            elif len(response_header) == 0:
                # No headers text was found. Return empty string.
                response_header = ''

            elif len(response_header) == 1:

                # Pull from capture group.
                response_header = response_header[0]

                # Strip any newlines, if present.
                response_header = re.sub(r'(\n|\r)+', '', response_header)

                # Remove any repeating whitespace, plus any outer whitespace.
                response_header = re.sub(r'(\s)+', ' ', response_header).strip()

            # Return formatted header value.
            return response_header

    def get_context_messages(self, response):
        """Parses out context messages from provided response.

        :param response: Response object or response context to get messages from.
        :return: Parsed out response messages.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            context = response.context
        else:
            context = response

        # Attempt to parse messages from context.
        found_messages = []
        if (context is not None) and ('messages' in context) and (len(context['messages']) > 0):
            # Messages found in response context.
            messages = context['messages']

            for message in messages:
                found_messages.append(str(message.message).strip())

        # Return found messages.
        return found_messages

    def _trim_response_content(self, response, content_starts_after=None, content_ends_before=None):
        """Trims response content, by trimming values at start or end of page content.

        :param response:
        :param content_starts_after:
        :param content_ends_before:
        :return: Dictionary of [sanitized content, trimmed/truncated content].
        """
        strip_err_msg = 'Could not find "{0}" value in content response. Provided value was:\n{1}'

        # Sanitize and format response content.
        minimized_content = self.get_minimized_response_content(response, strip_newlines=True)
        truncated_content = minimized_content

        # Rename variables for internal readability.
        strip_actual_start = content_starts_after
        strip_actual_end = content_ends_before

        if strip_actual_start:
            # Value passed that expected_content should occur AFTER.
            # Find first instance (from top of HTML output) of where this value occurs,
            # and then strip this and all above output.

            # First check that value actually exists in provided response.
            # Because we can't strip if this initial value is not present.
            stripped_start = self.get_minimized_response_content(strip_actual_start, strip_newlines=True)
            if stripped_start not in truncated_content:
                display_start = self.get_minimized_response_content(strip_actual_start, strip_newlines=False)
                self.fail(strip_err_msg.format('content_starts_after', display_start))
            # If we made it this far, then value was found. Remove.
            truncated_content = stripped_start.join(truncated_content.split(stripped_start)[1:])

        if strip_actual_end:
            # Value passed that expected_content should occur BEFORE.
            # Find first instance (from bottom of HTML output) of where this value occurs,
            # and then strip this and all below output.

            # First check that value actually exists in provided response.
            # Because we can't strip if this initial value is not present.
            stripped_end = self.get_minimized_response_content(strip_actual_end, strip_newlines=True)
            if stripped_end not in truncated_content:
                display_end = self.get_minimized_response_content(strip_actual_end, strip_newlines=False)
                self.fail(strip_err_msg.format('content_ends_before', display_end))
            # If we made it this far, then value was found. Remove.
            truncated_content = stripped_end.join(truncated_content.split(stripped_end)[:1])

        # Return both sanitized original content, and the stripped equivalent.
        return {
            'minimized_content': minimized_content,
            'truncated_content': truncated_content,
        }

    # endregion Helper Functions

    # region Hook Functions

    def _assertResponse__pre_builtin_tests(
        self,
        url,
        *args,
        get=True,
        data=None,
        expected_status=200,
        expected_redirect_url=None,
        url_args=None,
        url_kwargs=None,
        redirect_args=None,
        redirect_kwargs=None,
        expected_title=None,
        expected_header=None,
        expected_messages=None,
        expected_not_messages=None,
        expected_content=None,
        expected_not_content=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        ignore_content_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        **kwargs,
    ):
        """Hook function to allow injecting code prior to running any of the built-in assertResponse() tests.

        For maximum usability, this function receives all args/kwargs provided to the default assertResponse()
        function.

        This hook does nothing by default, and is exclusively provided for custom extension logic.
        """

        # Set class variable to track that hook is not implemented.
        # Still using the default implementation that does nothing.
        self.hook_checks.pre_assert_is_okay = False

    def _assertResponse__post_builtin_tests(
        self,
        url,
        *args,
        get=True,
        data=None,
        expected_status=200,
        expected_redirect_url=None,
        url_args=None,
        url_kwargs=None,
        redirect_args=None,
        redirect_kwargs=None,
        expected_title=None,
        expected_header=None,
        expected_messages=None,
        expected_not_messages=None,
        expected_content=None,
        expected_not_content=None,
        auto_login=True,
        user=None,
        user_permissions=None,
        user_groups=None,
        ignore_content_ordering=False,
        content_starts_after=None,
        content_ends_before=None,
        **kwargs,
    ):
        """Hook function to allow injecting code after running all of the built-in assertResponse() tests.

        For maximum usability, this function receives all args/kwargs provided to the default assertResponse()
        function.

        This hook does nothing by default, and is exclusively provided for custom extension logic.
        """

        # Set class variable to track that hook is not implemented.
        # Still using the default implementation that does nothing.
        self.hook_checks.post_assert_is_okay = False

    def _get_login_user__extra_user_auth_setup(
        self,
        user,
        *args,
        auto_login=True,
        user_permissions=None,
        user_groups=None,
        **kwargs,
    ):
        """Hook function, to allow running extra authentication setup logic on User object.

        Useful such as for running things like 2-Factor setup logic for User.

        For maximum usability, this function receives all args/kwargs provided to the default _get_login_user()
        function.

        This hook does nothing by default, and is exclusively provided for custom extension logic.
        :return: Must return a User object. Either the original one as provided, or an updated version based on
                 custom logic.
        """

        # Set class variable to track that hook is not implemented.
        # Still using the default implementation that does nothing.
        self.hook_checks.auth_setup_is_okay = False

        return user

    def _hook_function_warning_check(self, user, *args, **kwargs):
        """Warning check function for built-in project hooks.

        Specifically, any supplemental args/kwargs (outside of what is defined by the project)
        are exclusively used to optionally provide data to these hook functions.

        If these hook functions are not implemented, but args/kwargs are passed in an
        assertion, then warnings will trigger.

        This is defined as a separate function, so that it can be easily overridden
        per-project, if needed.
        """

        should_raise_warning = self._hook_function_warning_check_if_statement(user)
        if should_raise_warning:
            # No custom hooks have been implemented.
            # Check if any args or kwargs have been provided.
            if len(args) > 0 or len(kwargs) > 0:
                # Either args or kwargs have been provided, which are exclusively meant for hook functions.
                # But no hook functions have been implemented.
                # Raise warning, as this is probably not an intended state.
                warn_msg = (
                    "Supplemental args/kwargs have been provided to an assertResponse statement. "
                    "Any supplemental args/kwargs are exclusively used to provide custom data to "
                    "built-in hook functions, but no hook functions seem to be implemented for your project. "
                    "Either remove the use of args/kwargs in the assertion, or implement one of the hook functions."
                )
                # Create console warning message.
                warnings.warn(warn_msg)
                # Create logging warning message.
                logging.warning(warn_msg)

    def _hook_function_warning_check_if_statement(self, user):
        """If statement to determine if hook functions should raise warning.

        Separate function for maximum customizability per project.
        """

        # Django imports here to avoid situational "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser

        should_raise_warning = False
        if isinstance(user, AnonymousUser):
            # User is anonymous. Skip auth hook.
            if (
                # Comment to prevent "black" formatting.
                not self.hook_checks.pre_assert_is_okay
                and not self.hook_checks.post_assert_is_okay
            ):
                should_raise_warning = True

        else:
            # User is not anonymous. Also consider auth hook.

            if (
                # Comment to prevent "black" formatting.
                not self.hook_checks.pre_assert_is_okay
                and not self.hook_checks.post_assert_is_okay
                and not self.hook_checks.auth_setup_is_okay
            ):
                should_raise_warning = True

        # Return calculated value.
        return should_raise_warning

    # endregion Hook Functions


# Define acceptable imports on file.
__all__ = [
    'IntegrationTestCase',
]
