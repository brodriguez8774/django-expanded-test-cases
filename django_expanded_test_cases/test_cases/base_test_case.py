"""
Testing class for generalized logic.
"""

# Third-Party Imports.
from django.test import TestCase

# Internal Imports.
from django_expanded_test_cases.constants import (
    ETC_DEBUG_PRINT__LOGGING_SEPARATOR,
    ETC_DEBUG_PRINT__STD_OUT_SEPARATOR,
    ETC_OUTPUT_EMPHASIS_COLOR,
    ETC_OUTPUT_ERROR_COLOR,
)
from django_expanded_test_cases.mixins import CoreTestCaseMixin


class BaseTestCase(TestCase, CoreTestCaseMixin):
    """Generalized testing functionality. Builds upon Django's default TestCase class."""

    @classmethod
    def setUpClass(cls, *args, debug_print=None, **kwargs):
        """Test logic setup run at the start of class creation."""

        # Call parent logic.
        return_val = super().setUpClass()
        CoreTestCaseMixin.setUpClass(*args, debug_print=debug_print, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    @classmethod
    def setUpTestData(cls, *args, **kwargs):
        """Test logic setup run at the start of class creation, specifically for data setup."""

        # Call parent logic.
        return_val = super().setUpTestData()
        CoreTestCaseMixin.setUpTestData(*args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def setUp(self, *args, **kwargs):
        """Test logic setup run at the start of function/method execution."""

        # Call parent logic.
        return_val = super().setUp()
        CoreTestCaseMixin.setUp(self, *args, **kwargs)

        self._error_displayed = False

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def subTest(self, *args, **kwargs):
        """Test logic setup run every time we enter a subtest."""

        # Call parent logic.
        return_val = super().subTest()
        CoreTestCaseMixin.subTest(self, *args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        """Test logic setup run at the end of class execution, as part of termination/clean up."""

        # Call parent logic.
        return_val = super().tearDownClass()
        CoreTestCaseMixin.tearDownClass(*args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

    def tearDown(self, *args, **kwargs):
        """Test logic setup run at the end of function/method execution, as part of termination/clean up."""

        # Call parent logic.
        return_val = super().tearDown()
        CoreTestCaseMixin.tearDown(self, *args, **kwargs)

        # Return original python class value, if any.
        # ETC setup/teardown functions never contain a return value.
        return return_val

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
        if not hasattr(self, '_error_displayed') or not self._error_displayed:
            # Print error to both logging and standard console output.
            self._debug_print(
                '{0} {1} UnitTesting {2} {0}'.format(
                    ('=' * 10),
                    self.__class__.__name__,
                    type(err).__name__,
                ),
                fore=ETC_OUTPUT_ERROR_COLOR,
                style=ETC_OUTPUT_EMPHASIS_COLOR,
            )
            self._debug_print('{0}\n\n'.format(str(err)))

            # Save that we have output error.
            self._error_displayed = True

            # Optionally display custom debug-output separators for additional end-of-test clarity.
            if len(ETC_DEBUG_PRINT__STD_OUT_SEPARATOR) > 0:
                # Local std_out separator is defined. Print to console.
                self._debug_print(ETC_DEBUG_PRINT__STD_OUT_SEPARATOR)
            if len(ETC_DEBUG_PRINT__LOGGING_SEPARATOR) > 0:
                # Local std_out separator is defined. Log with logger.
                import logging
                logger = logging.getLogger(__name__)
                logger.error(ETC_DEBUG_PRINT__LOGGING_SEPARATOR)

    # region Default Test Function Overrides

    def fail(self, *args, **kwargs):
        """Fail immediately, with the given message."""

        try:
            return super().fail(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertEqual(self, *args, **kwargs):
        """Fail if the two objects are unequal as determined by the '==' operator."""

        try:
            return super().assertEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # NOTE: Depreciated as of Python3.2.
    def assertEquals(self, *args, **kwargs):
        """Fail if the two objects are unequal as determined by the '==' operator."""

        try:
            return super().assertEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotEqual(self, *args, **kwargs):
        """Fail if the two objects are equal as determined by the '!=' operator."""

        try:
            return super().assertNotEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # NOTE: Depreciated as of Python3.2.
    def assertNotEquals(self, *args, **kwargs):
        """Fail if the two objects are equal as determined by the '!=' operator."""

        try:
            return super().assertNotEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertTrue(self, *args, **kwargs):
        """Check that the expression is true."""

        try:
            return super().assertTrue(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertFalse(self, *args, **kwargs):
        """Check that the expression is false."""

        try:
            return super().assertFalse(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIs(self, *args, **kwargs):
        """Just like self.assertTrue(a is b), but with a nicer default message."""

        try:
            return super().assertIs(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsNot(self, *args, **kwargs):
        """Just like self.assertTrue(a is not b), but with a nicer default message."""

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
        """Same as self.assertTrue(obj is None), with a nicer default message."""

        try:
            return super().assertIsNone(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsNotNone(self, *args, **kwargs):
        """Included for symmetry with assertIsNone."""

        try:
            return super().assertIsNotNone(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIn(self, *args, **kwargs):
        """Just like self.assertTrue(a in b), but with a nicer default message."""

        try:
            return super().assertIn(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotIn(self, *args, **kwargs):
        """Just like self.assertTrue(a not in b), but with a nicer default message."""

        try:
            return super().assertNotIn(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertIsInstance(self, *args, **kwargs):
        """Same as self.assertTrue(isinstance(obj, cls)), with a nicer default message."""

        try:
            return super().assertIsInstance(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotIsInstance(self, *args, **kwargs):
        """Included for symmetry with assertIsInstance."""

        try:
            return super().assertNotIsInstance(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertRaises(self, *args, **kwargs):
        """Fail unless an exception of class expected_exception is raised
        by the callable when invoked with specified positional and
        keyword arguments. If a different type of exception is
        raised, it will not be caught, and the test case will be
        deemed to have suffered an error, exactly as for an
        unexpected exception.

        If called with the callable and arguments omitted, will return a
        context object used like this::

            with self.assertRaises(SomeException):
                do_something()

        An optional keyword argument 'msg' can be provided when assertRaises
        is used as a context object.

        The context manager keeps a reference to the exception as
        the 'exception' attribute. This allows you to inspect the
        exception after the assertion::

           with self.assertRaises(SomeException) as cm:
               do_something()
           the_exception = cm.exception
           self.assertEqual(the_exception.error_code, 3)
        """

        try:
            return super().assertRaises(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertRaisesRegex(self, *args, **kwargs):
        """Asserts that the message in a raised exception matches a regex.

        Args:
            expected_exception: Exception class expected to be raised.
            expected_regex: Regex (re.Pattern object or string) expected
                            to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                 when assertRaisesRegex is used as a context manager.
        """

        try:
            return super().assertRaisesRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertRaisesRegexp(self, *args, **kwargs):
        """Asserts that the message in a raised exception matches a regex.

        Args:
            expected_exception: Exception class expected to be raised.
            expected_regex: Regex (re.Pattern object or string) expected
                            to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                 when assertRaisesRegex is used as a context manager.
        """

        try:
            return super().assertRaisesRegexp(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertWarns(self, *args, **kwargs):
        """Fail unless a warning of class warnClass is triggered
        by the callable when invoked with specified positional and
        keyword arguments.  If a different type of warning is
        triggered, it will not be handled: depending on the other
        warning filtering rules in effect, it might be silenced, printed
        out, or raised as an exception.

        If called with the callable and arguments omitted, will return a
        context object used like this::

            with self.assertWarns(SomeWarning):
                do_something()

        An optional keyword argument 'msg' can be provided when assertWarns
        is used as a context object.

        The context manager keeps a reference to the first matching
        warning as the 'warning' attribute; similarly, the 'filename'
        and 'lineno' attributes give you information about the line
        of Python code from which the warning was triggered.
        This allows you to inspect the warning after the assertion::

           with self.assertWarns(SomeWarning) as cm:
               do_something()
           the_warning = cm.warning
           self.assertEqual(the_warning.some_attribute, 147)
        """

        try:
            return super().assertWarns(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertWarnsRegex(self, *args, **kwargs):
        """Asserts that the message in a triggered warning matches a regexp.
        Basic functioning is similar to assertWarns() with the addition
        that only warnings whose messages also match the regular expression
        are considered successful matches.

        Args:
            expected_warning: Warning class expected to be triggered.
            expected_regex: Regex (re.Pattern object or string) expected
                            to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                 when assertWarnsRegex is used as a context manager.
        """

        try:
            return super().assertWarnsRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertWarnsMessage(self, *args, **kwargs):
        """Same as assertRaisesMessage but for assertWarns() instead of assertRaises()."""

        try:
            return super().assertWarnsMessage(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertLogs(self, *args, **kwargs):
        """Fail unless a log message of level *level* or higher is emitted
        on *logger_name* or its children.  If omitted, *level* defaults to
        INFO and *logger* defaults to the root logger.

        This method must be used as a context manager, and will yield
        a recording object with two attributes: `output` and `records`.
        At the end of the context manager, the `output` attribute will
        be a list of the matching formatted log messages and the
        `records` attribute will be a list of the corresponding LogRecord
        objects.

        Example::

            with self.assertLogs('foo', level='INFO') as cm:
                logging.getLogger('foo').info('first message')
                logging.getLogger('foo.bar').error('second message')
            self.assertEqual(cm.output, ['INFO:foo:first message',
                                         'ERROR:foo.bar:second message'])
        """

        try:
            return super().assertLogs(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # NOTE: New as of Python 3.10.
    def assertNoLogs(self, *args, **kwargs):
        """Fail unless no log messages of level *level* or higher are emitted
        on *logger_name* or its children.

        This method must be used as a context manager.
        """

        try:
            return super().assertNoLogs(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertAlmostEqual(self, *args, **kwargs):
        """Fail if the two objects are unequal as determined by their
        difference rounded to the given number of decimal places
        (default 7) and comparing to zero, or by comparing that the
        difference between the two objects is more than the given
        delta.

        Note that decimal places (from zero) are usually not the same
        as significant digits (measured from the most significant digit).

        If the two objects compare equal then they will automatically
        compare almost equal.
        """

        try:
            return super().assertAlmostEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertAlmostEquals(self, *args, **kwargs):
        """Fail if the two objects are unequal as determined by their
        difference rounded to the given number of decimal places
        (default 7) and comparing to zero, or by comparing that the
        difference between the two objects is more than the given
        delta.

        Note that decimal places (from zero) are usually not the same
        as significant digits (measured from the most significant digit).

        If the two objects compare equal then they will automatically
        compare almost equal.
        """

        try:
            return super().assertAlmostEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotAlmostEqual(self, *args, **kwargs):
        """Fail if the two objects are equal as determined by their
        difference rounded to the given number of decimal places
        (default 7) and comparing to zero, or by comparing that the
        difference between the two objects is less than the given delta.

        Note that decimal places (from zero) are usually not the same
        as significant digits (measured from the most significant digit).

        Objects that are equal automatically fail.
        """

        try:
            return super().assertNotAlmostEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertNotAlmostEquals(self, *args, **kwargs):
        """Fail if the two objects are equal as determined by their
        difference rounded to the given number of decimal places
        (default 7) and comparing to zero, or by comparing that the
        difference between the two objects is less than the given delta.

        Note that decimal places (from zero) are usually not the same
        as significant digits (measured from the most significant digit).

        Objects that are equal automatically fail.
        """

        try:
            return super().assertNotAlmostEquals(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertGreater(self, *args, **kwargs):
        """Just like self.assertTrue(a > b), but with a nicer default message."""

        try:
            return super().assertGreater(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertGreaterEqual(self, *args, **kwargs):
        """Just like self.assertTrue(a >= b), but with a nicer default message."""

        try:
            return super().assertGreaterEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertLess(self, *args, **kwargs):
        """Just like self.assertTrue(a < b), but with a nicer default message."""

        try:
            return super().assertLess(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertLessEqual(self, *args, **kwargs):
        """Just like self.assertTrue(a <= b), but with a nicer default message."""

        try:
            return super().assertLessEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertRegex(self, *args, **kwargs):
        """Fail the test unless the text matches the regular expression."""

        try:
            return super().assertRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertRegexpMatches(self, *args, **kwargs):
        """Fail the test unless the text matches the regular expression."""

        try:
            return super().assertRegexpMatches(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertNotRegex(self, *args, **kwargs):
        """Fail the test if the text matches the regular expression."""

        try:
            return super().assertNotRegex(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python 3.2.
    def assertNotRegexpMatches(self, *args, **kwargs):
        """Fail the test if the text matches the regular expression."""
        try:
            return super().assertNotRegexpMatches(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertCountEqual(self, *args, **kwargs):
        """Asserts that two iterables have the same elements, the same number of
        times, without regard to order.

            self.assertEqual(Counter(list(first)),
                             Counter(list(second)))

         Example:
            - [0, 1, 1] and [1, 0, 1] compare equal.
            - [0, 0, 1] and [0, 1] compare unequal.

        """

        try:
            return super().assertCountEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertMultiLineEqual(self, *args, **kwargs):
        """Assert that two multi-line strings are equal."""

        try:
            return super().assertMultiLineEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertSequenceEqual(self, *args, **kwargs):
        """An equality assertion for ordered sequences (like lists and tuples).

        For the purposes of this function, a valid ordered sequence type is one
        which can be indexed, has a length, and has an equality operator.

        Args:
            seq1: The first sequence to compare.
            seq2: The second sequence to compare.
            seq_type: The expected datatype of the sequences, or None if no
                    datatype should be enforced.
            msg: Optional message to use on failure instead of a list of
                    differences.
        """

        try:
            return super().assertSequenceEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertListEqual(self, *args, **kwargs):
        """A list-specific equality assertion.

        Args:
            list1: The first list to compare.
            list2: The second list to compare.
            msg: Optional message to use on failure instead of a list of
                 differences.
        """

        try:
            return super().assertListEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertTupleEqual(self, *args, **kwargs):
        """A tuple-specific equality assertion.

        Args:
            tuple1: The first tuple to compare.
            tuple2: The second tuple to compare.
            msg: Optional message to use on failure instead of a list of
                 differences.
        """

        try:
            return super().assertTupleEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertSetEqual(self, *args, **kwargs):
        """A set-specific equality assertion.

        Args:
            set1: The first set to compare.
            set2: The second set to compare.
            msg: Optional message to use on failure instead of a list of
                 differences.

        assertSetEqual uses ducktyping to support different types of sets, and
        is optimized for sets specifically (parameters must support a
        difference method).
        """
        try:
            return super().assertSetEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    def assertDictEqual(self, *args, **kwargs):
        """Just like self.assertTrue(a is not b), but with a nicer default message."""

        try:
            return super().assertDictEqual(*args, **kwargs)
        except Exception as err:
            # If any error occurs, this makes sure it displays to console as the most recent output.
            self._handle_test_error(err)
            raise err

    # Depreciated as of Python ???.
    def assertDictContainsSubset(self, *args, **kwargs):
        """Checks whether dictionary is a superset of subset."""

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
