"""
Core testing logic that pertains to handling Response objects.
"""

# System Imports.
import logging, re

# Third-Party Imports.
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseBase

# Internal Imports.
from . import CoreTestCaseMixin
from django_expanded_test_cases.constants import (
    OUTPUT_ERROR,
    RESPONSE_DEBUG_CONTENT,
    RESPONSE_DEBUG_HEADERS,
    RESPONSE_DEBUG_CONTEXT,
    RESPONSE_DEBUG_MESSAGES,
    RESPONSE_DEBUG_SESSION,
    RESPONSE_DEBUG_FORMS,
    RESPONSE_DEBUG_USER_INFO,
    OUTPUT_EMPHASIS,
)


# Initialize logging.
logger = logging.getLogger(__name__)


class ResponseTestCaseMixin(CoreTestCaseMixin):
    """Includes testing logic used in handling Response objects."""

    @classmethod
    def set_up_class(cls, debug_print=None):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase, calling the literal function
        here would override instead.

        :param debug_print: Optional bool that indicates if debug output should print to console.
                            Param overrides setting value if both param and setting are set.
        """
        # Run parent setup logic.
        super().set_up_class(debug_print=debug_print)

    # region Debug Output Functions

    def show_debug_content(self, response_content):
        """Prints debug response page output."""

        # Handle for potential param types.
        if isinstance(response_content, HttpResponseBase):
            response_content = response_content.content.decode('utf-8')
        elif isinstance(response_content, bytes):
            response_content = response_content.decode('utf-8')

        # Standardize output for easier analysis.
        response_content = self.standardize_characters(response_content)
        response_content = self.standardize_newlines(response_content)

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.content'),
            fore=RESPONSE_DEBUG_CONTENT,
            style=OUTPUT_EMPHASIS,
        )

        # Print out data, if present.
        if response_content:
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
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.headers'),
            fore=RESPONSE_DEBUG_HEADERS,
            style=OUTPUT_EMPHASIS,
        )

        # Print out data, if present.
        if response_headers is not None and len(response_headers) > 0:
            for key, value in response_headers.items():
                self._debug_print('    * "{0}": "{1}"'.format(key, value), fore=RESPONSE_DEBUG_HEADERS)
        else:
            self._debug_print('    No response headers found.')
        self._debug_print()

    def show_debug_context(self, response_context):
        """Prints debug response context data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            response_context = response_context.context or {}

        if response_context is not None:
            # Attempt to access key object. If fails, attempt to generate dict of values.
            try:
                response_context.keys()
            except AttributeError:
                # Handling for:
                #     * django.template.context.RequestContext
                #     * django.template.context.Context
                # No guarantee this will work for other aribtrary types.
                # Handle as they come up.
                temp_dict = {}
                for context in response_context:
                    temp_dict = {**temp_dict, **context}
                response_context = temp_dict

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.context'),
            fore=RESPONSE_DEBUG_CONTEXT,
            style=OUTPUT_EMPHASIS,
        )

        # NOTE: Response context object is strange, in that it's basically a dictionary,
        # and it allows .keys() but not .values(). Thus, iterate on keys only and pull respective value.
        if response_context is not None and len(response_context.keys()) > 0:
            # pass
            for key in response_context.keys():
                context_value = str(response_context.get(key))
                # Truncate display if very long.
                if len(context_value) > 80:
                    context_value = '"{0}"..."{1}"'.format(context_value[:40], context_value[-40:])
                self._debug_print('    * {0}: {1}'.format(key, context_value), fore=RESPONSE_DEBUG_CONTEXT)
        else:
            self._debug_print('    No context data found.', fore=RESPONSE_DEBUG_CONTEXT)
        self._debug_print()

    def show_debug_session_data(self, client):
        """Prints debug response session data."""

        # Handle for potential param types.
        if isinstance(client, HttpResponseBase):
            client = client.client

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'client.session'),
            fore=RESPONSE_DEBUG_SESSION,
            style=OUTPUT_EMPHASIS,
        )

        if client is not None and len(client.session.items()) > 0:
            for key, value in client.session.items():
                self._debug_print('    * {0}: {1}'.format(key, value), fore=RESPONSE_DEBUG_SESSION)
        else:
            self._debug_print('    No session data found.', fore=RESPONSE_DEBUG_SESSION)
        self._debug_print()

    def show_debug_messages(self, response_context):
        """Prints debug response message data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            response_context = response_context.context

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'response.context["messages"]'),
            fore=RESPONSE_DEBUG_MESSAGES,
            style=OUTPUT_EMPHASIS,
        )

        # Print out data, if present.
        if response_context is not None and 'messages' in response_context:
            messages = response_context['messages']
            if len(messages) > 0:
                for message in messages:
                    self._debug_print('    * "{0}"'.format(message), fore=RESPONSE_DEBUG_MESSAGES)
            else:
                self._debug_print('    No context messages found.', fore=RESPONSE_DEBUG_MESSAGES)
        else:
            self._debug_print('    No context messages found.', fore=RESPONSE_DEBUG_MESSAGES)
        self._debug_print()

    def show_debug_form_data(self, response_context):
        """Prints debug response form data."""

        # Handle for potential param types.
        if isinstance(response_context, HttpResponseBase):
            response_context = response_context.context

        self._debug_print()
        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'Form Data'),
            fore=RESPONSE_DEBUG_FORMS,
            style=OUTPUT_EMPHASIS,
        )

        # Check if form or formset data is actually present.
        if 'form' in response_context or 'formset' in response_context:
            # Form or formset present on page.

            # Attempt to get form data.
            form_present = False
            if 'form' in response_context:
                form_present = True
                form = response_context['form']

                # Print general form data.
                self._debug_print('    Provided Form Fields:', fore=RESPONSE_DEBUG_FORMS)
                fields_submitted = False
                for key, value in form.data.items():
                    self._debug_print('        {0}: {1}'.format(key, value), fore=RESPONSE_DEBUG_FORMS)
                    fields_submitted = True
                if not fields_submitted:
                    self._debug_print('        No form field data submitted.', fore=RESPONSE_DEBUG_FORMS)

                # Print form data errors if present.
                if not form.is_valid():
                    self._debug_print()
                    if len(form.errors) > 0 or len(form.non_field_errors()) > 0:
                        self._debug_print('    Form Invalid:'.format(not form.is_valid()), fore=RESPONSE_DEBUG_FORMS)
                        if len(form.non_field_errors()) > 0:
                            self._debug_print('        Non-field Frrors:', fore=RESPONSE_DEBUG_FORMS)
                            for error in form.non_field_errors():
                                self._debug_print('            {0}'.format(error), fore=RESPONSE_DEBUG_FORMS)

                        if len(form.errors) > 0:
                            self._debug_print('        Field Errors:', fore=RESPONSE_DEBUG_FORMS)
                            for error in form.errors:
                                self._debug_print('            {0}'.format(error), fore=RESPONSE_DEBUG_FORMS)

                else:
                    self._debug_print('    Form found and valid.', fore=RESPONSE_DEBUG_FORMS)

            # Attempt to get formset data.
            if 'formset' in response_context:
                if form_present:
                    self._debug_print()
                formset = response_context['formset']

                for form in formset:
                    self._debug_print('Form(set) Errors:')
                    for error in form.non_field_errors():
                        self._debug_print('    {0}'.format(error), fore=RESPONSE_DEBUG_FORMS)
                    for error in form.errors:
                        self._debug_print('    {0}'.format(error), fore=RESPONSE_DEBUG_FORMS)
        else:
            # No identifiable form or formset data present on page.
            self._debug_print('    No form data found.', fore=RESPONSE_DEBUG_FORMS)

        self._debug_print()

    def show_debug_user_info(self, user):
        """Prints debug user data."""

        # Imported here to prevent potential "Apps aren't loaded yet" error.
        from django.contrib.auth.models import AnonymousUser

        self._debug_print(
            '{0} {1} {0}'.format('=' * 10, 'User Info'),
            fore=RESPONSE_DEBUG_USER_INFO,
            style=OUTPUT_EMPHASIS,
        )

        # Only proceed if we got a proper user model.
        if isinstance(user, get_user_model()):

            # General user information.
            self._debug_print('    * Username: "{0}"'.format(user.username), fore=RESPONSE_DEBUG_USER_INFO)
            self._debug_print('    * First: "{0}"'.format(user.first_name), fore=RESPONSE_DEBUG_USER_INFO)
            self._debug_print('    * Last: "{0}"'.format(user.last_name), fore=RESPONSE_DEBUG_USER_INFO)
            self._debug_print('    * Email: "{0}"'.format(user.email), fore=RESPONSE_DEBUG_USER_INFO)

            # User auth data.
            self._debug_print(
                '    * is_authenticated: {0}'.format(user.is_authenticated),
                fore=RESPONSE_DEBUG_USER_INFO,
            )

            # User groups.
            self._debug_print('    * User Groups: {0}'.format(user.groups.all()), fore=RESPONSE_DEBUG_USER_INFO)

            # User permissions.
            self._debug_print(
                '    * User Permissions: {0}'.format(user.user_permissions.all()),
                fore=RESPONSE_DEBUG_USER_INFO,
            )

        elif isinstance(user, AnonymousUser):

            self._debug_print('    Anonymous user. No user is logged in.', fore=RESPONSE_DEBUG_USER_INFO)

        else:
            self._debug_print('    * Invalid user "{0}" of type "{1}". Expected "{2}".'.format(
                user,
                type(user),
                type(get_user_model()),
            ), fore=OUTPUT_ERROR)
        self._debug_print()

    # endregion Debug Output Functions.

    def standardize_html_tags(self, value):
        """Standardizes spacing around html-esque elements, to remove unnecessary spacing.

        For example, "<h1> MyHeader </h1>" will simplify down to "<h1>MyHeader</h1>".

        Ensures that the actual expected value can be directly checked,
        instead of trying to account for extraneous template whitespacing.

        :param value: Str value to standardize.
        :return: Sanitized str.
        """
        value = str(value)

        # Remove any whitespace around an opening html bracket ( < ).
        value = re.sub(r'(( )*)<(( )*)', '<', value)

        # Remove any whitespace around a closing html bracket ( > ).
        value = re.sub(r'(( )*)>(( )*)', '>', value)

        # Remove any whitespace around an opening array bracket ( [ ).
        value = re.sub(r'(( )*)\[(( )*)', '[', value)

        # Remove any whitespace around a closing array bracket ( ] ).
        value = re.sub(r'(( )*)](( )*)', ']', value)

        # Remove any whitespace around an opening dict bracket ( { ).
        value = re.sub(r'(( )*){(( )*)', '{', value)

        # Remove any whitespace around a closing dict bracket ( } ).
        value = re.sub(r'(( )*)}(( )*)', '}', value)

        return value

    def get_minimized_response_content(self, response, strip_newlines=False):
        """Returns response content, but with minimalistic formatting.

        For example, will trim all newline characters and repeating spaces.
        Also will standardize common characters to output in a single format.

        :param response: Response object or response content to parse.
        :param strip_newlines: Optional bool, indicating if all newlines should be converted into spaces,
            for extra-minimalistic formatting.
            Generally True for UnitTest direct comparison. False for console output/human examination.
        :return: Formatted response content.
        """
        # Handle for provided response types.
        if isinstance(response, HttpResponseBase):
            response_content = response.content.decode('utf-8')
        else:
            response_content = str(response)

        # Standardize basic characters, for easier comparison.
        response_content = self.standardize_characters(response_content)

        # Trim all extra whitespaces, for easier comparison.
        if strip_newlines:
            # All whitespace is converted into a single space.
            # Newlines are also converted into a single space.
            response_content = self.standardize_whitespace(response_content)
        else:
            # All whitespace is converted into a single space.
            # Repeating newlines are condensed down into a single newline.
            response_content = self.standardize_newlines(response_content)

        # Further trim whitespace around specific characters, for easier comparison.
        response_content = self.standardize_html_tags(response_content)

        return response_content

    # region Html Search Functions

    def find_elements_by_tag(self, content, element):
        """Finds all HTML elements that match the provided element tag.

        :param content: Content to search through.
        :param element: Html element to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Sanitize provided element value. We don't care how the user was provided the syntax.
        element = self.get_minimized_response_content(element)
        element = element.lstrip('<').rstrip('>').strip('/').strip()

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(name=element)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Validate parsed value.
        if not len(element_list) > 0:
            self.fail(f'Unable to find element "<{element}>" in content. Provided content was:\n{content}')

        # Return found list.
        return element_list

    def find_element_by_tag(self, content, element):
        """Finds first HTML element that matches the provided element tag.

        :param content: Content to search through.
        :param element: Html element to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Sanitize provided element value. We don't care how the user was provided the syntax.
        element = self.get_minimized_response_content(element)
        element = element.lstrip('<').rstrip('>').strip('/').strip()

        # Call parent function logic.
        element_list = self.find_elements_by_tag(content, element)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "<{element}>" element. Expected only one instance. '
                f'Content was:\n{content}'
             )

        # Return found item.
        return element_list[0]

    def find_elements_by_id(self, content, element_id):
        """Finds all HTML elements that match the provided id.

        :param content: Content to search through.
        :param element_id: Element id to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(id=element_id)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find id "{element_id}" in content. Provided content was:\n{content}')

        # Provide warning if two or more values were found.
        if len(element_list) > 1:
            logger.warning(
                'It\'s considered bad practice to have multiple matching id tags in one html response. '
                'Consider refactoring elements to keep each id unique.\n'
                'Found {0} total elements with id of "{1}".'.format(len(element_list), element_id)
            )

        # Return found values.
        return element_list

    def find_element_by_id(self, content, element_id):
        """Finds first HTML element that matches the provided id.

        :param content: Content to search through.
        :param element_id: Element id to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_id(content, element_id)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{element_id}" id. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_class(self, content, css_class):
        """Finds all HTML elements that match the provided css class.

        :param content: Content to search through.
        :param css_class: Css class to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(class_=css_class)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find class "{css_class}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_class(self, content, css_class):
        """Finds first HTML element that matches the provided css class.

        :param content: Content to search through.
        :param css_class: Css class to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_class(content, css_class)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{css_class}" class. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_css_selector(self, content, css_selector):
        """Finds all HTML elements that match the provided css selector.

        :param content: Content to search through.
        :param css_selector: Css selector to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.select(css_selector)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find css selector "{css_selector}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_css_selector(self, content, css_selector):
        """Finds first HTML element that matches the provided css selector.

        :param content: Content to search through.
        :param css_selector: Css selector to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_css_selector(content, css_selector)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{css_selector}" css selector. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_data_attribute(self, content, data_attribute, data_value):
        """Finds all HTML elements that match the provided data attribute and data value.

        :param content: Content to search through.
        :param data_attribute: The key of the data attribute to search for.
        :param data_value: The value of the data attribute to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        attr_dict = {data_attribute: data_value}
        elements = soup.find_all(attrs=attr_dict)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(
                f'Unable to find data attribute "{data_attribute}" with value "{data_value}" in content. Provided '
                f'content was:\n{content}'
            )

        # Return found values.
        return element_list

    def find_element_by_data_attribute(self, content, data_attribute, data_value):
        """Finds first HTML element that matches the provided data attribute and data value.

        :param content: Content to search through.
        :param data_attribute: The key of the data attribute to search for.
        :param data_value: The value of the data attribute to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_data_attribute(content, data_attribute, data_value)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{data_attribute}" data attribute with value "{data_value}". '
                f'Expected only one instance. Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_name(self, content, element_name):
        """Finds all HTML elements that match the provided name attribute.

        :param content: Content to search through.
        :param element_name: Element name to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        attr_dict = {'name': element_name}
        elements = soup.find_all(attrs=attr_dict)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find name "{element_name}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_name(self, content, element_name):
        """Finds first HTML element that matches the provided name attribute.

        :param content: Content to search through.
        :param element_name: Element name to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_name(content, element_name)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{element_name}" name. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    def find_elements_by_link_text(self, content, link_text):
        """Finds all HTML elements that match the provided link text.

        :param content: Content to search through.
        :param link_text: Link text to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Search for all matching elements.
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(href=link_text)
        element_list = [self.get_minimized_response_content(element.prettify()) for element in elements]

        # Verify one or more values were found.
        if not len(element_list) > 0:
            self.fail(f'Unable to find link text "{link_text}" in content. Provided content was:\n{content}')

        # Return found values.
        return element_list

    def find_element_by_link_text(self, content, link_text):
        """Finds first HTML element that matches the provided link text.

        :param content: Content to search through.
        :param link_text: Link text to search for.
        """
        # Ensure response content is in expected minimized format.
        content = self.get_minimized_response_content(content)

        # Call parent function logic.
        element_list = self.find_elements_by_link_text(content, link_text)

        # Verify only one value was found.
        if len(element_list) > 1:
            self.fail(
                f'Found multiple instances of "{link_text}" link text. Expected only one instance. '
                f'Content was:\n{content}'
            )

        # Return found item.
        return element_list[0]

    # endregion Html Search Functions


# Define acceptable imports on file.
__all__ = [
    'ResponseTestCaseMixin',
]
