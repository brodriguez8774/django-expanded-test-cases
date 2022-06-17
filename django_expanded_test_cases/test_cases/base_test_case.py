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


class BaseTestCase(TestCase, CoreTestCaseMixin):
    """Generalized testing functionality. Builds upon Django's default TestCase class."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreMixin setup logic.
        cls.set_up_class(debug_print=debug_print)

    def run(self, *args, **kwargs):
        """Run method used for testrunner to actually run the test"""
        # If running in Pytest, use default logic.
        if 'pytest' in sys.modules:
            return super().run(*args, *kwargs)

        # Save original std out/err.
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr

        # Intercept std out/err so we don't output useless garbage.
        str_buffer = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = str_buffer

        # Call parent logic.
        result = super().run(*args, *kwargs)

        # Revert std out/err handling.
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

        # If the result object does not have errors or failures that we can use
        # to know if we need to alter the output, just return the result.
        # NOTE: This seems to happen when running tests via manage.py --parallel
        if not hasattr(result.errors, '__len__') or not hasattr(result.failures, '__len__'):
            return result

        # See if result object has expanded_error_count attribute and set
        # to zero if non-existent.
        if not hasattr(result, 'expanded_error_count'):
            setattr(result, 'expanded_error_count', 0)

        # See if result object has expanded_failure_count attribute and set
        # to zero if non-existent
        if not hasattr(result, 'expanded_failure_count'):
            setattr(result, 'expanded_failure_count', 0)

        # Bases separator to be used in altering output.
        base_separator_str = '{0:-^' + str(os.get_terminal_size().columns) + '}'

        # Check if result object has "errors" populated. Intercept if so.
        if hasattr(result, 'errors'):
            if len(result.errors) > result.expanded_error_count:
                err_output = '\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n\n\n'.format(
                    base_separator_str.format(' Captured Print Statements '),
                    str_buffer[0].getvalue(),
                    base_separator_str.format(' Captured Error Statements '),
                    str_buffer[1].getvalue(),
                    base_separator_str.format(' Captured Stack Trace '),
                    result.errors[result.expanded_error_count][1],
                )
                updated_err = ()
                for index in range(len(result.errors[result.expanded_error_count])):
                    if index == 1:
                        updated_err += (err_output,)
                    else:
                        updated_err += (result.errors[result.expanded_error_count][index],)

                result.errors[result.expanded_error_count] = result.errors

                result.expanded_error_count += 1

        # Check if result object has "failures" populated. Intercept if so.
        if hasattr(result, 'failures'):
            if len(result.failures) > result.expanded_failure_count:
                fail_output = '\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n\n\n'.format(
                    base_separator_str.format(' Captured Print Statements '),
                    str_buffer[0].getvalue(),
                    base_separator_str.format(' Captured Error Statements '),
                    str_buffer[1].getvalue(),
                    base_separator_str.format(' Captured Stack Trace '),
                    result.failures[result.expanded_failure_count][1],
                )
                updated_fail = ()
                for index in range(len(result.failures[result.expanded_failure_count])):
                    if index == 1:
                        updated_fail += (fail_output,)
                    else:
                        updated_fail += (result.failures[result.expanded_failure_count][index],)

                result.failures[result.expanded_failure_count] = updated_fail

                result.expanded_failure_count += 1

        return result


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
]
