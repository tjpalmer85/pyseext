from selenium.webdriver.support.ui import WebDriverWait

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class ComponentQuery(HasReferencedJavaScript):
    """A class to help with using Ext.ComponentQuery
    """

    # Class variables
    _QUERY_TEMPLATE = "return globalThis.PySeExt.ComponentQuery.query('{cq}')"
    _QUERY_TEMPLATE_WITH_ROOT = "return globalThis.PySeExt.ComponentQuery.query('{cq}', '{root_id}')"

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """

        # Instance variables
        self._driver = driver

        # Initialise our base class
        super().__init__(driver)

    def query(self, cq, root_id=None):
        """Executes a ComponentQuery and returns the result

        Args:
            cq (str): The query to execute
            root_id (str):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

        Returns:
            selenium.webdriver.remote.webelement[]: An array of DOM elements that match the query or an empty array if not found
        """
        if root_id == None:
            script = self._QUERY_TEMPLATE.format(cq=cq)
        else:
            script = self._QUERY_TEMPLATE_WITH_ROOT.format(cq=cq, root_id=root_id)

        return self._driver.execute_script(script)

    def wait_for_query(self, cq, root_id=None, timeout=3):
        """Method that waits for the specified CQ to match something

        Args:
            cq (str): The query to execute
            root (str):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 3)
        """
        WebDriverWait(self._driver, timeout).until(ComponentQuery.ComponentQueryFoundExpectation(cq))
        return self.query(cq, root_id)

    def wait_for_single_query(self, cq, root_id=None, timeout=3):
        """Method that waits for the specified CQ to match a single result.
        If there are multiple matches then an error is thrown.

        Args:
            cq (str): The query to execute
            root (str):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 3)
        """
        WebDriverWait(self._driver, timeout).until(ComponentQuery.ComponentQueryFoundExpectation(cq))
        results = self.query(cq, root_id)
        if len(results) > 1:
            raise ComponentQuery.QueryMatchedMultipleElementsException(cq, len(results))

        return results[0]

    def wait_for_single_query_visible(self, cq, root_id=None, timeout=3):
        """Method that waits for the specified CQ to match a single visible result.
        If there are multiple matches then an error is thrown.

        Args:
            cq (str): The query to execute
            root (str):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 3)
        """
        if not cq.endswith('{isVisible(true)}'):
            cq = cq + '{isVisible(true)}'

        return self.wait_for_single_query(cq, root_id, timeout)

    class ComponentQueryFoundExpectation():
        """ An expectation for checking that an Ext.ComponentQuery is found
        """

        def __init__(self, cq):
            """Initialises an instance of this class.
            """
            self._cq = cq

        def __call__(self, driver):
            """Method that determines whether a CQ is found
            """
            results = ComponentQuery(driver).query(self._cq)
            return results != None and len(results) > 0

    class QueryMatchedMultipleElementsException(Exception):
        """Exception class thrown when expecting a single component query match and get multiple
        """

        def __init__(self, cq, count, message="Expected a single match from ComponentQuery '{cq}' but got {count}."):
            """Initialises an instance of this exception

            Args:
                cq (str): The component query that has been executed
                count (int): The number of results that we got
                message (str, optional): The message for the exception. Must contain a 'cq' and 'count' format inserts. Defaults to "Expected a single match from ComponentQuery '{cq}' but got '{count}'".
            """
            self.message = message
            self._cq = cq
            self._count = count

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(cq=self._cq, count=self._count)