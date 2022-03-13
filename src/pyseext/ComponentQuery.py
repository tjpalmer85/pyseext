from selenium.webdriver.support.ui import WebDriverWait

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class ComponentQuery(HasReferencedJavaScript):
    """A class to help with using Ext.ComponentQuery
    """

    _QUERY_TEMPLATE = "return globalThis.PySeExt.ComponentQuery.query('{cq}')"
    _QUERY_TEMPLATE_WITH_ROOT = "return globalThis.PySeExt.ComponentQuery.query('{cq}', '{rootId}')"

    _driver = None

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._driver = driver

        # Initialise our base class
        super().__init__(driver)

    def query(self, cq, rootId=None):
        """Executes a ComponentQuery and returns the result

        Args:
            cq (str): The query to execute
            rootId (str):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

        Returns:
            selenium.webdriver.remote.webelement[]: An array of DOM elements that match the query or an empty array if not found
        """
        if rootId == None:
            script = self._QUERY_TEMPLATE.format(cq=cq)
        else:
            script = self._QUERY_TEMPLATE_WITH_ROOT.format(cq=cq, rootId=rootId)

        return self._driver.execute_script(script)

    def wait_for_query(self, cq, rootId=None, timeout=3):
        """Method that waits for the specified CQ to match something

        Args:
            cq (str): The query to execute
            root (str):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 3)
        """
        WebDriverWait(self._driver, timeout).until(ComponentQuery.ComponentQueryFoundExpectation(cq))
        return self.query(cq, rootId)

    def find_field(self, formCQ, name):
        """Attempts to get a field by name from the specified form panel

        Args:
            form (selenium.webdriver.remote.webelement): The form panel in which to look for the field
            name (str): The name of the field

        Returns:
            selenium.webdriver.remote.webelement: The field DOM element, or None if not found.
        """
        script = self._find_field_template.format(formCQ=formCQ, name=name)
        return self._driver.execute_script(script)

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
