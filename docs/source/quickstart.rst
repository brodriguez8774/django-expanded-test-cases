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

One of the most useful features the `Django Expanded TestCases` library provides
is automatically displaying debug page response output to console, on test
failure.

This technically works with Django's default
`manage.py test <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
command. But ``manage.py``'s base functionality is to assume all testing console
output is meaningful, and display it to console unconditionally. As far as we
can tell, there does not seem to be a way to change this behavior.

With large projects (or even small and medium projects with decent amounts of
tests), this ends with unwieldy amounts of unhelpful text outputting to
console, even when all tests pass. And when tests fail, this drowns out any
useful debug output that might have occurred.

Thus, when using this package, we **strongly** recommend switching to running
tests via PyTest.


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
    value with the path to the settings file, starting from project root.

    Ex: If your settings file is defined at
    ``<project_root>/configuration/settings.py``, then the value for this
    setting should be ``configuration.settings``.

From this point, UnitTests can be invoked through Pytest, at project root with
the following commands:

.. code:: python

    pytest                  # Run pytest on all files that match ini definition.
    pytest path/to/check    # Run PyTest on a specific folder.
    pytest -n auto          # Run PyTest parallel, if pytest-xdist is installed.

See :doc:`general_usage` for next steps.


Manage.py Test QuickStart
-------------------------

.. warning::

    While this project can function with ``manage.py test``, the debug output
    functionality will be effectively unavailable. Instead, we strongly
    recommend considering using PyTest to run project UnitTests.

For a basic setup, there should be minimal configuration to use this project
with Django's default ``manage.py test`` command.

In your settings file, add the following line to disable spam from debug output:

.. code:: python

    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = False

For more details about project settings, see :doc:`configuration`. Otherwise,
see :doc:`general_usage` for next steps.
