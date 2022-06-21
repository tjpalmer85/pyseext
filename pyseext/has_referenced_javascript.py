"""
Module that contains our HasReferencedJavaScript class.
"""
from logging import Logger
from os import path
import pkg_resources

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

class HasReferencedJavaScript:
    """Base class to be used by our test classes that have JavaScript that they need to load
    """

    # Class variables
    _SCRIPT_LOADED_TEST_TEMPLATE: str = \
        "return globalThis.Ext && globalThis.Ext.isDefined && globalThis.Ext.isDefined(globalThis.PySeExt && globalThis.PySeExt.{class_name})"
    """The script template to use to determine whether the JavaScript for a class has been loaded"""

    _SCRIPT_LOAD_TIMEOUT: float = 10
    """The script loading timeout to use. Defaults to 10 seconds."""

    _ASYNC_SCRIPT_TEMPLATE: str = "var {callback_parameter_name} = arguments[arguments.length - 1]; {script}"
    """The script template to use to call some Asynchronous JavaScript, that has a callback for its last parameter.
    Requires the inserts: {callback_parameter_name}, {script}"""

    def __init__(self, driver: WebDriver, logger: Logger):
        """Initialises an instance of this class

        Args:
            driver (WebDriver): The webdriver to use
            logger (logging.Logger): The logger to use
        """
        self._driver = driver
        """The WebDriver instance for this class instance"""

        self._logger = logger
        """The Logger instance for this class instance"""

        self.ensure_javascript_loaded()

    def ensure_javascript_loaded(self):
        """Ensures that our JavaScript has been loaded into the DOM.

        If it hasn't then it is loaded.
        """
        class_name = type(self).__name__

        # If our JavaScript has not been loaded then load it now
        if not self._driver.execute_script(self._SCRIPT_LOADED_TEST_TEMPLATE.format(class_name=class_name)):
            # Read JavaScript from package resources
            stream = pkg_resources.resource_stream(__package__, path.join('js', f'PySeExt.{class_name}.js'))

            self._logger.debug("Loading JavaScript from '%s'", stream.name)
            self._driver.execute_script(str(stream.read(), encoding = "utf-8"))

            # Wait for it to the loaded
            WebDriverWait(self._driver,
                          self._SCRIPT_LOAD_TIMEOUT).until(HasReferencedJavaScript.JavaScriptLoadedExpectation(class_name,
                                                                                                               self._SCRIPT_LOADED_TEST_TEMPLATE))

    def get_async_script_content(self, script: str, callback_parameter_name: str = 'callback') -> str:
        """Builds some async script content, to call some JavaScript that takes a callback function.

        Note, we cannot get a value back from the JavaScript (that I know of), but we can get notified of completion.

        Args:
            script (str): The script containing the asynchronous JavaScript being called.
            callback_parameter_name (str, optional): The name of the callback parmeter to use for the script.
                                                     Defaults to 'callback'.

        Returns:
            str: The script, prefixed with some code that captures the callback passes from the web driver.
        """
        return self._ASYNC_SCRIPT_TEMPLATE.format(callback_parameter_name=callback_parameter_name, script=script)

    class JavaScriptLoadedExpectation():
        """ An expectation for checking that our JavaScript has loaded
        """

        def __init__(self, class_name: str, test_template: str):
            """Initialises an instance of this class

            Args:
                class_name (str): The name of the class that we're loading the script for
                test_template (str): The template to use to test for the script being loaded
            """
            self._class_name = class_name
            self._test_template = test_template

        def __call__(self, driver):
            """Method that determines whether our JavaScript is present
            """
            return driver.execute_script(self._test_template.format(class_name=self._class_name))
