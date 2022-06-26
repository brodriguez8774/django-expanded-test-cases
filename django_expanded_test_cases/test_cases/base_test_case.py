"""
Testing class for generalized logic.
"""

# System Imports.
import inspect
from functools import wraps
from django.test import TestCase

# User Imports.
from django_expanded_test_cases.mixins import CoreTestCaseMixin
from django_expanded_test_cases.constants import DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT


def wrapper(method, test_class):
    """Wrapper logic to intercept all functions on AssertionError and print error at bottom of output."""
    @wraps(method)
    def wrapped(*args, **kwargs):
        print("Method")
        print(method)
        print()
        print("Method Args")
        print(args)
        print()
        print("Test Class")
        print(test_class)
        print()
        print("Test Class Displayed Bool")
        print(test_class.debug_err_displayed)
        print()
        if not DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT:
            # Debug printing not enabled. Return original function logic.
            return method(*args, **kwargs)
        else:
            try:
                return method(*args, **kwargs)
            except AssertionError as err:
                # Assertion failed.
                if test_class.debug_err_displayed is False:
                    test_class.debug_err_displayed = True
                    print('\n')
                    print(err)
                    print('')
                    raise err
    return wrapped

class BaseTestCase(TestCase, CoreTestCaseMixin):
    """Generalized testing functionality. Builds upon Django's default TestCase class."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreMixin setup logic.
        cls.set_up_class(debug_print=debug_print)

    def setUp(self):
        super().setUp()
        self.debug_err_displayed = False

        # Wrap all assertion methods
        all_methods = inspect.getmembers(self)
        for method_name, method in all_methods:
            if method_name.startswith('assert'):
                # print(method_name)
                setattr(self, method_name, wrapper(method, self))


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
]
