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

The functionality provided by **Django-Expanded-Test-Cases** has been tested
with both
`Django Manage.py testing framework <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
and `PyTest <docs.pytest.org>`_.

Please see `PyTest Configuration QuickStart`_ or
`Manage.py Test QuickStart`_.


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

Nothing extra needs to be done in order for the provided TestCase classes to
work with Django's default ``manage.py test`` command.

For more details about available settings, see the :doc:`configuration` page.

For information on how to use this package, see the :doc:`general_usage` page.
