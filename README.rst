PySeExt Module Repository
========================

This project contains a package to aid the testing of ExtJS applications from Python using Selenium.

---------------
Naming Standards:

This is the first time I have written any Python, so I have looked around for standards that seem to be common.
I have settled on those listed `here<https://namingconvention.org/python/>`.

.. list-table:: TL;DR
   :widths: 33 33 34
   :header-rows: 1

   * - Type
     - Public
     - Internal
   * - Packages
     - lower_with_under
   * - Modules
     - lower_with_under
     - _lower_with_under
   * - Classes
     - CapWords
     - _CapWords
   * Exceptions
     - CapWords
   * Functions
     - lower_with_under()
     - _lower_with_under()
   * Global/Class Constants
     - CAPS_WITH_UNDER
     - _CAPS_WITH_UNDER
   * Global/Class Variables
     - lower_with_under
     - _lower_with_under
   * Instance Variables
     - lower_with_under
     - _lower_with_under
   * Method Names
     - lower_with_under()
     - _lower_with_under()
   * Function/Method Parameters
     - lower_with_under
   * Local Variables
     - lower_with_under

---------------

If you want to learn more about ``setup.py`` files, check out `this repository <https://github.com/kennethreitz/setup.py>`_.
