"""
Module that contains our FormHelper class.
"""
import logging
from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver

from pyseext.field_helper import FieldHelper
from pyseext.button_helper import ButtonHelper
from pyseext.input_helper import InputHelper

class FormHelper:
    """A class to help with interacting with Ext form panels and forms
    """

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        """The Logger instance for this class"""

        self._driver = driver
        """The WebDriver instance for this class"""

        self._button_helper = ButtonHelper(driver)
        """The `ButtonHelper` instance for this class"""

        self._field_helper = FieldHelper(driver)
        """The `FieldHelper` instance for this class"""

        self._input_helper = InputHelper(driver)
        """The `InputHelper` instance for this class"""

    def set_form_values(self, form_cq: str, field_values: Union[dict, list[Union[str, float, int, None]]]):
        """Sets the values on the specified form panel.

        If using the list version, you can only supply values that can be typed into input elements, so
        it won't work as expected for checkboxes or radio buttons.

        Args:
            form_cq (str): The component query that identifies the form panel on which to set the values.
            field_values (Union[dict, list[Union[str, float, int, None]]]):
                Either a dictionary containing the 'name' and 'value' of the fields.
                    The values can be strings, numbers or an object containing:
                        - value (Any): The value for the field
                        - delay (int): Number of seconds to delay after setting a value (a botch for remote combos at the moment)
                        - tab_off (bool): Indicates whether to tab off the field after typing (another botch for remote combos)
                                            and only works with fields that are being typed into.
                Or an array of values to type into the fields, in order of appearance, tabbing on from each field.
                    A value of None in the array means that no value should be entered.

        """
        if isinstance(field_values, dict):
            self._logger.info("Populating form '%s' with values: %s", form_cq, field_values)

            for field_name in field_values.keys():
                self._field_helper.set_field_value(form_cq, field_name, field_values[field_name])

        elif isinstance(field_values, list):
            self._field_helper.focus_field(form_cq, 0)

            for field_value in field_values:
                if field_value:
                    self._input_helper.type(str(field_value))

                self._input_helper.type_tab()

        else:
            raise TypeError(f"Parameter 'field_values' is not of type 'dict' or a 'list', but type '{type(field_values)}'.")

    def submit_by_button(self, form_cq: str, text: str = 'Ok'):
        """Submits a form by clicking on it's submit button.

        Args:
            form_cq (str): The component query that identifies the form panel to submit.
            text (str, optional): The text on the submit button. Defaults to 'Ok'.
        """
        self._button_helper.click_button_by_text(text, form_cq)
