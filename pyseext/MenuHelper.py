from selenium.webdriver.common.action_chains import ActionChains

from pyseext.ComponentQuery import ComponentQuery

class MenuHelper:
    """A class to help with interacting with Ext menus and menu items
    """

    # Class variables
    _ENABLED_MENU_ITEM_TEMPLATE = 'menuitem[text="{text}"][disabled=false]'
    _DISABLED_MENU_ITEM_TEMPLATE = 'menuitem[text="{text}"][disabled=true]'

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """

        # Instance variables
        self._cq = ComponentQuery(driver)
        self._action_chains = ActionChains(driver)

    def click_menu_item_by_text(self, text: str, root_id: str = None):
        """Finds a visible, enabled menu item with the specified text and clicks it.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        menu_item = self._cq.wait_for_single_query_visible(self._ENABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)

        # Rather than call click, move mouse to the menu item and click...
        self._action_chains.move_to_element(menu_item)
        self._action_chains.click()
        self._action_chains.perform()

    def check_menu_item_enabled(self, text: str, root_id: str = None):
        """Checks that we can find an enabled menu item with the specified text.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self._cq.wait_for_single_query(self._ENABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)

    def check_menu_item_disabled(self, text: str, root_id:str = None):
        """Checks that we can find a disabled menu item with the specified text.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self._cq.wait_for_single_query(self._DISABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)
