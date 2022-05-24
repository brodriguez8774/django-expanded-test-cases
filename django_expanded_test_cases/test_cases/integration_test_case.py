"""
Testing logic for views and other multi-part components.
"""

# System Imports.
from django.test import TestCase

# User Imports.
from .core_mixin import CoreTestCaseMixin


class IntegrationTestCase(TestCase, CoreTestCaseMixin):
    """Testing functionality for views and other multi-part components."""

    def setUp(self):
        # Run parent setup logic.
        super().setUp()
