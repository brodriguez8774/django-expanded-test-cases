"""
Imports logic for "django_expanded_test_cases/test_cases/" folder.
Makes project imports to this folder behave like a standard file.
"""

# Expanded "Base" TestCase utility class.
from .base_test_case import BaseTestCase


# Expanded "Integration" TestCase utility class.
from .integration_test_case import IntegrationTestCase


# Expanded "Live Server" TestCase utility class.
try:
    from .live_server_test_case import LiveServerTestCase
except ModuleNotFoundError:
    # Project likely does not have DjangoChannels package installed.
    # This is okay, as we don't want this logic as a hard requirement to use this library.
    pass
