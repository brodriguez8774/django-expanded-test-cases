"""
Tests for test_cases/base_test_case.py.
"""

# System Imports.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# User Imports.
from django_expanded_test_cases import BaseTestCase


class BaseClassTest(BaseTestCase):
    """Tests for BaseTestCase class."""

    # region User Management Function Tests

    def test__get_user(self):
        """
        Tests get_user() function.
        """
        with self.subTest('Test "test_superuser" user - Default password'):
            test_superuser = self.get_user('test_superuser')

            self.assertEqual(test_superuser, self.test_superuser)
            self.assertEqual(test_superuser.username, 'test_superuser')
            self.assertTrue(test_superuser.check_password('password'))
            self.assertEqual(test_superuser.unhashed_password, 'password')
            self.assertEqual(test_superuser.is_superuser, True)
            self.assertEqual(test_superuser.is_staff, False)

        with self.subTest('Test "test_admin" user - Default password'):
            test_admin = self.get_user('test_admin')

            self.assertEqual(test_admin, self.test_admin)
            self.assertEqual(test_admin.username, 'test_admin')
            self.assertTrue(test_admin.check_password('password'))
            self.assertEqual(test_admin.unhashed_password, 'password')
            self.assertEqual(test_admin.is_superuser, False)
            self.assertEqual(test_admin.is_staff, True)

        with self.subTest('Test "test_user" user - Default password'):
            test_user = self.get_user('test_user')

            self.assertEqual(test_user, self.test_user)
            self.assertEqual(test_user.username, 'test_user')
            self.assertTrue(test_user.check_password('password'))
            self.assertEqual(test_user.unhashed_password, 'password')
            self.assertEqual(test_user.is_superuser, False)
            self.assertEqual(test_user.is_staff, False)

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

        with self.subTest('Test add perm by codename'):
            # Test adding permission.
            self.add_user_permission('test_perm_1', user='test_user')
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Test adding different permission.
            self.add_user_permission('test_perm_2', user='test_admin')
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

        with self.subTest('Test add perm by name'):
            # Test adding permission.
            self.add_user_permission('Test Perm 1', user='test_user')
            self.assertEqual(self.test_user.user_permissions.all().count(), 1)
            self.assertEqual(self.test_user.user_permissions.all()[0], perm_1)

            # Test adding different permission.
            self.add_user_permission('Test Perm 2', user='test_admin')
            self.assertEqual(self.test_admin.user_permissions.all().count(), 1)
            self.assertEqual(self.test_admin.user_permissions.all()[0], perm_2)

            # Verify other users are unaffected.
            self.assertFalse(self.test_superuser.user_permissions.all().exists())

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

        # Test adding group.
        self.add_user_group('group_1', user='test_user')
        self.assertEqual(self.test_user.groups.all().count(), 1)
        self.assertEqual(self.test_user.groups.all()[0], group_1)

        # Test adding different group.
        self.add_user_group('group_2', user='test_admin')
        self.assertEqual(self.test_admin.groups.all().count(), 1)
        self.assertEqual(self.test_admin.groups.all()[0], group_2)

        # Verify other users are unaffected.
        self.assertFalse(self.test_superuser.groups.all().exists())

    # endregion User Management Function Tests

    # region Helper Function Tests

    def test__generate_get_url(self):
        """
        Tests generate_get_url() function.
        """
        with self.subTest('Generate from passed "url" param'):
            # Test no params.
            url = self.generate_get_url('http://127.0.0.1/')
            self.assertEqual(url, 'http://127.0.0.1/')

            # Test one str param.
            url = self.generate_get_url('http://127.0.0.1/', test_1='one')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one')

            # Test two str params.
            url = self.generate_get_url('http://127.0.0.1/', test_1='one', test_2='two')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one&test_2=two')

            # Test one non-str simple param.
            url = self.generate_get_url('http://127.0.0.1/', test_1=1)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1')

            # Test two non-str simple params.
            url = self.generate_get_url('http://127.0.0.1/', test_1=1, test_2=True)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1&test_2=True')

            # Test one non-str complex param.
            url = self.generate_get_url('http://127.0.0.1/', test_1=['a', 'b', 'c'])
            self.assertEqual(url, 'http://127.0.0.1/?test_1=%5B%27a%27%2C+%27b%27%2C+%27c%27%5D')

            # Test two non-str complex params.
            url = self.generate_get_url('http://127.0.0.1/', test_1=['foo', 'bar'], test_2={'cat': 'Tabby', 'dog': 'Spot'})
            self.assertEqual(
                url,
                (
                    'http://127.0.0.1/?test_1=%5B%27foo%27%2C+%27bar%27%5D&test_2=%7B%27cat%27%3A+'
                    '%27Tabby%27%2C+%27dog%27%3A+%27Spot%27%7D'
                ),
            )

        with self.subTest('Generate from class "self.url" variable'):
            # Set class variable.
            self.url = 'http://127.0.0.1/'

            # Test no params.
            url = self.generate_get_url()
            self.assertEqual(url, 'http://127.0.0.1/')

            # Test one str param.
            url = self.generate_get_url(test_1='one')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one')

            # Test two str params.
            url = self.generate_get_url(test_1='one', test_2='two')
            self.assertEqual(url, 'http://127.0.0.1/?test_1=one&test_2=two')

            # Test one non-str simple param.
            url = self.generate_get_url(test_1=1)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1')

            # Test two non-str simple params.
            url = self.generate_get_url(test_1=1, test_2=True)
            self.assertEqual(url, 'http://127.0.0.1/?test_1=1&test_2=True')

            # Test one non-str complex param.
            url = self.generate_get_url(test_1=['a', 'b', 'c'])
            self.assertEqual(url, 'http://127.0.0.1/?test_1=%5B%27a%27%2C+%27b%27%2C+%27c%27%5D')

            # Test two non-str complex params.
            url = self.generate_get_url(test_1=['foo', 'bar'], test_2={'cat': 'Tabby', 'dog': 'Spot'})
            self.assertEqual(
                url,
                (
                    'http://127.0.0.1/?test_1=%5B%27foo%27%2C+%27bar%27%5D&test_2=%7B%27cat%27%3A+'
                    '%27Tabby%27%2C+%27dog%27%3A+%27Spot%27%7D'
                ),
            )

    def assert_symbol_standardization(self, symbol_str, expected_return):
        """
        Helper sub-function for testing the standardization methods.
        """
        # Test in smaller child function.
        return_val = self.standardize_symbols(symbol_str)
        self.assertEqual(return_val, expected_return)

        # Test in full parent function.
        return_val = self.standardize_characters(symbol_str)
        self.assertEqual(return_val, expected_return)

    def assert_number_standardization(self, number_str, expected_return):
        """
        Helper sub-function for testing the standardization methods.
        """
        # Test in smaller child function.
        return_val = self.standardize_numbers(number_str)
        self.assertEqual(return_val, expected_return)

        # Test in full parent function.
        return_val = self.standardize_characters(number_str)
        self.assertEqual(return_val, expected_return)

    def assert_letter_standardization(self, letter_str, expected_return):
        """
        Helper sub-function for testing the standardization methods.
        """
        # Test in smaller child function.
        return_val = self.standardize_letters(letter_str)
        self.assertEqual(return_val, expected_return)

        # Test in full parent function.
        return_val = self.standardize_characters(letter_str)
        self.assertEqual(return_val, expected_return)

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
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('</br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('<br/>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('<br />')
            self.assertEqual(return_val, '')
        with self.subTest('Test <br> tag - As inner element'):
            return_val = self.standardize_newlines('A<br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A</br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A<br/>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A<br />B')
            self.assertEqual(return_val, 'A\nB')

        with self.subTest('Test single newline characters - Isolated'):
            return_val = self.standardize_newlines('\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\r\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n\r')
            self.assertEqual(return_val, '')
        with self.subTest('Test single newline characters - As inner element'):
            return_val = self.standardize_newlines('A\nB')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\r\nB')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n\rB')
            self.assertEqual(return_val, 'A\nB')

        with self.subTest('Test repeated newline characters - Isolated'):
            return_val = self.standardize_newlines('\n\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n\n\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n\r\n\r\n')
            self.assertEqual(return_val, '')
        with self.subTest('Test repeated newline characters - As inner element'):
            return_val = self.standardize_newlines('A\n\nB')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n\n\nB')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n\r\n\r\nB')
            self.assertEqual(return_val, 'A\nB')

        with self.subTest('Test with whitespace - Isolated'):
            return_val = self.standardize_newlines('<br>   <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('<br>   <br>   <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('<br>   \n   <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n   \n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n   \n   \n')
            self.assertEqual(return_val, '')
        with self.subTest('Test with whitespace - As inner element'):
            return_val = self.standardize_newlines('A<br>   <br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A<br>   <br>   <br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A<br>   \n   <br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n   \nB')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n   \n   \nB')
            self.assertEqual(return_val, 'A\nB')

        with self.subTest('Test with non-breaking space - Isolated'):
            return_val = self.standardize_newlines('<br> &nbsp; <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('<br> &nbsp; <br> &nbsp; <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('<br> &nbsp; \n &nbsp; <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n &nbsp; \n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_newlines('\n &nbsp; \n &nbsp; \n')
            self.assertEqual(return_val, '')
        with self.subTest('Test with non-breaking space - As inner element'):
            return_val = self.standardize_newlines('A<br> &nbsp; <br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A<br> &nbsp; <br> &nbsp; <br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A<br> &nbsp; \n &nbsp; <br>B')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n &nbsp; \nB')
            self.assertEqual(return_val, 'A\nB')
            return_val = self.standardize_newlines('A\n &nbsp; \n &nbsp; \nB')
            self.assertEqual(return_val, 'A\nB')

    def test__standardize_whitespace(self):
        """
        Tests standardize_whitespace() function.
        """
        with self.subTest('Test <br> tag - Isolated'):
            return_val = self.standardize_whitespace('<br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('</br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('<br/>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('<br />')
            self.assertEqual(return_val, '')
        with self.subTest('Test <br> tag - As inner element'):
            return_val = self.standardize_whitespace('A<br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A</br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A<br/>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A<br />B')
            self.assertEqual(return_val, 'A B')

        with self.subTest('Test single newline characters - Isolated'):
            return_val = self.standardize_whitespace('\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\r\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n\r')
            self.assertEqual(return_val, '')
        with self.subTest('Test single newline characters - As inner element'):
            return_val = self.standardize_whitespace('A\nB')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\r\nB')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n\rB')
            self.assertEqual(return_val, 'A B')

        with self.subTest('Test repeated newline characters - Isolated'):
            return_val = self.standardize_whitespace('\n\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n\n\n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n\r\n\r\n')
            self.assertEqual(return_val, '')
        with self.subTest('Test repeated newline characters - As inner element'):
            return_val = self.standardize_whitespace('A\n\nB')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n\n\nB')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n\r\n\r\nB')
            self.assertEqual(return_val, 'A B')

        with self.subTest('Test with whitespace - Isolated'):
            return_val = self.standardize_whitespace('<br>   <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('<br>   <br>   <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('<br>   \n   <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n   \n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n   \n   \n')
            self.assertEqual(return_val, '')
        with self.subTest('Test with whitespace - As inner element'):
            return_val = self.standardize_whitespace('A<br>   <br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A<br>   <br>   <br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A<br>   \n   <br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n   \nB')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n   \n   \nB')
            self.assertEqual(return_val, 'A B')

        with self.subTest('Test with whitespace - Isolated'):
            return_val = self.standardize_whitespace('<br> &nbsp; <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('<br> &nbsp; <br> &nbsp; <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('<br> &nbsp; \n &nbsp; <br>')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n &nbsp; \n')
            self.assertEqual(return_val, '')
            return_val = self.standardize_whitespace('\n &nbsp; \n &nbsp; \n')
            self.assertEqual(return_val, '')
        with self.subTest('Test with whitespace - As inner element'):
            return_val = self.standardize_whitespace('A<br> &nbsp; <br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A<br> &nbsp; <br> &nbsp; <br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A<br> &nbsp; \n &nbsp; <br>B')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n &nbsp; \nB')
            self.assertEqual(return_val, 'A B')
            return_val = self.standardize_whitespace('A\n &nbsp; \n &nbsp; \nB')
            self.assertEqual(return_val, 'A B')

    # endregion Helper Function Tests
