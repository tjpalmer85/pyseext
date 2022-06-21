"""
Module that contains our LocalStorageHelper class.
"""
import logging
from typing import Any
from pyseext.has_referenced_javascript import HasReferencedJavaScript

from selenium.webdriver.remote.webdriver import WebDriver

class LocalStorageHelper(HasReferencedJavaScript):
    """A class to help with using local storage, through Ext's interfaces.
    """

    # Class variables
    _STORE_VALUE_TEMPLATE: str = "return globalThis.PySeExt.LocalStorageHelper.storeValue('{key}', {value})"
    """The script template to use to call the JavaScript method PySeExt.LocalStorageHelper.storeValue
    Requires the inserts: {key}, {value}"""

    _CLEAR_VALUE_TEMPLATE: str = "return globalThis.PySeExt.LocalStorageHelper.clearValue('{key}')"
    """The script template to use to call the JavaScript method PySeExt.LocalStorageHelper.clearValue
    Requires the inserts: {key}"""

    _GET_STORED_VALUE_TEMPLATE: str = "return globalThis.PySeExt.LocalStorageHelper.getStoredValue('{key}')"
    """The script template to use to call the JavaScript method PySeExt.LocalStorageHelper.getStoredValue
    Requires the inserts: {key}"""

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (WebDriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        """The Logger instance for this class instance"""

        self._driver = driver
        """The WebDriver instance for this class instance"""

        # Initialise our base class
        super().__init__(driver, self._logger)

    def store_value(self, key: str, value: Any):
        """Stores a value in our persistent storage (implemented as local storage).
        If a value exists for the key it is overwritten.

        Values can be retrieved using #getStoredValue.

        Supports strings, numbers, booleans, dates, objects and arrays.

        Args:
            key (str): The key to use when storing the value.
            value (Any): The value to store.
        """
        self._logger.debug("Storing value '%s' under key '%s'", value, key)

        script = self._STORE_VALUE_TEMPLATE.format(key=key, value=value)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def clear_value(self, key: str):
        """Clears a value in our persistent storage (implemented as local storage).

        Args:
            key (str): The key to clear.
        """
        self._logger.debug("Clearing value with key '%s'", key)

        script = self._CLEAR_VALUE_TEMPLATE.format(key=key)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def get_stored_value(self, key: str) -> Any:
        """Retrieves a value that has been saved in #storedData using #storeValue.

        Args:
            key (str): The key to use to retrieve the data.

        Returns:
            Any: The retrieved value or None if key does not exist.
        """
        script = self._CLEAR_VALUE_TEMPLATE.format(key=key)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)
