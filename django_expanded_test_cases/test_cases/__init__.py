"""
Imports logic for "django_expanded_test_cases/test_cases/" folder.
Makes project imports to this folder behave like a standard file.
"""

# Expanded "Base" TestCase utility class.
from .base_test_case import BaseTestCase


# Expanded "Integration" TestCase utility class.
from .integration_test_case import IntegrationTestCase


# Expanded "Django Live Server" TestCase utility class.
try:
    from .live_server_test_case import LiveServerTestCase
except ModuleNotFoundError:
    # Project likely does not have selenium package installed.
    # This is okay, as we don't want this logic as a hard requirement to use this library.

    # However, we do want to define a dummy class to give feedback errors.
    class LiveServerTestCase(BaseTestCase):
        err_msg = """
        Cannot use LiveServerTestCase class without "selenium" package installed.
        To use this TestCase, add the following packages to your project:
            * selenium              # Required

        For more information, see:
        https://www.selenium.dev/documentation/webdriver/getting_started/
        """
        @classmethod
        def setUpClass(cls):
            raise Exception(cls.err_msg)

        def setUp(self):
            raise Exception(self.err_msg)

        def __int__(self):
            raise Exception(self.err_msg)


# Expanded "Channels Live Server" TestCase utility class.
try:
    from .channels_live_server_test_case import ChannelsLiveServerTestCase
except ModuleNotFoundError:
    # Project likely does not have DjangoChannels package or associated daphne package installed.
    # This is okay, as we don't want this logic as a hard requirement to use this library.

    # However, we do want to define a dummy class to give feedback errors.
    class ChannelsLiveServerTestCase(BaseTestCase):
        err_msg = """
        Cannot use ChannelsLiveServerTestCase class without "channels" package installed.
        To use this TestCase, add the following packages to your project:
            * channels              # Required
            * daphne                # Required
            * selenium              # Required

        For more information, see:
        https://www.selenium.dev/documentation/webdriver/getting_started/
        """
        @classmethod
        def setUpClass(cls):
            raise Exception(cls.err_msg)

        def setUp(self):
            raise Exception(self.err_msg)

        def __int__(self):
            raise Exception(self.err_msg)
