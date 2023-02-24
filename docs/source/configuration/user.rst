User Setting Configuration
**************************

The following
`Django settings <https://docs.djangoproject.com/en/dev/topics/settings/>`_
allow configuration of the **ExpandedTestCases** package, regarding User
settings.

All of these settings are optional, and will fall back to a default value if
not defined.

Note::
    By default, **ExpandedTestCases** will always generate 4 default users. One
    super user, one admin user, one deactivated User, and one standard user.

    Most of these settings change properties on generation and handling of
    these users.

    Some of these settings also change general user handling during test
    runtime.


Configuring Test User Identifiers
=================================

The following settings allow specifying what field is used as the User model's
"identifier", as well as what value each user is populated with.

DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER
-----------------------------------------------

By default, Django assumes a project uses the ``username`` field on a user as
the primary identifier.
This setting allows specifying a different identifier field.

:Type: ``string``
:Default: ``username``

Example::

    DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER = 'email'


DJANGO_EXPANDED_TESTCASES_DEFAULT_SUPER_USER_IDENTIFIER
-------------------------------------------------------

By default, **ExpanedTestCases** will generate a test superuser model
identified by either ``super_user``, or ``super_user@example.com``.
Which one is selected depends on the above
``DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER`` value.

Alternatively, specify a custom identifier here.

:Type: ``string``
:Default: ``test_superuser`` or ``test_superuser@example.com``, depending on
          above IDENTIFIER setting.

Example::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_SUPER_USER_IDENTIFIER = 'my_really_cool_value'


DJANGO_EXPANDED_TESTCASES_DEFAULT_ADMIN_USER_IDENTIFIER
-------------------------------------------------------

By default, **ExpanedTestCases** will generate a test admin user model
identified by either ``test_admin``, or ``test_admin@example.com``.
Which one is selected depends on the above
``DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER`` value.

Alternatively, specify a custom identifier here.

:Type: ``string``
:Default: ``test_admin`` or ``test_admin@example.com``, depending on above
          IDENTIFIER setting.

Example::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_ADMIN_USER_IDENTIFIER = 'my_really_cool_value'


DJANGO_EXPANDED_TESTCASES_DEFAULT_STANDARD_USER_IDENTIFIER
----------------------------------------------------------

By default, **ExpanedTestCases** will generate a test standard user model
identified by either ``test_user``, or ``test_user@example.com``.
Which one is selected depends on the above
``DJANGO_EXPANDED_TESTCASES_DEFAULT_STANDARD_USER_IDENTIFIER`` value.

Alternatively, specify a custom identifier here.

:Type: ``string``
:Default: ``test_user`` or ``test_user@example.com``, depending on above
          IDENTIFIER setting.

Example::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_STANDARD_USER_IDENTIFIER = 'my_really_cool_value'


Other Test User Configurations
==============================

DJANGO_EXPANDED_TESTCASES_DEFAULT_INACTIVE_USER_IDENTIFIER
----------------------------------------------------------

By default, **ExpanedTestCases** will generate a test inactive user model
identified by either ``test_inactive``, or ``test_inactive@example.com``.
Which one is selected depends on the above
``DJANGO_EXPANDED_TESTCASES_DEFAULT_INACTIVE_USER_IDENTIFIER`` value.

Alternatively, specify a custom identifier here.

:Type: ``string``
:Default: ``test_inactive`` or ``test_inactive@example.com``, depending on above
          IDENTIFIER setting.

Example::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_INACTIVE_USER_IDENTIFIER = 'my_really_cool_value'


DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD
------------------------------------------

When generating any test user, **ExpanedTestCases** will provide a default
password if none is provided. This password can be changed here.

:Type: ``string``
:Default: ``password``

Example::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD = 'a_new_password'


DJANGO_EXPANDED_TESTCASES_GENERATE_USERS_WITH_REAL_NAMES
--------------------------------------------------------

When generating initial test users, **ExpanedTestCases** will attempt to provide
default names. For example, the super user attempts to generate with
``SuperUserFirst`` as the first_name field and ``SuperUserLast`` as the
last_name field.

For more normalized names, set this value to true. For example, this will change
the super user to generate with the name ``John Doe``.

:Type: ``bool``
:Default: ``False``

Example::

    DJANGO_EXPANDED_TESTCASES_GENERATE_USERS_WITH_REAL_NAMES = True
