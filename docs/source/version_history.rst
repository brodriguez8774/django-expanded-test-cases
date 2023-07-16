Version History
***************


0.5.0 - Improved Integration TestCase & Initial LiveServer TestCases
====================================================================
* Generally reworked/improved how URLs are handled in response assertions.

  * All **assertResponse** type calls take args for additional parameters for
    url parsing, provided as args or kwargs (for Django
    `reverse <https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse>`_
    calls), or query_parameters (for GET style url calls).
  * These parameters can be sent for both standard url resolving, and redirect
    url resolving.

* Changed ``response.url`` to ``response.full_url``.

  * ``response.url`` now contains the response url minus site root, while
    ``response.full_url`` contains response url with site root.

* Added `assertTextStartsWith()` and `assertTextEndsWith()` functions.

  * These are more forgiving versions of `assertText()`, with similar output on
    failure.

* Added setting for behavior of `assertTitle()` function in page response tests.

  * To make behavior consistent across functions, the `assertTitle()`'s
    `exact_match` arg (default of `True`) has been renamed to `allow_partials`
    (default of `False`).

* Updated default value of `DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS`
  to be False, to better match what is likely the default expected logic for
  most users.

* `LiveServerTestCase` has been split into `LiveServerTestCase` and
  `ChannelsLiveServerTestCase` and is now tentatively usable.

  * `LiveServerTestCase` uses basic selenium testing, while
    `ChannelsLiveServerTestCase` uses selinium via DjangoChannels.

* General small bugfixes.


0.4.0 - Debug Output Customization
==================================

* Updates project settings to allow better customization of debug output upon
  UnitTest failure.
* Also refactors existing settings to be more consistent and uniform.

  * Some existing settings names have changed.

* Docs now reflect setting options for debug customization.


0.3.0 - Default Test User Customization
=======================================

* Includes customization of how test-users are handled, when running any given
  Integration/Response test.

  * For more details, see :ref:`configuration/users:Configuring Test Users`.
  * As part of this change, the default way of handling users has changed.
    Original default handling was equivalent to ``relaxed``, but now is
    equivalent to ``anonymous`` to better match with Django's default behavior.


0.2.4 - Minor Updates
=====================

* Minor updates for docs and Python3.11.


0.2.3 - Various Bugfixes and Improvements to Testing Reliability
================================================================

* Fixed multiple various bugs and potential inconsistencies with test handling.
* Updated Integration content check to indicate when a value matches all except
  for text capitalization.


0.2.2 - Preliminary Setup/Upgrades for Improved Test Output + LiveServer Testing
================================================================================

* Initial implementation of improved test output text coloring.

  * Slightly buggy, and definitely needs work. But its still more helpful than
    nothing.

* Start of LiveServer/Selenium testing classes.

  * Definitely in a "pre-release" state and not yet viable for use.
  * For now, continue to use the default Django/Selenium LiveServer testing
    classes.


0.2.1 - Bugfixes and Improved Output Display
============================================

* Generally improve project debug print output, including basic coloring.
* Bug corrections.


0.2.0 - Stable Core Logic
=========================

* Core TestCase classes seem stable and tested in a real project environment.
* Improved/cleaned general assertion error messages.
* Improved functionality of AssertContent function.


0.1.1 - Pre-release for Core Logic
==================================

* Most "core" functionality implemented.
* **BaseTestCase** and **IntegrationTestCase** classes created.
* Initial docs created.
* Generally ready for version 0.2. Will update after live testing in actual
  projects, as a proper dependency.


0.1.0 - Initial release
=======================

* First release.
* Very much WIP and subject to change.
* Minimal functionality.
* Not recommended for import/use in a live production project.
