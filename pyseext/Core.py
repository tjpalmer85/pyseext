import logging
from typing import Union, Any

from selenium.webdriver.support.ui import WebDriverWait

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class Core(HasReferencedJavaScript):
    """A class to help with core testing functionality.
    """

    def __init__(self, driver):
        """Initialises an instance of this class.

        Args:
            driver (selenium.webdriver): The webdriver to use.
        """

        # Instance variables
        self._logger = logging.getLogger(__name__)
        self._driver = driver

        # Initialise our base class
        super().__init__(driver, self._logger)

    def wait_for_dom_ready(self, timeout: float = 30):
        """Method that waits until Ext indicates that the DOM is ready.
        Calls Ext.isDomReady.
        Will throw a TimeOutException if the value is not true within the specified timeout period.

        Args:
            timeout (float): Number of seconds before timing out (default 30)
        """
        WebDriverWait(self._driver, timeout).until(Core.IsDomReadyExpectation())

    def try_get_object_member(self, object: Union[dict, Any], member: str, default = None):
        """Attempts to get the member from an object, but if object itself is not a dictionary
        then it is returned.

        Useful when a value in a dictionary we're processing might be an object or not, and we
        want to process them in the same way.

        Args:
            object (Union[dict, Any]): The object from which to get the member's value.
            member (str): The key for the member we're after.
            default (Any, optional): The default to return if not found. Defaults to None.

        Returns:
            Any: The value of the member, or the default if not found.
        """
        if isinstance(object, dict):
            return object.get(member, default)
        else:
            return default

    class IsDomReadyExpectation():
        """ An expectation for checking Ext.isDomReady
        """

        def __init__(self):
            """Initialises an instance of this class.
            """

        def __call__(self, driver):
            """Method that determines whether Ext.isDomReady
            """
            return driver.execute_script('return !!(globalThis.Ext && globalThis.Ext.isDomReady)')
