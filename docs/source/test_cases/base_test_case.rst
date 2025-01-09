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


assertText()
------------

.. code::

    self.assertText(expected_text, actual_text, strip=True)


This is effectively a wrapper for assertEqual(), which is meant specifically
for comparing two bits of text.
The difference is that on failure, this attempts to print full values to
console on mismatch (``assertEqual()`` will truncate if values are too long).

Furthermore if `Colorama <https://pypi.org/project/colorama/>`_ is installed,
then text will be colored according to what characters did and did not match.


:param expected_text: The value you expect to find.
:param actual_text: The variable value you're testing against, to match against
                    ``expected_text``.
:param strip: A boolean indicating if white space characters should be stripped
              from both comparison values, prior to comparing.
              Set False to skip stripping.


assertTextStartsWith()
----------------------

.. code::

    self.assertTextStartsWith(expected_text, actual_text, strip=True)

Similar to above
:ref:`test_cases/base_test_case:assertText()`, except it only cares about
matching from the start of the comparison strings.

If ``expected_text`` is shorter than ``actual_text``, then this assertion
only matches equal to the total characters found in ``expected_text``.

If ``expected_text`` is longer than ``actual_text``, then raise an error
for the missing characters, but still attempt to compare full strings to
indicate if all other values match or not.


:param expected_text: The value you expect to find.
:param actual_text: The variable value you're testing against, to match against
                    ``expected_text``.
:param strip: A boolean indicating if white space characters should be stripped
              from both comparison values, prior to comparing.
              Set False to skip stripping.


assertTextEndsWith()
----------------------

.. code::

    self.assertTextEndsWith(expected_text, actual_text, strip=True)

Similar to above
:ref:`test_cases/base_test_case:assertText()`, except it only cares about
matching from the end of the comparison strings.

If ``expected_text`` is shorter than ``actual_text``, then this assertion
only matches equal to the total characters found in ``expected_text``.

If ``expected_text`` is longer than ``actual_text``, then raise an error
for the missing characters, but still attempt to compare full strings to
indicate if all other values match or not.


:param expected_text: The value you expect to find.
:param actual_text: The variable value you're testing against, to match against
                    ``expected_text``.
:param strip: A boolean indicating if white space characters should be stripped
              from both comparison values, prior to comparing.
              Set False to skip stripping.


Helper Functions
================

Reminder that the ``BaseTestCase`` class is meant to be minimalistic. So most
"helper functions" here are simply basic wrappers which sanitize all reasonable
types of input, and then return the expected value.


User Helper Functions
---------------------

get_user()
^^^^^^^^^^

.. code::

    self.get_user(user, password='password', extra_usergen_kwargs=**kwargs)

Helper function to obtain a given User object.

Treats the provided value as the field defined in settings as the
:ref:`user model identifier <configuration/auth:USER_MODEL_IDENTIFIER>`.

Returns the User object that matches.
If no such User exists in the database yet, then a new one is first created.

For testing purposes, also makes sure the provided password is assigned to the
test user object, and then includes this raw value as an attribute on the
returned object, found as ``user_object.password``.


:param user: Identifier to use to attempt to get user with.
:param password: The password to assign this user. On the returned User
                object, the raw password value can be accessed via a
                provided ``unhashed_password`` field.
:param extra_usergen_kwargs: Optional extra kwargs to pass into the
                            ``get_user_model().objects.create_user()`` function.
                            If your project has custom logic for the
                            ``create_user()`` function, then you can use this to
                            pass additional values in.

:return: Found User object.


add_user_permission()
^^^^^^^^^^^^^^^^^^^^^

.. code::

    self.add_user_permission(user_permission, user='test_user')

Helper function to add
`permissions <https://docs.djangoproject.com/en/dev/topics/auth/default/#permissions-and-authorization>`_
to a given User.


:param user_permission: Permission object, or name of permission object, to
                       add to User.
:parm user: User to add permission to.
            Can take in either a literal user object, or the identifier of a
            user.
            Defaults to ``test_user``.

:return: Updated User object.


add_user_group()
^^^^^^^^^^^^^^^^

.. code::

    self.add_user_group(user_group, user='test_user')

Helper function to add
`groups <https://docs.djangoproject.com/en/dev/topics/auth/default/#groups>`_
to a given User.


:param user_group: Group object, or name of group object, to add to User.
:param user: User to add group to.
             Can take in either a literal user object, or the identifier of a
             user.
             Defaults to ``test_user``.

:return: Updated User object.


Other Helper Functions
----------------------

generate_get_url()
^^^^^^^^^^^^^^^^^^

.. code::

    self.generate_get_url(url=None, **kwargs)

Helper function to generate a full GET request URL.

Any provided kwargs are assumed to be
`URL Parameters <https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL#parameters>`_,
and are appended to the end of the URL accordingly.

.. note::

    If you're repeatedly accessing the same URL, you can define the value
    ``self.url`` class variable.


:param url: The desired url string value to use as the
           `URL path <https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL#path_to_resource>`_.
:param kwargs: A dictionary of key-value pairs, to be converted to Url
               Parameters in the final url.

:return: The generated url string.


standardize_characters()
^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    self.standardize_characters(value)

Standardizes characters in provided string.

For example, in HTML, the "greater than" symbol can be denoted in multiple
ways, such as ``>``, ``&gt;``, ``&#62;``, or ``&#x3E``.

This function takes all such known "equivalent" representations of various
characters, and reformats them to a single type for consistency.

Many of the assertions in this package use this function, in order to make
testing easier and more consistent. (In our above example, the programmer
probably doesn't care WHICH version of the "greater than" symbol is present.
They most likely would only care that one of the several representations is
present.)


:param value: A string value to convert to standardized characters.

:return: A string of more standardized characters.


standardize_whitespace()
^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    self.standardize_whitespace(value)

Standardizes whitespace characters in provided string.

When possible, all repeating whitespace and whitespace-esque characters
(including newlines) are reduced down to a single space.


:param value: A string value to convert to standardized characters.

:return: A string of more standardized characters.


standardize_newlines()
^^^^^^^^^^^^^^^^^^^^^^

.. code::

    self.standardize_newlines(value)

Standardizes newline/whitespace characters in provided string.

When possible, all repeating newlines are converted down to a single ``\n``
character, and whitespace and whitespace-esque characters
(excluding newlines) are reduced down to a single space.

If multiple newline characters and space characters repeat in a row, then
that's reduced down to a single newline with up to one space on either side.


:param value: A string value to convert to standardized characters.

:return: A string of more standardized characters.
