.. Django Expanded Test Cases documentation master file, created by
   sphinx-quickstart on Fri Jun  3 11:23:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django "Expanded Test Cases" Package
====================================

Expands the existing Django TestCase class with extra functionality.

Different TestCase classes are provided, each providing separate sets of
functionality.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   general_usage
   test_cases
   configuration


Expected Roadmap
================

* v 0.1.x

    * Initial release.
    * Minimal functionality. Minimal documentation. Likely to change
      significantly.
    * Not recommended for import/use in a live production project.

* v 0.2.x

    * Project is in a viable state to import and use in other projects, even if
      only for only basic response testing.
    * **BaseTestCase** and **IntegrationTestCase** are roughly stable.

        * Further functionality may still be added at a later date. But core
          logic is present.

    * At least some documentation exists for BaseTestCase and IntegrationTestCase.

* v 0.3.x

    * Project is in a viable state to test both basic responses and selenium
      browser responses.
    * **LiveServerTestCase** is roughly stable.

        * Further functionality may still be added at a later date. But core
          logic is present.

    * Documentation for BaseTestCase and IntegrationTestCase is fairly thorough,
      if not complete.
    * At least some documentation exists for LiveServerTestCase.


* v 0.4.x

    * Project is in a viable state to test basic responses, selenium browser
      responses, and CSV file downloads.
    * **Csv/ReportTestCase** is roughly stable.

        * Further functionality may still be added at a later date. But core
          logic is present.

    * Documentation for LiveServerTestCase is fairly thorough, if not complete.
    * At least some documentation exists for Csv/ReportTestCase.

* Unsure of roadmap past this point. To be decided at a later date.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
