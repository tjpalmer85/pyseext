"""
Module that contains our ComponentQuery class.
"""
import logging
from typing import Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

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

    _QUERY_TEMPLATE_WITH_CSS_SELECTOR: str = "return globalThis.PySeExt.ComponentQuery.query('{cq}', undefined, '{css_selector}')"
    """The script template to use to execute a component query, and then execute a CSS selector query against each matched element.
    Requires the inserts: {cq}, {css_selector}"""

    _QUERY_TEMPLATE_WITH_ROOT_AND_CSS_SELECTOR: str = "return globalThis.PySeExt.ComponentQuery.query('{cq}', '{root_id}', '{css_selector}')"
    """The script template to use to execute a component query under a specified root, and then execute a CSS selector query against each matched element.
    Requires the inserts: {cq}, {root_id}, {css_selector}"""

    _IS_COMPONENT_INSTANCE_OF_CLASS_TEMPLATE: str = "return globalThis.PySeExt.ComponentQuery.isComponentInstanceOf('{class_name}', '{cq}')"
    """The script template to use to determine whether a component query matches a component of the specified class.
    Requires the inserts: {class_name}, {cq}"""

    _IS_COMPONENT_INSTANCE_OF_CLASS_TEMPLATE_WITH_ROOT: str = "return globalThis.PySeExt.ComponentQuery.isComponentInstanceOf('{class_name}', '{cq}', '{root_id}')"
    """The script template to use to determine whether a component query matches a component of the specified class.
    Requires the inserts: {class_name}, {cq}, {root_id}"""

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

    def query(self, cq: str, root_id: Union[str, None] = None, css_selector: Union[str, None] = None) -> list[WebElement]:
        """Executes a ComponentQuery and returns the result

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            css_selector (str, optional): An optional CSS selector that can be used to get child elements of a found component,
                                          e.g. a clear trigger on a field would be '.x-form-clear-trigger'.
        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if not found
        """
        if root_id is None and css_selector is None:
            self._logger.debug("Executing CQ '%s'", cq)
            script = self._QUERY_TEMPLATE.format(cq=cq)
        elif css_selector is None:
            self._logger.debug("Executing CQ '%s' under root '%s'", cq, root_id)
            script = self._QUERY_TEMPLATE_WITH_ROOT.format(cq=cq, root_id=root_id)
        elif root_id is None:
            self._logger.debug("Executing CQ '%s' with CSS selector '%s'", cq, css_selector)
            script = self._QUERY_TEMPLATE_WITH_CSS_SELECTOR.format(cq=cq, css_selector=css_selector)
        else:
            self._logger.debug("Executing CQ '%s' under root '%s' with CSS selector '%s'", cq, root_id, css_selector)
            script = self._QUERY_TEMPLATE_WITH_ROOT_AND_CSS_SELECTOR.format(cq=cq, root_id=root_id, css_selector=css_selector)

        self.ensure_javascript_loaded()
        query_result = self._driver.execute_script(script)

        self._logger.debug("CQ '%s' gave results: %s", cq, query_result)

        return query_result

    def wait_for_query(self, cq: str, root_id: Union[str, None] = None, timeout: float = 10, throw_if_not_found: bool = True, css_selector: Union[str, None] = None) -> list[WebElement]:
        """Method that waits for the specified CQ to match something

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)
            throw_if_not_found (bool): Indicates whether to throw an exception if not found (default True).
            css_selector (str, optional): An optional CSS selector that can be used to get child elements of a found component,
                                          e.g. a clear trigger on a field would be '.x-form-clear-trigger'.

        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if not found (and not configured to throw)
        """
        try:
            WebDriverWait(self._driver, timeout).until(ComponentQuery.ComponentQueryFoundExpectation(cq))
            return self.query(cq, root_id, css_selector)
        except TimeoutException as exc:
            if throw_if_not_found:
                raise ComponentQuery.QueryNotFoundException(cq, timeout, root_id) from exc

            return []

    def wait_for_single_query(self, cq: str, root_id: Union[str, None] = None, timeout: float = 10, css_selector: Union[str, None] = None) -> WebElement:
        """Method that waits for the specified CQ to match a single result.
        If there are multiple matches then an error is thrown.

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)
            css_selector (str, optional): An optional CSS selector that can be used to get child elements of a found component,
                                          e.g. a clear trigger on a field would be '.x-form-clear-trigger'.

        Returns:
            WebElement: The DOM element that matches the query
        """
        results = self.wait_for_query(cq, root_id, timeout, True, css_selector)
        if len(results) > 1:
            raise ComponentQuery.QueryMatchedMultipleElementsException(cq, len(results))

        return results[0]

    def wait_for_single_query_visible(self, cq: str, root_id: Union[str, None] = None, timeout: float = 10, css_selector: Union[str, None] = None) -> WebElement:
        """Method that waits for the specified CQ to match a single visible result.
        If there are multiple matches then an error is thrown.

        Args:
            cq (str): The query to execute
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)
            css_selector (str, optional): An optional CSS selector that can be used to get child elements of a found component,
                                          e.g. a clear trigger on a field would be '.x-form-clear-trigger'.

        Returns:
            WebElement: The DOM element that matches the query
        """
        if not cq.endswith('{isVisible(true)}'):
            cq = cq + '{isVisible(true)}'

        return self.wait_for_single_query(cq, root_id, timeout, css_selector)

    def is_component_instance_of_class(self, class_name: str, cq: str, root_id: Union[str, None] = None, timeout: float = 1) -> bool:
        """Determines whether the component for the specified CQ is an instance of the specified class name.

        Note, will return True if the component is a subclass of the type too.

        If the component is not found then an error is thrown.

        Args:
            class_name (str): The class name to test for, e.g. 'Ext.container.Container'.
            cq (str): The query to find the component.
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 1)

        Returns:
            bool: True if the component is an instance of the specified class (including a subclass). False otherwise.
        """
        if root_id is None:
            script = self._IS_COMPONENT_INSTANCE_OF_CLASS_TEMPLATE.format(class_name=class_name, cq=cq)
        else:
            script = self._IS_COMPONENT_INSTANCE_OF_CLASS_TEMPLATE_WITH_ROOT.format(class_name=class_name, cq=cq, root_id=root_id)

        self.ensure_javascript_loaded()
        result = self._driver.execute_script(script)

        if result is None:
            raise ComponentQuery.QueryNotFoundException(cq, timeout, root_id)

        return result

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
