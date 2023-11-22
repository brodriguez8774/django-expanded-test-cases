"""
Imports logic for "django_expanded_test_cases/mixins/" folder.
Makes project imports to this folder behave like a standard file.
"""

# Expanded "Base" TestCase utility mixins.
from .core_mixin import CoreTestCaseMixin


# Expanded "Integration" TestCase utility mixins.
from .response_mixin import ResponseTestCaseMixin


# Expanded "LiveServer" TestCase utility mixins.
try:
    from .live_server_mixin import LiveServerMixin
except ModuleNotFoundError:
    # Project likely does not have selenium package installed.
    # This is okay, as we don't want this logic as a hard requirement to use this library.

    # However, we do want to define a dummy class to give feedback errors.
    class LiveServerTestCase():
        err_msg = """
        Cannot use LiveServer TestCases class without "selenium" package installed.
        To use these TestCases, add the following packages to your project:
            * selenium              # Required
            * channels              # Optional, used in ChannelsLiveServerTestCase only.
            * daphne                # Optional, used in ChannelsLiveServerTestCase only.

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
