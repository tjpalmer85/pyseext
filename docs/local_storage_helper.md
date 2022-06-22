Module pyseext.local_storage_helper
===================================
Module that contains our LocalStorageHelper class.

Classes
-------

`LocalStorageHelper(driver: selenium.webdriver.remote.webdriver.WebDriver)`
:   A class to help with using local storage, through Ext's interfaces.
        
    
    Initialises an instance of this class
    
    Args:
        driver (WebDriver): The webdriver to use

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Methods

    `clear_value(self, key: str)`
    :   Clears a value in our persistent storage (implemented as local storage).
        
        Args:
            key (str): The key to clear.

    `get_stored_value(self, key: str) ‑> Any`
    :   Retrieves a value that has been saved in #storedData using #storeValue.
        
        Args:
            key (str): The key to use to retrieve the data.
        
        Returns:
            Any: The retrieved value or None if key does not exist.

    `store_value(self, key: str, value: Any)`
    :   Stores a value in our persistent storage (implemented as local storage).
        If a value exists for the key it is overwritten.
        
        Values can be retrieved using #getStoredValue.
        
        Supports strings, numbers, booleans, dates, objects and arrays.
        
        Args:
            key (str): The key to use when storing the value.
            value (Any): The value to store.