LiveServerTestCase
******************


The **LiveServerTestCase** class provides additional wrapper functionality for
writing UnitTests which directly check a browser window instance, such as
`Selenium <https://www.selenium.dev/documentation/>`_.


This class can be very helpful in testing logic that requires live browser
manipulation, such as any logic that uses JavaScript to function.


.. note::

   While testing with live browser instances can definitely be useful, it also
   tends to provide more overhead.

   When possible, consider testing via :ref:`IntegrationTestCase` class
   instead, as it is designed to test most request/response logic in a more
   lightweight, performance-friendly manner.


.. attention::

    This TestCase is not yet implemented.

    See :doc:`index` for roadmap.