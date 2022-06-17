Module pyseext.button_helper
============================
Module that contains our ButtonHelper class.

Classes
-------

`ButtonHelper(driver)`
:   A class to help with interacting with Ext buttons
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Methods

    `check_button_disabled(self, text: str, root_id: Optional[str] = None)`
    :   Checks that we can find a disabled button with the specified text.
        
        Args:
            text (str): The text on the button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

    `check_button_enabled(self, text: str, root_id: Optional[str] = None)`
    :   Checks that we can find an enabled button with the specified text.
        
        Args:
            text (str): The text on the button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

    `click_button(self, cq: str, root_id: Optional[str] = None)`
    :   Finds a button using the supplied component query and clicks it.
        
        Args:
            cq (str): The component query to find the button.
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

    `click_button_by_text(self, text: str, root_id: Optional[str] = None)`
    :   Finds a visible, enabled button with the specified text and clicks it.
        
        Args:
            text (str): The text on the button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

    `click_button_on_messagebox(self, text: str = 'OK')`
    :   Clicks a button on a messagebox.
        
        The messagebox must be visible.
        
        Args:
            text (str, optional): The text of the button to click. Defaults to 'OK'.