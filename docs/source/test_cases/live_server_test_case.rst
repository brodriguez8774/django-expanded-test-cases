LiveServerTestCase
******************


The **LiveServerTestCase** and **ChannelsLiveServerTestCase** classes provide
additional wrapper functionality for writing tests that directly check a
browser window instance, such as when using
`Selenium <https://www.selenium.dev/documentation/>`_.


These classes can be very helpful in testing logic that requires live browser
manipulation, such as any logic that uses JavaScript to function.


.. note::

   While testing with live browser instances can definitely be useful, it also
   tends to provide more overhead.

   When possible, consider testing via the
   :doc:`IntegrationTestCase<./integration_test_case/overview>`
   class instead, as it is designed to test most request/response logic in
   a more lightweight, performance-friendly manner.
