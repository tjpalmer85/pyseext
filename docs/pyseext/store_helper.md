Module pyseext.store_helper
===========================
Module that contains our StoreHelper class.

Classes
-------

`StoreHelper(driver)`
:   A class to help with using stores, through Ext's interfaces.
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Methods

    `reset_store_load_count(self, store_holder_cq: str)`
    :   Resets the load count on the specified store, provided the store is not configured with autoLoad set to true.
        
        If set to auto load then this method does nothing.
        
        The load count on a store is incremented everytime a load occurs. It is not reset when the data is cleared.
        A store's isLoaded method returns true if the load count is greater than zero.
        
        Calling this method is useful to use before performing an action that will trigger a load, since you can then
        wait for the stores isLoaded method to return true.
        This is far more reliable than waiting for the load event, since it may have already been fired by the time the
        test gets that far.
        
        Args:
            store_holder_cq (str): The component query to use to find the store holder.

    `trigger_reload(self, store_holder_cq: str)`
    :   Triggers a reload on the specified store.
        
        Args:
            store_holder_cq (str): The component query to use to find the store holder.

    `trigger_reload_and_wait(self, store_holder_cq: str)`
    :   Triggers a load on the specified store and waits for it to complete.
        
        Basically resets the store load count, triggers a reload and then waits for the store to
        show as loaded.
        
        Args:
            store_holder_cq (str): The component query to use to find the store holder.

    `wait_for_store_loaded(self, store_holder_cq: str)`
    :   Waits for the specified store to return true from its isLoaded method.
        
        Should generally be used after calling #resetStoreLoadCount and performing an
        action that triggers a store load.
        
        Args:
            store_holder_cq (str): The component query to use to find the store holder.