"""
Tests for test_cases/base_test_case.py.
"""

# System Imports.

# User Imports.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django_expanded_test_cases.test_cases import BaseTestCase


class BaseClassTest(BaseTestCase):
    """Tests for BaseTestCase class."""

    def setUp(self, debug_print=None):
        # Run parent setup logic.
        super().setUp(debug_print=debug_print)

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

    def test__standardize_characters__symbols(self):
        """
        Tests symbols in standardize_characters() function.
        """
        with self.subTest('Test exclamation mark'):
            return_val = self.standardize_characters('&#33; &#x21; &excl; !')
            self.assertEqual(return_val, '! ! ! !')

        with self.subTest('Test quotation'):
            return_val = self.standardize_characters('&#34; &#x22; &quot; "')
            self.assertEqual(return_val, '" " " "')

        with self.subTest('Test number sign'):
            return_val = self.standardize_characters('&#35; &#x23; &num; #')
            self.assertEqual(return_val, '# # # #')

        with self.subTest('Test dollar sign'):
            return_val = self.standardize_characters('&#36; &#x24; &dollar; $')
            self.assertEqual(return_val, '$ $ $ $')

        with self.subTest('Test percent sign'):
            return_val = self.standardize_characters('&#37; &#x25; &percnt; %')
            self.assertEqual(return_val, '% % % %')

        with self.subTest('Test ampersand'):
            return_val = self.standardize_characters('&#38; &#x26; &amp; &')
            self.assertEqual(return_val, '& & & &')

        with self.subTest('Test apostrophe'):
            return_val = self.standardize_characters('&#39; &#x27; &apos; \'')
            self.assertEqual(return_val, "' ' ' '")

        with self.subTest('Test opening parenthesis'):
            return_val = self.standardize_characters('&#40; &#x28; &lpar; (')
            self.assertEqual(return_val, '( ( ( (')

        with self.subTest('Test closing parenthesis'):
            return_val = self.standardize_characters('&#41; &#x29; &rpar; )')
            self.assertEqual(return_val, ') ) ) )')

        with self.subTest('Test asterisk'):
            return_val = self.standardize_characters('&#42; &#x2A; &#x2a; &ast; *')
            self.assertEqual(return_val, '* * * * *')

        with self.subTest('Test plus'):
            return_val = self.standardize_characters('&#43; &#x2B; &#x2b; &plus; +')
            self.assertEqual(return_val, '+ + + + +')

        with self.subTest('Test comma'):
            return_val = self.standardize_characters('&#44; &#x2C; &#x2c; &comma; ,')
            self.assertEqual(return_val, ', , , , ,')

        with self.subTest('Test minus'):
            return_val = self.standardize_characters('&#45; &#8722; &#x2D; &#x2d; &minus; -')
            self.assertEqual(return_val, '- - - - - -')

        with self.subTest('Test period'):
            return_val = self.standardize_characters('&#46; &#x2E; &#x2e; &period; .')
            self.assertEqual(return_val, '. . . . .')

        with self.subTest('Test slash'):
            return_val = self.standardize_characters('&#47; &#x2F; &#x2f; &sol; /')
            self.assertEqual(return_val, '/ / / / /')

        with self.subTest('Test colon'):
            return_val = self.standardize_characters('&#58; &#x3A; &#x3a; &colon; :')
            self.assertEqual(return_val, ': : : : :')

        with self.subTest('Test semicolon'):
            return_val = self.standardize_characters('&#59; &#x3B; &#x3b; &semi; ;')
            self.assertEqual(return_val, '; ; ; ; ;')

        with self.subTest('Test less than'):
            return_val = self.standardize_characters('&#60; &#x3C; &#x3c; &lt; <')
            self.assertEqual(return_val, '< < < < <')

        with self.subTest('Test equals'):
            return_val = self.standardize_characters('&#61; &#x3D; &#x3d; &equals; =')
            self.assertEqual(return_val, '= = = = =')

        with self.subTest('Test greater than'):
            return_val = self.standardize_characters('&#62; &#x3E; &#x3e; &gt; >')
            self.assertEqual(return_val, '> > > > >')

        with self.subTest('Test question mark'):
            return_val = self.standardize_characters('&#63; &#x3F; &#x3f; &quest; ?')
            self.assertEqual(return_val, '? ? ? ? ?')

        with self.subTest('Test at sign'):
            return_val = self.standardize_characters('&#64; &#x40; &commat; @')
            self.assertEqual(return_val, '@ @ @ @')

        with self.subTest('Test opening square bracket'):
            return_val = self.standardize_characters('&#91; &#x5B; &#x5b; &lbrack; [')
            self.assertEqual(return_val, '[ [ [ [ [')

        with self.subTest('Test backslash'):
            return_val = self.standardize_characters('&#92; &#x5C; &#x5c; &bsol; \\')
            self.assertEqual(return_val, '\\ \\ \\ \\ \\')

        with self.subTest('Test closing square bracket'):
            return_val = self.standardize_characters('&#93; &#x5D; &#x5d; &rbrack; ]')
            self.assertEqual(return_val, '] ] ] ] ]')

        with self.subTest('Test up arrow'):
            return_val = self.standardize_characters('&#94; &#x5E; &#x5e; &Hat; ^')
            self.assertEqual(return_val, '^ ^ ^ ^ ^')

        with self.subTest('Test underscore'):
            return_val = self.standardize_characters('&#95; &#x5F; &#x5f; &lowbar; _')
            self.assertEqual(return_val, '_ _ _ _ _')

        with self.subTest('Test grave accent'):
            return_val = self.standardize_characters('&#96; &#x60; &grave; `')
            self.assertEqual(return_val, '` ` ` `')

        with self.subTest('Test opening dict bracket'):
            return_val = self.standardize_characters('&#123; &#x7B; &#x7b; &lbrace; {')
            self.assertEqual(return_val, '{ { { { {')

        with self.subTest('Test pipe'):
            return_val = self.standardize_characters('&#124; &#x7C; &#x7c; &vert; |')
            self.assertEqual(return_val, '| | | | |')

        with self.subTest('Test closing dict bracket'):
            return_val = self.standardize_characters('&#125; &#x7D; &#x7d; &rbrace; }')
            self.assertEqual(return_val, '} } } } }')

        with self.subTest('Test tilde'):
            return_val = self.standardize_characters('&#126; &#x7E; &#x7e; &tilde; ~')
            self.assertEqual(return_val, '~ ~ ~ ~ ~')

    # endregion Helper Function Tests
