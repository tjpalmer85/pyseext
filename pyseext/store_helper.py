"""
Module that contains our StoreHelper class.
"""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pyseext.has_referenced_javascript import HasReferencedJavaScript

class StoreHelper(HasReferencedJavaScript):
    """A class to help with using stores, through Ext's interfaces.
    """

    # Class variables
    _RESET_STORE_LOAD_COUNT_TEMPLATE: str = "return globalThis.PySeExt.StoreHelper.resetStoreLoadCount('{store_holder_cq}')"
    """The script template to use to call the JavaScript method PySeExt.StoreHelper.resetStoreLoadCount"""

    _WAIT_FOR_STORE_LOADED_TEMPLATE: str = "return globalThis.PySeExt.StoreHelper.waitForStoreLoaded('{store_holder_cq}', callback)"
    """The script template to use to call the asynchronous JavaScript method PySeExt.StoreHelper.waitForStoreLoaded"""

    _RELOAD_STORE_TEMPLATE: str = "return globalThis.PySeExt.StoreHelper.reload('{store_holder_cq}')"
    """The script template to use to call the JavaScript method PySeExt.StoreHelper.reload"""

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        """The Logger instance for this class"""

        self._driver = driver
        """The WebDriver instance for this class"""

        # Initialise our base class
        super().__init__(driver, self._logger)

    def reset_store_load_count(self, store_holder_cq: str):
        """Resets the load count on the specified store, provided the store is not configured with autoLoad set to true.

        If set to auto load then this method does nothing.

        The load count on a store is incremented everytime a load occurs. It is not reset when the data is cleared.
        A store's isLoaded method returns true if the load count is greater than zero.

        Calling this method is useful to use before performing an action that will trigger a load, since you can then
        wait for the stores isLoaded method to return true.
        This is far more reliable than waiting for the load event, since it may have already been fired by the time the
        test gets that far.

        Args:
            store_holder_cq (str): The component query to use to find the store holder.
        """
        self._logger.debug("Resetting loadCount on store owned by '%s'", store_holder_cq)

        script = self._RESET_STORE_LOAD_COUNT_TEMPLATE.format(store_holder_cq=store_holder_cq)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def wait_for_store_loaded(self, store_holder_cq: str):
        """ Waits for the specified store to return true from its isLoaded method.

        Should generally be used after calling #resetStoreLoadCount and performing an
        action that triggers a store load.

        Args:
            store_holder_cq (str): The component query to use to find the store holder.
        """
        self._logger.debug("Waiting for store owned by '%s' to load", store_holder_cq)

        async_script = self.get_async_script_content(self._WAIT_FOR_STORE_LOADED_TEMPLATE).format(store_holder_cq=store_holder_cq)
        self.ensure_javascript_loaded()
        self._driver.execute_async_script(async_script)

        self._logger.debug("Store owned by '%s' loaded", store_holder_cq)

    def trigger_reload(self, store_holder_cq: str):
        """Triggers a reload on the specified store.

        Args:
            store_holder_cq (str): The component query to use to find the store holder.
        """
        script = self._RELOAD_STORE_TEMPLATE.format(store_holder_cq=store_holder_cq)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def trigger_reload_and_wait(self, store_holder_cq: str):
        """Triggers a load on the specified store and waits for it to complete.

        Basically resets the store load count, triggers a reload and then waits for the store to
        show as loaded.

        Args:
            store_holder_cq (str): The component query to use to find the store holder.
        """
        self.reset_store_load_count(store_holder_cq)
        self.trigger_reload(store_holder_cq)
        self.wait_for_store_loaded(store_holder_cq)

    # FIXME: Some method ideas:
    # .....:    - check_store_contains(self, store_holder_cq: str, data: list[dict], should_only_contain_specified_data: bool = False)= > bool
    # .....:        Method that checks that the store contains the specified data, and optionally only the specified data.
    # .....:        Can be used to check combobox data, say.
