import logging
import time

from pyseext.FieldHelper import FieldHelper
from pyseext.ButtonHelper import ButtonHelper

class FormHelper():
    """A class to help with interacting with Ext form panels and forms
    """

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        self._driver = driver
        self._button_helper = ButtonHelper(driver)
        self._field_helper = FieldHelper(driver)

    def set_form_values(self, form_cq: str, field_values: dict):
        """Sets the values on the specified form panel

        Args:
            field_values (dict): Dictionary containing the 'name' and 'value' of the fields.
                                 The values can be strings, numbers or an object containing:
                                  - value (Any): The value for the field
                                  - delay (int): Number of seconds to delay after setting a value (a botch for remote combos at the moment)
                                  - tab_off (bool): Indicates whether to tab off the field after typing (another botch for remote combos)
                                                    and only works with fields that are being typed into.
        """
        if not type(field_values) is dict:
            raise TypeError("Parameter 'field_values' is not of type 'dict', but type '{type}'.".format(type=type(field_values)))

        self._logger.info(f"Populating form '{form_cq}' with values: {field_values}")

        def get_field_config_member(value, member: str, default = None):
            """Gets the member from a field config.

            Args:
                value (Any): The value or value config for the field.
                member (str): The member we're after.
                default (Any, optional): The default to return if not found. Defaults to None.

            Returns:
                Any: The value of the config, or the default if not found.
            """
            if isinstance(value, dict):
                return value.get(member, default)
            else:
                return default

        for field_name in field_values.keys():
            field_xtype = self._field_helper.get_field_xtype(form_cq, field_name)

            # FIXME: This is a mess!
            # .....: Need a field helper class, and for much of this complexity factored out!
            # .....: Also need much better support for comboboxes...
            if field_xtype:
                # Field found!
                value_or_config = field_values[field_name]

                field_value = get_field_config_member(value_or_config, 'value', value_or_config)
                delay = get_field_config_member(value_or_config, 'delay')
                tab_off = get_field_config_member(value_or_config, 'tab_off', False)

                # Now need to set it's value
                if (field_xtype.endswith('textfield') or
                    field_xtype.endswith('number') or
                    field_xtype.endswith('datefield') or
                    ((field_xtype.endswith('combo') or field_xtype.endswith('combobox')) and
                      isinstance(field_value, str))):
                    # Field can be typed into
                    field = self._field_helper.find_field_input_element(form_cq, field_name)
                    self._field_helper.type_into_element(field, field_value, delay, tab_off)
                elif field_xtype.endswith('checkbox'):
                    self._field_helper.set_checkbox_value(form_cq, field_name, field_value)
                elif (field_xtype.endswith('combo') or
                    field_xtype.endswith('combobox') or
                    field_xtype.endswith('radiogroup') or   # FIXME: For a radio group, can get child controls using getBoxes(query), so could click on children if wanted!
                    field_xtype.endswith('radio')):

                    # We want to directly set the value on the field rather than type it in
                    self._field_helper.set_field_value(form_cq, field_name, field_value)

                    if delay:
                        time.sleep(delay)
                else:
                    raise FieldHelper.UnsupportedFieldXTypeException(form_cq, field_name, field_xtype)
            else:
                raise FieldHelper.FieldNotFoundException(form_cq, field_name)

    def submit_by_button(self, form_cq: str, text: str = 'Ok'):
        """Submits a form by clicking on it's submit button.

        Args:
            form_cq (str): The component query that identifies the form panel to submit.
            text (str, optional): The text on the submit button. Defaults to 'Ok'.
        """
        self._button_helper.click_button_by_text(text, form_cq)
