"""
Module that contains our ComponentQuery class.
"""
import logging
from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException

from pyseext.has_referenced_javascript import HasReferencedJavaScript


class ComponentQuery(HasReferencedJavaScript):
    """A class to help with using Ext.ComponentQuery"""

    # Class variables
    _QUERY_TEMPLATE: str = "return globalThis.PySeExt.ComponentQuery.query('{cq}')"
    """The script template to use to execute a component query.
    Requires the inserts: {cq}"""

    _QUERY_TEMPLATE_WITH_ROOT: str = "return globalThis.PySeExt.ComponentQuery.query('{cq}', '{root_id}')"
    """The script template to use to execute a component query under a specified root.
    Requires the inserts: {cq}, {root_id}"""

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (WebDriver): The webdriver to use
        """
        # Instance variables
        self._logger = logging.getLogger(__name__)
        """The logger instance for this class instance"""

        self._driver = driver
        """The WebDriver instance for this class instance"""

        # Initialise our base class
        super().__init__(driver, self._logger)

    def query(self, cq: str, root_id: Union[str, None] = None) -> list[WebElement]:
        """Executes a ComponentQuery and returns the result

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.

        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if not found
        """
        if root_id is None:
            self._logger.debug("Executing CQ '%s'", cq)
            script = self._QUERY_TEMPLATE.format(cq=cq)
        else:
            self._logger.debug("Executing CQ '%s' under root '%s'", cq, root_id)
            script = self._QUERY_TEMPLATE_WITH_ROOT.format(cq=cq, root_id=root_id)

        self.ensure_javascript_loaded()
        query_result = self._driver.execute_script(script)

        self._logger.debug("CQ '%s' gave results: %s", cq, query_result)

        return query_result

    def wait_for_query(self, cq: str, root_id: Union[str, None] = None, timeout: float = 10) -> list[WebElement]:
        """Method that waits for the specified CQ to match something

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)

        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if not found
        """
        try:
            WebDriverWait(self._driver, timeout).until(ComponentQuery.ComponentQueryFoundExpectation(cq))
            return self.query(cq, root_id)
        except TimeoutException as exc:
            raise ComponentQuery.QueryNotFoundException(cq, timeout, root_id) from exc

    def wait_for_single_query(self, cq: str, root_id: Union[str, None] = None, timeout: float = 10) -> WebElement:
        """Method that waits for the specified CQ to match a single result.
        If there are multiple matches then an error is thrown.

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)

        Returns:
            WebElement: The DOM element that matches the query
        """
        results = self.wait_for_query(cq, root_id, timeout)
        if len(results) > 1:
            raise ComponentQuery.QueryMatchedMultipleElementsException(cq, len(results))

        return results[0]

    def wait_for_single_query_visible(self, cq: str, root_id: Union[str, None] = None, timeout: float = 10) -> WebElement:
        """Method that waits for the specified CQ to match a single visible result.
        If there are multiple matches then an error is thrown.

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)

        Returns:
            WebElement: The DOM element that matches the query
        """
        if not cq.endswith('{isVisible(true)}'):
            cq = cq + '{isVisible(true)}'

        return self.wait_for_single_query(cq, root_id, timeout)

    class ComponentQueryFoundExpectation:
        """ An expectation for checking that an Ext.ComponentQuery is found"""

        def __init__(self, cq: str):
            """Initialises an instance of this class.
            """
            self._cq = cq

        def __call__(self, driver):
            """Method that determines whether a CQ is found
            """
            results = ComponentQuery(driver).query(self._cq)
            return results is not None and len(results) > 0

    class QueryMatchedMultipleElementsException(Exception):
        """Exception class thrown when expecting a single component query match and get multiple"""

        def __init__(self, cq: str, count: int, message: str = "Expected a single match from ComponentQuery '{cq}' but got {count}."):
            """Initialises an instance of this exception

            Args:
                cq (str): The component query that has been executed
                timeout (float): Number of seconds before timing out
                count (int): The number of results that we got
                message (str, optional): The message for the exception. Must contain a 'cq' and 'count' format inserts.
                                         Defaults to "Expected a single match from ComponentQuery '{cq}' but got '{count}'".
            """
            self.message = message
            self._cq = cq
            self._count = count

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception"""
            return self.message.format(cq=self._cq, count=self._count)

    class QueryNotFoundException(Exception):
        """Exception class thrown when a component query could not be found"""

        def __init__(self,
                     cq: str,
                     timeout: float,
                     root_id: Union[str, None] = None,
                     message_without_root: str = "Waiting for component query '{cq}' timed out after {timeout} seconds",
                     message_with_root: str = "Waiting for component query '{cq}' under root '{root_id}' timed out after {timeout} seconds"):
            """Initialises an instance of this exception

            Args:
                cq (str): The component query that has been executed
                timeout (float): Number of seconds waited
                root_id (str, optional): The id of the container within which the query was performed.
                message_without_root (str, optional): The message for the exception when there is no root. Must contain a 'cq' and 'timeout' format inserts.
                                                      Defaults to "Waiting for component query '{cq}' timed out after {timeout} seconds".
                message_with_root (str, optional): The message for the exception when there is a root. Must contain a 'cq', 'root_id' and 'timeout' format inserts.
                                                   Defaults to "Waiting for component query '{cq}' under root '{root_id}' timed out after {timeout} seconds".
            """
            self._cq = cq
            self._timeout = timeout
            self._root_id = root_id

            if root_id is None:
                self.message = message_without_root
            else:
                self.message = message_with_root

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception"""
            if self._root_id is None:
                return self.message.format(cq=self._cq, timeout=self._timeout)
            else:
                return self.message.format(cq=self._cq, timeout=self._timeout, root_id=self._root_id)
