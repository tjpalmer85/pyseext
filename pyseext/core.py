"""
Module that contains our Core class.
"""
import logging
import time
from typing import Union, Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from pyseext.has_referenced_javascript import HasReferencedJavaScript

class Core(HasReferencedJavaScript):
    """A class to help with core testing functionality.
    """

    # Class variables
    _IS_DOM_READY: str = "return !!(globalThis.Ext && globalThis.Ext.isDomReady)"
    _IS_AJAX_REQUEST_IN_PROGRESS: str = "return globalThis.PySeExt.Core.isAjaxRequestInProgress()"

    # FIXME: Could use a means of injecting event sniffing perhaps?
    # .....: Using Ext.mixin.Observable.capture

    # FIXME: Another thought is to inject a means to show field names on forms, xtype on components, etc?

    def __init__(self, driver: WebDriver):
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

    def try_get_object_member(self, obj: Union[dict, Any], member: str, default: Any = None) -> Any:
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
        if isinstance(obj, dict):
            return obj.get(member, default)

        return default

    def is_ajax_request_in_progress(self) -> bool:
        """Indicates whether there is currently an Ajax request in progress.

        Returns:
            bool: True if there is a request in progress, False otherwise.
        """
        script = self._IS_AJAX_REQUEST_IN_PROGRESS
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def wait_for_no_ajax_requests_in_progress(self,
                                              timeout: float = 30,
                                              poll_frequecy: float = 0.2,
                                              recheck_time_if_false: float = 0.2):
        """Method that waits until there are no Ajax requests in progress.

        Will throw a TimeOutException if the value is not true within the specified timeout period.

        Args:
            timeout (float, optional): Number of seconds before timing out. Defaults to 30.
            poll_frequency (float, optional): Number of seconds to poll. Defaults to 0.2.
            recheck_time_if_false (float, optional): If we get a result such that no Ajax calls are in progress, this is the amount of time to wait to check again. Defaults to 0.2.
        """
        WebDriverWait(self._driver, timeout, poll_frequency = poll_frequecy).until(Core.IsNoAjaxCallInProgressExpectation(recheck_time_if_false))

    class IsDomReadyExpectation():
        """ An expectation for checking Ext.isDomReady
        """

        def __init__(self):
            """Initialises an instance of this class.
            """

        def __call__(self, driver):
            """Method that determines whether Ext.isDomReady
            """
            return driver.execute_script(Core._IS_DOM_READY)

    class IsNoAjaxCallInProgressExpectation():
        """ An expectation for checking whether there is an Ajax call in progress.
        """

        def __init__(self, recheck_time_if_false: Union[float, None] = None):
            """Initialises an instance of this class.

            Args:
                recheck_time_if_false (float, optional): If we get a value of false (so there is not a call in progress),
                                                         this is the amount of time to wait to check again. Defaults to None.
            """
            self._recheck_time_if_false = recheck_time_if_false

        def __call__(self, driver):
            """Method that determines whether Ext.isDomReady
            """
            is_call_in_progress = Core(driver).is_ajax_request_in_progress()

            if not is_call_in_progress and self._recheck_time_if_false:
                time.sleep(self._recheck_time_if_false)
                is_call_in_progress = Core(driver).is_ajax_request_in_progress()

            return not is_call_in_progress

    class ArgumentException(Exception):
        """Exception class thrown when we have an argument exception.
        """

        def __init__(self, name: str, message: str = "The argument with name '{name}' is invalid."):
            """Initialises an instance of this exception

            Args:
                name (str): The name of the argument
                message (str, optional): The exception message. Defaults to "The argument with name '{name}' is invalid.".
            """
            self.message = message
            self._name = name

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(name=self._name)
