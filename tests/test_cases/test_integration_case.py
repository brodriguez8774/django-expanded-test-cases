"""
Tests for test_cases/integration_test_case.py.
"""

# System Imports.
from django.http import HttpResponse

# User Imports.
from django_expanded_test_cases.test_cases import IntegrationTestCase


class IntegrationClassTest(IntegrationTestCase):
    """Tests for IntegrationTestCase class."""

    # region Assertion Tests

    # region Response Assertion Tests

    def test__assertResponse__url(self):
        """
        Tests URL value returned response object in assertResponse() function.
        """
        with self.subTest('With no site_root_url value defined - Via literal value'):
            # Test 404 page url.
            response = self.assertResponse('bad_url', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')
            response = self.assertResponse('bad_url/', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')
            response = self.assertResponse('127.0.0.1/bad_url/', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')
            response = self.assertResponse('///bad_url///', expected_status=404)
            self.assertEqual(response.url, '127.0.0.1/bad_url/')

            # Test "index" page url.
            response = self.assertResponse('')
            self.assertEqual(response.url, '127.0.0.1/')
            response = self.assertResponse('/')
            self.assertEqual(response.url, '127.0.0.1/')
            response = self.assertResponse('127.0.0.1/')
            self.assertEqual(response.url, '127.0.0.1/')

            # Test "login" page url.
            response = self.assertResponse('login/')
            self.assertEqual(response.url, '127.0.0.1/login/')
            response = self.assertResponse('/login/')
            self.assertEqual(response.url, '127.0.0.1/login/')
            response = self.assertResponse('127.0.0.1/login/')
            self.assertEqual(response.url, '127.0.0.1/login/')

            # Test "one message" page url.
            response = self.assertResponse('one-message/')
            self.assertEqual(response.url, '127.0.0.1/one-message/')
            response = self.assertResponse('/one-message/')
            self.assertEqual(response.url, '127.0.0.1/one-message/')
            response = self.assertResponse('127.0.0.1/one-message/')
            self.assertEqual(response.url, '127.0.0.1/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('two-messages/')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')
            response = self.assertResponse('/two-messages/')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')
            response = self.assertResponse('127.0.0.1/two-messages/')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('user/detail/1/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')
            response = self.assertResponse('/user/detail/1/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')
            response = self.assertResponse('127.0.0.1/user/detail/1/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('user/detail/2/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')
            response = self.assertResponse('/user/detail/2/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')
            response = self.assertResponse('127.0.0.1/user/detail/2/')
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')

        with self.subTest('With no site_root_url value defined - Via reverse()'):
            # Test "index" page url.
            response = self.assertResponse('expanded_test_cases:index')
            self.assertEqual(response.url, '127.0.0.1/')

            # Test "login" page url.
            response = self.assertResponse('expanded_test_cases:login')
            self.assertEqual(response.url, '127.0.0.1/login/')

            # Test "one message" page url.
            response = self.assertResponse('expanded_test_cases:one-message')
            self.assertEqual(response.url, '127.0.0.1/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('expanded_test_cases:two-messages')
            self.assertEqual(response.url, '127.0.0.1/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(1,))
            self.assertEqual(response.url, '127.0.0.1/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 2})
            self.assertEqual(response.url, '127.0.0.1/user/detail/2/')

        with self.subTest('With custom site_root_url value defined'):
            self.site_root_url = 'https://my_really_cool_site.com/'

            # Test "index" page url.
            response = self.assertResponse('expanded_test_cases:index')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/')

            # Test "login" page url.
            response = self.assertResponse('expanded_test_cases:login')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/login/')

            # Test "one message" page url.
            response = self.assertResponse('expanded_test_cases:one-message')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/one-message/')

            # Test "two messages" page url.
            response = self.assertResponse('expanded_test_cases:two-messages')
            self.assertEqual(response.url, 'https://my_really_cool_site.com/two-messages/')

            # Test "user detail" page url via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(1,))
            self.assertEqual(response.url, 'https://my_really_cool_site.com/user/detail/1/')

            # Test "user detail" page url via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 2})
            self.assertEqual(response.url, 'https://my_really_cool_site.com/user/detail/2/')

    def test__assertResponse__status_code(self):
        """
        Tests "status_code" functionality of assertResponse() function.
        """
        with self.subTest('With status_code=200 - Basic view'):
            # Test 200 in direct url.
            response = self.assertResponse('')
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url.
            response = self.assertResponse('expanded_test_cases:index')
            self.assertEqual(response.status_code, 200)

        with self.subTest('With status_code=200 - View with params'):
            # Test 200 in direct url.
            response = self.assertResponse('user/detail/1/')
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url, via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(2,))
            self.assertEqual(response.status_code, 200)

            # Test 200 in reverse() url, via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 3})
            self.assertEqual(response.status_code, 200)

        with self.subTest('With status_code=404'):
            # Test 404 in direct url.
            response = self.assertResponse('bad_url', expected_status=404)
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via args.
            response = self.assertResponse('expanded_test_cases:user-detail', args=(234,), expected_status=404)
            self.assertEqual(response.status_code, 404)

            # Test 404 in reverse() url, via kwargs.
            response = self.assertResponse('expanded_test_cases:user-detail', kwargs={'pk': 345}, expected_status=404)
            self.assertEqual(response.status_code, 404)

    def test__assertGetResponse(self):
        """
        Tests assertGetResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """
        response = self.assertGetResponse('expanded_test_cases:index')

        self.assertEqual(response.url, '127.0.0.1/')
        self.assertEqual(response.status_code, 200)

    def test__assertPostResponse(self):
        """
        Tests assertPostResponse() function.
        Note: Most logic in here passes into the assertResponse() function.
            Thus we just do basic checks here and do most of the heavy-testing in assertResponse().
        """
        response = self.assertPostResponse('expanded_test_cases:index')

        self.assertEqual(response.url, '127.0.0.1/')
        self.assertEqual(response.status_code, 200)

    # endregion Response Assertion Tests

    # region Element Assertion Tests

    def test__assertStatusCode__success(self):
        """
        Tests assertStatusCode() function, in cases when it should succeed.
        """
        with self.subTest('Status 200'):
            response = HttpResponse(status=200)
            self.assertStatusCode(response, 200)
            self.assertStatusCode(response.status_code, 200)

        with self.subTest('Status 400'):
            response = HttpResponse(status=400)
            self.assertStatusCode(response, 400)
            self.assertStatusCode(response.status_code, 400)

        with self.subTest('Status 403'):
            response = HttpResponse(status=403)
            self.assertStatusCode(response, 403)
            self.assertStatusCode(response.status_code, 403)

        with self.subTest('Status 404'):
            response = HttpResponse(status=404)
            self.assertStatusCode(response, 404)
            self.assertStatusCode(response.status_code, 404)

        with self.subTest('Status 500'):
            response = HttpResponse(status=500)
            self.assertStatusCode(response, 500)
            self.assertStatusCode(response.status_code, 500)

    def test__assertStatusCode__fail(self):
        """
        Tests assertStatusCode() function, in cases when it should fail.
        """
        with self.subTest('Expected 200, got 404'):
            response = HttpResponse(status=404)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response, 200)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response.status_code, 200)

        with self.subTest('Expected 404, got 200'):
            response = HttpResponse(status=200)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response, 404)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response.status_code, 404)

        with self.subTest('Expected 200, got 500'):
            response = HttpResponse(status=500)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response, 200)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response.status_code, 200)

        with self.subTest('Expected 500, got 200'):
            response = HttpResponse(status=200)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response, 500)
            with self.assertRaises(AssertionError):
                self.assertStatusCode(response.status_code, 500)

    def test__assertPageTitle__success(self):
        """
        Tests assertPageTitle() function, in cases when it should succeed.
        """
        with self.subTest('Including title tag in expected'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, '<title>Test Title</title>')

        with self.subTest('Including title tag in expected, with extra whitespace around tag'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, '   <title>    Test Title    </title>   ')

        with self.subTest('No title element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertPageTitle(response, '')

        with self.subTest('Title exists, but is empty'):
            response = HttpResponse('<title></title>')
            self.assertPageTitle(response, '')

        with self.subTest('Title exists, but is whitespace'):
            response = HttpResponse('<title>   </title>')
            self.assertPageTitle(response, '')

        with self.subTest('Basic title'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertPageTitle(response, 'Test Title')

        with self.subTest('Basic title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<title>   Test    Title   </title>')
            self.assertPageTitle(response, 'Test Title')

        with self.subTest('Complex title - Exact Match'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertPageTitle(response, 'Test Title | My Custom App | My Really Cool Site', exact_match=True)

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating) - Exact Match'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertPageTitle(response, 'Test Title | My Custom App | My Really Cool Site', exact_match=True)

        with self.subTest('Complex title - Loose Match'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertPageTitle(response, 'Test Title', exact_match=False)
            self.assertPageTitle(response, 'My Custom App', exact_match=False)
            self.assertPageTitle(response, 'My Really Cool Site', exact_match=False)

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating) - Loose Match'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertPageTitle(response, 'Test Title', exact_match=False)
            self.assertPageTitle(response, 'My Custom App', exact_match=False)
            self.assertPageTitle(response, 'My Really Cool Site', exact_match=False)

    def test__assertPageTitle__failure(self):
        """
        Tests assertPageTitle() function, in cases when it should fail.
        """
        with self.subTest('Checking for title when none exists'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('')
                self.assertPageTitle(response, 'Test Title')

        with self.subTest('Expected value is on page, but not in title tag'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Test Title')
            with self.assertRaises(AssertionError):
                response = HttpResponse('<h1>Test Title</h1><p>Test Title</p>')
                self.assertPageTitle(response, 'Test Title')

        with self.subTest('Assuming extra whitespace is still present'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('<title>   Test    Title   </title>')
                self.assertPageTitle(response, '   Test    Title   ')

        with self.subTest('Set to exact match, but only passing in title subsection'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'Test Title')
            with self.assertRaises(AssertionError):
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'My Custom App')
            with self.assertRaises(AssertionError):
                response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
                self.assertPageTitle(response, 'My Really Cool Site')

        with self.subTest('Set to partial match, but value is not in title'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Wrong Value')
            with self.assertRaises(AssertionError):
                response = HttpResponse('Test Title')
                self.assertPageTitle(response, 'Test Title and More')

    def test__assertPageHeader__success(self):
        """
        Tests assertPageHeader() function, in cases when it should succeed.
        """
        with self.subTest('Including header tag in expected'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertPageHeader(response, '<h1>Test Header</h1>')

        with self.subTest('Including header tag in expected, with extra whitespace around tag'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertPageHeader(response, '   <h1>    Test Header    </h1>   ')

        with self.subTest('No header element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertPageHeader(response, '')

        with self.subTest('Header exists, but is empty'):
            response = HttpResponse('<h1></h1>')
            self.assertPageHeader(response, '')

        with self.subTest('Header exists, but is whitespace'):
            response = HttpResponse('<h1>   </h1>')
            self.assertPageHeader(response, '')

        with self.subTest('Basic header'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertPageHeader(response, 'Test Header')

        with self.subTest('Basic header, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<h1>   Test    Header   </h1>')
            self.assertPageHeader(response, 'Test Header')

    def test__assertPageHeader__failure(self):
        """
        Tests assertPageHeader() function, in cases when it should fail.
        """
        with self.subTest('Checking for header when none exists'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('')
                self.assertPageHeader(response, 'Test Header')

        with self.subTest('Expected value is on page, but not in header tag'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('Test Header')
                self.assertPageHeader(response, 'Test Header')
            with self.assertRaises(AssertionError):
                response = HttpResponse('<h2>Test Header</h2><p>Test Header</p>')
                self.assertPageHeader(response, 'Test Header')

        with self.subTest('Assuming extra whitespace is still present'):
            with self.assertRaises(AssertionError):
                response = HttpResponse('<h1>   Test    Header   </h1>')
                self.assertPageHeader(response, '   Test    Header   ')

    # endregion Element Assertion Tests

    # endregion Assertion Tests

    # region Helper Function Tests

    def test__get_page_title__empty_title(self):
        """
        Tests get_page_title() function, when page title is empty.
        """
        with self.subTest('No title element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertEqual(self.get_page_title(response), '')
            self.assertEqual(self.get_page_title(response.content), '')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), '')

        with self.subTest('Title exists, but is empty'):
            response = HttpResponse('<title></title>')
            self.assertEqual(self.get_page_title(response), '')
            self.assertEqual(self.get_page_title(response.content), '')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), '')

        with self.subTest('Title exists, but is whitespace'):
            response = HttpResponse('<title>   </title>')
            self.assertEqual(self.get_page_title(response), '')
            self.assertEqual(self.get_page_title(response.content), '')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), '')

    def test__get_page_title__populated_title(self):
        """
        Tests get_page_title() function, when page title is populated.
        """
        with self.subTest('Basic title'):
            response = HttpResponse('<title>Test Title</title>')
            self.assertEqual(self.get_page_title(response), 'Test Title')
            self.assertEqual(self.get_page_title(response.content), 'Test Title')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), 'Test Title')

        with self.subTest('Basic title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<title>   Test    Title   </title>')
            self.assertEqual(self.get_page_title(response), 'Test Title')
            self.assertEqual(self.get_page_title(response.content), 'Test Title')
            self.assertEqual(self.get_page_title(response.content.decode('utf-8')), 'Test Title')

        with self.subTest('Complex title'):
            response = HttpResponse('<title>Test Title | My Custom App | My Really Cool Site</title>')
            self.assertEqual(self.get_page_title(response), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(self.get_page_title(response.content), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(
                self.get_page_title(response.content.decode('utf-8')),
                'Test Title | My Custom App | My Really Cool Site',
            )

        with self.subTest('Complex title, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse(
                '<title>   Test   Title    \n|\n   My Custom App   \n|\n   My Really Cool Site   </title>'
            )
            self.assertEqual(self.get_page_title(response), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(self.get_page_title(response.content), 'Test Title | My Custom App | My Really Cool Site')
            self.assertEqual(
                self.get_page_title(response.content.decode('utf-8')),
                'Test Title | My Custom App | My Really Cool Site',
            )

    def test__get_page_header__empty_header(self):
        """
        Tests get_page_header() function, when page H1 header is empty.
        """
        with self.subTest('No header element in response (simulates things like file downloads)'):
            response = HttpResponse('')
            self.assertEqual(self.get_page_header(response), '')
            self.assertEqual(self.get_page_header(response.content), '')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), '')

        with self.subTest('Header exists, but is empty'):
            response = HttpResponse('<h1></h1>')
            self.assertEqual(self.get_page_header(response), '')
            self.assertEqual(self.get_page_header(response.content), '')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), '')

        with self.subTest('Header exists, but is whitespace'):
            response = HttpResponse('<h1>   </h1>')
            self.assertEqual(self.get_page_header(response), '')
            self.assertEqual(self.get_page_header(response.content), '')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), '')

    def test__get_page_header__populated_header(self):
        """
        Tests get_page_header() function, when page H1 header is populated.
        """
        with self.subTest('Basic header'):
            response = HttpResponse('<h1>Test Header</h1>')
            self.assertEqual(self.get_page_header(response), 'Test Header')
            self.assertEqual(self.get_page_header(response.content), 'Test Header')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), 'Test Header')

        with self.subTest('Basic header, with extra whitespace (to simulate Django templating)'):
            response = HttpResponse('<h1>   Test    Header   </h1>')
            self.assertEqual(self.get_page_header(response), 'Test Header')
            self.assertEqual(self.get_page_header(response.content), 'Test Header')
            self.assertEqual(self.get_page_header(response.content.decode('utf-8')), 'Test Header')

    def test__get_context_messages(self):
        """
        Tests get_context_messages() function.
        """
        with self.subTest('No messages'):
            response = self._get_page_response('expanded_test_cases:index')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 0)

        with self.subTest('Single message'):
            response = self._get_page_response('expanded_test_cases:one-message')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 1)
            self.assertIn('This is a test message.', messages)

        with self.subTest('Two messages'):
            response = self._get_page_response('expanded_test_cases:two-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 2)
            self.assertIn('Test message #1.', messages)
            self.assertIn('Test message #2.', messages)

        with self.subTest('Three messages'):
            response = self._get_page_response('expanded_test_cases:three-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 3)
            self.assertIn('Test info message.', messages)
            self.assertIn('Test warning message.', messages)
            self.assertIn('Test error message.', messages)

        with self.subTest('TemplateResponse check'):
            response = self._get_page_response('expanded_test_cases:template-response-messages')
            messages = self.get_context_messages(response)
            self.assertEqual(len(messages), 3)
            self.assertIn('Test info message.', messages)
            self.assertIn('Test warning message.', messages)
            self.assertIn('Test error message.', messages)

    # endregion Helper Function Tests
