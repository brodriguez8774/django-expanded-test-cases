"""
Testing class for generalized logic.
"""

# System Imports.
import os
import sys
from io import StringIO
from django.test import TestCase

# User Imports.
from django_expanded_test_cases.mixins import CoreTestCaseMixin


BASE_ERROR_COUNT = 0
BASE_FAILURE_COUNT = 0


class BaseTestCase(TestCase, CoreTestCaseMixin):
    """Generalized testing functionality. Builds upon Django's default TestCase class."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreMixin setup logic.
        cls.set_up_class(debug_print=debug_print)

    def run(self, *args, **kwargs):
        """"""
        # If running in Pytest, use default logic.
        if 'pytest' in sys.modules:
            return super().run(*args, *kwargs)

        # Save original std out/err.
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr

        # Intercept std out/err so we don't output useless garbage.
        str_buffer = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = str_buffer
        base_seperator_str = '{0:-^' + str(os.get_terminal_size().columns) + '}'
        try:
            # Call parent logic.
            result = super().run(*args, *kwargs)

            # Revert std out/err handling.
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr

            # Check if result object has "errors" populated. Intercept if so.
            global BASE_ERROR_COUNT
            if hasattr(result, 'errors'):
                if len(result.errors) > BASE_ERROR_COUNT:
                    err_output = '\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n\n\n'.format(
                        base_seperator_str.format(' Captured Print Statements '),
                        str_buffer[0].getvalue(),
                        base_seperator_str.format(' Captured Error Statements '),
                        str_buffer[1].getvalue(),
                        base_seperator_str.format(' Captured Stack Trace '),
                        result.errors[BASE_ERROR_COUNT][1],
                    )
                    updated_err = ()
                    for index in range(len(result.errors[BASE_ERROR_COUNT])):
                        if index == 1:
                            updated_err += (err_output,)
                        else:
                            updated_err += (result.errors[BASE_ERROR_COUNT][index],)

                    result.errors[BASE_ERROR_COUNT] = result.errors

                    BASE_ERROR_COUNT += 1

            # Check if result object has "failures" populated. Intercept if so.
            global BASE_FAILURE_COUNT
            if hasattr(result, 'failures'):
                if len(result.failures) > BASE_FAILURE_COUNT:
                    fail_output = '\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n\n\n'.format(
                        base_seperator_str.format(' Captured Print Statements '),
                        str_buffer[0].getvalue(),
                        base_seperator_str.format(' Captured Error Statements '),
                        str_buffer[1].getvalue(),
                        base_seperator_str.format(' Captured Stack Trace '),
                        result.failures[BASE_FAILURE_COUNT][1],
                    )
                    updated_fail = ()
                    for index in range(len(result.failures[BASE_FAILURE_COUNT])):
                        if index == 1:
                            updated_fail += (fail_output,)
                        else:
                            updated_fail += (result.failures[BASE_FAILURE_COUNT][index],)

                    result.failures[BASE_FAILURE_COUNT] = updated_fail

                    BASE_FAILURE_COUNT += 1

        finally:
            return result


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
]
