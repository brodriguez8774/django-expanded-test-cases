"""
Custom Exception/Error classes for Django Expanded Test Cases project.
"""

# System Imports.
from abc import ABC


class ExpandedTestCasesBaseException(ABC, Exception):
    """General customized exception for ETC project.

    Holds boilerplate logic and should NOT be directly called.
    """
    def __init__(self, value):
        # Ensure expected type for exception message.
        if value is None:
            value = ''
        self.value = str(value).strip()

        # Populate to default value if not provided.
        if self.value == '':
            self.value = 'Runtime error for ExpandedTestCases package logic.'

    @property
    def exception(self):
        return self.value


class EtcSeleniumSetUpError(Exception):
    """Runtime error when setting up for Selenium testing."""


class EtcSeleniumRuntimeError(Exception):
    """Runtime error when using Selenium testing."""
