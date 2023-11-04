"""
Tests for test_cases/base_test_case.py.
"""

# System Imports.
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings

# Internal Imports.
from django_expanded_test_cases import BaseTestCase
from django_expanded_test_cases.constants import (
    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
    ETC_OUTPUT_RESET_COLOR,
)


lorem_str = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec dui ex, convallis eu nulla dignissim, pretium luctus
tellus. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque
porttitor accumsan dapibus. Nulla gravida malesuada suscipit. Ut diam ante, viverra nec tincidunt sit amet, pulvinar
sit amet augue. Curabitur rutrum ut tortor vitae lobortis. Nulla tincidunt libero eros, non ullamcorper ipsum
condimentum nec. Quisque id diam ultrices lacus vehicula congue. Aenean luctus, velit non imperdiet porttitor, felis
leo lobortis quam, vitae porttitor nunc ligula convallis felis. Nullam aliquam fringilla mauris, at bibendum mauris
malesuada id. Nullam eu placerat augue. Vestibulum ultrices metus in nisl iaculis bibendum. Ut nec bibendum erat.
Curabitur pretium massa et eros rutrum volutpat.

Nulla nec lectus mollis, accumsan tellus non, ullamcorper leo. Pellentesque ac risus ut est dignissim dictum a ac
sapien. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas vitae massa vel
nisi varius finibus. In hac habitasse platea dictumst. Nam lorem sapien, auctor ac velit ut, venenatis malesuada mauris.
Vestibulum rhoncus, est at tristique laoreet, ipsum magna feugiat libero, quis interdum odio tellus non diam.
Suspendisse mattis aliquam arcu, in efficitur velit mattis at. Sed sodales purus in nisl interdum mollis. Aenean pretium
volutpat nibh sit amet sagittis. Suspendisse dignissim egestas elit, sed efficitur massa consectetur eu. Phasellus a
sodales velit. Donec ac viverra ex.

Ut fringilla sem nec consequat rutrum. Nunc pharetra vel purus vulputate pharetra. Nulla eget euismod nisl. Etiam
tincidunt nulla at viverra feugiat. Donec efficitur ante in dui posuere blandit sit amet tincidunt enim. Aenean
fermentum maximus nisl, quis consectetur massa interdum quis. Maecenas convallis tincidunt orci et maximus. Phasellus
sit amet vestibulum purus, sit amet vestibulum neque. Fusce aliquam leo vitae neque egestas, et lobortis tortor
tristique. Ut tempor pharetra nibh ac pretium. Suspendisse ante sem, vestibulum in volutpat at, iaculis vitae libero.
Aenean faucibus interdum rutrum. Curabitur blandit ac lectus quis posuere. Donec nisl purus, pellentesque vitae ligula
eget, pharetra gravida nulla.

Nulla pharetra nisl non ligula tempus, non dictum nisi aliquet. Sed volutpat velit sed mauris feugiat, eget porttitor
odio hendrerit. Morbi ac leo molestie, aliquam eros eu, dapibus neque. Duis rhoncus elit a justo lacinia mattis. Nullam
commodo tortor nisl, ac suscipit nisl sodales scelerisque. Mauris nec turpis ac lacus accumsan scelerisque a id neque.
Ut vel mi et nisl cursus egestas.

Phasellus posuere vitae felis vitae laoreet. Aenean tellus lorem, rhoncus ut consequat nec, finibus vel est. Etiam nisl
ante, tincidunt at ante vitae, iaculis rutrum erat. Quisque est massa, molestie eget consectetur vel, eleifend in arcu.
Vestibulum elementum nisl ut lorem fermentum viverra. Quisque augue dui, finibus ut consectetur tempor, bibendum non ex.
Nunc pretium ipsum in nulla accumsan pretium. Mauris nec volutpat leo, nec venenatis lacus. Quisque non magna id ipsum
ullamcorper iaculis sed sit amet ligula. Morbi sem lacus, tempor id eros sed, vestibulum sollicitudin velit. Cras sed
tortor ante. Fusce tincidunt, massa sed fermentum ultricies, justo ipsum venenatis purus, quis mollis nunc eros et
libero.
"""


class BaseClassTest(BaseTestCase):
    """Tests for BaseTestCase class."""

    def get_logging_output(self, log_capture, record_num):
        """Helper function to read captured logging output."""
        return str(log_capture.records[record_num].message).strip()

    # region Assertion Tests

    def test__assertText__success(self):
        """
        Tests assertText() function, in cases when it should succeed.
        """
        with self.subTest('Empty string'):
            self.assertText('', '')

        with self.subTest('Single character'):
            # Basic match.
            self.assertText('a', 'a')
            self.assertText(1, 1)
            self.assertText('1', 1)
            self.assertText(1, '1')

            # Match with outer whitespace.
            self.assertText(' a ', 'a')
            self.assertText('a', ' a ')
            self.assertText(' a ', ' a ')

        with self.subTest('Small string'):
            # Basic match.
            self.assertText('abc', 'abc')

            # Match with inner whitespace.
            self.assertText('a b c', 'a b c')

            # Match with outer whitespace.
            self.assertText(' abc ', 'abc')
            self.assertText('abc', ' abc ')
            self.assertText(' abc ', ' abc ')

            # Match with inner and outer whitespace.
            self.assertText(' a b c ', 'a b c')
            self.assertText('a b c', ' a b c ')
            self.assertText(' a b c ', ' a b c ')

        with self.subTest('Large string'):
            # Full lorem.
            self.assertText(lorem_str, lorem_str)

            # Substring match.
            lorem_len = len(lorem_str)
            self.assertText(lorem_str[:int(lorem_len / 2)], lorem_str[:int(lorem_len / 2)])
            self.assertText(lorem_str[int(lorem_len / 2):], lorem_str[int(lorem_len / 2):])

    def test__assertText__fail(self):
        """
        Tests assertText() function, in cases when it should fail.
        """
        exception_msg = '\'{0}\' != \'{1}\'\n- {0}\n{2}+ {1}\n{3}'

        with self.subTest('Single character mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertText('a', 'b')
            self.assertEqual(exception_msg.format('a', 'b', '', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertText('a', 'A')
            self.assertEqual(exception_msg.format('a', 'A', '', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertText('a', 1)
            self.assertEqual(exception_msg.format('a', '1', '', ''), str(err.exception))

        with self.subTest('Whitespace mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertText('a b c', 'abc')
            self.assertEqual(exception_msg.format('a b c', 'abc', '?  - -\n', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertText('abc', 'a b c')
            self.assertEqual(exception_msg.format('abc', 'a b c', '', '?  + +\n'), str(err.exception))

        with self.subTest('Inner value mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertText('This is a test sentence.', 'This is a test')
            self.assertEqual(
                exception_msg.format(
                    'This is a test sentence.',
                    'This is a test',
                    '?               ----------\n',
                    '',
                ),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertText('This is a test sentence.', 'This is test sentence.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'This is test sentence.', '?        --\n', ''),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertText('This is a test sentence.', 'test sentence.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'test sentence.', '? ----------\n', ''),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertText('This is a test sentence.', 'This is a test.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'This is a test.', '?               ---------\n', ''),
                str(err.exception),
            )

        with self.subTest('Large string'):
            half_lorem_len = int(len(lorem_str) / 2)

            # With character replaced.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len - 1)] + 'z' + lorem_str[(half_lorem_len + 1):]
                self.assertText(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

            # With character added.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len)] + 'z' + lorem_str[(half_lorem_len + 1):]
                self.assertText(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

            # With character removed.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len - 1)] + lorem_str[(half_lorem_len + 1):]
                self.assertText(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

    def test__assertText_coloring__missing_lines(self):
        """Tests assertText() function color output, when assertion fails due to incorrect line counts.

        When lines are present, character counts and character values should fully match.
        """
        with self.subTest('With expected as empty'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('', 'Actuals has values here. Expected does not.')
            std_out_lines = std_out.getvalue().split('\n')[3:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[5], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Actuals has values here. Expected does not.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[13], '')

        with self.subTest('With actuals as empty'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Expected has values here. Actuals does not.', '')
            std_out_lines = std_out.getvalue().split('\n')[5:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Expected has values here. Actuals does not.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[9], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[13], '')

        with self.subTest('With expected as empty and actuals as multi-line'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('', 'Actuals has values here.\nExpected does not.')
            std_out_lines = std_out.getvalue().split('\n')[4:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[5], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Actuals has values here.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], '{0}Expected does not.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[13], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[14], '')

        with self.subTest('With actuals as empty and expected as multi-line'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Expected has values here.\nActuals does not.', '')
            std_out_lines = std_out.getvalue().split('\n')[4:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Expected has values here.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], '{0}Actuals does not.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[9], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[10], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[13], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[14], '')

        with self.subTest('With expected as one line less - At end'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('One line.', 'One line.\nTwo line.')
            print('std_out.getvalue():')
            print(std_out.getvalue())
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[5], '{0}One line.{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[9], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[10], '{0}One line.{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[11], '{0}Two line.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[12], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[13], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[14], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[15], '')

        with self.subTest('With actuals as one line less - At end'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('One line.\nTwo line.', 'One line.')
            std_out_lines = std_out.getvalue().split('\n')[5:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[5], '{0}One line.{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[6], '{0}Two line.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[9], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[10], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[11], '{0}One line.{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(std_out_lines[12], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[13], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[14], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[15], '')

    def test__assertText_coloring__missing_characters(self):
        """Tests assertText() function color output, when assertion fails due to inccorect character counts.

        All tests here should have equal line counts, but char counts per-line won't match.
        For lines that have equal char counts, the characters should fully match.
        """
        with self.subTest('With expected as one char missing - At start'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('esting.', 'Testing.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}esting.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Testing.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With actuals as one char missing - At start'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing.', 'esting.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Testing.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}esting.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With expected as multiple characters missing - At start'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('sting.', 'Testing.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}sting.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Testing.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With actuals as multiple characters missing - At start'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing.', 'sting.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Testing.{1}'.format(ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}sting.{1}'.format(ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With expected as one char missing - At middle'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Tesing.', 'Testing.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Tes{1}ing.{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Tes{1}ting.{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With actuals as one char missing - At middle'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing.', 'Tesing.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Tes{1}ting.{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Tes{1}ing.{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With expected as multiple characters missing - At middle'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Teng.', 'Testing.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Te{1}ng.{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Te{1}sting.{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With actuals as multiple characters missing - At middle'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing.', 'Teng.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Te{1}sting.{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Te{1}ng.{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With expected as one char missing - At end'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing', 'Testing.')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Testing{1}{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Testing{1}.{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With actuals as one char missing - At end'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing.', 'Testing')
            std_out_lines = std_out.getvalue().split('\n')[6:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Testing{1}.{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Testing{1}{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With expected as multiple characters missing - At end'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Test', 'Testing.')
            std_out_lines = std_out.getvalue().split('\n')[5:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Test{1}{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Test{1}ing.{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With actuals as multiple characters missing - At end'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('Testing.', 'Test')
            std_out_lines = std_out.getvalue().split('\n')[5:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}Test{1}ing.{2}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_EXPECTED_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}Test{1}{2}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_ACTUALS_ERROR_COLOR, ETC_OUTPUT_RESET_COLOR),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

    def test__assertText_coloring__wrong_characters(self):
        """Tests assertText() function color output, when assertion fails due incorrect characters.

        All tests here should have equal line counts and char counts per-line.
        """
        with self.subTest('With wrong character at start - Small str'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('aBC', 'ABC')
            std_out_lines = std_out.getvalue().split('\n')[7:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}a{1}BC{2}'.format(
                    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}A{1}BC{2}'.format(
                    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With wrong characters at start - Larger str'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('tHIS is a test value.', 'This is a test value.')
            std_out_lines = std_out.getvalue().split('\n')[7:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}tHIS{1} is a test value.{2}'.format(
                    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}This{1} is a test value.{2}'.format(
                    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With wrong character at middle - Small str'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('AbC', 'ABC')
            std_out_lines = std_out.getvalue().split('\n')[7:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}A{1}b{0}C{2}'.format(
                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}A{1}B{0}C{2}'.format(
                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With wrong character at middle - Larger str'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('This IS A TEST value.', 'This is a test value.')
            std_out_lines = std_out.getvalue().split('\n')[5:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}This {1}IS{0} {1}A{0} {1}TEST{0} value.{2}'.format(
                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}This {1}is{0} {1}a{0} {1}test{0} value.{2}'.format(
                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With wrong character at end - Small str'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('ABc', 'ABC')
            std_out_lines = std_out.getvalue().split('\n')[7:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}AB{1}c{2}'.format(
                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}AB{1}C{2}'.format(
                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

        with self.subTest('With wrong characters at end - Larger str'):
            std_out = StringIO()
            with redirect_stdout(std_out):
                with self.assertRaises(AssertionError):
                    self.assertText('This is a test VALUE!', 'This is a test value.')
            std_out_lines = std_out.getvalue().split('\n')[5:]

            # Test all line values.
            self.assertEqual(std_out_lines[0], '')
            self.assertEqual(std_out_lines[1], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[2], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[3], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[4], '{0}EXPECTED:{1}'.format(ETC_OUTPUT_EXPECTED_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[5],
                '{0}This is a test {1}VALUE!{2}'.format(
                    ETC_OUTPUT_EXPECTED_MATCH_COLOR,
                    ETC_OUTPUT_EXPECTED_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[6], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[7], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[8], '{0}ACTUAL:{1}'.format(ETC_OUTPUT_ACTUALS_MATCH_COLOR, ETC_OUTPUT_RESET_COLOR))
            self.assertEqual(
                std_out_lines[9],
                '{0}This is a test {1}value.{2}'.format(
                    ETC_OUTPUT_ACTUALS_MATCH_COLOR,
                    ETC_OUTPUT_ACTUALS_ERROR_COLOR,
                    ETC_OUTPUT_RESET_COLOR,
                ),
            )
            self.assertEqual(std_out_lines[10], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[11], ETC_OUTPUT_RESET_COLOR)
            self.assertEqual(std_out_lines[12], '')

    def test__assertTextStartsWith__success(self):
        """
        Tests assertTextStartsWith() function, in cases when it should succeed.
        """
        with self.subTest('Empty string'):
            self.assertTextStartsWith('', '')

        with self.subTest('Single character'):
            # Basic match.
            self.assertTextStartsWith('a', 'a')
            self.assertTextStartsWith(1, 1)
            self.assertTextStartsWith('1', 1)
            self.assertTextStartsWith(1, '1')

            # Match with outer whitespace.
            self.assertTextStartsWith(' a ', 'a')
            self.assertTextStartsWith('a', ' a ')
            self.assertTextStartsWith(' a ', ' a ')

        with self.subTest('Small string'):
            # Basic match.
            self.assertTextStartsWith('abc', 'abc')
            self.assertTextStartsWith('ab', 'abc')
            self.assertTextStartsWith('a', 'abc')

            # Match with inner whitespace.
            self.assertTextStartsWith('a b c', 'a b c')
            self.assertTextStartsWith('a b', 'a b c')
            self.assertTextStartsWith('a', 'a b c')

            # Match with outer whitespace.
            self.assertTextStartsWith(' abc ', 'abc')
            self.assertTextStartsWith(' ab ', 'abc')
            self.assertTextStartsWith(' a ', 'abc')
            self.assertTextStartsWith('abc', ' abc ')
            self.assertTextStartsWith('ab', ' abc ')
            self.assertTextStartsWith('a', ' abc ')
            self.assertTextStartsWith(' abc ', ' abc ')
            self.assertTextStartsWith(' ab ', ' abc ')
            self.assertTextStartsWith(' a ', ' abc ')

            # Match with inner and outer whitespace.
            self.assertTextStartsWith(' a b c ', 'a b c')
            self.assertTextStartsWith(' a b ', 'a b c')
            self.assertTextStartsWith(' a ', 'a b c')
            self.assertTextStartsWith('a b c', ' a b c ')
            self.assertTextStartsWith('a b', ' a b c ')
            self.assertTextStartsWith('a', ' a b c ')
            self.assertTextStartsWith(' a b c ', ' a b c ')
            self.assertTextStartsWith(' a b ', ' a b c ')
            self.assertTextStartsWith(' a ', ' a b c ')

        with self.subTest('Large string'):
            # Full lorem.
            self.assertTextStartsWith(lorem_str, lorem_str)

            # Substring match.
            lorem_len = len(lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len - 1)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len - 2)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len - 3)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len - 4)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len - 5)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len / 2)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len / 3)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len / 4)], lorem_str)
            self.assertTextStartsWith(lorem_str[:int(lorem_len / 5)], lorem_str)

    def test__assertTextStartsWith__fail(self):
        """
        Tests assertTextStartsWith() function, in cases when it should fail.
        """
        exception_msg = '\'{0}\' != \'{1}\'\n- {0}\n{2}+ {1}\n{3}'

        with self.subTest('Single character mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('a', 'b')
            self.assertEqual(exception_msg.format('a', 'b', '', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('a', 'A')
            self.assertEqual(exception_msg.format('a', 'A', '', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('a', 1)
            self.assertEqual( exception_msg.format('a', '1', '', ''), str(err.exception))

        with self.subTest('Whitespace mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('a b c', 'abc')
            self.assertEqual(exception_msg.format('a b c', 'abc', '?  - -\n', ''), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('a b', 'abc')
            self.assertEqual(exception_msg.format('a b', 'abc', '?  -\n', '?   +\n'), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('abc', 'a b c')
            self.assertEqual(exception_msg.format('abc', 'a b c', '', '?  + +\n'), str(err.exception))
            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('ab', 'a b c')
            self.assertEqual(exception_msg.format('ab', 'a b c', '', ''), str(err.exception))

        with self.subTest('Inner value mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('This is a test sentence.', 'This is test sentence.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'This is test sentence.', '?        --\n', ''),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('This is a test sentence.', 'test sentence.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'test sentence.', '? ----------\n', ''),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertTextStartsWith('This is a test sentence.', 'This is a test.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'This is a test.', '?               ---------\n', ''),
                str(err.exception),
            )

        with self.subTest('Large string'):
            half_lorem_len = int(len(lorem_str) / 2)

            # With character replaced.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len - 1)] + 'z' + lorem_str[(half_lorem_len + 1):]
                self.assertTextStartsWith(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

            # With character added.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len)] + 'z' + lorem_str[(half_lorem_len + 1):]
                self.assertTextStartsWith(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

            # With character removed.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len - 1)] + lorem_str[(half_lorem_len + 1):]
                self.assertTextStartsWith(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

    def test__assertTextEndsWith__success(self):
        """
        Tests assertTextEndsWith() function, in cases when it should succeed.
        """
        with self.subTest('Empty string'):
            self.assertTextEndsWith('', '')

        with self.subTest('Single character'):
            # Basic match.
            self.assertTextEndsWith('a', 'a')
            self.assertTextEndsWith(1, 1)
            self.assertTextEndsWith('1', 1)
            self.assertTextEndsWith(1, '1')

            # Match with outer whitespace.
            self.assertTextEndsWith(' a ', 'a')
            self.assertTextEndsWith('a', ' a ')
            self.assertTextEndsWith(' a ', ' a ')

        with self.subTest('Small string'):
            # Basic match.
            self.assertTextEndsWith('abc', 'abc')
            self.assertTextEndsWith('bc', 'abc')
            self.assertTextEndsWith('c', 'abc')

            # Match with inner whitespace.
            self.assertTextEndsWith('a b c', 'a b c')
            self.assertTextEndsWith('b c', 'a b c')
            self.assertTextEndsWith('c', 'a b c')

            # Match with outer whitespace.
            self.assertTextEndsWith(' abc ', 'abc')
            self.assertTextEndsWith(' bc ', 'abc')
            self.assertTextEndsWith(' c ', 'abc')
            self.assertTextEndsWith('abc', ' abc ')
            self.assertTextEndsWith('bc', ' abc ')
            self.assertTextEndsWith('c', ' abc ')
            self.assertTextEndsWith(' abc ', ' abc ')
            self.assertTextEndsWith(' bc ', ' abc ')
            self.assertTextEndsWith(' c ', ' abc ')

            # Match with inner and outer whitespace.
            self.assertTextEndsWith(' a b c ', 'a b c')
            self.assertTextEndsWith(' b c ', 'a b c')
            self.assertTextEndsWith(' c ', 'a b c')
            self.assertTextEndsWith('a b c', ' a b c ')
            self.assertTextEndsWith('b c', ' a b c ')
            self.assertTextEndsWith('c', ' a b c ')
            self.assertTextEndsWith(' a b c ', ' a b c ')
            self.assertTextEndsWith(' b c ', ' a b c ')
            self.assertTextEndsWith(' c ', ' a b c ')

        with self.subTest('Large string'):
            # Full lorem.
            self.assertTextEndsWith(lorem_str, lorem_str)

            # Substring match.
            lorem_len = len(lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len - 1):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len - 2):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len - 3):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len - 4):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len - 5):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len / 2):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len / 3):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len / 4):], lorem_str)
            self.assertTextEndsWith(lorem_str[int(lorem_len / 5):], lorem_str)

    def test__assertTextEndsWith__fail(self):
        """
        Tests assertTextEndsWith() function, in cases when it should fail.
        """
        exception_msg = '\'{0}\' != \'{1}\'\n- {0}\n{2}+ {1}\n{3}'

        with self.subTest('Single character mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('a', 'b')
            self.assertEqual(exception_msg.format('a', 'b', '', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('a', 'A')
            self.assertEqual(exception_msg.format('a', 'A', '', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('a', 1)
            self.assertEqual(exception_msg.format('a', '1', '', ''), str(err.exception))

        with self.subTest('Whitespace mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('a b c', 'abc')
            self.assertEqual(exception_msg.format('a b c', 'abc', '?  - -\n', ''), str(err.exception))

            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('abc', 'a b c')
            self.assertEqual(exception_msg.format('abc', 'a b c', '', '?  + +\n'), str(err.exception))

        with self.subTest('Inner value mismatch'):
            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('This is a test sentence.', 'This is a test')
            self.assertEqual(
                exception_msg.format(
                    'This is a test sentence.',
                    'This is a test',
                    '?               ----------\n',
                    '',
                ),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('This is a test sentence.', 'This is test sentence.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'This is test sentence.', '?        --\n', ''),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('This is a test sentence.', 'test sentence.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'test sentence.', '? ----------\n', ''),
                str(err.exception),
            )

            with self.assertRaises(AssertionError) as err:
                self.assertTextEndsWith('This is a test sentence.', 'This is a test.')
            self.assertEqual(
                exception_msg.format('This is a test sentence.', 'This is a test.', '?               ---------\n', ''),
                str(err.exception),
            )

        with self.subTest('Large string'):
            half_lorem_len = int(len(lorem_str) / 2)

            # With character replaced.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len - 1)] + 'z' + lorem_str[(half_lorem_len + 1):]
                self.assertTextEndsWith(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

            # With character added.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len)] + 'z' + lorem_str[(half_lorem_len + 1):]
                self.assertTextEndsWith(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

            # With character removed.
            with self.assertRaises(AssertionError) as err:
                modified_str = lorem_str[:(half_lorem_len - 1)] + lorem_str[(half_lorem_len + 1):]
                self.assertTextEndsWith(lorem_str, modified_str)
            # self.assertEqual(str(err.exception), exception_msg)

    # endregion Assertion Tests

    # region User Management Function Tests

    def test__get_user__with_project_defaults(self):
        """
        Tests get_user() function.
        """
        with self.subTest('Test "test_superuser" user - With project defaults'):
            test_superuser = self.get_user('test_superuser')

            self.assertEqual(test_superuser, self.test_superuser)
            self.assertEqual(test_superuser.username, 'test_superuser')
            self.assertTrue(test_superuser.check_password('password'))
            self.assertEqual(test_superuser.unhashed_password, 'password')
            self.assertEqual(test_superuser.first_name, 'SuperUserFirst')
            self.assertEqual(test_superuser.last_name, 'SuperUserLast')
            self.assertEqual(test_superuser.email, 'super_user@example.com')
            self.assertEqual(test_superuser.is_superuser, True)
            self.assertEqual(test_superuser.is_staff, False)
            self.assertEqual(test_superuser.is_active, True)

        with self.subTest('Test "test_admin" user - With project defaults'):
            test_admin = self.get_user('test_admin')

            self.assertEqual(test_admin, self.test_admin)
            self.assertEqual(test_admin.username, 'test_admin')
            self.assertTrue(test_admin.check_password('password'))
            self.assertEqual(test_admin.unhashed_password, 'password')
            self.assertEqual(test_admin.first_name, 'AdminUserFirst')
            self.assertEqual(test_admin.last_name, 'AdminUserLast')
            self.assertEqual(test_admin.email, 'admin_user@example.com')
            self.assertEqual(test_admin.is_superuser, False)
            self.assertEqual(test_admin.is_staff, True)
            self.assertEqual(test_admin.is_active, True)

        with self.subTest('Test "test_inactive" user - With project defaults'):
            test_inactive = self.get_user('test_inactive')

            self.assertEqual(test_inactive, self.test_inactive_user)
            self.assertEqual(test_inactive.username, 'test_inactive')
            self.assertTrue(test_inactive.check_password('password'))
            self.assertEqual(test_inactive.unhashed_password, 'password')
            self.assertEqual(test_inactive.first_name, 'InactiveUserFirst')
            self.assertEqual(test_inactive.last_name, 'InactiveUserLast')
            self.assertEqual(test_inactive.email, 'inactive_user@example.com')
            self.assertEqual(test_inactive.is_superuser, False)
            self.assertEqual(test_inactive.is_staff, False)
            self.assertEqual(test_inactive.is_active, False)

        with self.subTest('Test "test_user" user - With project defaults'):
            test_user = self.get_user('test_user')

            self.assertEqual(test_user, self.test_user)
            self.assertEqual(test_user.username, 'test_user')
            self.assertTrue(test_user.check_password('password'))
            self.assertEqual(test_user.unhashed_password, 'password')
            self.assertEqual(test_user.first_name, 'UserFirst')
            self.assertEqual(test_user.last_name, 'UserLast')
            self.assertEqual(test_user.email, 'user@example.com')
            self.assertEqual(test_user.is_superuser, False)
            self.assertEqual(test_user.is_staff, False)
            self.assertEqual(test_user.is_active, True)

    def test__add_user_permission(self):
        """
        Tests add_user_permission() function.
        """
        # Generate dummy content_type.
        test_content_type = ContentType.objects.create(app_label='test_app', model='test_model')

        # Initialize Permission models.
        perm_1 = Permission.objects.create(
            content_type=test_content_type,
            codename='test_perm_1',
            name='Test Perm 1',
        )
        perm_2 = Permission.objects.create(
            content_type=test_content_type,
            codename='test_perm_2',
            name='Test Perm 2',
        )

        # Verify initial user Permissions.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add permission to default user'):
            # In context of this test, the "default user" is test_user.

            # Test adding permission.
            return_val = self.add_user_permission('test_perm_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add permission by direct model'):
            # Test adding permission.
            return_val = self.add_user_permission(perm_1, user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self.add_user_permission(perm_2, user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add permission by codename'):
            # Test adding permission.
            return_val = self.add_user_permission('test_perm_1', user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self.add_user_permission('test_perm_2', user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add permission by name'):
            # Test adding permission.
            return_val = self.add_user_permission('Test Perm 1', user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            return_val = self.add_user_permission('Test Perm 2', user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

        with self.subTest('Test add permission by class user'):
            # Test adding permission.
            self.user = 'test_user'
            return_val = self.add_user_permission('test_perm_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different permission.
            self.user = 'test_admin'
            return_val = self.add_user_permission('test_perm_2')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected permissions.
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset permission relations.
        self.test_user.user_permissions.remove(perm_1)
        self.test_admin.user_permissions.remove(perm_2)

        # Verify user Permission states.
        self.assertFalse(self.test_superuser.user_permissions.all().exists())
        self.assertFalse(self.test_admin.user_permissions.all().exists())
        self.assertFalse(self.test_user.user_permissions.all().exists())

    def test__add_user_group(self):
        """
        Tests add_user_group() function.
        """
        # Initialize Group models.
        group_1 = Group.objects.create(name='group_1')
        group_2 = Group.objects.create(name='group_2')

        # Verify initial user Groups.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add group to default user'):
            # In context of this test, the "default user" is test_user.

            # Test adding group.
            return_val = self.add_user_group('group_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add group to user by direct model'):
            # Test adding group.
            return_val = self.add_user_group(group_1, user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different group.
            return_val = self.add_user_group(group_2, user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add permission to user by name'):
            # Test adding group.
            return_val = self.add_user_group('group_1', user='test_user')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different group.
            return_val = self.add_user_group('group_2', user='test_admin')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

        with self.subTest('Test add group by class user'):
            # Test adding group.
            self.user = self.test_user
            return_val = self.add_user_group('group_1')
            self.assertEqual(return_val, self.test_user)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)

            # Verify other users are unaffected.
            self.assertFalse(self.test_admin.user_permissions.all().exists())
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

            # Test adding different group.
            self.user = self.test_admin
            return_val = self.add_user_group('group_2')
            self.assertEqual(return_val, self.test_admin)

            # Verify respective users received expected groups.
            self.assertEqual(self.test_user.groups.all().count(), 1)
            self.assertEqual(self.test_user.groups.all()[0], group_1)
            self.assertEqual(self.test_admin.groups.all().count(), 1)
            self.assertEqual(self.test_admin.groups.all()[0], group_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

        # Reset group relations.
        self.test_user.groups.remove(group_1)
        self.test_admin.groups.remove(group_2)

        # Verify user Group states.
        self.assertFalse(self.test_superuser.groups.all().exists())
        self.assertFalse(self.test_admin.groups.all().exists())
        self.assertFalse(self.test_user.groups.all().exists())

    # endregion User Management Function Tests

    # region Helper Function Tests

    def test__generate_get_url(self):
        """
        Tests generate_get_url() function.
        """
        with self.subTest('Generate from passed "url" param'):
            # Test no params.
            url = self.generate_get_url('http://127.0.0.1')
            self.assertText('http://127.0.0.1/', url)
            url = self.generate_get_url('http://127.0.0.1/')
            self.assertText('http://127.0.0.1/', url)
            url = self.generate_get_url('http://127.0.0.1/aaa')
            self.assertText('http://127.0.0.1/aaa/', url)
            url = self.generate_get_url('http://127.0.0.1/bbb/')
            self.assertText('http://127.0.0.1/bbb/', url)

            # Test one str param.
            url = self.generate_get_url('http://127.0.0.1/my-page', test_1='one')
            self.assertText('http://127.0.0.1/my-page/?test_1=one', url)

            # Test two str params.
            url = self.generate_get_url('http://127.0.0.1/my-page', test_1='one', test_2='two')
            self.assertText('http://127.0.0.1/my-page/?test_1=one&test_2=two', url)

            # Test one non-str simple param.
            url = self.generate_get_url('http://127.0.0.1/my-page', test_1=1)
            self.assertText('http://127.0.0.1/my-page/?test_1=1', url)

            # Test two non-str simple params.
            url = self.generate_get_url('http://127.0.0.1/my-page', test_1=1, test_2=True)
            self.assertText('http://127.0.0.1/my-page/?test_1=1&test_2=True', url)

            # Test one non-str complex param.
            url = self.generate_get_url('http://127.0.0.1/my-page', test_1=['a', 'b', 'c'])
            self.assertText('http://127.0.0.1/my-page/?test_1=%5B%27a%27%2C+%27b%27%2C+%27c%27%5D', url)

            # Test two non-str complex params.
            url = self.generate_get_url(
                'http://127.0.0.1/my-page',
                test_1=['foo', 'bar'],
                test_2={'cat': 'Tabby', 'dog': 'Spot'},
            )
            self.assertText(
                (
                    'http://127.0.0.1/my-page/?test_1=%5B%27foo%27%2C+%27bar%27%5D&test_2=%7B%27cat%27%3A+'
                    '%27Tabby%27%2C+%27dog%27%3A+%27Spot%27%7D'
                ),
                url,
            )

        with self.subTest('Generate from class "self.url" variable'):
            # Set class variable.
            self.url = 'http://127.0.0.1/test-page/'

            # Test no params.
            url = self.generate_get_url()
            self.assertText('http://127.0.0.1/test-page/', url)

            # Test one str param.
            url = self.generate_get_url(test_1='one')
            self.assertText('http://127.0.0.1/test-page/?test_1=one', url)

            # Test two str params.
            url = self.generate_get_url(test_1='one', test_2='two')
            self.assertText('http://127.0.0.1/test-page/?test_1=one&test_2=two', url)

            # Test one non-str simple param.
            url = self.generate_get_url(test_1=1)
            self.assertText('http://127.0.0.1/test-page/?test_1=1', url)

            # Test two non-str simple params.
            url = self.generate_get_url(test_1=1, test_2=True)
            self.assertText('http://127.0.0.1/test-page/?test_1=1&test_2=True', url)

            # Test one non-str complex param.
            url = self.generate_get_url(test_1=['a', 'b', 'c'])
            self.assertText('http://127.0.0.1/test-page/?test_1=%5B%27a%27%2C+%27b%27%2C+%27c%27%5D', url)

            # Test two non-str complex params.
            url = self.generate_get_url(test_1=['foo', 'bar'], test_2={'cat': 'Tabby', 'dog': 'Spot'})
            self.assertText(
                (
                    'http://127.0.0.1/test-page/?test_1=%5B%27foo%27%2C+%27bar%27%5D&test_2=%7B%27cat%27%3A+'
                    '%27Tabby%27%2C+%27dog%27%3A+%27Spot%27%7D'
                ),
                url,
            )

        with self.subTest('With mixed characters'):
            # Base url.
            url = self.generate_get_url('/my/url/here', test='testing stuff?<blah>weird_values-aaa')
            self.assertText('/my/url/here/?test=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

            # With ending slash.
            url = self.generate_get_url('/my/url/here/', test='testing stuff?<blah>weird_values-aaa')
            self.assertText('/my/url/here/?test=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

        with self.subTest('With extra ? to start query params'):
            # Base url.
            url = self.generate_get_url('/my/url/here?', my_value='test')
            self.assertText('/my/url/here/?my_value=test', url)

            # With ending slash.
            url = self.generate_get_url('/my/url/here/?', my_value='test')
            self.assertText('/my/url/here/?my_value=test', url)

        with self.subTest('With mixed characters and extra ? to start query params'):
            # Base url.
            url = self.generate_get_url('/my/url/here?', test='testing stuff?<blah>weird_values-aaa')
            self.assertText('/my/url/here/?test=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

            # With ending slash.
            url = self.generate_get_url('/my/url/here/?', test='testing stuff?<blah>weird_values-aaa')
            self.assertText('/my/url/here/?test=testing+stuff%3F%3Cblah%3Eweird_values-aaa', url)

        with self.subTest('With multiple instances of ? and /'):
            # Base url.
            url = self.generate_get_url('/my/url/here////???//', my_value='test')
            self.assertText('/my/url/here/?my_value=test', url)

    def assert_symbol_standardization(self, symbol_str, expected_return):
        """
        Helper sub-function for testing the standardization methods.
        """
        # Test in smaller child function.
        return_val = self.standardize_symbols(symbol_str)
        self.assertText(expected_return, return_val)

        # Test in full parent function.
        return_val = self.standardize_characters(symbol_str)
        self.assertText(expected_return, return_val)

    def assert_number_standardization(self, number_str, expected_return):
        """
        Helper sub-function for testing the standardization methods.
        """
        # Test in smaller child function.
        return_val = self.standardize_numbers(number_str)
        self.assertText(expected_return, return_val)

        # Test in full parent function.
        return_val = self.standardize_characters(number_str)
        self.assertText(expected_return, return_val)

    def assert_letter_standardization(self, letter_str, expected_return):
        """
        Helper sub-function for testing the standardization methods.
        """
        # Test in smaller child function.
        return_val = self.standardize_letters(letter_str)
        self.assertText(expected_return, return_val)

        # Test in full parent function.
        return_val = self.standardize_characters(letter_str)
        self.assertText(expected_return, return_val)

    def test__standardize_characters__symbols(self):
        """
        Tests symbols in standardize_characters() functions.
        """
        with self.subTest('Test standard spaces'):
            self.assert_symbol_standardization(
                '&#32; &#x20;  ',
                '     ',
            )

        with self.subTest('Test non-breaking spaces'):
            self.assert_symbol_standardization(
                '&#160; &#xA0; &#xa0; &nbsp;  ',
                '         ',
            )

        with self.subTest('Test exclamation mark'):
            self.assert_symbol_standardization(
                '&#33; &#x21; &excl; !',
                '! ! ! !',
            )

        with self.subTest('Test quotation'):
            self.assert_symbol_standardization(
                '&#34; &#x22; &quot; "',
                '" " " "',
            )

        with self.subTest('Test number sign'):
            self.assert_symbol_standardization(
                '&#35; &#x23; &num; #',
                '# # # #',
            )

        with self.subTest('Test dollar sign'):
            self.assert_symbol_standardization(
                '&#36; &#x24; &dollar; $',
                '$ $ $ $',
            )

        with self.subTest('Test percent sign'):
            self.assert_symbol_standardization(
                '&#37; &#x25; &percnt; %',
                '% % % %',
            )

        with self.subTest('Test ampersand'):
            self.assert_symbol_standardization(
                '&#38; &#x26; &amp; &',
                '& & & &',
            )

        with self.subTest('Test apostrophe'):
            self.assert_symbol_standardization(
                '&#39; &#x27; &apos; \'',
                "' ' ' '",
            )

        with self.subTest('Test opening parenthesis'):
            self.assert_symbol_standardization(
                '&#40; &#x28; &lpar; (',
                '( ( ( (',
            )

        with self.subTest('Test closing parenthesis'):
            self.assert_symbol_standardization(
                '&#41; &#x29; &rpar; )',
                ') ) ) )',
            )

        with self.subTest('Test asterisk'):
            self.assert_symbol_standardization(
                '&#42; &#x2A; &#x2a; &ast; *',
                '* * * * *',
            )

        with self.subTest('Test plus'):
            self.assert_symbol_standardization(
                '&#43; &#x2B; &#x2b; &plus; +',
                '+ + + + +',
            )

        with self.subTest('Test comma'):
            self.assert_symbol_standardization(
                '&#44; &#x2C; &#x2c; &comma; ,',
                ', , , , ,',
            )

        with self.subTest('Test minus'):
            self.assert_symbol_standardization(
                '&#45; &#8722; &#x2D; &#x2d; &minus; -',
                '- - - - - -',
            )

        with self.subTest('Test period'):
            self.assert_symbol_standardization(
                '&#46; &#x2E; &#x2e; &period; .',
                '. . . . .',
            )

        with self.subTest('Test slash'):
            self.assert_symbol_standardization(
                '&#47; &#x2F; &#x2f; &sol; /',
                '/ / / / /',
            )

        with self.subTest('Test colon'):
            self.assert_symbol_standardization(
                '&#58; &#x3A; &#x3a; &colon; :',
                ': : : : :',
            )

        with self.subTest('Test semicolon'):
            self.assert_symbol_standardization(
                '&#59; &#x3B; &#x3b; &semi; ;',
                '; ; ; ; ;',
            )

        with self.subTest('Test less than'):
            self.assert_symbol_standardization(
                '&#60; &#x3C; &#x3c; &lt; <',
                '< < < < <',
            )

        with self.subTest('Test equals'):
            self.assert_symbol_standardization(
                '&#61; &#x3D; &#x3d; &equals; =',
                '= = = = =',
            )

        with self.subTest('Test greater than'):
            self.assert_symbol_standardization(
                '&#62; &#x3E; &#x3e; &gt; >',
                '> > > > >',
            )

        with self.subTest('Test question mark'):
            self.assert_symbol_standardization(
                '&#63; &#x3F; &#x3f; &quest; ?',
                '? ? ? ? ?',
            )

        with self.subTest('Test at sign'):
            self.assert_symbol_standardization(
                '&#64; &#x40; &commat; @',
                '@ @ @ @',
            )

        with self.subTest('Test opening square bracket'):
            self.assert_symbol_standardization(
                '&#91; &#x5B; &#x5b; &lbrack; [',
                '[ [ [ [ [',
            )

        with self.subTest('Test backslash'):
            self.assert_symbol_standardization(
                '&#92; &#x5C; &#x5c; &bsol; \\',
                '\\ \\ \\ \\ \\',
            )

        with self.subTest('Test closing square bracket'):
            self.assert_symbol_standardization(
                '&#93; &#x5D; &#x5d; &rbrack; ]',
                '] ] ] ] ]',)

        with self.subTest('Test up arrow'):
            self.assert_symbol_standardization(
                '&#94; &#x5E; &#x5e; &Hat; ^',
                '^ ^ ^ ^ ^',
            )

        with self.subTest('Test underscore'):
            self.assert_symbol_standardization(
                '&#95; &#x5F; &#x5f; &lowbar; _',
                '_ _ _ _ _',
            )

        with self.subTest('Test grave accent'):
            self.assert_symbol_standardization(
                '&#96; &#x60; &grave; `',
                '` ` ` `',
            )

        with self.subTest('Test opening dict bracket'):
            self.assert_symbol_standardization(
                '&#123; &#x7B; &#x7b; &lbrace; {',
                '{ { { { {',
            )

        with self.subTest('Test pipe'):
            self.assert_symbol_standardization(
                '&#124; &#x7C; &#x7c; &vert; |',
                '| | | | |',
            )

        with self.subTest('Test closing dict bracket'):
            self.assert_symbol_standardization(
                '&#125; &#x7D; &#x7d; &rbrace; }',
                '} } } } }',
            )

        with self.subTest('Test tilde'):
            self.assert_symbol_standardization(
                '&#126; &#x7E; &#x7e; &tilde; ~',
                '~ ~ ~ ~ ~',
            )

    def test__standardize_characters__numbers(self):
        """
        Tests numbers in standardize_characters() functions.
        """
        with self.subTest('Test 0'):
            self.assert_number_standardization(
                '&#48; &#x30; 0',
                '0 0 0',
            )

        with self.subTest('Test 1'):
            self.assert_number_standardization(
                '&#49; &#x31; 1',
                '1 1 1',
            )

        with self.subTest('Test 2'):
            self.assert_number_standardization(
                '&#50; &#x32; 2',
                '2 2 2',
            )

        with self.subTest('Test 3'):
            self.assert_number_standardization(
                '&#51; &#x33; 3',
                '3 3 3',
            )

        with self.subTest('Test 4'):
            self.assert_number_standardization(
                '&#52; &#x34; 4',
                '4 4 4',
            )

        with self.subTest('Test 5'):
            self.assert_number_standardization(
                '&#53; &#x35; 5',
                '5 5 5',
            )

        with self.subTest('Test 6'):
            self.assert_number_standardization(
                '&#54; &#x36; 6',
                '6 6 6',
            )

        with self.subTest('Test 7'):
            self.assert_number_standardization(
                '&#55; &#x37; 7',
                '7 7 7',
            )

        with self.subTest('Test 8'):
            self.assert_number_standardization(
                '&#56; &#x38; 8',
                '8 8 8',
            )

        with self.subTest('Test 9'):
            self.assert_number_standardization(
                '&#57; &#x39; 9',
                '9 9 9',
            )

    def test__standardize_characters__letters(self):
        """
        Tests letters in standardize_characters() functions.
        """
        with self.subTest('Test A'):
            self.assert_letter_standardization(
                '&#65; &#x41; A',
                'A A A',
            )

        with self.subTest('Test B'):
            self.assert_letter_standardization(
                '&#66; &#x42; B',
                'B B B',
            )

        with self.subTest('Test C'):
            self.assert_letter_standardization(
                '&#67; &#x43; C',
                'C C C',
            )

        with self.subTest('Test D'):
            self.assert_letter_standardization(
                '&#68; &#x44; D',
                'D D D',
            )

        with self.subTest('Test E'):
            self.assert_letter_standardization(
                '&#69; &#x45; E',
                'E E E',
            )

        with self.subTest('Test F'):
            self.assert_letter_standardization(
                '&#70; &#x46; F',
                'F F F',
            )

        with self.subTest('Test G'):
            self.assert_letter_standardization(
                '&#71; &#x47; G',
                'G G G',
            )

        with self.subTest('Test H'):
            self.assert_letter_standardization(
                '&#72; &#x48; H',
                'H H H',
            )

        with self.subTest('Test I'):
            self.assert_letter_standardization(
                '&#73; &#x49; I',
                'I I I',
            )

        with self.subTest('Test J'):
            self.assert_letter_standardization(
                '&#74; &#x4A; &#x4a; J',
                'J J J J',
            )

        with self.subTest('Test K'):
            self.assert_letter_standardization(
                '&#75; &#x4B; &#x4b; K',
                'K K K K',
            )

        with self.subTest('Test L'):
            self.assert_letter_standardization(
                '&#76; &#x4C; &#x4c; L',
                'L L L L',
            )

        with self.subTest('Test M'):
            self.assert_letter_standardization(
                '&#77; &#x4D; &#x4d; M',
                'M M M M',
            )

        with self.subTest('Test N'):
            self.assert_letter_standardization(
                '&#78; &#x4E; &#x4e; N',
                'N N N N',
            )

        with self.subTest('Test O'):
            self.assert_letter_standardization(
                '&#79; &#x4F; &#x4f; O',
                'O O O O',
            )

        with self.subTest('Test P'):
            self.assert_letter_standardization(
                '&#80; &#x50; P',
                'P P P',
            )

        with self.subTest('Test Q'):
            self.assert_letter_standardization(
                '&#81; &#x51; Q',
                'Q Q Q',
            )

        with self.subTest('Test R'):
            self.assert_letter_standardization(
                '&#82; &#x52; R',
                'R R R',
            )

        with self.subTest('Test S'):
            self.assert_letter_standardization(
                '&#83; &#x53; S',
                'S S S',
            )

        with self.subTest('Test T'):
            self.assert_letter_standardization(
                '&#84; &#x54; T',
                'T T T',
            )

        with self.subTest('Test U'):
            self.assert_letter_standardization(
                '&#85; &#x55; U',
                'U U U',
            )

        with self.subTest('Test V'):
            self.assert_letter_standardization(
                '&#86; &#x56; V',
                'V V V',
            )

        with self.subTest('Test W'):
            self.assert_letter_standardization(
                '&#87; &#x57; W',
                'W W W',
            )

        with self.subTest('Test X'):
            self.assert_letter_standardization(
                '&#88; &#x58; X',
                'X X X',
            )

        with self.subTest('Test Y'):
            self.assert_letter_standardization(
                '&#89; &#x59; Y',
                'Y Y Y',
            )

        with self.subTest('Test Z'):
            self.assert_letter_standardization(
                '&#90; &#x5A; &#x5a; Z',
                'Z Z Z Z',
            )

        with self.subTest('Test a'):
            self.assert_letter_standardization(
                '&#97; &#x61; a',
                'a a a',
            )

        with self.subTest('Test b'):
            self.assert_letter_standardization(
                '&#98; &#x62; b',
                'b b b',
            )

        with self.subTest('Test c'):
            self.assert_letter_standardization(
                '&#99; &#x63; c',
                'c c c',
            )

        with self.subTest('Test d'):
            self.assert_letter_standardization(
                '&#100; &#x64; d',
                'd d d',
            )

        with self.subTest('Test e'):
            self.assert_letter_standardization(
                '&#101; &#x65; e',
                'e e e',
            )

        with self.subTest('Test f'):
            self.assert_letter_standardization(
                '&#102; &#x66; f',
                'f f f',
            )

        with self.subTest('Test g'):
            self.assert_letter_standardization(
                '&#103; &#x67; g',
                'g g g',
            )

        with self.subTest('Test h'):
            self.assert_letter_standardization(
                '&#104; &#x68; h',
                'h h h',
            )

        with self.subTest('Test i'):
            self.assert_letter_standardization(
                '&#105; &#x69; i',
                'i i i',
            )

        with self.subTest('Test j'):
            self.assert_letter_standardization(
                '&#106; &#x6A; &#x6a; j',
                'j j j j',
            )

        with self.subTest('Test k'):
            self.assert_letter_standardization(
                '&#107; &#x6B; &#x6b; k',
                'k k k k',
            )

        with self.subTest('Test l'):
            self.assert_letter_standardization(
                '&#108; &#x6C; &#x6c; l',
                'l l l l',
            )

        with self.subTest('Test m'):
            self.assert_letter_standardization(
                '&#109; &#x6D; &#x6d; m',
                'm m m m',
            )

        with self.subTest('Test n'):
            self.assert_letter_standardization(
                '&#110; &#x6E; &#x6e; n',
                'n n n n',
            )

        with self.subTest('Test o'):
            self.assert_letter_standardization(
                '&#111; &#x6F; &#x6f; o',
                'o o o o',
            )

        with self.subTest('Test p'):
            self.assert_letter_standardization(
                '&#112; &#x70; p',
                'p p p',
            )

        with self.subTest('Test q'):
            self.assert_letter_standardization(
                '&#113; &#x71; q',
                'q q q',
            )

        with self.subTest('Test r'):
            self.assert_letter_standardization(
                '&#114; &#x72; r',
                'r r r',
            )

        with self.subTest('Test s'):
            self.assert_letter_standardization(
                '&#115; &#x73; s',
                's s s',
            )

        with self.subTest('Test t'):
            self.assert_letter_standardization(
                '&#116; &#x74; t',
                't t t',
            )

        with self.subTest('Test u'):
            self.assert_letter_standardization(
                '&#117; &#x75; u',
                'u u u',
            )

        with self.subTest('Test v'):
            self.assert_letter_standardization(
                '&#118; &#x76; v',
                'v v v',
            )

        with self.subTest('Test w'):
            self.assert_letter_standardization(
                '&#119; &#x77; w',
                'w w w',
            )

        with self.subTest('Test x'):
            self.assert_letter_standardization(
                '&#120; &#x78; x',
                'x x x',
            )

        with self.subTest('Test y'):
            self.assert_letter_standardization(
                '&#121; &#x79; y',
                'y y y',
            )

        with self.subTest('Test z'):
            self.assert_letter_standardization(
                '&#122; &#x7A; &#x7a; z',
                'z z z z',
            )

    def test__standardize_newlines(self):
        """
        Tests standardize_newlines() function.
        """
        with self.subTest('Test <br> tag - Isolated'):
            return_val = self.standardize_newlines('<br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('</br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('<br/>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('<br />')
            self.assertText('', return_val)
        with self.subTest('Test <br> tag - As inner element'):
            return_val = self.standardize_newlines('A<br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A</br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A<br/>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A<br />B')
            self.assertText('A\nB', return_val)

        with self.subTest('Test single newline characters - Isolated'):
            return_val = self.standardize_newlines('\n')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\r\n')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n\r')
            self.assertText('', return_val)
        with self.subTest('Test single newline characters - As inner element'):
            return_val = self.standardize_newlines('A\nB')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\r\nB')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n\rB')
            self.assertText('A\nB', return_val)

        with self.subTest('Test repeated newline characters - Isolated'):
            return_val = self.standardize_newlines('\n\n')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n\n\n')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n\r\n\r\n')
            self.assertText('', return_val)
        with self.subTest('Test repeated newline characters - As inner element'):
            return_val = self.standardize_newlines('A\n\nB')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n\n\nB')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n\r\n\r\nB')
            self.assertText('A\nB', return_val)

        with self.subTest('Test with whitespace - Isolated'):
            return_val = self.standardize_newlines('<br>   <br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('<br>   <br>   <br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('<br>   \n   <br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n   \n')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n   \n   \n')
            self.assertText('', return_val)
        with self.subTest('Test with whitespace - As inner element'):
            return_val = self.standardize_newlines('A<br>   <br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A<br>   <br>   <br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A<br>   \n   <br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n   \nB')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n   \n   \nB')
            self.assertText('A\nB', return_val)

        with self.subTest('Test with non-breaking space - Isolated'):
            return_val = self.standardize_newlines('<br> &nbsp; <br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('<br> &nbsp; <br> &nbsp; <br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('<br> &nbsp; \n &nbsp; <br>')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n &nbsp; \n')
            self.assertText('', return_val)
            return_val = self.standardize_newlines('\n &nbsp; \n &nbsp; \n')
            self.assertText('', return_val)
        with self.subTest('Test with non-breaking space - As inner element'):
            return_val = self.standardize_newlines('A<br> &nbsp; <br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A<br> &nbsp; <br> &nbsp; <br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A<br> &nbsp; \n &nbsp; <br>B')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n &nbsp; \nB')
            self.assertText('A\nB', return_val)
            return_val = self.standardize_newlines('A\n &nbsp; \n &nbsp; \nB')
            self.assertText('A\nB', return_val)

    def test__standardize_whitespace(self):
        """
        Tests standardize_whitespace() function.
        """
        with self.subTest('Test <br> tag - Isolated'):
            return_val = self.standardize_whitespace('<br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('</br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('<br/>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('<br />')
            self.assertText('', return_val)
        with self.subTest('Test <br> tag - As inner element'):
            return_val = self.standardize_whitespace('A<br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A</br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A<br/>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A<br />B')
            self.assertText('A B', return_val)

        with self.subTest('Test single newline characters - Isolated'):
            return_val = self.standardize_whitespace('\n')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\r\n')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n\r')
            self.assertText('', return_val)
        with self.subTest('Test single newline characters - As inner element'):
            return_val = self.standardize_whitespace('A\nB')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\r\nB')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n\rB')
            self.assertText('A B', return_val)

        with self.subTest('Test repeated newline characters - Isolated'):
            return_val = self.standardize_whitespace('\n\n')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n\n\n')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n\r\n\r\n')
            self.assertText('', return_val)
        with self.subTest('Test repeated newline characters - As inner element'):
            return_val = self.standardize_whitespace('A\n\nB')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n\n\nB')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n\r\n\r\nB')
            self.assertText('A B', return_val)

        with self.subTest('Test with whitespace - Isolated'):
            return_val = self.standardize_whitespace('<br>   <br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('<br>   <br>   <br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('<br>   \n   <br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n   \n')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n   \n   \n')
            self.assertText('', return_val)
        with self.subTest('Test with whitespace - As inner element'):
            return_val = self.standardize_whitespace('A<br>   <br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A<br>   <br>   <br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A<br>   \n   <br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n   \nB')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n   \n   \nB')
            self.assertText('A B', return_val)

        with self.subTest('Test with whitespace - Isolated'):
            return_val = self.standardize_whitespace('<br> &nbsp; <br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('<br> &nbsp; <br> &nbsp; <br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('<br> &nbsp; \n &nbsp; <br>')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n &nbsp; \n')
            self.assertText('', return_val)
            return_val = self.standardize_whitespace('\n &nbsp; \n &nbsp; \n')
            self.assertText('', return_val)
        with self.subTest('Test with whitespace - As inner element'):
            return_val = self.standardize_whitespace('A<br> &nbsp; <br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A<br> &nbsp; <br> &nbsp; <br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A<br> &nbsp; \n &nbsp; <br>B')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n &nbsp; \nB')
            self.assertText('A B', return_val)
            return_val = self.standardize_whitespace('A\n &nbsp; \n &nbsp; \nB')
            self.assertText('A B', return_val)

    # endregion Helper Function Tests


# TODO: For now, patching doesn't seem to work. Unsure why because the "real name" test works fine.
#   Figure out later.
# @override_settings(DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD='changed_value')
# class BaseClassTest_WithModifiedPassword(BaseTestCase):
#     """Tests for BaseTestCase class, when using settings to generate users with different passwords.
#
#     Required as a separate class, since user generation is handled on class initialization.
#     """
#     @classmethod
#     @patch('django_expanded_test_cases.mixins.core_mixin.ETC_DEFAULT_USER_PASSWORD', 'changed_value')
#     def setUpTestData(cls):
#         # Call parent logic.
#         super().setUpTestData()
#
#     # @patch('django_expanded_test_cases.mixins.core_mixin.ETC_DEFAULT_USER_PASSWORD', 'changed_value')
#     # def get_user(self, *args, **kwargs):
#     #     # Call parent logic.
#     #     return super().get_user(*args, **kwargs)
#
#     def test__get_user__with_modified_password(self):
#         """
#         Tests get_user() function.
#
#         Note: We test all expected model attributes, to ensure that the setting doesn't change anything unexpected.
#         """
#
#         with self.subTest('Test "test_superuser" user - With modified password'):
#             test_superuser = self.get_user('test_superuser')
#
#             print('password: "{0}"'.format(test_superuser.unhashed_password))
#
#             self.assertEqual(test_superuser, self.test_superuser)
#             self.assertEqual(test_superuser.username, 'test_superuser')
#             self.assertTrue(test_superuser.check_password('changed_value'))
#             self.assertEqual(test_superuser.unhashed_password, 'changed_value')
#             self.assertEqual(test_superuser.first_name, 'SuperUserFirst')
#             self.assertEqual(test_superuser.last_name, 'SuperUserLast')
#             self.assertEqual(test_superuser.email, 'super_user@example.com')
#             self.assertEqual(test_superuser.is_superuser, True)
#             self.assertEqual(test_superuser.is_staff, False)
#             self.assertEqual(test_superuser.is_active, True)
#
#         with self.subTest('Test "test_admin" user - With modified password'):
#             test_admin = self.get_user('test_admin')
#
#             self.assertEqual(test_admin, self.test_admin)
#             self.assertEqual(test_admin.username, 'test_admin')
#             self.assertTrue(test_admin.check_password('changed_value'))
#             self.assertEqual(test_admin.unhashed_password, 'changed_value')
#             self.assertEqual(test_admin.first_name, 'AdminUserFirst')
#             self.assertEqual(test_admin.last_name, 'AdminUserLast')
#             self.assertEqual(test_admin.email, 'admin_user@example.com')
#             self.assertEqual(test_admin.is_superuser, False)
#             self.assertEqual(test_admin.is_staff, True)
#             self.assertEqual(test_admin.is_active, True)
#
#         with self.subTest('Test "test_inactive" user - With modified password'):
#             test_inactive = self.get_user('test_inactive')
#
#             self.assertEqual(test_inactive, self.test_inactive_user)
#             self.assertEqual(test_inactive.username, 'test_inactive')
#             self.assertTrue(test_inactive.check_password('changed_value'))
#             self.assertEqual(test_inactive.unhashed_password, 'changed_value')
#             self.assertEqual(test_inactive.first_name, 'InactiveUserFirst')
#             self.assertEqual(test_inactive.last_name, 'InactiveUserLast')
#             self.assertEqual(test_inactive.email, 'inactive_user@example.com')
#             self.assertEqual(test_inactive.is_superuser, False)
#             self.assertEqual(test_inactive.is_staff, False)
#             self.assertEqual(test_inactive.is_active, False)
#
#         with self.subTest('Test "test_user" user - With modified password'):
#             test_user = self.get_user('test_user')
#
#             self.assertEqual(test_user, self.test_user)
#             self.assertEqual(test_user.username, 'test_user')
#             self.assertTrue(test_user.check_password('changed_value'))
#             self.assertEqual(test_user.unhashed_password, 'changed_value')
#             self.assertEqual(test_user.first_name, 'UserFirst')
#             self.assertEqual(test_user.last_name, 'UserLast')
#             self.assertEqual(test_user.email, 'user@example.com')
#             self.assertEqual(test_user.is_superuser, False)
#             self.assertEqual(test_user.is_staff, False)
#             self.assertEqual(test_user.is_active, True)


class BaseClassTest_WithRealNames(BaseTestCase):
    """Tests for BaseTestCase class, when using settings to generate users with real names.

    Required as a separate class, since user generation is handled on class initialization.
    """
    @classmethod
    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_GENERATE_USERS_WITH_REAL_NAMES', True)
    def setUpTestData(cls):
        # Call parent logic.
        super().setUpTestData()

    def test__get_user__with_real_names(self):
        """
        Tests get_user() function.

        Note: We test all expected model attributes, to ensure that the setting doesn't change anything unexpected.
        """
        with self.subTest('Test "test_superuser" user - With real names'):
            test_superuser = self.get_user('test_superuser')

            self.assertEqual(test_superuser, self.test_superuser)
            self.assertEqual(test_superuser.username, 'test_superuser')
            self.assertTrue(test_superuser.check_password('password'))
            self.assertEqual(test_superuser.unhashed_password, 'password')
            self.assertEqual(test_superuser.first_name, 'John')
            self.assertEqual(test_superuser.last_name, 'Doe')
            self.assertEqual(test_superuser.email, 'super_user@example.com')
            self.assertEqual(test_superuser.is_superuser, True)
            self.assertEqual(test_superuser.is_staff, False)
            self.assertEqual(test_superuser.is_active, True)

        with self.subTest('Test "test_admin" user - With real names'):
            test_admin = self.get_user('test_admin')

            self.assertEqual(test_admin, self.test_admin)
            self.assertEqual(test_admin.username, 'test_admin')
            self.assertTrue(test_admin.check_password('password'))
            self.assertEqual(test_admin.unhashed_password, 'password')
            self.assertEqual(test_admin.first_name, 'Jenny')
            self.assertEqual(test_admin.last_name, 'Johnson')
            self.assertEqual(test_admin.email, 'admin_user@example.com')
            self.assertEqual(test_admin.is_superuser, False)
            self.assertEqual(test_admin.is_staff, True)
            self.assertEqual(test_admin.is_active, True)

        with self.subTest('Test "test_inactive" user - With real names'):
            test_inactive = self.get_user('test_inactive')

            self.assertEqual(test_inactive, self.test_inactive_user)
            self.assertEqual(test_inactive.username, 'test_inactive')
            self.assertTrue(test_inactive.check_password('password'))
            self.assertEqual(test_inactive.unhashed_password, 'password')
            self.assertEqual(test_inactive.first_name, 'Clang')
            self.assertEqual(test_inactive.last_name, 'Zythor')
            self.assertEqual(test_inactive.email, 'inactive_user@example.com')
            self.assertEqual(test_inactive.is_superuser, False)
            self.assertEqual(test_inactive.is_staff, False)
            self.assertEqual(test_inactive.is_active, False)

        with self.subTest('Test "test_user" user - With real names'):
            test_user = self.get_user('test_user')

            self.assertEqual(test_user, self.test_user)
            self.assertEqual(test_user.username, 'test_user')
            self.assertTrue(test_user.check_password('password'))
            self.assertEqual(test_user.unhashed_password, 'password')
            self.assertEqual(test_user.first_name, 'Sammy')
            self.assertEqual(test_user.last_name, 'Smith')
            self.assertEqual(test_user.email, 'user@example.com')
            self.assertEqual(test_user.is_superuser, False)
            self.assertEqual(test_user.is_staff, False)
            self.assertEqual(test_user.is_active, True)
