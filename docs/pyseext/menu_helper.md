Module pyseext.menu_helper
==========================
Module that contains our MenuHelper class.

Classes
-------

`MenuHelper(driver)`
:   A class to help with interacting with Ext menus and menu items
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Methods

    `check_menu_item_disabled(self, text: str, root_id: Optional[str] = None)`
    :   Checks that we can find a disabled menu item with the specified text.
        
        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

    `check_menu_item_enabled(self, text: str, root_id: Optional[str] = None)`
    :   Checks that we can find an enabled menu item with the specified text.
        
        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.

    `click_menu_item(self, cq: str, root_id: Optional[str] = None)`
    :   Finds a menu item using the supplied component query and clicks it.
        
        Args:
            cq (str): The component query to find the menu item.
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.

    `click_menu_item_by_text(self, text: str, root_id: Optional[str] = None)`
    :   Finds a visible, enabled menu item with the specified text and clicks it.
        
        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.