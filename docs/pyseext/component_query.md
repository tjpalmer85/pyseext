Module pyseext.component_query
==============================
Module that contains our ComponentQuery class.

Classes
-------

`ComponentQuery(driver)`
:   A class to help with using Ext.ComponentQuery
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Class variables

    `ComponentQueryFoundExpectation`
    :   An expectation for checking that an Ext.ComponentQuery is found

    `QueryMatchedMultipleElementsException`
    :   Exception class thrown when expecting a single component query match and get multiple

    ### Methods

    `query(self, cq: str, root_id: Optional[str] = None) ‑> list[selenium.webdriver.remote.webelement.WebElement]`
    :   Executes a ComponentQuery and returns the result
        
        Args:
            cq (str): The query to execute
            root_id (str, optional):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        
        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if not found

    `wait_for_query(self, cq: str, root_id: Optional[str] = None, timeout: float = 10) ‑> list[selenium.webdriver.remote.webelement.WebElement]`
    :   Method that waits for the specified CQ to match something
        
        Args:
            cq (str): The query to execute
            root (str, optional):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)
        
        Returns:
            list[WebElement]: An array of DOM elements that match the query or an empty array if not found

    `wait_for_single_query(self, cq: str, root_id: Optional[str] = None, timeout: float = 10) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Method that waits for the specified CQ to match a single result.
        If there are multiple matches then an error is thrown.
        
        Args:
            cq (str): The query to execute
            root (str, optional):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)
        
        Returns:
            WebElement: The DOM element that matches the query

    `wait_for_single_query_visible(self, cq: str, root_id: Optional[str] = None, timeout: float = 10) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Method that waits for the specified CQ to match a single visible result.
        If there are multiple matches then an error is thrown.
        
        Args:
            cq (str): The query to execute
            root (str, optional):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
            timeout (float): Number of seconds before timing out (default 10)
        
        Returns:
            WebElement: The DOM element that matches the query