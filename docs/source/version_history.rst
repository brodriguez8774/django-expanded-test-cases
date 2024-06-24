Version History
***************



0.7.2 - Further Debug Quality of Life
=====================================

* Added additional settings to automatically hide sections of html for
  IntegrationTestCase debug output on test failure.

  * Very useful for sites with large amounts of consistent header/footer
    templating. If a majority of your tests don't need this templating, these
    new values allow hiding said content on debug output, so it only displays
    more relevant content.

  * Particularly useful if the site uses a third-party package to handle most
    header, footer, and page-navigation elements.

  * Settings are:

    * `DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_BEFORE` - String of content
      at start of html to hide. Can include head, header, and common-navigation
      elements.

    * `DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_AFTER` - String of content at
      end of html to hide. Can include footer, copyright, and end-of-page
      elements.

    * `DJANGO_EXPANDED_TESTCASES_SKIP_CONTENT_HEAD` - Boolean indicating if page
      head html should be hidden. If true, skips showing <head> element. This
      head element tends to include html metadata. Not to be confused with the
      <header> element, which often includes logo and main navigation.

* Correction to how project file structure was changed in 0.7.0. Probably won't
  affect most, but now is organized more consistently with other packages,
  while still addressing the original issue that 0.7.0 attempted to fix.


0.7.1 - "Debug Output" Quality of Life
======================================

* Added debug customization features that have been requested.

  * Can now use a setting to disable logging output during tests. Either
    limiting lower logging levels or disabling entirely.

  * Added visual separator options for test debug output.

  * Updated assertContent statement to be more informative with contextual
    output, when providing a single statement with multiple checks.

* Fixed a few rare bugs and Django depreciation warnings.


0.7.0 - Minor Project File Restructuring
========================================

* Slight change in project file naming, to try to fix an inconsistent issue when
  trying to access package debugging views.

  * Shouldn't have any affect on package usage unless a project was directly
    accessing these debug views.


0.6.5 - Bugfix Update
=====================

* Correction for bug in standardization of assertTitle function logic.


0.6.4 - Bugfix Update
=====================

* Correction for bug in regards to ContextDict/ContextList objects and
  displaying debug output.


0.6.3 - Minor Test-Failure Debug Output Customization
=====================================================

* Now supports using regex to hide sections of debug output on test failure.

  * Useful for debugging template output with large amounts of content.

  * Particularly useful for templates that include third-party content (which
    you're unlikely to test for, that should be done in the third-party app
    itself), or projects with large amounts of header/footer/javascript html
    content.


0.6.2 - Further Minor Updates
=============================

* Correct more debug output from last version.

* Add assertContent functionality to optionally include custom error messages on failure.


0.6.1 - Minor Updates
=====================

* Correct some leftover debug output from last version.

* Add a missing assertion type to IntegrationTestcase.


0.6.0 - LiveServer Test Case Initial Release
============================================

* ``LiveServerTestCase`` and ``ChannelsLiveServerTestCase`` both exists, and at
  least function in a non-multi-threaded environment.

    * Seems to have some issues in multi-threaded testing environments. Needs
      further examination.

    * New documentation for this is fairly non-existent at the moment. All
      test case options are available to view at
      ``<project_root>/django_expanded_text_cases/`text_cases/constants.py``.


0.5.1 - Update Docs and Preparation for 0.6 LiveServer Release
==============================================================

* Updated/corrected docs.

* Updated beta LiveServer classes to function with Chromedriver version 115 and
  higher.


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
