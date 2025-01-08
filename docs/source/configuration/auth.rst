Auth Handling Configuration
***************************

The following
`Django settings <https://docs.djangoproject.com/en/dev/topics/settings/>`_
allow configuration of the **ExpandedTestCases** package, regarding User
and Auth settings.

All of these settings are optional, and will fall back to a default value if
not defined.


.. Note::
    By default, **ExpandedTestCases** will always generate 4 default test users.
    One super user, one admin user, one deactivated User, and one standard user.

    Most settings on this page change properties for generation and handling
    of these users.

    Some of these settings also change general user handling during test
    runtime.


Configuring Test Users
======================

AUTO_GENERATE_USERS
-------------------

By default, **ExpandedTestCases** provides default testing users.
If this is not desired, this setting can be set to False to disable
said functionality.

If test users are disabled, then most other settings on this page
will have no effect either.


:Type: ``bool``
:Default: ``True``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_AUTO_GENERATE_USERS = False


REQUEST_USER_STRICTNESS
-----------------------

This setting configures
:doc:`Response Assertions<../test_cases/integration_test_case/response_assertions>`,
when no user value is explicitly passed in.

To match with Django's default behavior, these assertions will default to
using an
`Anonymous
User <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#anonymoususer-object>`_
in any page requests, when no user is passed in.

Alternatively, this setting can be set to ``relaxed`` or ``strict`` to change
this behavior.

The ``relaxed`` mode will auto-provide the "standard user" instance, if a user
instance is not explicitly passed in.

Meanwhile, the ``strict`` mode requires that any response test either have the
``auto_login`` arg set to False, or that a user instance explicitly
be provided.
If one of these two criteria are not met, then the assertion will raise a
``ValidationError``.


.. note::
    When the above description mentions "providing a user instance", the ETC
    package can accept this in one of two ways.

    First, each IntegrationTest
    :doc:`Response Assertion<../test_cases/integration_test_case/response_assertions>`
    has a ``user`` arg. This is the most
    direct way to pass in a user, on a per-assertion basis.

    Alternatively, if you find yourself having multiple response assertions
    in a row that all use the same user, you can set the class variable
    ``self.user``.
    All tests that follow afterwards will fall back to this
    ``self.user`` variable, if no user is provided as an arg.


:Type: ``string``
:Default: ``anonymous``
:Options: [``anonymous``, ``relaxed``, ``strict``]

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_REQUEST_USER_STRICTNESS = 'strict'


Configuring Test User Identifiers
=================================

The following settings allow specifying what field is used as the User model's
"identifier", as well as what value each user is populated with.


USER_MODEL_IDENTIFIER
---------------------

By default, this package assumes a project uses the ``username`` field on a
user as the primary identifier.

This setting allows specifying a different identifier field.
To do so, provide the literal model field name intended to use.


:Type: ``string``
:Default: ``username``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER = 'email'


DEFAULT_SUPER_USER_IDENTIFIER
-----------------------------

By default, this package will generate a test superuser model
identified by either ``super_user``, or ``super_user@example.com``.
(Which one is selected depends on the above ``USER_MODEL_IDENTIFIER`` value).

Alternatively, specify a custom identifier here.


:Type: ``string``
:Default: ``test_superuser`` or ``test_superuser@example.com``, depending on
          above USER_MODEL_IDENTIFIER setting.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_SUPER_USER_IDENTIFIER = 'my_really_cool_value'


DEFAULT_ADMIN_USER_IDENTIFIER
-----------------------------

By default, this package will generate a test admin user model
identified by either ``test_admin``, or ``test_admin@example.com``.
(Which one is selected depends on the above ``USER_MODEL_IDENTIFIER`` value).

Alternatively, specify a custom identifier here.


:Type: ``string``
:Default: ``test_admin`` or ``test_admin@example.com``, depending on above
          USER_MODEL_IDENTIFIER setting.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_ADMIN_USER_IDENTIFIER = 'my_really_cool_value'


DEFAULT_STANDARD_USER_IDENTIFIER
--------------------------------

By default, this package will generate a test standard user model
identified by either ``test_user``, or ``test_user@example.com``.
(Which one is selected depends on the above ``USER_MODEL_IDENTIFIER`` value).

Alternatively, specify a custom identifier here.


:Type: ``string``
:Default: ``test_user`` or ``test_user@example.com``, depending on above
          USER_MODEL_IDENTIFIER setting.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_STANDARD_USER_IDENTIFIER = 'my_really_cool_value'


DEFAULT_INACTIVE_USER_IDENTIFIER
--------------------------------

By default, this package will generate a test standard user model
identified by either ``test_inactive``, or ``test_inactive@example.com``.
(Which one is selected depends on the above ``USER_MODEL_IDENTIFIER`` value).

Alternatively, specify a custom identifier here.


:Type: ``string``
:Default: ``test_inactive`` or ``test_inactive@example.com``, depending on above
          USER_MODEL_IDENTIFIER setting.

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_INACTIVE_USER_IDENTIFIER = 'my_really_cool_value'



Other Test User Configurations
==============================


DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD
------------------------------------------

When generating any test user, **ExpanedTestCases** will provide a default
password if none is provided.
This password can be changed here.


:Type: ``string``
:Default: ``password``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_DEFAULT_PASSWORD = 'my_new_password'


DJANGO_EXPANDED_TESTCASES_GENERATE_USERS_WITH_REAL_NAMES
--------------------------------------------------------

When generating four provided test users, this package will
also attempt to generate name values.

By default, the super user attempts to generate with
``SuperUserFirst`` as the first_name field and ``SuperUserLast`` as the
last_name field.

For more normalized names, set this to true.
For example, this will change the super user to generate with the name
``John Doe``, instead of ``SuperUserFirst SuperUserLast``.


:Type: ``bool``
:Default: ``False``

**Example:**

.. code::

    DJANGO_EXPANDED_TESTCASES_GENERATE_USERS_WITH_REAL_NAMES = True
