"""
Core testing logic, universal to all test cases.
"""

# System Imports.
from django.contrib.auth import get_user_model


class CoreTestCaseMixin:
    """Core testing logic, used in all other expanded TestCase classes."""

    def setUp(self):
        pass
