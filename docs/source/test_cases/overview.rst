Overview
********

All TestCases in **Django-Expanded-Test-Cases** use Django's original
`TestCase <https://docs.djangoproject.com/en/dev/topics/testing/overview/>`_
as a base class.

From there, the following TestCase classes provide additional functionality:

* :ref:`BaseTestCase` - Minimalistic TestCase class. All other TestCases inherit
  from this.
* :ref:`IntegrationTestCase` - Class for testing direct
  `Django response objects <https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_.
  Aka, testing view responses outside of a live browser window instance.
* :ref:`LiveServerTestCase` - Class for testing view responses inside a live
  browser window instance. Such as via
  `Selenium <https://www.selenium.dev/documentation/>`_.
