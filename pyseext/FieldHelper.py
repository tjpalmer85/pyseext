import logging
import random
import time
from typing import Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class FieldHelper(HasReferencedJavaScript):
    """A class to help with interacting with Ext fields
    """

    # Class variables
    _FIND_FIELD_INPUT_ELEMENT_TEMPLATE = "return globalThis.PySeExt.FieldHelper.findFieldInputElement('{form_cq}', '{name}')"
    _GET_FIELD_XTYPE_TEMPLATE = "return globalThis.PySeExt.FieldHelper.getFieldXType('{form_cq}', '{name}')"
    _GET_FIELD_VALUE_TEMPLATE = "return globalThis.PySeExt.FieldHelper.getFieldValue('{form_cq}', '{name}')"
    _SET_CHECKBOX_VALUE_TEMPLATE = "return globalThis.PySeExt.FieldHelper.setCheckboxValue('{form_cq}', '{name}', {checked})"
    _SET_FIELD_VALUE_TEMPLATE = "return globalThis.PySeExt.FieldHelper.setFieldValue('{form_cq}', '{name}', {value})"

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        self._driver = driver
        self._action_chains = ActionChains(driver)

        # Initialise our base class
        super().__init__(driver, self._logger)

    def find_field_input_element(self, form_cq: str, name: str):
        """Attempts to get a field by name from the specified form panel

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field

        Returns:
            selenium.webdriver.remote.webelement: The field's input element DOM element, or None if not found.
        """
        script = self._FIND_FIELD_INPUT_ELEMENT_TEMPLATE.format(form_cq=form_cq, name=name)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def get_field_xtype(self, form_cq: str, name: str):
        """Attempts to get the xtype of a field by name from the specified form panel

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field

        Returns:
            str: The xtype of the field, or None if not found.
        """
        script = self._GET_FIELD_XTYPE_TEMPLATE.format(form_cq=form_cq, name=name)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def get_field_value(self, form_cq: str, name: str):
        """Attempts to get the value of a field by name from the specified form panel

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field

        Returns:
            Any: The value of the field, or None if not found.
        """
        script = self._GET_FIELD_VALUE_TEMPLATE.format(form_cq=form_cq, name=name)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def set_checkbox_value(self, form_cq: str, field_name: str, checked: bool = True):
        """Sets the checked value for a checkbox.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
            checked (bool, optional): The checked value for the checkbox. Defaults to True.
        """

        # FIXME: Perhaps change this to get the value, and if checked state is not correct to
        # .....: click on the element?

        script = self._SET_CHECKBOX_VALUE_TEMPLATE.format(form_cq=form_cq, name=field_name, checked=str(checked).lower())
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def set_field_value(self, form_cq: str, field_name: str, value: Union[int, str]):
        """Sets the value for a field to a numeric value.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
            value (Union[int, str]): The value for the field.
        """
        # If value is a string then we want to quote it in our script
        if isinstance(value, str):
            value = "'{value}'".format(value=value)

        script = self._SET_FIELD_VALUE_TEMPLATE.format(form_cq=form_cq, name=field_name, value=value)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def type_into_element(self, element, text: str, delay: int = None, tab_off: bool = False):
        """Types into an input element in a more realistic manner.

        Args:
            element (selenium.webdriver.remote.webelement): The element to type into.
            text (str): The text to type.
            delay (int): The number of seconds to delay after typing.
            tab_off (bool): Indicates whether to tab off the field after typing, and delay.
        """
        # Ensure text really is a string
        text = str(text)

        # First move to and click on element to give it focus
        self._action_chains.move_to_element(element)
        self._action_chains.click()
        self._action_chains.perform()

        # Now type each character
        self.type(text)

        if delay:
            time.sleep(delay)

        if tab_off:
            self.type_tab()

    def type(self, text: str):
        """Types into the currently focused element in a realistic manner.

        Args:
            text (str): The text to type.
        """
        for character in text:
            self._action_chains.send_keys(character)
            self._action_chains.perform()
            time.sleep(random.uniform(0.0001, 0.002))

    def type_tab(self):
        """Type a tab character into the currently focused element
        """
        self._action_chains.send_keys(Keys.TAB)
        self._action_chains.perform()

    class FieldNotFoundException(Exception):
        """Exception class thrown when we failed to find the specified field
        """

        def __init__(self, form_cq: str, field_name: str, message: str = "Failed to find field named '{field_name}' on form with CQ '{form_cq}'."):
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

    class UnsupportedFieldXTypeException(Exception):
        """Exception class thrown when we have been asked to perform an action that is not
        supported for the given field xtype.
        """

        def __init__(self, form_cq: str, field_name: str, xtype: str, message: str = "The field named '{field_name}' on form with CQ '{form_cq}' is of an xtype '{xtype}' which is not supported for the requested operation."):
            """Initialises an instance of this exception

            Args:
                form_cq (str): The CQ used to find the form
                field_name (str): The name of the field
                xtype (str): The xtype of the field.
                message (str, optional): The exception message. Defaults to "The field named '{field_name}' on form with CQ '{form_cq}' is of an xtype '{xtype}' which is not supported for the requested operation."
            """
            self.message = message
            self._form_cq = form_cq
            self._field_name = field_name
            self._xtype = xtype

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(field_name=self._field_name, form_cq=self._form_cq, xtype=self._xtype)