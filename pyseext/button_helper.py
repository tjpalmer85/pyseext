"""
Module that contains our ButtonHelper class.
"""

import logging
from typing import Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from pyseext.component_query import ComponentQuery

class ButtonHelper:
    """A class to help with interacting with Ext buttons"""

    # Class variables
    _ENABLED_BUTTON_TEMPLATE: str = 'button[text="{text}"][disabled=false]'
    """The component query template to use to find an enabled button.
    Requires the inserts: {text}"""

    _DISABLED_BUTTON_TEMPLATE: str = 'button[text="{text}"][disabled=true]'
    """The component query template to use to find a disabled button.
    Requires the inserts: {text}"""

    _MESSAGEBOX_BUTTON_TEMPLATE: str = 'messagebox{{isVisible(true)}} button[text="{text}"]'
    """The component query template to use to find a button on a visible message box.
    Requires the inserts: {text}"""

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

    def click_button(self, cq: str, root_id: Union[str, None] = None):
        """Finds a button using the supplied component query and clicks it.

        Args:
            cq (str): The component query to find the button.
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        button = self._cq.wait_for_single_query_visible(cq, root_id)

        # Rather than call click, move mouse to button and click...
        self._logger.info("Clicking button with CQ '%s'", cq)

        self._action_chains.move_to_element(button)
        self._action_chains.click()
        self._action_chains.perform()

    def click_button_by_text(self, text: str, root_id: Union[str, None] = None):
        """Finds a visible, enabled button with the specified text and clicks it.

        Args:
            text (str): The text on the button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self.click_button(self._ENABLED_BUTTON_TEMPLATE.format(text=text), root_id)

    def check_button_enabled(self, text: str, root_id: Union[str, None] = None):
        """Checks that we can find an enabled button with the specified text.

        Args:
            text (str): The text on the button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self._cq.wait_for_single_query(self._ENABLED_BUTTON_TEMPLATE.format(text=text), root_id)

    def check_button_disabled(self, text: str, root_id: Union[str, None] = None):
        """Checks that we can find a disabled button with the specified text.

        Args:
            text (str): The text on the button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        self._cq.wait_for_single_query(self._DISABLED_BUTTON_TEMPLATE.format(text=text), root_id)

    def click_button_on_messagebox(self, text: str = 'OK'):
        """Clicks a button on a messagebox.

        The messagebox must be visible.

        Args:
            text (str, optional): The text of the button to click. Defaults to 'OK'.
        """
        self.click_button(self._MESSAGEBOX_BUTTON_TEMPLATE.format(text=text))

    def click_button_arrow(self, button_text: str, root_id: Union[str, None] = None):
        """Clicks the dropdown arrow of a split button to open its menu.
        
        Args:
            button_text (str): The text on the main button
            root_id (str, optional): The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        # Find the button element
        button_cq = f'button[text="{button_text}"]'
        button = self._cq.wait_for_single_query_visible(button_cq, root_id)

        self._logger.info("Clicking dropdown arrow for button with text '%s'", button_text)

        # Get the button's width and click on the right side where the arrow is
        button_width = button.size['width']
        arrow_offset = (button_width // 2) - 10

        # Move to the button and click on the arrow area
        self._action_chains.move_to_element_with_offset(button, arrow_offset, 0)
        self._action_chains.click()
        self._action_chains.perform()
