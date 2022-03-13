from selenium.webdriver.support.ui import WebDriverWait

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class FormHelper(HasReferencedJavaScript):
    """A class to help with interacting with Ext form panels and forms
    """

    _FIND_FIELD_INPUT_ELEMENT_TEMPLATE = "return globalThis.PySeExt.FormHelper.findFieldInputElement('{form_cq}', '{name}')"

    _driver = None

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._driver = driver

        # Initialise our base class
        super().__init__(driver)

    def find_field_input_element(self, form_cq, name):
        """Attempts to get a field by name from the specified form panel

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field

        Returns:
            selenium.webdriver.remote.webelement: The field's input element DOM element, or None if not found.
        """
        script = self._FIND_FIELD_INPUT_ELEMENT_TEMPLATE.format(form_cq=form_cq, name=name)
        return self._driver.execute_script(script)