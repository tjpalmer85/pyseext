from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path

class HasReferencedJavaScript:
    """Base class to be used by our test classes that have JavaScript that they need to load
    """

    # Class variables
    _SCRIPT_LOADED_TEST_TEMPLATE = "return Ext.isDefined(globalThis.PySeExt && globalThis.PySeExt.{class_name})"
    _SCRIPT_LOAD_TIMEOUT = 2
    _ASYNC_SCRIPT_TEMPLATE = "var {callback_parameter_name} = arguments[arguments.length - 1]; {script}"

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """

        class_name = type(self).__name__

        # If our JavaScript has not been loaded then load it now
        if not driver.execute_script(self._SCRIPT_LOADED_TEST_TEMPLATE.format(class_name=class_name)):
            js_path = './js/PySeExt.{class_name}.js'.format(class_name=class_name)
            print('Loading script: ', js_path)

            source_path = Path(__file__).resolve()
            source_dir = source_path.parent

            js_path = source_dir.joinpath(js_path)
            print('Full path: ', js_path)

            driver.execute_script(open(js_path).read())

            # Wait for it to the loaded
            WebDriverWait(driver, self._SCRIPT_LOAD_TIMEOUT).until(HasReferencedJavaScript.JavaScriptLoadedExpectation(class_name, self._SCRIPT_LOADED_TEST_TEMPLATE))

    def get_async_script_content(self, script, callback_parameter_name='callback'):
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

        def __init__(self, class_name, test_template):
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
