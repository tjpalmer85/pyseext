Module pyseext.has_referenced_javascript
========================================
Module that contains our HasReferencedJavaScript class.

Classes
-------

`HasReferencedJavaScript(driver: selenium.webdriver.remote.webdriver.WebDriver, logger: logging.Logger)`
:   Base class to be used by our test classes that have JavaScript that they need to load
        
    
    Initialises an instance of this class
    
    Args:
        driver (WebDriver): The webdriver to use
        logger (logging.Logger): The logger to use

    ### Descendants

    * pyseext.component_query.ComponentQuery
    * pyseext.core.Core
    * pyseext.field_helper.FieldHelper
    * pyseext.grid_helper.GridHelper
    * pyseext.local_storage_helper.LocalStorageHelper
    * pyseext.observable_helper.ObservableHelper
    * pyseext.store_helper.StoreHelper
    * pyseext.tree_helper.TreeHelper

    ### Class variables

    `JavaScriptLoadedExpectation`
    :   An expectation for checking that our JavaScript has loaded

    ### Methods

    `ensure_javascript_loaded(self)`
    :   Ensures that our JavaScript has been loaded into the DOM.
        
        If it hasn't then it is loaded.

    `get_async_script_content(self, script: str, callback_parameter_name: str = 'callback') ‑> str`
    :   Builds some async script content, to call some JavaScript that takes a callback function.
        
        Note, we cannot get a value back from the JavaScript (that I know of), but we can get notified of completion.
        
        Args:
            script (str): The script containing the asynchronous JavaScript being called.
            callback_parameter_name (str, optional): The name of the callback parmeter to use for the script.
                                                     Defaults to 'callback'.
        
        Returns:
            str: The script, prefixed with some code that captures the callback passes from the web driver.