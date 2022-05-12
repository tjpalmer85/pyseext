from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class LocalStorageHelper(HasReferencedJavaScript):
    """A class to help with using local storage, through Ext's interfaces.
    """

    # Class variables
    _STORE_VALUE_TEMPLATE = "return globalThis.PySeExt.LocalStorageHelper.storeValue('{key}', {value})"
    _CLEAR_VALUE_TEMPLATE = "return globalThis.PySeExt.LocalStorageHelper.clearValue('{key}')"
    _GET_STORED_VALUE_TEMPLATE = "return globalThis.PySeExt.LocalStorageHelper.getStoredValue('{key}')"

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._driver = driver

        # Initialise our base class
        super().__init__(driver)

    def store_value(self, key, value):
        """Stores a value in our persistent storage (implemented as local storage).
        If a value exists for the key it is overwritten.
        
        Values can be retrieved using #getStoredValue.
        
        Supports strings, numbers, booleans, dates, objects and arrays.

        Args:
            key (string): The key to use when storing the value.
            value (object): The value to store.
        """
        script = self._STORE_VALUE_TEMPLATE.format(key=key, value=value)
        return self._driver.execute_script(script)        

    def clear_value(self, key):
        """Clears a value in our persistent storage (implemented as local storage).

        Args:
            key (string): The key to clear.
        """
        script = self._CLEAR_VALUE_TEMPLATE.format(key=key)
        return self._driver.execute_script(script)    

    def get_stored_value(self, key):
        """Retrieves a value that has been saved in #storedData using #storeValue.

        Args:
            key (string): The key to use to retrieve the data.

        Returns:
            The retrieved value or None if key does not exist.
        """
        script = self._CLEAR_VALUE_TEMPLATE.format(key=key)
        return self._driver.execute_script(script)        