Version History
***************


0.2.4 - Minor Updates
================================================================

* Minor updates for docs and Python3.11.


0.2.3 - Various Bugfixes and Improvements to Testing Reliability
================================================================

* Fixed multiple various bugs and potential inconsistencies with test handling.
* Updated Integration content check to indicate when a value matches all except for text capitalization.


0.2.2 - Preliminary Setup/Upgrades for Improved Test Output + LiveServer Testing
===============================================================================

* Initial implementation of improved test output text coloring.

  * Slightly buggy, and definitely needs work. But its still more helpful than nothing.

* Start of LiveServer/Selenium testing classes.

  * Definitely in a "pre-release" state and not yet viable for use.
  * For now, continue to use the default Django/Selenium LiveServer testing classes.


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
