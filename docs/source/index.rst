.. Django Expanded Test Cases documentation master file, created by
   sphinx-quickstart on Fri Jun  3 11:23:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Django-Expanded-Test-Cases
==========================

The **Django-Expanded-Test-Cases** package is a set of TestCase
classes that expand upon Django's default
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
class and
`UnitTesting <https://docs.python.org/3/library/unittest.html>`_ logic.

A majority of additional features provided in this package amounts to helper
wrappers around sets of commonly used testing statements.
So what might normally take 5 or 10 lines of testing logic is condensed down
to a single assertion.

For a large project with many thousands of tests, this can add up fast.

Within this package, are three different TestCase classes that can be used as
a drop-in replacement for
`Django's included TestCases <https://docs.djangoproject.com/en/4.0/topics/testing/tools/#provided-test-case-classes>`_
They are :doc:`test_cases/base_test_case`,
:doc:`test_cases/integration_test_case`, and
:doc:`test_cases/live_server_test_case`.
Each one provides separate sets of additional functionality.


Below is an example of **ETC**'s debug output when a UnitTest fails for a basic view, while checking the ``<h1>`` tag.

.. image:: https://user-images.githubusercontent.com/14208531/231304818-fb0dbe31-ead9-4de8-8efe-a3fc858cbddd.png


.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

   quickstart
   package_overview
   general_usage
   managing_test_users


.. toctree::
   :maxdepth: 2
   :caption: Provided Test Case Classes:

   test_cases/overview
   test_cases/base_test_case
   test_cases/integration_test_case
   test_cases/live_server_test_case


.. toctree::
   :maxdepth: 2
   :caption: Package Setting Configuration:

   configuration/general
   configuration/users
   configuration/debug_output


.. toctree::
   :maxdepth: 1
   :caption: Versions:

   roadmap
   version_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
