.. Django Expanded Test Cases documentation master file, created by
   sphinx-quickstart on Fri Jun  3 11:23:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Django-Expanded-Test-Cases Package
==================================

The **Django-Expanded-TestCases** package is meant to be a set of utility
classes and functions, which expands upon those defined in Django's default
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
class and
`UnitTesting <https://docs.python.org/3/library/unittest.html>`_ logic.

A majority of logic provided in this package amounts to helper wrappers around
sets of commonly used testing statements. So what might normally take 5 or 10
lines of testing logic is condensed down to a single assertion.

For a large project with many thousands of tests, this can add up fast.

Within this package, different TestCase classes are provided, each providing
separate sets of functionality.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   general_usage
   configuration


.. toctree::
   :maxdepth: 2
   :caption: Provided Test Cases:

   test_cases/overview
   test_cases/base_test_case
   test_cases/integration_test_case
   test_cases/live_server_test_case


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
