"""Mixin class for all tests which apply to all LiveServerTestCase classes."""

# System Imports.
import logging
from pathlib import Path


class UniversalLiveTestMixin:
    """Tests which apply to all LiveServerTestCase classes (both selenium and channels)."""

    # region Core Logic Tests

    def test__window_handling(self):
        """
        Tests standard create/get/destroy driver functions.
        """
        # Get initial driver.
        driver = self.create_driver()

        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__window_handling.html').resolve())

        # Verify handle length before test.
        self.assertEqual(1, len(driver.window_handles))

        with self.subTest('Test open_new_window() function'):

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<h1>Window 1</h1>')
                file.write('<h2>Window 1</h2>')
                file.write('<h3>Window 1</h3>')
                file.write('<h4>Window 1</h4>')
                file.write('<h5>Window 1</h5>')
                file.write('<h6>Window 1</h6>')
                file.write('<p>Window 1</p>')
                file.write('<span>Window 1</span>')
                file.write('<li>Window 1</li>')

            # Get driver object to open generated file.
            self.open_new_window(driver)
            driver.get('file://{0}'.format(file_name))

            # Verify updated window count.
            self.assertEqual(2, len(driver.window_handles))

            # Check for expected elements.
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(1, len(results))
            self.assertIn('<li>\n Window 1\n</li>', results)

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<h1>Window 2</h1>')
                file.write('<h2>Window 2</h2>')
                file.write('<h3>Window 2</h3>')
                file.write('<h4>Window 2</h4>')
                file.write('<h5>Window 2</h5>')
                file.write('<h6>Window 2</h6>')
                file.write('<p>Window 2</p>')
                file.write('<span>Window 2</span>')
                file.write('<li>Window 2</li>')

            # Get driver object to open generated file.
            self.open_new_window(driver)
            driver.get('file://{0}'.format(file_name))

            # Verify updated window count.
            self.assertEqual(len(driver.window_handles), 3)

            # Check for expected elements.
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(1, len(results))
            self.assertIn('<li>\n Window 2\n</li>', results)

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<h1>Window 3</h1>')
                file.write('<h2>Window 3</h2>')
                file.write('<h3>Window 3</h3>')
                file.write('<h4>Window 3</h4>')
                file.write('<h5>Window 3</h5>')
                file.write('<h6>Window 3</h6>')
                file.write('<p>Window 3</p>')
                file.write('<span>Window 3</span>')
                file.write('<li>Window 3</li>')

            # Get driver object to open generated file.
            self.open_new_window(driver)
            driver.get('file://{0}'.format(file_name))

            # Verify updated window count.
            self.assertEqual(4, len(driver.window_handles))

            # Check for expected elements.
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(1, len(results))
            self.assertIn('<li>\n Window 3\n</li>', results)

        # Three separate windows created.
        # We have verified we can access expected data immediately after each windows creation.
        # Now verify we can switch between them and still get expected data.
        # Aka, verify that we didn't accidentally reuse the same window for all above tests.
        with self.subTest('Test switch_to_window() function'):
            # Verify we actually have four separate windows (3 we created plus the default).
            self.assertEqual(4, len(driver.window_handles))

            # Get individual driver objects.
            first_window_index = 1
            second_window_index = 2
            third_window_index = 3

            # Verify each window handle is unique.
            # Window "handle" checks.
            self.assertNotEqual(driver.window_handles[first_window_index], driver.window_handles[second_window_index])
            self.assertNotEqual(driver.window_handles[second_window_index], driver.window_handles[third_window_index])
            self.assertNotEqual(driver.window_handles[first_window_index], driver.window_handles[third_window_index])

            # Verify able to switch between windows and get different data for each.
            self.switch_to_window(driver, first_window_index)
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(1, len(results))
            self.assertIn('<li>\n Window 1\n</li>', results)

            self.switch_to_window(driver, second_window_index)
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(1, len(results))
            self.assertIn('<li>\n Window 2\n</li>', results)

            self.switch_to_window(driver, third_window_index)
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(1, len(results))
            self.assertIn('<li>\n Window 3\n</li>', results)

        # Verified that our windows are unique and have expected data.
        # Now verify we can close individual windows as expected.
        with self.subTest('Test close_window() function'):
            # Double check we still have three separate drivers.
            self.assertEqual(4, len(driver.window_handles))

            # Close our middle window.
            self.close_window(driver, 2)

            # Verify actually closed.
            self.assertEqual(3, len(driver.window_handles))
            for index in range(len(driver.window_handles)):
                # Check contents of each open window.
                self.switch_to_window(driver, index)

                # Verify we do NOT have our closed window data present.
                self.assertFalse('Window 2' in driver.page_source)

                # If not the "default" window, verify some content while we're at it.
                if index == 1:
                    results = self.find_elements_by_text(driver, 'Window 1')
                    self.assertEqual(9, len(results))
                    self.assertIn('<li>\n Window 1\n</li>', results)
                elif index == 2:
                    results = self.find_elements_by_text(driver, 'Window 3')
                    self.assertEqual(9, len(results))
                    self.assertIn('<li>\n Window 3\n</li>', results)

            # Close first window.
            self.close_window(driver, 1)

            # Verify actually closed.
            self.assertEqual(2, len(driver.window_handles))
            for index in range(len(driver.window_handles)):
                # Check contents of each open window.
                self.switch_to_window(driver, index)

                # Verify we do NOT have our closed window data present.
                self.assertFalse('Window 1' in driver.page_source)
                self.assertFalse('Window 2' in driver.page_source)

                # If not the "default" window, verify some content while we're at it.
                if index == 1:
                    results = self.find_elements_by_text(driver, 'Window 3')
                    self.assertEqual(9, len(results))
                    self.assertIn('<li>\n Window 3\n</li>', results)

            # Close remaining window.
            self.close_window(driver, 1)

            # Verify actually closed.
            self.assertEqual(1, len(driver.window_handles))
            for index in range(len(driver.window_handles)):
                # Check contents of each open window.
                self.switch_to_window(driver, index)

                # Verify we do NOT have our closed window data present.
                self.assertFalse('Window 1' in driver.page_source)
                self.assertFalse('Window 2' in driver.page_source)
                self.assertFalse('Window 3' in driver.page_source)

    # endregion Core Logic Tests

    # region Helper Function Tests

    def test__find_elements_by_tag__success(self):
        """
        Tests find_elements_by_tag() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_tag__success.html').resolve())

        with self.subTest('When expected element is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n</li>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(driver, '<li>')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n</li>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(driver, '</li>')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n</li>', results)

        with self.subTest('When expected element is the only item, with void element - Standard tag'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<hr>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_tag(driver, 'hr')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(driver, '<hr>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(driver, '<hr/>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)

        with self.subTest('When expected element is the only item, with void element - Old style tag'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<hr/>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_tag(driver, 'hr')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(driver, '<hr>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(driver, '<hr/>')
            self.assertEqual(len(results), 1)
            self.assertIn('<hr/>', results)

        with self.subTest('When expected element exists multiple times - Two instances'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li>One</li><li>Two</li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n One\n</li>', results)
            self.assertIn('<li>\n Two\n</li>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(driver, '<li>')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n One\n</li>', results)
            self.assertIn('<li>\n Two\n</li>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(driver, '</li>')
            self.assertEqual(len(results), 2)
            self.assertIn('<li>\n One\n</li>', results)
            self.assertIn('<li>\n Two\n</li>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p>One</p></li>
                            <li><p>Two</p></li>
                            <li><p>Three</p></li>
                        </ul>
                        <ul>
                            <li><p>Four</p></li>
                            <li><p>Five</p></li>
                            <li><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(len(results), 6)
            self.assertIn('<li>\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Three\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Four\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Five\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Six\n</p>\n</li>', results)
            # By standard element open tag.
            results = self.find_elements_by_tag(driver, '<li>')
            self.assertEqual(len(results), 6)
            self.assertIn('<li>\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Three\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Four\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Five\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Six\n</p>\n</li>', results)
            # By standard element close tag.
            results = self.find_elements_by_tag(driver, '</li>')
            self.assertEqual(len(results), 6)
            self.assertIn('<li>\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Three\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Four\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Five\n</p>\n</li>', results)
            self.assertIn('<li>\n<p>\n Six\n</p>\n</li>', results)

    def test__find_elements_by_tag__failure(self):
        """
        Tests find_elements_by_tag() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_tag__failure.html').resolve())

        with self.subTest('When expected element is not present - Blank response'):
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is not present - Single-item response'):
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<html><head></head><body><p></p></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is not present - Multi-item response'):
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "li" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p>Some text.</p>
                        <p>Some more text.</p>
                        <p>Some text with the str "li" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_tag__success(self):
        """
        Tests find_element_by_tag() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_tag__success.html').resolve())

        with self.subTest('When expected element is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_element_by_tag(driver, 'li')
            self.assertText('<li>\n</li>', results)
            # By standard element open tag.
            results = self.find_element_by_tag(driver, '<li>')
            self.assertText('<li>\n</li>', results)
            # By standard element close tag.
            results = self.find_element_by_tag(driver, '</li>')
            self.assertText('<li>\n</li>', results)

        with self.subTest('When expected element is the only item, with void element - Standard tag'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<hr>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_element_by_tag(driver, 'hr')
            self.assertText('<hr/>\n', results)
            # By standard element open tag.
            results = self.find_element_by_tag(driver, '<hr>')
            self.assertText('<hr/>\n', results)
            # By standard element close tag.
            results = self.find_element_by_tag(driver, '<hr/>')
            self.assertText('<hr/>\n', results)

        with self.subTest('When expected element is the only item, with void element - Old style tag'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<hr/>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_element_by_tag(driver, 'hr')
            self.assertText('<hr/>\n', results)
            # By standard element open tag.
            results = self.find_element_by_tag(driver, '<hr>')
            self.assertText('<hr/>\n', results)
            # By standard element close tag.
            results = self.find_element_by_tag(driver, '<hr/>')
            self.assertText('<hr/>\n', results)

        with self.subTest('When expected element exists plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p>One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_element_by_tag(driver, 'li')
            self.assertText('<li>\n<p>\n One\n</p>\n</li>', results)
            # By standard element open tag.
            results = self.find_element_by_tag(driver, '<li>')
            self.assertText('<li>\n<p>\n One\n</p>\n</li>', results)
            # By standard element close tag.
            results = self.find_element_by_tag(driver, '</li>')
            self.assertText('<li>\n<p>\n One\n</p>\n</li>', results)

    def test__find_element_by_tag__failure(self):
        """
        Tests find_element_by_tag() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_tag__failure.html').resolve())

        with self.subTest('When expected element is not present - Blank response'):
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is not present - Single-item response'):
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is not present - Multi-item response'):
            err_msg = (
                'Unable to find element "<li>" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "li" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p>Some text.</p>
                        <p>Some more text.</p>
                        <p>Some text with the str "li" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is present multiple times'):
            err_msg = (
                'Found multiple instances of "<li>" element. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<li></li><li></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li></li><li></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, 'li')
            self.assertText(err_msg, str(err.exception))
            # By standard element open tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '<li>')
            self.assertText(err_msg, str(err.exception))
            # By standard element close tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_tag(driver, '</li>')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_id__success(self):
        """
        Tests find_elements_by_id() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_id__success.html').resolve())

        with self.subTest('When expected id is the only item'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li id="test_id"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_id(driver, 'test_id')
            self.assertText(len(results), 1)
            self.assertIn('<li id="test_id">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p id="test_id"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_id(driver, 'test_id')
            self.assertText(len(results), 1)
            self.assertIn('<p id="test_id">\n</p>', results)

        with self.subTest('When expected id exists multiple times - Two instances'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li id="test_id">One</li><li id="test_id">Two</li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertLogs(level=logging.WARNING):
                results = self.find_elements_by_id(driver, 'test_id')
            self.assertEqual(len(results), 2)
            self.assertIn('<li id="test_id">\n One\n</li>', results)
            self.assertIn('<li id="test_id">\n Two\n</li>', results)

        with self.subTest('When expected id exists multiple times - Three instances plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li id="test_id"><p>One</p></li>
                            <li id="test_id"><p>Two</p></li>
                            <li id="some_value"><p>Three</p></li>
                        </ul>
                        <ul>
                            <li id="test_id"><p>Four</p></li>
                            <li id="another_id"><p>Five</p></li>
                            <li id="test"><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertLogs(level=logging.WARNING):
                results = self.find_elements_by_id(driver, 'test_id')
            self.assertEqual(len(results), 3)
            self.assertIn('<li id="test_id">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li id="test_id">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li id="test_id">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p id="test_id">One</p></li>
                            <li><p id="test_id">Two</p></li>
                            <li><p id="some_value">Three</p></li>
                        </ul>
                        <ul>
                            <li><p id="test_id">Four</p></li>
                            <li><p id="another_id">Five</p></li>
                            <li><p id="test">Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertLogs(level=logging.WARNING):
                results = self.find_elements_by_id(driver, 'test_id')
            self.assertEqual(len(results), 3)
            self.assertIn('<p id="test_id">\n One\n</p>', results)
            self.assertIn('<p id="test_id">\n Two\n</p>', results)
            self.assertIn('<p id="test_id">\n Four\n</p>', results)

    def test__find_elements_by_id__failure(self):
        """
        Tests find_elements_by_id() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_id__failure.html').resolve())

        with self.subTest('When expected id is not present - Blank response'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is not present - Single-item response'):
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p id="test"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p id="test"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is not present - Multi-item response'):
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p id="some_value">Some text.</p>\n'
                '<p id="another_id">Some more text.</p>\n'
                '<p>Some text with the str "id" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p id="some_value">Some text.</p>
                        <p id="another_id">Some more text.</p>
                        <p>Some text with the str "id" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_id__success(self):
        """
        Tests find_element_by_id() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_id__success.html').resolve())

        with self.subTest('When expected id is the only item'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li id="test_id"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_id(driver, 'test_id')
            self.assertText('<li id="test_id">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p id="test_id"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_id(driver, 'test_id')
            self.assertText('<p id="test_id">\n</p>', results)

        with self.subTest('When expected id exists plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li id=test_id><p>One</p></li>
                            <li><p>Two</p></li>
                            <li id="some_value"><p>Three</p></li>
                        </ul>
                        <ul>
                            <li id="another_id"><p>Four</p></li>
                            <li><p>Five</p></li>
                            <li id="test"><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_id(driver, 'test_id')
            self.assertText('<li id="test_id">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p id=test_id>One</p></li>
                            <li><p>Two</p></li>
                            <li id="some_value"><p>Three</p></li>
                        </ul>
                        <ul>
                            <li id="another_id"><p>Four</p></li>
                            <li><p>Five</p></li>
                            <li id="test"><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_id(driver, 'test_id')
            self.assertText('<p id="test_id">\n One\n</p>', results)

    def test__find_element_by_id__failure(self):
        """
        Tests find_element_by_id() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_id__failure.html').resolve())

        with self.subTest('When expected id is not present - Blank response'):
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is not present - Single-item response'):
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p id="some_id"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p id="some_id"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is not present - Multi-item response'):
            err_msg = (
                'Unable to find id "test_id" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p id="some_value">Some text.</p>\n'
                '<p id="another_id">Some more text.</p>\n'
                '<p>Some text with the str "id" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                """
                <div>
                    <h1>Page Header</h1>
                    <p id="some_value">Some text.</p>
                    <p id="another_id">Some more text.</p>
                    <p>Some text with the str "id" in it.</p>
                </div>
                """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            with self.assertRaises(AssertionError) as err:
                self.find_element_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected id is present multiple times'):
            # As <li> tag.
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<li id="test_id"></li><li id="test_id"></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li id="test_id"></li><li id="test_id"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<p id="test_id"></p><p id="test_id"></p>'
                '</body></html>'
            )
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p id="test_id"></p><p id="test_id"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

            # As mixed tags.
            err_msg = (
                'Found multiple instances of "test_id" id. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<li id="test_id"><p id="test_id">Test</p></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li id="test_id"><p id="test_id">Test</p></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                with self.assertLogs(level=logging.WARNING):
                    self.find_element_by_id(driver, 'test_id')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_class__success(self):
        """
        Tests find_elements_by_class() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_class__success.html').resolve())

        with self.subTest('When expected class is the only item'):
            # As <li>  tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li class="test_class"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_class(driver, 'test_class')
            self.assertEqual(len(results), 1)
            self.assertIn('<li class="test_class">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p class="test_class"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_class(driver, 'test_class')
            self.assertEqual(len(results), 1)
            self.assertIn('<p class="test_class">\n</p>', results)

        with self.subTest('When expected class exists multiple times - Two instances'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li class="test_class">One</li><li class="test_class">Two</li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_class(driver, 'test_class')
            self.assertEqual(len(results), 2)
            self.assertIn('<li class="test_class">\n One\n</li>', results)
            self.assertIn('<li class="test_class">\n Two\n</li>', results)

        with self.subTest('When expected class exists plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li class="test_class"><p>One</p></li>
                            <li class="test_class"><p>Two</p></li>
                            <li class="some_value"><p>Three</p></li>
                        </ul>
                        <ul>
                            <li class="test_class test"><p>Four</p></li>
                            <li class="another_class"><p>Five</p></li>
                            <li class="test"><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_class(driver, 'test_class')
            self.assertEqual(len(results), 3)
            self.assertIn('<li class="test_class">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li class="test_class">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li class="test_class test">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p class="test_class">One</p></li>
                            <li><p class="test_class">Two</p></li>
                            <li><p class="some_value">Three</p></li>
                        </ul>
                        <ul>
                            <li><p class="test_class test">Four</p></li>
                            <li><p class="another_class">Five</p></li>
                            <li><p class="test">Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_class(driver, 'test_class')
            self.assertEqual(len(results), 3)
            self.assertIn('<p class="test_class">\n One\n</p>', results)
            self.assertIn('<p class="test_class">\n Two\n</p>', results)
            self.assertIn('<p class="test_class test">\n Four\n</p>', results)

    def test__find_elements_by_class__failure(self):
        """
        Tests find_elements_by_class() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_class__failure.html').resolve())

        with self.subTest('When expected class is not present - Blank response'):
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is not present - Single-item response'):
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p class="some_class"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p class="some_class"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is not present - Multi-item response'):
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "class" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p>Some text.</p>
                        <p>Some more text.</p>
                        <p>Some text with the str "class" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_class__success(self):
        """
        Tests find_element_by_class() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_class__success.html').resolve())

        with self.subTest('When expected class is the only item'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li class="test_class"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_class(driver, 'test_class')
            self.assertText('<li class="test_class">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p class="test_class"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_class(driver, 'test_class')
            self.assertText('<p class="test_class">\n</p>', results)

        with self.subTest('When expected class exists plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li class="test_class"><p>One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_class(driver, 'test_class')
            self.assertText('<li class="test_class">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p class="test_class">One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_class(driver, 'test_class')
            self.assertText('<p class="test_class">\n One\n</p>', results)

    def test__find_element_by_class__failure(self):
        """
        Tests find_element_by_class() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_class__failure.html').resolve())

        with self.subTest('When expected class is not present - Blank response'):
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is not present - Single-item response'):
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p class="some_class"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p class="some_class"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is not present - Multi-item response'):
            err_msg = (
                'Unable to find class "test_class" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p class="some_class">Some text.</p>\n'
                '<p class="another_class">Some more text.</p>\n'
                '<p class="test">Some text with the str "class" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p class="some_class">Some text.</p>
                        <p class="another_class">Some more text.</p>
                        <p class="test">Some text with the str "class" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected class is present multiple times'):
            # As <li> tag.
            err_msg = (
                'Found multiple instances of "test_class" class. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<li class="test_class"></li><li class="test_class"></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li class="test_class"></li><li class="test_class"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            err_msg = (
                'Found multiple instances of "test_class" class. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<p class="test_class"></p><p class="test_class"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p class="test_class"></p><p class="test_class"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_class(driver, 'test_class')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_css_selector__success(self):
        """
        Tests find_elements_by_css_selector() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_css_selector__success.html').resolve())

        with self.subTest('When expected css_selector is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li><p class="test_class"><a>One</a></p></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertEqual(len(results), 1)
            self.assertIn('<a>\n One\n</a>', results)

        with self.subTest('When expected element exists multiple times - Two instances'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <li><p class="test_class"><a>One</a></p></li>
                    <li><p class="test_class"><a>Two</a></p></li>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertEqual(len(results), 2)
            self.assertIn('<a>\n One\n</a>', results)
            self.assertIn('<a>\n Two\n</a>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p class="test_class"><a>One</a></p></li>
                            <li><p class="test_class"><a>Two</a></p></li>
                            <li><p class="test_class">Three</p></li>
                        </ul>
                        <ul>
                            <li><p class="test_class"><a>Four</a></p></li>
                            <li><p class="test_class"><div><a>Five</a></div></p></li>
                            <li><p class="other_class"><a>Six</a></p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertEqual(len(results), 3)
            self.assertIn('<a>\n One\n</a>', results)
            self.assertIn('<a>\n Two\n</a>', results)
            self.assertIn('<a>\n Four\n</a>', results)

    def test__find_elements_by_css_selector__failure(self):
        """
        Tests find_elements_by_css_selector() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_css_selector__failure.html').resolve())

        with self.subTest('When expected css_selector is not present - Blank response'):
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is not present - Single-item response'):
            # Missing all parts.
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing two parts.
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<li></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing one part.
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<li><p class="test_class"></p></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li><p class="test_class"></p></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is not present - Multi-item response'):
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "css_selector" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p>Some text.</p>
                        <p>Some more text.</p>
                        <p>Some text with the str "css_selector" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_css_selector__success(self):
        """
        Tests find_element_by_css_selector() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_css_selector__success.html').resolve())

        with self.subTest('When expected css_selector is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li><p class="test_class"><a>One</a></p></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText('<a>\n One\n</a>', results)

        with self.subTest('When expected css_selector exists plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p class="test_class"><a>One</a></p></li>
                            <li><a>Two</a></li>
                            <li><p class="test_class"><div><a>Three</a></div></p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText('<a>\n One\n</a>', results)

    def test__find_element_by_css_selector__failure(self):
        """
        Tests find_element_by_css_selector() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_css_selector__failure.html').resolve())

        with self.subTest('When expected css_selector is not present - Blank response'):
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is not present - Single-item response'):
            # Missing all parts.
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing two parts.
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<li></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

            # Missing one parts.
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<li><p class="test_class"></p></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li><p class="test_class"></p></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is not present - Multi-item response'):
            err_msg = (
                'Unable to find css selector "li .test_class > a" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p>Some text.</p>\n'
                '<p>Some more text.</p>\n'
                '<p>Some text with the str "css_selector" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p>Some text.</p>
                        <p>Some more text.</p>
                        <p>Some text with the str "css_selector" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected css_selector is present multiple times'):
            err_msg = (
                'Found multiple instances of "li .test_class > a" css selector. Expected only one instance.'
                ' Content was:\n'
                '<html><head></head><body>'
                '<li><p class="test_class"><a>One</a></p></li>\n'
                '<li><p class="test_class"><a>Two</a></p></li>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <li><p class="test_class"><a>One</a></p></li>
                    <li><p class="test_class"><a>Two</a></p></li>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_css_selector(driver, 'li .test_class > a')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_data_attribute__success(self):
        """
        Tests find_elements_by_data_attribute() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_data_attribute__success.html').resolve())

        with self.subTest('When expected data_attribute is the only item, with standard element'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li my_attr="my_val"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertEqual(len(results), 1)
            self.assertIn('<li my_attr="my_val">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p my_attr="my_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertEqual(len(results), 1)
            self.assertIn('<p my_attr="my_val">\n</p>', results)

        with self.subTest('When expected data_attribute exists multiple times - Two instances'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li my_attr="my_val">One</li><li my_attr="my_val">Two</li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertEqual(len(results), 2)
            self.assertIn('<li my_attr="my_val">\n One\n</li>', results)
            self.assertIn('<li my_attr="my_val">\n Two\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p my_attr="my_val">One</p><p my_attr="my_val">Two</p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertEqual(len(results), 2)
            self.assertIn('<p my_attr="my_val">\n One\n</p>', results)
            self.assertIn('<p my_attr="my_val">\n Two\n</p>', results)

        with self.subTest('When expected data_attribute exists multiple times - Three instances plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li my_attr="my_val"><p>One</p></li>
                            <li my_attr="my_val"><p>Two</p></li>
                            <li other_attr="other_val"><p>Three</p></li>
                        </ul>
                        <ul>
                            <li my_attr="my_val" test_attr="test_val"><p>Four</p></li>
                            <li another_attr="my_val"><p>Five</p></li>
                            <li my_attr="another_val"><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))


            results = self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertEqual(len(results), 3)
            self.assertIn('<li my_attr="my_val">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li my_attr="my_val">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li my_attr="my_val" test_attr="test_val">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p my_attr="my_val">One</p></li>
                            <li><p my_attr="my_val">Two</p></li>
                            <li><p other_attr="other_val">Three</p></li>
                        </ul>
                        <ul>
                            <li><p my_attr="my_val" test_attr="test_val">Four</p></li>
                            <li><p another_attr="my_val">Five</p></li>
                            <li><p my_attr="another_val">Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))


            results = self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertEqual(len(results), 3)
            self.assertIn('<p my_attr="my_val">\n One\n</p>', results)
            self.assertIn('<p my_attr="my_val">\n Two\n</p>', results)
            self.assertIn('<p my_attr="my_val" test_attr="test_val">\n Four\n</p>', results)

    def test__find_elements_by_data_attribute__failure(self):
        """
        Tests find_elements_by_data_attribute() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_data_attribute__failure.html').resolve())

        with self.subTest('When expected data_attribute is not present - Blank response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute is not present - Single-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<p some_attr="some_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p some_attr="some_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute key is not present - Single-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<p some_attr="my_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p some_attr="my_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute value is not present - Single-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<p my_attr="some_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p my_attr="some_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute is not present - Multi-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p some_attr="some_val">Some text.</p>\n'
                '<p another_attr="another_val">Some more text.</p>\n'
                '<p test="test">Some text with the str "data_attribute" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p some_attr="some_val">Some text.</p>
                        <p another_attr="another_val">Some more text.</p>
                        <p test="test">Some text with the str "data_attribute" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_data_attribute__success(self):
        """
        Tests find_element_by_data_attribute() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_data_attribute__success.html').resolve())

        with self.subTest('When expected data_attribute is the only item, with standard element'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li my_attr="my_val"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText('<li my_attr="my_val">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p my_attr="my_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText('<p my_attr="my_val">\n</p>', results)

        with self.subTest('When expected data_attribute exists plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li my_attr="my_val"><p>One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText('<li my_attr="my_val">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p my_attr="my_val">One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText('<p my_attr="my_val">\n One\n</p>', results)

    def test__find_element_by_data_attribute__failure(self):
        """
        Tests find_element_by_data_attribute() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_data_attribute__failure.html').resolve())

        with self.subTest('When expected data_attribute is not present - Blank response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute is not present - Single-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<p some_attr="some_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p some_attr="some_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute key is not present - Single-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<p some_attr="my_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p some_attr="my_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute value is not present - Single-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<p my_attr="some_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p my_attr="some_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected data_attribute is not present - Multi-item response'):
            err_msg = (
                'Unable to find data attribute "my_attr" with value "my_val" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p some_attr="some_val">Some text.</p>\n'
                '<p another_attr="another_val">Some more text.</p>\n'
                '<p test="test">Some text with the str "data_attribute" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p some_attr="some_val">Some text.</p>
                        <p another_attr="another_val">Some more text.</p>
                        <p test="test">Some text with the str "data_attribute" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is present multiple times'):
            # As <li> tag.
            err_msg = (
                'Found multiple instances of "my_attr" data attribute with value "my_val". Expected only one instance. '
                'Content was:\n'
                '<html><head></head><body>'
                '<li my_attr="my_val"></li><li my_attr="my_val"></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li my_attr="my_val"></li><li my_attr="my_val"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            err_msg = (
                'Found multiple instances of "my_attr" data attribute with value "my_val". Expected only one instance. '
                'Content was:\n'
                '<html><head></head><body>'
                '<p my_attr="my_val"></p><p my_attr="my_val"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p my_attr="my_val"></p><p my_attr="my_val"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_data_attribute(driver, 'my_attr', 'my_val')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_name__success(self):
        """
        Tests find_elements_by_name() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_name__success.html').resolve())

        with self.subTest('When expected name is the only item'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li name="test_name"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_name(driver, 'test_name')
            self.assertEqual(len(results), 1)
            self.assertIn('<li name="test_name">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p name="test_name"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_name(driver, 'test_name')
            self.assertEqual(len(results), 1)
            self.assertIn('<p name="test_name">\n</p>', results)

        with self.subTest('When expected name exists multiple times - Two instances'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li name="test_name">One</li><li name="test_name">Two</li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_name(driver, 'test_name')
            self.assertEqual(len(results), 2)
            self.assertIn('<li name="test_name">\n One\n</li>', results)
            self.assertIn('<li name="test_name">\n Two\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p name="test_name">One</p><p name="test_name">Two</p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_name(driver, 'test_name')
            self.assertEqual(len(results), 2)
            self.assertIn('<p name="test_name">\n One\n</p>', results)
            self.assertIn('<p name="test_name">\n Two\n</p>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li name="test_name"><p>One</p></li>
                            <li name="test_name"><p>Two</p></li>
                            <li name="some_name"><p>Three</p></li>
                        </ul>
                        <ul>
                            <li name="test_name"><p>Four</p></li>
                            <li name="another_name"><p>Five</p></li>
                            <li name="test"><p>Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_name(driver, 'test_name')
            self.assertEqual(len(results), 3)
            self.assertIn('<li name="test_name">\n<p>\n One\n</p>\n</li>', results)
            self.assertIn('<li name="test_name">\n<p>\n Two\n</p>\n</li>', results)
            self.assertIn('<li name="test_name">\n<p>\n Four\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p name="test_name">One</p></li>
                            <li><p name="test_name">Two</p></li>
                            <li><p name="other_name">Three</p></li>
                        </ul>
                        <ul>
                            <li><p name="test_name">Four</p></li>
                            <li><p name="another_name">Five</p></li>
                            <li><p name="test">Six</p></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_name(driver, 'test_name')
            self.assertEqual(len(results), 3)
            self.assertIn('<p name="test_name">\n One\n</p>', results)
            self.assertIn('<p name="test_name">\n Two\n</p>', results)
            self.assertIn('<p name="test_name">\n Four\n</p>', results)

    def test__find_elements_by_name__failure(self):
        """
        Tests find_elements_by_name() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_name__failure.html').resolve())

        with self.subTest('When expected name is not present - Blank response'):
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected name is not present - Single-item response'):
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p name="other_name"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p name="other_name"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected name is not present - Multi-item response'):
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p name="other_name">Some text.</p>\n'
                '<p name="another_name">Some more text.</p>\n'
                '<p name="test">Some text with the str "name" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p name="other_name">Some text.</p>
                        <p name="another_name">Some more text.</p>
                        <p name="test">Some text with the str "name" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_name__success(self):
        """
        Tests find_element_by_name() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_name__success.html').resolve())

        with self.subTest('When expected name is the only item, with standard element'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li name="test_name"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_name(driver, 'test_name')
            self.assertText('<li name="test_name">\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p name="test_name"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_name(driver, 'test_name')
            self.assertText('<p name="test_name">\n</p>', results)

        with self.subTest('When expected element exists plus extra'):
            # As <li> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li name="test_name"><p>One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_name(driver, 'test_name')
            self.assertText('<li name="test_name">\n<p>\n One\n</p>\n</li>', results)

            # As <p> tag.
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><p name="test_name">One</p></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_name(driver, 'test_name')
            self.assertText('<p name="test_name">\n One\n</p>', results)

    def test__find_element_by_name__failure(self):
        """
        Tests find_element_by_name() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_name__failure.html').resolve())

        with self.subTest('When expected name is not present - Blank response'):
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected name is not present - Single-item response'):
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<p name="other_name"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p name="other_name"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected name is not present - Multi-item response'):
            err_msg = (
                'Unable to find name "test_name" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<p name="other_name">Some text.</p>\n'
                '<p name="another_name">Some more text.</p>\n'
                '<p name="test">Some text with the str "li" in it.</p>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <p name="other_name">Some text.</p>
                        <p name="another_name">Some more text.</p>
                        <p name="test">Some text with the str "li" in it.</p>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected element is present multiple times'):
            # As <li> tag.
            err_msg = (
                'Found multiple instances of "test_name" name. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<li name="test_name"></li><li name="test_name"></li>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<li name="test_name"></li><li name="test_name"></li>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

            # As <p> tag.
            err_msg = (
                'Found multiple instances of "test_name" name. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<p name="test_name"></p><p name="test_name"></p>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<p name="test_name"></p><p name="test_name"></p>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_name(driver, 'test_name')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_link_text__success(self):
        """
        Tests find_elements_by_link_text() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_link_text__success.html').resolve())

        with self.subTest('When expected link_text is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="test_link_text"></a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_link_text(driver, 'test_link_text')
            self.assertEqual(len(results), 1)
            self.assertIn('<a href="test_link_text">\n</a>', results)

        with self.subTest('When expected link_text exists multiple times - Two instances'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="test_link_text">One</a><a href="test_link_text">Two</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_link_text(driver, 'test_link_text')
            self.assertEqual(len(results), 2)
            self.assertIn('<a href="test_link_text">\n One\n</a>', results)
            self.assertIn('<a href="test_link_text">\n Two\n</a>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><a href="test_link_text">One</a></li>
                            <li><a href="test_link_text">Two</a></li>
                            <li><a href="other_link_text">Three</a></li>
                        </ul>
                        <ul>
                            <li><a href="test_link_text">Four</a></li>
                            <li><a href="another_link_text">Five</a></li>
                            <li><a href="test">Six</a></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_link_text(driver, 'test_link_text')
            self.assertEqual(len(results), 3)
            self.assertIn('<a href="test_link_text">\n One\n</a>', results)
            self.assertIn('<a href="test_link_text">\n Two\n</a>', results)
            self.assertIn('<a href="test_link_text">\n Four\n</a>', results)

    def test__find_elements_by_link_text__failure(self):
        """
        Tests find_elements_by_link_text() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_link_text__failure.html').resolve())

        with self.subTest('When expected link_text is not present - Blank response'):
            err_msg = (
                'Unable to find link text "test_link_text" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is not present - Single-item response'):
            err_msg = (
                'Unable to find link text "test_link_text" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<a href="other_link_text"></a>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="other_link_text"></a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is not present - Multi-item response'):
            err_msg = (
                'Unable to find link text "test_link_text" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="other_link_text">Some text.</a>\n'
                '<a href="another_link_text">Some more text.</a>\n'
                '<a href="test">Some text with the str "link_text" in it.</a>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <a href="other_link_text">Some text.</a>
                        <a href="another_link_text">Some more text.</a>
                        <a href="test">Some text with the str "link_text" in it.</a>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_link_text__success(self):
        """
        Tests find_element_by_link_text() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_link_text__success.html').resolve())

        with self.subTest('When expected element is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="test_link_text"></a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_link_text(driver, 'test_link_text')
            self.assertText('<a href="test_link_text">\n</a>', results)

        with self.subTest('When expected element exists plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><a href="test_link_text">One</a></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_link_text(driver, 'test_link_text')
            self.assertText('<a href="test_link_text">\n One\n</a>', results)

    def test__find_element_by_link_text__failure(self):
        """
        Tests find_element_by_link_text() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_link_text__failure.html').resolve())

        with self.subTest('When expected link_text is not present - Blank response'):
            err_msg = (
                'Unable to find link text "test_link_text" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is not present - Single-item response'):
            err_msg = (
                'Unable to find link text "test_link_text" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<a href="other_link_text"></a>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="other_link_text"></a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is not present - Multi-item response'):
            err_msg = (
                'Unable to find link text "test_link_text" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="other_link_text">Some text.</a>\n'
                '<a href="another_link_text">Some more text.</a>\n'
                '<a href="test">Some text with the str "link_text" in it.</a>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <a href="other_link_text">Some text.</a>
                        <a href="another_link_text">Some more text.</a>
                        <a href="test">Some text with the str "link_text" in it.</a>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected link_text is present multiple times'):
            err_msg = (
                'Found multiple instances of "test_link_text" link text. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<a href="test_link_text"></a><a href="test_link_text"></a>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="test_link_text"></a><a href="test_link_text"></a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_link_text(driver, 'test_link_text')
            self.assertText(err_msg, str(err.exception))

    def test__find_elements_by_text__success(self):
        """
        Tests find_elements_by_text() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_text__success.html').resolve())

        with self.subTest('When expected text is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="">test_element_text</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_text(driver, 'test_element_text')
            self.assertEqual(len(results), 1)
            self.assertIn('<a href="">\n test_element_text\n</a>', results)

        with self.subTest('When expected text exists multiple times - Two instances'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="">test_element_text One</a><a href="">test_element_text Two</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            # By base element tag.
            results = self.find_elements_by_text(driver, 'test_element_text')
            self.assertEqual(len(results), 2)
            self.assertIn('<a href="">\n test_element_text One\n</a>', results)
            self.assertIn('<a href="">\n test_element_text Two\n</a>', results)

        with self.subTest('When expected element exists multiple times - Three instances plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><a href="">test_element_text One</a></li>
                            <li><a href="">test_element_text Two</a></li>
                            <li><a href="">other_element_text Three</a></li>
                        </ul>
                        <ul>
                            <li><a href="">test_element_text Four</a></li>
                            <li><a href="">another_element_text Five</a></li>
                            <li><a href="">test Six</a></li>
                        </ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_text(driver, 'test_element_text')
            self.assertEqual(len(results), 3)
            self.assertIn('<a href="">\n test_element_text One\n</a>', results)
            self.assertIn('<a href="">\n test_element_text Two\n</a>', results)
            self.assertIn('<a href="">\n test_element_text Four\n</a>', results)

    def test__find_elements_by_text__failure(self):
        """
        Tests find_elements_by_text() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_elements_by_text__failure.html').resolve())

        with self.subTest('When expected text is not present - Blank response'):
            err_msg = (
                'Unable to find element text "test_element_text" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Single-item response'):
            err_msg = (
                'Unable to find element text "test_element_text" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<a href="">other_element_text</a>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="">other_element_text</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Multi-item response'):
            err_msg = (
                'Unable to find element text "test_element_text" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="">other_element_text Some text.</a>\n'
                '<a href="">another_element_text Some more text.</a>\n'
                '<a href="">test Some text with the str "element_text" in it.</a>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <a href="">other_element_text Some text.</a>
                        <a href="">another_element_text Some more text.</a>
                        <a href="">test Some text with the str "element_text" in it.</a>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_elements_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

    def test__find_element_by_text__success(self):
        """
        Tests find_element_by_text() function, in cases when it should succeed.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_text__success.html').resolve())

        with self.subTest('When expected element is the only item, with standard element'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="">test_element_text</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_text(driver, 'test_element_text')
            self.assertText('<a href="">\n test_element_text\n</a>', results)

        with self.subTest('When expected element exists plus extra'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <ul>
                            <li><a href="">test_element_text One</a></li>
                        </ul>
                        <ul></ul>
                    </div>
                    <div>
                        <ul></ul>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            results = self.find_element_by_text(driver, 'test_element_text')
            self.assertText('<a href="">\n test_element_text One\n</a>', results)

    def test__find_element_by_text__failure(self):
        """
        Tests find_element_by_text() function, in cases when it should fail.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__find_element_by_text__failure.html').resolve())

        with self.subTest('When expected text is not present - Blank response'):
            err_msg = (
                'Unable to find element text "test_element_text" in content. Provided content was:\n'
                '<html><head></head><body></body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Single-item response'):
            err_msg = (
                'Unable to find element text "test_element_text" in content. '
                'Provided content was:\n'
                '<html><head></head><body>'
                '<a href="">other_element_text</a>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="">other_element_text</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is not present - Multi-item response'):
            err_msg = (
                'Unable to find element text "test_element_text" in content. Provided content was:\n'
                '<html><head></head><body>'
                '<div>\n'
                '<h1>Page Header</h1>\n'
                '<a href="">other_element_text Some text.</a>\n'
                '<a href="">another_element_text Some more text.</a>\n'
                '<a href="">test Some text with the str "element_text" in it.</a>\n'
                '</div>\n'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write(
                    """
                    <div>
                        <h1>Page Header</h1>
                        <a href="">other_element_text Some text.</a>
                        <a href="">another_element_text Some more text.</a>
                        <a href="">test Some text with the str "element_text" in it.</a>
                    </div>
                    """
                )

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

        with self.subTest('When expected text is present multiple times'):
            err_msg = (
                'Found multiple instances of "test_element_text" element text. Expected only one instance. Content was:\n'
                '<html><head></head><body>'
                '<a href="">test_element_text</a><a href="">test_element_text</a>'
                '</body></html>'
            )

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<a href="">test_element_text</a><a href="">test_element_text</a>')

            # Get driver object to open generated file.
            driver = self.get_driver()
            driver.get('file://{0}'.format(file_name))

            with self.assertRaises(AssertionError) as err:
                self.find_element_by_text(driver, 'test_element_text')
            self.assertText(err_msg, str(err.exception))

    # endregion Helper Function Tests


class UniversalLiveTestMixin__DriverTests:
    """Tests which apply to all LiveServerTestCase classes (both selenium and channels).

    Specifically, this mixin contains tests that mess with driver create/grab/destroy.
    Easier to just keep it separate from the rest, to ensure consistency in testing.
    """

    def test__driver_handling(self):
        """
        Tests standard create/get/destroy driver functions.
        """
        # Declare file name for all subtests.
        file_name = str(Path('./tests/mock_pages/test__driver_handling.html').resolve())

        with self.subTest('Test driver_create() function'):
            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<h1>Driver 1</h1>')
                file.write('<h2>Driver 1</h2>')
                file.write('<h3>Driver 1</h3>')
                file.write('<h4>Driver 1</h4>')
                file.write('<h5>Driver 1</h5>')
                file.write('<h6>Driver 1</h6>')
                file.write('<p>Driver 1</p>')
                file.write('<span>Driver 1</span>')
                file.write('<li>Driver 1</li>')

            # Get driver object to open generated file.
            driver = self.create_driver()
            first_driver = driver
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n Driver 1\n</li>', results)

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<h1>Driver 2</h1>')
                file.write('<h2>Driver 2</h2>')
                file.write('<h3>Driver 2</h3>')
                file.write('<h4>Driver 2</h4>')
                file.write('<h5>Driver 2</h5>')
                file.write('<h6>Driver 2</h6>')
                file.write('<p>Driver 2</p>')
                file.write('<span>Driver 2</span>')
                file.write('<li>Driver 2</li>')

            # Get driver object to open generated file.
            driver = self.create_driver()
            second_driver = driver
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n Driver 2\n</li>', results)

            # Open file and write expected page contents.
            with open(file_name, 'w') as file:
                file.write('<h1>Driver 3</h1>')
                file.write('<h2>Driver 3</h2>')
                file.write('<h3>Driver 3</h3>')
                file.write('<h4>Driver 3</h4>')
                file.write('<h5>Driver 3</h5>')
                file.write('<h6>Driver 3</h6>')
                file.write('<p>Driver 3</p>')
                file.write('<span>Driver 3</span>')
                file.write('<li>Driver 3</li>')

            # Get driver object to open generated file.
            driver = self.create_driver()
            third_driver = driver
            driver.get('file://{0}'.format(file_name))

            results = self.find_elements_by_tag(driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n Driver 3\n</li>', results)

        # Three separate drivers created.
        # We have verified we can access expected data immediately after each driver creation.
        # Now verify we can switch between them and still get expected data.
        # Aka, verify that we didn't accidentally reuse the same window for all above tests.
        with self.subTest('Test driver_get() function'):
            # Verify we actually have three our separate drivers.
            self.assertEqual(4, len(self._driver_set))
            self.assertIn(first_driver, self._driver_set)
            self.assertIn(second_driver, self._driver_set)
            self.assertIn(third_driver, self._driver_set)

            # Verify each driver is different, each driver handle is unique, and each driver session is unique.
            # Driver checks.
            self.assertNotEqual(first_driver, second_driver)
            self.assertNotEqual(second_driver, third_driver)
            self.assertNotEqual(first_driver, third_driver)
            # Driver "handle" checks.
            self.assertNotEqual(first_driver.window_handles, second_driver.window_handles)
            self.assertNotEqual(second_driver.window_handles, third_driver.window_handles)
            self.assertNotEqual(first_driver.window_handles, third_driver.window_handles)
            # Driver session checks.
            self.assertNotEqual(first_driver.session_id, second_driver.session_id)
            self.assertNotEqual(second_driver.session_id, third_driver.session_id)
            self.assertNotEqual(first_driver.session_id, third_driver.session_id)

            # Verify each driver only has one associated window.
            self.assertEqual(1, len(first_driver.window_handles))
            self.assertEqual(1, len(second_driver.window_handles))
            self.assertEqual(1, len(third_driver.window_handles))

            # Verify able to switch between drivers and get different data for each.
            self.switch_to_window(first_driver, 0)
            results = self.find_elements_by_tag(first_driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n Driver 1\n</li>', results)

            self.switch_to_window(second_driver, 0)
            results = self.find_elements_by_tag(second_driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n Driver 2\n</li>', results)

            self.switch_to_window(third_driver, 0)
            results = self.find_elements_by_tag(third_driver, 'li')
            self.assertEqual(len(results), 1)
            self.assertIn('<li>\n Driver 3\n</li>', results)

        # Verified that our drivers are unique and have expected data.
        # Now verify we can close individual drivers as expected.
        # Note: For below tests, unsure how useful the session_id comparisons are.
        #   But it's at least attempting to verify a driver is still present, and then check said driver for a known
        #   still-valid id. Unsure how better to identify drivers when other tests are generating an arbitrary number
        #   of drivers in the background.
        with self.subTest('Test driver_close() function'):
            # Double check we still have three separate drivers.
            self.assertEqual(4, len(self._driver_set))

            # Save some data for verification.
            first_session_id = first_driver.session_id
            second_session_id = second_driver.session_id
            third_session_id = third_driver.session_id

            # Close our middle driver.
            self.close_driver(second_driver)

            # Verify actually closed.
            self.assertEqual(3, len(self._driver_set))
            self.assertIn(first_driver, self._driver_set)
            self.assertNotIn(second_driver, self._driver_set)
            self.assertIn(third_driver, self._driver_set)
            self.assertEqual(first_session_id, first_driver.session_id)
            self.assertEqual(third_session_id, third_driver.session_id)
            self.assertNotEqual(second_session_id, first_driver.session_id)
            self.assertNotEqual(second_session_id, third_driver.session_id)

            # Close first driver.
            self.close_driver(third_driver)

            # Verify actually closed.
            self.assertEqual(2, len(self._driver_set))
            self.assertIn(first_driver, self._driver_set)
            self.assertNotIn(second_driver, self._driver_set)
            self.assertNotIn(third_driver, self._driver_set)
            self.assertEqual(first_session_id, first_driver.session_id)
            self.assertNotEqual(second_session_id, first_driver.session_id)
            self.assertNotEqual(third_session_id, first_driver.session_id)

            # Close remaining driver and check that none (other than default) remain.
            self.close_driver(first_driver)
            self.assertEqual(1, len(self._driver_set))
            self.assertNotIn(first_driver, self._driver_set)
            self.assertNotIn(second_driver, self._driver_set)
            self.assertNotIn(third_driver, self._driver_set)
