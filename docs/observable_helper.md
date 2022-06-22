Module pyseext.observable_helper
================================
Module that contains our ObservableHelper class.

Classes
-------

`ObservableHelper(driver: selenium.webdriver.remote.webdriver.WebDriver)`
:   A class to help with observable objects in Ext.
        
    
    Initialises an instance of this class.
    
    Args:
        driver (WebDriver): The webdriver to use.

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Class variables

    `WaitForEventException`
    :   Exception class thrown when waiting for event returned an error.

    ### Methods

    `wait_for_event(self, component_cq: str, event_name: str, timeout: float = 10, member_accessor: Optional[str] = None)`
    :   Method to find an observable using a component query, optionally access a member on it (to get an owned observable),
        and then wait for an event with the specified name.
        
        Returns when the event has been caught, or throws if the timeout was reached or the observable could not be found or resolve to a single object.
        
        Args:
            component_cq (str): The component query to find the observable object, or the owner of the observable member.
            event_name (str): The name of the event to wait for.
            timeout (float, optional): The maximum amount of time to wait for the event, in seconds. Defaults to 10.
            member_accessor (str, optional): The name of the member to access on the component to find the observable to watch. Defaults to None.