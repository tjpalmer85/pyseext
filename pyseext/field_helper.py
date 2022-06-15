"""
Module that contains our FieldHelper class.
"""
import logging
import time
from typing import Union, Any

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from pyseext.has_referenced_javascript import HasReferencedJavaScript
from pyseext.core import Core
from pyseext.input_helper import InputHelper
from pyseext.store_helper import StoreHelper

class FieldHelper(HasReferencedJavaScript):
    """A class to help with interacting with Ext fields
    """

    # Class variables
    _FIND_FIELD_INPUT_ELEMENT_TEMPLATE: str = "return globalThis.PySeExt.FieldHelper.findFieldInputElement('{form_cq}', '{name}')"
    _GET_FIELD_XTYPE_TEMPLATE: str = "return globalThis.PySeExt.FieldHelper.getFieldXType('{form_cq}', '{name}')"
    _GET_FIELD_VALUE_TEMPLATE: str = "return globalThis.PySeExt.FieldHelper.getFieldValue('{form_cq}', '{name}')"
    _SET_FIELD_VALUE_TEMPLATE: str = "return globalThis.PySeExt.FieldHelper.setFieldValue('{form_cq}', '{name}', {value})"
    _IS_REMOTELY_FILTERED_COMBOBOX_TEMPLATE: str = "return globalThis.PySeExt.FieldHelper.isRemotelyFilteredComboBox('{form_cq}', '{name}')"
    _FOCUS_FIELD_TEMPLATE: str = "return globalThis.PySeExt.FieldHelper.focusField('{form_cq}', {index_or_name})"

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        self._driver = driver
        self._action_chains = ActionChains(driver)
        self._core = Core(driver)
        self._input_helper = InputHelper(driver)
        self._store_helper = StoreHelper(driver)

        # Initialise our base class
        super().__init__(driver, self._logger)

    def find_field_input_element(self, form_cq: str, name: str) -> WebElement:
        """Attempts to get a field by name from the specified form panel

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field

        Returns:
            WebElement: The field's input element DOM element, or None if not found.
        """
        script = self._FIND_FIELD_INPUT_ELEMENT_TEMPLATE.format(form_cq=form_cq, name=name)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def get_field_xtype(self, form_cq: str, name: str) -> str:
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

    def get_field_value(self, form_cq: str, name: str) -> Any:
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

    def set_field_value(self, form_cq: str, field_name: str, value: Union[dict, int, str]):
        """Sets the value for a field.

        If the field can be typed into by a user, and the value is typeable, then that is the approach taken.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field.
            field_name (str): The name of the field.
            value (Union[dict, int, str]): The value for the field.
                                           Supports being specified as a dictionary that can contain:
                                               - value (Union[int, str]): The value to set.
                                               - data (dict): A dictionary containing the data to find in the fields store.
                                                              If the field is not a store holder then an exception is thrown.
        """
        field_xtype = self.get_field_xtype(form_cq, field_name)

        if field_xtype:
            # Field found!
            field_value = self._core.try_get_object_member(value, 'value', value)
            delay = self._core.try_get_object_member(value, 'delay')
            tab_off = self._core.try_get_object_member(value, 'tab_off', False)

            # Now need to set it's value
            if (field_xtype.endswith('combo') or field_xtype.endswith('combobox')):
                is_combo_remote = self._is_field_remotely_filtered_combobox(form_cq, field_name)
                is_value_a_dict = isinstance(field_value, dict)

                if is_combo_remote:
                    if not is_value_a_dict:
                        # We want to type into the combobox, to filter it, and wait for it to load.
                        # Once loaded we expect to have a single value that will end up selected.
                        field = self.find_field_input_element(form_cq, field_name)
                        self._input_helper.type_into_element(field, field_value)

                        # This reset has to be here it seems, rather than before typing.
                        # I suspect that the load count gets incremented a few times as the box
                        # is typed into or something?

                        # Anyway, remote combos will take longer to load than this statement does.
                        # If not, then I guess that's a nice problem to have :-)
                        combobox_cq = self.get_field_component_query(form_cq, field_name)
                        self._store_helper.reset_store_load_count(combobox_cq)
                        self._store_helper.wait_for_store_loaded(combobox_cq)

                        # FIXME: Does the store have a count of one?
                        # .....: Do we really care? If multiple then the top one will be highlighted...

                        # Seems we need to tab off or sometimes the value will not stick?!
                        self._input_helper.type_tab()
                    else:
                        # FIXME: Implement!
                        raise NotImplementedError()
                else:
                    if not is_value_a_dict:
                        # We can just type into the combobox
                        field = self.find_field_input_element(form_cq, field_name)
                        self._input_helper.type_into_element(field, field_value, delay, tab_off)

                        # Seems we need to tab off or sometimes the value will not stick?!
                        self._input_helper.type_tab()
                    else:
                        # FIXME: Implement!
                        raise NotImplementedError()

            elif (field_xtype.endswith('textfield') or
                field_xtype.endswith('number') or
                field_xtype.endswith('datefield')):
                # Field can be typed into
                field = self.find_field_input_element(form_cq, field_name)
                self._input_helper.type_into_element(field, field_value, delay, tab_off)

            elif (field_xtype.endswith('checkbox') or
                field_xtype.endswith('radiogroup') or
                field_xtype.endswith('radio')):

                # FIXME: We could click on the elements here, after checking whether they
                # .....: are already set to the value we want.
                # .....: For a radio group, can get child controls using getBoxes(query),
                # .....: so could click on children if wanted!

                # Directly set the value on the field
                self.set_field_value_directly(form_cq, field_name, field_value)

                if delay:
                    time.sleep(delay)
            else:
                raise FieldHelper.UnsupportedFieldXTypeException(form_cq, field_name, field_xtype)
        else:
            raise FieldHelper.FieldNotFoundException(form_cq, field_name)

    def set_field_value_directly(self, form_cq: str, field_name: str, value: Union[int, str]):
        """Sets the value for a field using Ext's setValue method.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
            value (Union[int, str]): The value for the field.
        """
        # If value is a string then we want to quote it in our script
        if isinstance(value, str):
            value = f"'{value}'"

        # If value is a boolean we want to force it to lowercase
        if isinstance(value, bool):
            value = str(value).lower()

        script = self._SET_FIELD_VALUE_TEMPLATE.format(form_cq=form_cq, name=field_name, value=value)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def focus_field(self, form_cq: str, index_or_name: Union[int, str]):
        """Method to focus on a field on a form by (zero-based) index or name.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            index_or_name: (Union[int, str]): The zero-based index or name of the field to focus.
        """
        # If value is a string then we want to quote it in our script
        if isinstance(index_or_name, str):
            index_or_name = f"'{index_or_name}'"

        script = self._FOCUS_FIELD_TEMPLATE.format(form_cq=form_cq, index_or_name=index_or_name)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def get_field_component_query(self, form_cq: str, field_name: str):
        """Builds the component query for a field on a form.

        This is useful, since allows you to interact with a field using component query, so can
        utilise the methods in StoreHelper, say.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            field_name (str): The name of the field.
        """
        return f'{form_cq} field[name="{field_name}"]'

    def check_field_value(self, form_cq: str, field_name: str, value: Any) -> bool:
        """Method that checks that the value of the specified field is that specified.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field.
            field_name (str): The name of the field
            value (Any): The value that we expect the field to have.

        Returns:
            bool: True if the value of the field matches the expected, False otherwise.
        """
        field_value = self.get_field_value(form_cq, field_name)

        return field_value == value

    def _is_field_remotely_filtered_combobox(self, form_cq: str, name: str) -> bool:
        """Attempts to find a field by name from the specified form panel, and determine whether
        it is a remotely filtered combobox.

        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field

        Returns:
            bool: True if the field was found, and is a remotely filtered combobox. False otherwise.
        """
        script = self._IS_REMOTELY_FILTERED_COMBOBOX_TEMPLATE.format(form_cq=form_cq, name=name)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

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

        def __init__(self,
                     form_cq: str,
                     field_name: str,
                     xtype: str,
                     message: str = "The field named '{field_name}' on form with CQ '{form_cq}' is of an xtype '{xtype}' which is not supported for the requested operation."):
            """Initialises an instance of this exception

            Args:
                form_cq (str): The CQ used to find the form
                field_name (str): The name of the field
                xtype (str): The xtype of the field.
                message (str, optional): The exception message.
                                        Defaults to "The field named '{field_name}' on form with CQ '{form_cq}' is of an xtype '{xtype}' which is not supported for the requested operation."
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
