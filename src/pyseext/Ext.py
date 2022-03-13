from selenium.webdriver.support.ui import WebDriverWait

class Ext:
    """A class to help with using Ext
    """

    _driver = None

    def __init__(self, driver):
        """Initialises an instance of this class.

        Args:
            driver (selenium.webdriver): The webdriver to use.
        """
        self._driver = driver

    def wait_for_dom_ready(self, timeout=30):
        """Method that waits until Ext indicates that the DOM is ready.
        Calls Ext.isDomReady.
        Will throw a TimeOutException if the value is not true within the specified timeout period.

        Args:
            timeout (float): Number of seconds before timing out (default 30)
        """
        WebDriverWait(self._driver, timeout).until(Ext.IsDomReadyExpectation())

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