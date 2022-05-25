"""
Testing class for generalized logic.
"""

# System Imports.
from django.test import TestCase

# User Imports.
from .core_mixin import CoreTestCaseMixin


class BaseTestCase(TestCase, CoreTestCaseMixin):
    """Generalized testing functionality. Builds upon Django's default TestCase class."""

    def setUp(self, debug_print=None):
        # Run parent setup logic.
        super().setUp()

        # Also call CoreMixin setup logic.
        self.set_up(debug_print=debug_print)
