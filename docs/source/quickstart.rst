Quickstart
**********


Installation
============

Load up your VirtualEnvironment of choice and run:

.. code:: python

    pip install django-expanded-test-cases


Alternatively, add ``django-expanded-test-cases`` to your respective project
requirements file.


Testing Environments
====================

The functionality provided by **Django-Expanded-Test-Cases** will work with
both the default
`Django Manage.py testing framework <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
and `PyTest <docs.pytest.org>`_.
However, one of the most useful features of the **Django-Expanded-Test-Cases**
package is that it automatically displays debug page response output to the
console on test failure.
This feature works best when running tests via **PyTest** and thus is
the recommend way to run tests.
For a complete explanation as to why, see the "important" note below.

Please refer to the `PyTest Configuration QuickStart`_ section for setting up
**PyTest** to work with this package.
Refer to the `Manage.py Test QuickStart`_ section for setting up
**Manage.py** to work with this package.


.. important::

    When running tests, ``manage.py``'s base functionality is to assume all
    testing console output is meaningful, and display it to the console
    unconditionally. As far as we can tell, there does not seem to be a way to
    change this behavior.

    Because of this behavior, when using this package in a project with a
    decent amount of tests, output results in an unwieldy amount of unhelpful
    text being sent to the console.
    This happens regardless of whether all tests pass or there are failures to
    review. Any useful information that might have occurred quickly becomes
    near impossible to find and gain knowledge from.

    Thus, when using this package, we **strongly** recommend switching to
    running tests via `PyTest <docs.pytest.org>`_.

    PyTest only sends extra output to the console on test failure. So, when
    there is extra output, you know that all of it is relevant to the failing
    tests.


PyTest Configuration QuickStart
-------------------------------

See https://docs.pytest.org/en/stable/ for official documentation.


PyTest can be fairly trivial to set up for a project.

To start, install the base PyTest package, plus any additional sub-packages that
apply to your project:

.. code:: python

    pytest                # Base Pytest package.
    pytest-asyncio        # Additional Pytest logic for asyncio support.
    pytest-django         # Additional Pytest logic for Django support.
    pytest-xdist          # Additional Pytest features, such as multithreading and looping.


Next, define a `pytest.ini` file at project root. A minimal, default
configuration is provided below. Otherwise see
https://docs.pytest.org/en/stable/reference/customize.html for official Pytest
customization documentation.

.. code:: ini

    [pytest]
    DJANGO_SETTINGS_MODULE = path.example.to.project.settings
    python_files = tests.py test_*.py
    log_level = NOTSET

.. note::

    For the above snippet, be sure to replace the ``DJANGO_SETTINGS_MODULE``
    value with the path to the project's settings file, starting from the
    project root.

    Ex: If your settings file is defined at
    ``<project_root>/configuration/settings.py``, then the value for this
    setting should be ``configuration.settings``.

From this point, UnitTests can be invoked through Pytest, at project root with
the following commands:

.. code:: python

    pytest                  # Run pytest on all files that match ini definition.
    pytest path/to/check    # Run PyTest on a specific folder.
    pytest -n auto          # Run PyTest parallel, if pytest-xdist is installed.

For additional details about configuration and setup, see the
:doc:`configuration` page.

For information on how to use this package, see the :doc:`general_usage` page.


Manage.py Test QuickStart
-------------------------

.. warning::

    While this project can function with ``manage.py test``, the debug output
    functionality will send content to the console on every test regardless of
    pass or fail leading to an overwhelming amount of output. Instead, we
    **strongly** recommend that you consider using PyTest to run tests as
    PyTest will only output debug info on test failure.

Nothing extra needs to be done in order for the provided TestCase classes to
work with Django's default ``manage.py test`` command.

However, since you will get debug output on every test that uses the additional
asserts provided by the TestCases, it is recommended that you disable the debug
output so that console output is manageable.

To do so, add the following line to your ``settings.py`` file:

.. code:: python

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = False

For more details about available settings, see the :doc:`configuration` page.

For information on how to use this package, see the :doc:`general_usage` page.
