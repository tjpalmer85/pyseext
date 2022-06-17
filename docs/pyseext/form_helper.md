Module pyseext.form_helper
==========================
Module that contains our FormHelper class.

Classes
-------

`FormHelper(driver)`
:   A class to help with interacting with Ext form panels and forms
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Methods

    `set_form_values(self, form_cq: str, field_values: Union[dict, list[Union[str, float, int, NoneType]]])`
    :   Sets the values on the specified form panel.
        
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

    `submit_by_button(self, form_cq: str, text: str = 'Ok')`
    :   Submits a form by clicking on it's submit button.
        
        Args:
            form_cq (str): The component query that identifies the form panel to submit.
            text (str, optional): The text on the submit button. Defaults to 'Ok'.