"""
Testing class for generalized logic.
"""

# System Imports.
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


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
]
