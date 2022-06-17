"""
Testing class for generalized logic.
"""

# System Imports.
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
        print_debug_output = False
        try:
            # Call parent logic.
            result = super().run(*args, *kwargs)

            # Revert std out/err handling.
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr

            global BASE_ERROR_COUNT

            # Check result attributes.
            if hasattr(result, 'errors'):
                if len(result.errors) > BASE_ERROR_COUNT:
                    print_debug_output = True
                    BASE_ERROR_COUNT += 1

            global BASE_FAILURE_COUNT
            if hasattr(result, 'failures'):
                if len(result.failures) > BASE_FAILURE_COUNT:
                    print_debug_output = True
                    BASE_FAILURE_COUNT += 1

            if print_debug_output:
                for buffer in str_buffer:
                    print(buffer.getvalue())

        finally:
            return result


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
]
