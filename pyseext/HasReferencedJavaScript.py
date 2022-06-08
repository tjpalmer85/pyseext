import logging
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path

class HasReferencedJavaScript:
    """Base class to be used by our test classes that have JavaScript that they need to load
    """

    # Class variables
    _SCRIPT_LOADED_TEST_TEMPLATE = "return globalThis.Ext && globalThis.Ext.isDefined && globalThis.Ext.isDefined(globalThis.PySeExt && globalThis.PySeExt.{class_name})"
    _SCRIPT_LOAD_TIMEOUT = 5
    _ASYNC_SCRIPT_TEMPLATE = "var {callback_parameter_name} = arguments[arguments.length - 1]; {script}"

    def __init__(self, driver, logger):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
            logger (logging.Logger): The logger to use
        """
        self._driver = driver
        self._logger = logger
        self.ensure_javascript_loaded()

    def ensure_javascript_loaded(self):
        """Ensures that our JavaScript has been loaded into the DOM.

        If it hasn't then it is loaded.
        """
        class_name = type(self).__name__

        # If our JavaScript has not been loaded then load it now
        if not self._driver.execute_script(self._SCRIPT_LOADED_TEST_TEMPLATE.format(class_name=class_name)):
            js_path = f'./js/PySeExt.{class_name}.js'
            self._logger.debug(f'Loading script: {js_path}')

            source_path = Path(__file__).resolve()
            source_dir = source_path.parent

            js_path = source_dir.joinpath(js_path)

            self._driver.execute_script(open(js_path).read())

            # Wait for it to the loaded
            WebDriverWait(self._driver, self._SCRIPT_LOAD_TIMEOUT).until(HasReferencedJavaScript.JavaScriptLoadedExpectation(class_name, self._SCRIPT_LOADED_TEST_TEMPLATE))

    def get_async_script_content(self, script: str, callback_parameter_name: str = 'callback'):
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
