Managing Test Users
*******************

See also :doc:`configuration/auth`, for details on all project settings
to manipulate/change these provided user models.


Provided User Instances
=======================

Out of the box, the **Django-Expanded-Test-Cases** provides four separate users
to all tests.
These users help to ensure that tests are using a non-empty database. Feel free
to change (or ignore) these users as needed to best serve project
tests.

To outright disable these auto-generated users, see
:ref:`configuration/auth:AUTO_GENERATE_USERS`


Testing Response Default User Behavior
--------------------------------------

To outright disable these auto-generated users, see
:ref:`configuration/auth:REQUEST_USER_STRICTNESS`


User Identifiers
----------------

By default, these provided users have usernames follows:

* ``test_user`` - The default user, used in all corresponding functionality.
* ``test_admin`` - A provided "is_staff" user, who can see the Django admin.
* ``test_superuser`` - A provided "is_superuser" user, who can see all.
* ``test_inactive`` - A provided "disabled" user.

The ``test_user`` object is used as the default for most function calls.


If the ``DJANGO_EXPANDED_TESTCASES_USER_MODEL_IDENTIFIER`` setting is set to
``email``, then these usernames will have ``@example.com`` appended to the end.
For example, ``test_admin`` becomes ``test_admin@example.com``.


Furthermore, if these default identifiers aren't fitting for your project needs,
then each user can be configured with a
``DJANGO_EXPANDED_TESTCASES_DEFAULT_<user>_IDENTIFIER`` setting.

For more information about customizing test user identifiers, see
:ref:`configuration/auth:Configuring Test User Identifiers`


Expanding User Authentication Logic
===================================

Depending on the project, it's possible that users will need additional
authentication steps above and beyond the standard logic Django provides.
Generally, this is reflected in how users are set up in the corresponding
UnitTests.

To account for this, **Django-Expanded-Test-Cases** provides a function
that can be overridden for all test case classes that have built-in hook, to
allow injecting logic prior to loading a given view:

.. code::

    _get_login_user__extra_user_auth_setup()

A hook function to allow running any additional login/authentication logic
that may be required for a given user to access a view.

This function runs towards the end of user authentication, but before actually
attempting to log a user in via the Django testing client. By the time this
function executes, any built-in/provided user-permission and user-group logic
will have already ran.

By default, this function is emtpy, and does nothing other than return the
provided ``user`` arg.

:param user: The current user model that is attempting to log in to access a
            view.
:param user_permissions: Optional permissions to provide to the User before
                        attempting to render the response.
:param user_groups: Optional groups to provide to the User, before attempting to
                   render the response.
:return: The above ``user`` param, with any additional login logic run on it.

.. note::

    Any unhandled args/kwargs passed to a corresponding view function will
    also pass said args/kwargs inward to this auth hook function.

    This is to ensure that any required extra values for processing user
    authentication can ultimately be accessed for additional user login logic.


Test User Logic
===============

For most logic in **Django-Expanded-Test-Cases**, a view defaults to
manipulating a User object with the username of ``test_user``. This behavior can
be changed by providing a different User into the optional kwarg value of each
corresponding test call.

Alternatively, if a majority of the project tests check against a single user,
consider setting the attributes of the provided ``test_user`` model according
to project needs.

For example, the below snippet will change the first and last name of this
"default" testing user, such that all following UnitTesting logic will see this
updated first and last name, unless a separate user is explicitly provided.

.. code:: python

   // Grab provided ETC default testing user.
   my_default_user = self.get_user('test_user')

   // Change first and last name to some new value.
   my_default_user.first_name = 'UpdatedFirstName'
   my_default_user.last_name = 'UpdatedLastName'

   // Save model changes, so it persists in the database for the rest of the test.
   my_default_user.save()

If something like above is ran somewhere at the start of the inheriting test
class, then this logic will propagate to all inner tests. For example, placing
the above logic in either the class
`setUp() <https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp>`_
,
`setUpClass() <https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUpClass>`_
, or
`setUpTestData() <https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.TestCase.setUpTestData>`_
functions.

.. warning::

    If using one of the three above functions, reminder to account for Python's
    behavior of
    `super() <https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.SimpleTestCase.databases>`_
    , to prevent accidentally overriding pre-existing setup logic.
