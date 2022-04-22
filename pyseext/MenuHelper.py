from pyseext.ComponentQuery import ComponentQuery

class MenuHelper:
    """A class to help with interacting with Ext menus and menu items
    """

    _MENU_ITEM_TEMPLATE = 'menuitem[text="{text}"][disabled=false]'

    _cq = None

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._cq = ComponentQuery(driver)

    def click_menu_item_by_text(self, text, root_id=None):
        """Finds a visible, enabled menu item with the specified text and clicks it.

        Args:
            text (str): The text on the menu item
            root_id (str, optional):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        menu_item = self._cq.wait_for_single_query_visible(self._MENU_ITEM_TEMPLATE.format(text=text), root_id)

        # FIXME: Be nice if we could move the mouse to the button and click.
        # See here: https://www.lambdatest.com/blog/perform-mouse-actions-in-selenium-webdriver/
        menu_item.click()