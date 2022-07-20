"""
Module that contains our InputHelper class.
"""
import logging
import random
from typing import Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class InputHelper:
    """A class to help with user input."""

    TYPING_SLEEP_MINIMUM: float = 0.0001
    """The minimum amount of time in seconds to wait between key presses when typing. Defaults to 0.0001 seconds."""

    TYPING_SLEEP_MAXIMUM: float = 0.002
    """The maximum amount of time in seconds to wait between key presses when typing. Defaults to 0.002 seconds."""

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (WebDriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        """The Logger instance for this class instance"""

        self._driver = driver
        """The WebDriver instance for this class instance"""

        self._action_chains = ActionChains(driver)
        """The ActionChains instance for this class instance"""

    def type_into_element(self, element: WebElement, text: str, delay: Union[float, None] = None, tab_off: Union[bool, None] = False):
        """Types into an input element in a realistic manner.

        Args:
            element (WebElement): The element to type into.
            text (str): The text to type.
            delay (float, optional): The number of seconds to delay after typing. Defaults to None.
            tab_off (bool, optional): Indicates whether to tab off the field after typing, and delay. Defaults to False.
        """
        # Ensure text really is a string
        text = str(text)

        # Clear the element first, in case has something in it
        element.clear()

        # First move to and click on element to give it focus
        self._action_chains.move_to_element(element)
        self._action_chains.click()
        self._action_chains.perform()

        # Now type each character
        self.type(text)

        if delay:
            self._action_chains.pause(delay)
            self._action_chains.perform()

        if tab_off:
            self.type_tab()

    def type(self, text: str):
        """Types into the currently focused element in a realistic manner, unless our webdriver is remote, then just sends the complete string.

        Args:
            text (str): The text to type.
        """

        # If we are remote, then typing a character at a time involves a roundtrip for every character.
        # This is not ideal, since slows down the test massively.
        if not self._driver._is_remote: # pylint: disable=protected-access
            for character in text:
                self._action_chains.send_keys(character)
                self._action_chains.pause(random.uniform(self.TYPING_SLEEP_MINIMUM, self.TYPING_SLEEP_MAXIMUM))
                self._action_chains.perform()
        else:
            self._action_chains.send_keys(text)
            self._action_chains.perform()


    def type_tab(self):
        """Type a tab character into the currently focused element."""
        self._action_chains.send_keys(Keys.TAB)

        if not self._driver._is_remote: # pylint: disable=protected-access
            self._action_chains.pause(random.uniform(self.TYPING_SLEEP_MINIMUM, self.TYPING_SLEEP_MAXIMUM))

        self._action_chains.perform()
