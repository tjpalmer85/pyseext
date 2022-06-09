import logging

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
            raise TypeError(f"Parameter 'field_values' is not of type 'dict', but type '{type(field_values)}'.")

        self._logger.info(f"Populating form '{form_cq}' with values: {field_values}")

        for field_name in field_values.keys():
            self._field_helper.set_field_value(form_cq, field_name, field_values[field_name])

    def submit_by_button(self, form_cq: str, text: str = 'Ok'):
        """Submits a form by clicking on it's submit button.

        Args:
            form_cq (str): The component query that identifies the form panel to submit.
            text (str, optional): The text on the submit button. Defaults to 'Ok'.
        """
        self._button_helper.click_button_by_text(text, form_cq)
