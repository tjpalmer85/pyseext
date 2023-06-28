"""
Module that contains our MenuHelper class.
"""
import logging
from typing import Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pyseext.component_query import ComponentQuery

class MenuHelper:
    """A class to help with interacting with Ext menus and menu items"""

    # Class variables
    _ENABLED_MENU_ITEM_TEMPLATE: str = 'menuitem[text="{text}"][disabled=false]{{isVisible(true)}}'
    """The component query template to use to find an enabled, visible menu item.
    Requires the inserts: {text}"""

    _DISABLED_MENU_ITEM_TEMPLATE: str = 'menuitem[text="{text}"][disabled=true]{{isVisible(true)}}'
    """The component query template to use to find a disbled, visible menu item.
    Requires the inserts: {text}"""

    _ENABLED_MENU_ITEMS_CQ: str = 'menuitem[disabled=false]{isVisible(true)}'
    """The component query to use to find all enabled, visible menu items."""

    SPACER_TEXT_CONTEXT: str = ' '
    """The text content of a spacer element in a menu."""

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (WebDriver): The webdriver to use
        """

        # Instance variables
        self._logger = logging.getLogger(__name__)
        """The Logger instance for this class instance"""

        self._cq = ComponentQuery(driver)
        """The `ComponentQuery` instance for this class instance"""

        self._action_chains = ActionChains(driver)
        """The ActionChains instance for this class instance"""

    def move_to_menu_item(self, cq: str, root_id: Union[str, None] = None):
        """Finds a menu item using the supplied component query and moves to it.

        Args:
            cq (str): The component query to find the menu item.
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
        """
        menu_item = self._cq.wait_for_single_query_visible(cq, root_id)

        # Rather than call click, move mouse to button and click...
        self._logger.info("Moving to menu item with CQ '%s'", cq)

        self._action_chains.move_to_element(menu_item)
        self._action_chains.perform()

    def click_menu_item(self, cq: str, root_id: Union[str, None] = None):
        """Finds a menu item using the supplied component query and clicks it.

        Args:
            cq (str): The component query to find the menu item.
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
        """
        self.move_to_menu_item(cq, root_id)

        # Rather than call click, move mouse to button and click...
        self._logger.info("Clicking menu item with CQ '%s'", cq)

        self._action_chains.click()
        self._action_chains.perform()

    def click_menu_item_by_text(self, text: str, root_id: Union[str, None] = None):
        """Finds a visible, enabled menu item with the specified text and clicks it.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self.click_menu_item(self._ENABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)

    def move_to_menu_item_by_text(self, text: str, root_id: Union[str, None] = None):
        """Finds a visible, enabled menu item with the specified text and moves to it.

        Args:
            cq (str): The component query to find the menu item.
            root_id (str, optional): The id of the container within which to perform the query.
                                     If omitted, all components within the document are included in the search.
        """
        self.move_to_menu_item(self._ENABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)

    def try_get_menu_item_by_text(self, text: str, root_id: Union[str, None] = None, timeout: float = 1):
        """Finds a visible, enabled menu item with the specified text and returns it if found.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 1)

        Returns:
            WebElement: The DOM element for the menu item, if found.
        """
        cq = self._ENABLED_MENU_ITEM_TEMPLATE.format(text=text)
        results = self._cq.wait_for_query(cq=cq, root_id=root_id, timeout=timeout, throw_if_not_found=False)
        if len(results) > 1:
            raise ComponentQuery.QueryMatchedMultipleElementsException(cq, len(results))
        elif len(results) > 0:
            return results[0]
        else:
            return None

    def get_enabled_menu_items(self, root_id: Union[str, None] = None, timeout: float = 1) -> list[WebElement]:
        """Finds visible, enabled menu items.

        Args:
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 1)

        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if none found
        """
        return self._cq.wait_for_query(cq=self._ENABLED_MENU_ITEMS_CQ,
                                       root_id=root_id,
                                       timeout=timeout,
                                       throw_if_not_found=False)

    def check_menu_item_enabled(self, text: str, root_id: Union[str, None] = None):
        """Checks that we can find an enabled menu item with the specified text.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self._cq.wait_for_single_query(self._ENABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)

    def check_menu_item_disabled(self, text: str, root_id:Union[str, None] = None):
        """Checks that we can find a disabled menu item with the specified text.

        Args:
            text (str): The text on the menu item
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self._cq.wait_for_single_query(self._DISABLED_MENU_ITEM_TEMPLATE.format(text=text), root_id)
