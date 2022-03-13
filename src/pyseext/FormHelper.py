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

    def set_form_values(self, form_cq, field_values):
        """Sets the values on the specified form panel

        Args:
            field_values (dict): Dictionary containing the 'name' and 'value' of the fields.
        """
        if not type(field_values) is dict:
            raise TypeError("Parameter 'field_values' is not of type 'dict'")

        for field_name in field_values.keys():
            field = self.find_field_input_element(form_cq, field_name)
            if field:
                field.send_keys(field_values[field_name])
            else:
                raise FormHelper.FieldNotFoundException(form_cq, field_name)

    class FieldNotFoundException(Exception):
        """Exception class thrown when we failed to find the specified field
        """

        _form_cq = None
        _field_name = None

        def __init__(self, form_cq, field_name, message="Failed to find field named '{field_name}' on form with CQ '{form_cq}'."):
            """Initialises an instance of this exception

            Args:
                form_cq (str): The CQ used to find the form
                field_name (str): The name of the field
                message (str, optional): The exception message. Defaults to "Failed to find field named '{field_name}' on form with CQ '{form_cq}'.".
            """
            self.message = message
            self._form_cq = form_cq
            self._field_name = field_name

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(field_name=self._field_name, form_cq=self._form_cq)