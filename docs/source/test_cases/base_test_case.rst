BaseTestCase
************


The **BaseTestCase** class provides minimal additional functionality above what
the Django
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
class provides.

This classes main focus is to add some basic users that can be used in testing,
as well as some helper functions to work with those users.


Custom Assertions
=================


assertText
----------

.. code::

    assertText(actual_text, expected_text, strip=True)


Currently, this is mostly a wrapper for assertEqual(), which prints full
values to console on mismatch.

In the future, this may be updated to have more useful AssertionFailure
output, particularly for long values.

:param actual_text: The value you wish to verify.
:param expected_text: The value to compare against. These should match.


Helper Functions
================

Reminder that the ``BaseTestCase`` class is meant to be minimalistic. So most
"helper functions" here are simply basic wrappers which sanitize all reasonable
types of input, and then return the expected value.


get_user
--------

.. code::

    get_user(user, password='password')

Helper function to obtain a given User object.

Treats the provided value as the `username` field. Returns the User object that
matches. If no such User exists in the database yet, then a new one is first
created.

For testing purposes, also makes sure the provided password is assigned to the
user, and then includes this raw value as an attribute on the returned object.

:param password: The password to assign this user. On the returned User
                object, the raw password value can be accessed via a
                provided ``unhashed_password`` field.

:return: Found User object.


add_user_permission
-------------------

.. code::

    add_user_permission(user_permission, user='test_user')

Helper function to add
`permissions <https://docs.djangoproject.com/en/dev/topics/auth/default/#permissions-and-authorization>`_
to a given User.

:param user_permission: Permission object, or name of permission object, to
                       add to User.
:parm user: User to add permission to. Defaults to ``test_user``.

:return: Updated User object.


add_user_group
--------------

.. code::

    add_user_group(user_group, user='test_user')

Helper function to add
`groups <https://docs.djangoproject.com/en/dev/topics/auth/default/#groups>`_
to a given User.

:param user_group: Group object, or name of group object, to add to User.
:param user: User to add group to. Defaults to ``test_user``.

:return: Updated User object.


generate_get_url
----------------

.. code::

    generate_get_url(url=None, **kwargs)

Helper function to generate a full GET request URL.

Note: If you're repeatedly accessing the same URL, you can define the value
```self.url``` in the **BaseTestCase** class.

Any provided kwargs are assumed to be
`URL Parameters <https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL#parameters>`_,
and are appended to the end of the URL accordingly.

:param url: The desired url string value to use as the
           `URL path <https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL#path_to_resource>`_.

:return: The generated url string.
