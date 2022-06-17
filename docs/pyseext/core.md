Module pyseext.core
===================
Module that contains our Core class.

Classes
-------

`Core(driver)`
:   A class to help with core testing functionality.
        
    
    Initialises an instance of this class.
    
    Args:
        driver (selenium.webdriver): The webdriver to use.

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Class variables

    `ArgumentException`
    :   Exception class thrown when we have an argument exception.

    `IsDomReadyExpectation`
    :   An expectation for checking Ext.isDomReady

    `IsNoAjaxCallInProgressExpectation`
    :   An expectation for checking whether there is an Ajax call in progress.

    ### Methods

    `is_ajax_request_in_progress(self) ‑> bool`
    :   Indicates whether there is currently an Ajax request in progress.
        
        Returns:
            bool: True if there is a request in progress, False otherwise.

    `try_get_object_member(self, obj: Union[dict, Any], member: str, default: Any = None) ‑> Any`
    :   Attempts to get the member from an object, but if object itself is not a dictionary
        then it is returned.
        
        Useful when a value in a dictionary we're processing might be an object or not, and we
        want to process them in the same way.
        
        Args:
            object (Union[dict, Any]): The object from which to get the member's value.
            member (str): The key for the member we're after.
            default (Any, optional): The default to return if not found. Defaults to None.
        
        Returns:
            Any: The value of the member, or the default if not found.

    `wait_for_dom_ready(self, timeout: float = 30)`
    :   Method that waits until Ext indicates that the DOM is ready.
        Calls Ext.isDomReady.
        
        Will throw a TimeOutException if the value is not true within the specified timeout period.
        
        Args:
            timeout (float): Number of seconds before timing out (default 30)

    `wait_for_no_ajax_requests_in_progress(self, timeout: float = 30, poll_frequecy: float = 0.2, recheck_time_if_false: float = 0.2)`
    :   Method that waits until there are no Ajax requests in progress.
        
        Will throw a TimeOutException if the value is not true within the specified timeout period.
        
        Args:
            timeout (float, optional): Number of seconds before timing out. Defaults to 30.
            poll_frequency (float, optional): Number of seconds to poll. Defaults to 0.2.
            recheck_time_if_false (float, optional): If we get a result such that no Ajax calls are in progress, this is the amount of time to wait to check again. Defaults to 0.2.