Overview
********

All TestCases in **Django-Expanded-Test-Cases** use Django's original
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
as a base class.

From there, the following TestCase classes provide additional functionality:

* :doc:`base_test_case` - Minimalistic TestCase class. All other TestCases
  inherit from this.
* :doc:`IntegrationTestCase<./integration_test_case/overview>`
  - Class for testing direct
  `Django response objects <https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_.
  Aka, testing view responses outside of a live browser window instance.
* :doc:`live_server_test_case` - Class for testing view responses inside a live
  browser window instance. Such as via
  `Selenium <https://www.selenium.dev/documentation/>`_.
