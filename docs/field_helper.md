Module pyseext.field_helper
===========================
Module that contains our FieldHelper class.

Classes
-------

`FieldHelper(driver: selenium.webdriver.remote.webdriver.WebDriver)`
:   A class to help with interacting with Ext fields
        
    
    Initialises an instance of this class
    
    Args:
        driver (WebDriver): The webdriver to use

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Class variables

    `FieldNotFoundException`
    :   Exception class thrown when we failed to find the specified field

    `RecordNotFoundException`
    :   Exception class thrown when we failed to find the specified record in the a combobox

    `UnsupportedFieldXTypeException`
    :   Exception class thrown when we have been asked to perform an action that is not
        supported for the given field xtype.

    ### Methods

    `check_field_value(self, form_cq: str, name: str, value: Any) ‑> bool`
    :   Method that checks that the value of the specified field is that specified.
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field.
            name (str): The name of the field
            value (Any): The value that we expect the field to have.
        
        Returns:
            bool: True if the value of the field matches the expected, False otherwise.

    `find_field_input_element(self, form_cq: str, name: str) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Attempts to get a field by name from the specified form panel
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
        
        Returns:
            WebElement: The field's input element DOM element, or None if not found.

    `focus_field(self, form_cq: str, index_or_name: Union[int, str])`
    :   Method to focus on a field on a form by (zero-based) index or name.
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            index_or_name: (Union[int, str]): The zero-based index or name of the field to focus.

    `get_field_component_query(self, form_cq: str, name: str)`
    :   Builds the component query for a field on a form.
        
        This is useful, since allows you to interact with a field using component query, so can
        utilise the methods in StoreHelper, say.
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field.

    `get_field_value(self, form_cq: str, name: str) ‑> Any`
    :   Attempts to get the value of a field by name from the specified form panel
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
        
        Returns:
            Any: The value of the field, or None if not found.

    `get_field_xtype(self, form_cq: str, name: str) ‑> str`
    :   Attempts to get the xtype of a field by name from the specified form panel
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
        
        Returns:
            str: The xtype of the field, or None if not found.

    `select_combobox_value(self, form_cq: str, name: str, data: dict) ‑> bool`
    :   Selects a value on a combobox field by finding a record with the specified data.
        All members of the data object must match a record in the store.
        
        Waits until the combobox has finished loading first, and ensures that the select
        event is fired on the combobox if the record is found.
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
            data (dict): The data to find in the store and select.
        
        Returns:
            True if the value was found and selected, False otherwise.

    `set_field_value(self, form_cq: str, name: str, value: Union[dict, float, str])`
    :   Sets the value for a field.
        
        If the field can be typed into by a user, and the value is typeable, then that is the approach taken.
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field.
            name (str): The name of the field.
            value (Union[dict, float, str]): The value for the field.
        
                                             If the value is a number or string then it is typed into the field where possible,
                                             otherwise the value is set directly.
        
                                             If the value is a dictionary then either it, or it's value member is taken to be model
                                             data to select in a combobox.
        
                                             If the combobox is remotely filtered then it is expected that both a value member and
                                             a filterText member is specified, where the filterText is typed into the combobox, then
                                             the value selected.
        
                                             If the value is supplied as a dictionary and the field is not a store holder then
                                             an exception is thrown.

    `set_field_value_directly(self, form_cq: str, name: str, value: Union[int, str])`
    :   Sets the value for a field using Ext's setValue method.
        
        Args:
            form_cq (str): The component query that identifies the form panel in which to look for the field
            name (str): The name of the field
            value (Union[int, str]): The value for the field.