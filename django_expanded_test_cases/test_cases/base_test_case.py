"""
Testing class for generalized logic.
"""

# Third-Party Imports.
from django.test import TestCase

# Internal Imports.
from django_expanded_test_cases.constants import OUTPUT_EMPHASIS, OUTPUT_ERROR
from django_expanded_test_cases.mixins import CoreTestCaseMixin


class BaseTestCase(TestCase, CoreTestCaseMixin):
    """Generalized testing functionality. Builds upon Django's default TestCase class."""

    @classmethod
    def setUpClass(cls, debug_print=None):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreMixin setup logic.
        cls.set_up_class(debug_print=debug_print)

    @classmethod
    def setUpTestData(cls):
        """"""
        # Initialize default data models.
        cls.set_up_test_data()

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

        self._error_displayed = False

    def subTest(self, *args, **kwargs):
        # Call CoreMixin logic.
        self.sub_test()

        # Run parent logic.
        return super().subTest(*args, **kwargs)

    def _handle_test_error(self, err):
        """
        Handling for errors in UnitTesting.

        Mostly for ensuring consistent output on assertion failure.
        """
        # Only handle error if an earlier function call has not yet done so.
        # This helps prevent calling this logic multiple times on error (and thus spamming console output),
        # regardless of order of testing functions.
        # We also skip output such as when the logger is disabled.
        # This is likely due to temporary checks failing, and not a legitimate error/failure.
        if not self._error_displayed:
            # Print error to both logging and standard console output.
            self._debug_print(
                '{0} {1} UnitTesting {2} {0}'.format(
                    ('=' * 10),
                    self.__class__.__name__,
                    type(err).__name__,
                ),
                fore=OUTPUT_ERROR,
                style=OUTPUT_EMPHASIS,
            )
            self._debug_print('{0}\n\n'.format(str(err)))

            # Save that we have output error.
            self._error_displayed = True

    # region Default Test Function Overrides

    def fail(self, *args, **kwargs):
        try:
            return super().fail(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertEqual(self, *args, **kwargs):
        try:
            return super().assertEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # NOTE: Depreciated as of Python3.2.
    def assertEquals(self, *args, **kwargs):
        try:
            return super().assertEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotEqual(self, *args, **kwargs):
        try:
            return super().assertNotEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # NOTE: Depreciated as of Python3.2.
    def assertNotEquals(self, *args, **kwargs):
        try:
            return super().assertNotEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertTrue(self, *args, **kwargs):
        try:
            return super().assertTrue(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertFalse(self, *args, **kwargs):
        try:
            return super().assertFalse(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIs(self, *args, **kwargs):
        try:
            return super().assertIs(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsNot(self, *args, **kwargs):
        try:
            return super().assertIsNot(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNot(self, *args, **kwargs):
        try:
            return super().assertNot(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsNone(self, *args, **kwargs):
        try:
            return super().assertIsNone(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsNotNone(self, *args, **kwargs):
        try:
            return super().assertIsNotNone(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIn(self, *args, **kwargs):
        try:
            return super().assertIn(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotIn(self, *args, **kwargs):
        try:
            return super().assertNotIn(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsInstance(self, *args, **kwargs):
        try:
            return super().assertIsInstance(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotIsInstance(self, *args, **kwargs):
        try:
            return super().assertNotIsInstance(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertRaises(self, *args, **kwargs):
        try:
            return super().assertRaises(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertRaisesRegex(self, *args, **kwargs):
        try:
            return super().assertRaisesRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertRaisesRegexp(self, *args, **kwargs):
        try:
            return super().assertRaisesRegexp(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertWarns(self, *args, **kwargs):
        try:
            return super().assertWarns(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertWarnsRegex(self, *args, **kwargs):
        try:
            return super().assertWarnsRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertWarnsMessage(self, *args, **kwargs):
        try:
            return super().assertWarnsMessage(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertLogs(self, *args, **kwargs):
        try:
            return super().assertLogs(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # NOTE: New as of Python 3.10.
    def assertNoLogs(self, *args, **kwargs):
        try:
            return super().assertNoLogs(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertAlmostEqual(self, *args, **kwargs):
        try:
            return super().assertAlmostEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertAlmostEquals(self, *args, **kwargs):
        try:
            return super().assertAlmostEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotAlmostEqual(self, *args, **kwargs):
        try:
            return super().assertNotAlmostEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertNotAlmostEquals(self, *args, **kwargs):
        try:
            return super().assertNotAlmostEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertGreater(self, *args, **kwargs):
        try:
            return super().assertGreater(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertGreaterEqual(self, *args, **kwargs):
        try:
            return super().assertGreaterEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertLess(self, *args, **kwargs):
        try:
            return super().assertLess(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertLessEqual(self, *args, **kwargs):
        try:
            return super().assertLessEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertRegex(self, *args, **kwargs):
        try:
            return super().assertRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertRegexpMatches(self, *args, **kwargs):
        try:
            return super().assertRegexpMatches(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotRegex(self, *args, **kwargs):
        try:
            return super().assertNotRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertNotRegexpMatches(self, *args, **kwargs):
        try:
            return super().assertNotRegexpMatches(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertCountEqual(self, *args, **kwargs):
        try:
            return super().assertCountEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertMultiLineEqual(self, *args, **kwargs):
        try:
            return super().assertMultiLineEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertSequenceEqual(self, *args, **kwargs):
        try:
            return super().assertSequenceEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertListEqual(self, *args, **kwargs):
        try:
            return super().assertListEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertTupleEqual(self, *args, **kwargs):
        try:
            return super().assertTupleEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertSetEqual(self, *args, **kwargs):
        try:
            return super().assertSetEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertDictEqual(self, *args, **kwargs):
        try:
            return super().assertDictEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python ???.
    def assertDictContainsSubset(self, *args, **kwargs):
        try:
            return super().assertDictContainsSubset(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # endregion Default Test Function Overrides


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
]
