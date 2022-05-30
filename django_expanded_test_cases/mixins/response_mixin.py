"""
Core testing logic that pertains to handling Response objects.
"""

# System Imports.
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseBase

# User Imports.
from .core_mixin import CoreTestCaseMixin


class ResponseTestCaseMixin(CoreTestCaseMixin):
    """Includes testing logic used in handling Response objects."""

    # region Debug Output Functions

    def show_debug_content(self, response_content):
        """Prints debug response page output."""

        # Handle for potential param types.
        if isinstance(response_content, HttpResponseBase):
            response_content = response_content.content.decode('utf-8')
        elif isinstance(response_content, bytes):
            response_content = response_content.decode('utf-8')

        # Print out data, if present.
        if response_content:
            self._debug_print()
            self._debug_print(('{0} {1} {0}'.format('=' * 10, 'response.content')))
            self._debug_print(response_content)
            self._debug_print()

    def show_debug_headers(self, response_headers):
        """Prints debug response header data."""

        # Handle for potential param types.
        if isinstance(response_headers, HttpResponseBase):
            # Actual attr name seemed to change based on settings definitions.
            # Unsure of why though? May want to figure out details at later date.
            # This should account for both instances I'm pretty sure I encountered, though.
            if hasattr(response_headers, 'headers'):
                response_headers = response_headers.headers
            elif hasattr(response_headers, '_headers'):
                response_headers = response_headers._headers
            else:
                response_headers = None

        self._debug_print()
        self._debug_print(('{0} {1} {0}'.format('=' * 10, 'response.headers')))

        # Print out data, if present.
        if response_headers is not None and len(response_headers) > 0:
            for key, value in response_headers.items():
                self._debug_print('    * "{0}": "{1}"'.format(key, value))
        else:
            self._debug_print('    No response headers found.')
        self._debug_print()

    def show_debug_context(self, response_context):
        """Prints debug response context data."""
        raise NotImplementedError()

    def show_debug_session_data(self, client):
        """Prints debug response session data."""

        # Handle for potential param types.
        if isinstance(client, HttpResponseBase):
            client = client.client

        self._debug_print()
        self._debug_print('{0} {1} {0}'.format('=' * 10, 'client.session'))

        if client is not None and len(client.session.items()) > 0:
            for key, value in client.session.items():
                self._debug_print('    * {0}: {1}'.format(key, value))
        else:
            self._debug_print('    No session data found.')
        self._debug_print('')

    def show_debug_form_data(self, response_context):
        """Prints debug response form data."""
        raise NotImplementedError()

    def show_debug_messages(self, response_context):
        """Prints debug response message data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            response_context = response_context.context

        self._debug_print()
        self._debug_print(('{0} {1} {0}'.format('=' * 10, 'response.context["messages"]')))

        # Print out data, if present.
        if response_context is not None and 'messages' in response_context:
            messages = response_context['messages']
            if len(messages) > 0:
                for message in messages:
                    self._debug_print('    * "{0}"'.format(message))
            else:
                self._debug_print('    No context messages found.')
        self._debug_print()

    def show_debug_user_info(self, user):
        """Prints debug user data."""

        self._debug_print()
        self._debug_print('{0} {1} {0}'.format('=' * 10, 'User Info'))

        # Only proceed if we got a proper user model.
        if isinstance(user, get_user_model()):

            # General user information.
            self._debug_print('    * Username: "{0}"'.format(user.username))
            self._debug_print('    * First: "{0}"'.format(user.first_name))
            self._debug_print('    * Last: "{0}"'.format(user.last_name))
            self._debug_print('    * Email: "{0}"'.format(user.email))

            # User auth data.
            self._debug_print('    * is_authenticated: {0}'.format(user.is_authenticated))

            # User groups.
            self._debug_print('    * User Groups: {0}'.format(user.groups.all()))

            # User permissions.
            self._debug_print('    * User Permissions: {0}'.format(user.user_permissions.all()))

            self._debug_print()

        else:
            self._debug_print('    * Invalid user "{0}" of type "{1}". Expected "{2}".'.format(
                user,
                type(user),
                type(get_user_model()),
            ))

    # endregion Debug Output Functions.
