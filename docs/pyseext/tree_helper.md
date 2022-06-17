Module pyseext.tree_helper
==========================
Module that contains our TreeHelper class.

Classes
-------

`TreeHelper(driver)`
:   A class to help with using trees, through Ext's interfaces.
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Class variables

    `NodeFoundExpectation`
    :   An expectation for checking that a node has been found

    `NodeNotFoundException`
    :   Exception class thrown when we failed to find the specified node

    `TreeNotLoadingExpectation`
    :   An expectation for checking that a tree is not loading.

    ### Methods

    `get_node_element(self, tree_cq: str, node_data: dict, css_query: str) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Finds a node by data, then a child element by CSS query.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_data (dict): The node data to find.
            css_query (str): The CSS to query for in the found node row element.
                             Some expected ones:
                                Expander UI element = '.x-tree-expander'
                                Node icon = '.x-tree-icon'
                                Node text = '.x-tree-node-text'
                             If need those you'd use one of the other methods though.
                             This is in case need to click on another part of the node's row.
        
        Returns:
            WebElement: The DOM element for the node's expander.

    `get_node_expander_element(self, tree_cq: str, node_text_or_data: Union[str, dict]) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Finds a node by text or data, then the child HTML element that holds it's expander UI element.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
        
        Returns:
            WebElement: The DOM element for the node's expander.

    `get_node_icon_element(self, tree_cq: str, node_text_or_data: Union[str, dict]) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Finds a node by text or data, then the child HTML element that holds it's icon.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
        
        Returns:
            WebElement: The DOM element for the node icon.

    `get_node_text_element(self, tree_cq: str, node_text_or_data: Union[str, dict]) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Finds a node by text or data, then the child HTML element that holds it's text.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
        
        Returns:
            WebElement: The DOM element for the node text.

    `is_tree_loading(self, tree_cq: str)`
    :   Determine whether the tree (any part of it) is currently loading.
        
        You should call this before calling any tree interaction methods,
        since we cannot pass things back in callbacks!
        
        Args:
            tree_cq (str): The component query to use to find the tree.
        
        Returns:
            bool: True if the tree is loaded, False otherwise.

    `open_node_context_menu(self, tree_cq: str, node_text_or_data: Union[str, dict])`
    :   Finds a node's text element by text or data, then right clicks on it.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.

    `reload_node(self, tree_cq: str, node_text_or_data: Union[str, dict])`
    :   Finds a node by text or data, and triggers a reload on it, and its children.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.

    `wait_for_tree_node(self, tree_cq: str, node_text_or_data: Union[str, dict], parent_node_text_or_data: Union[str, dict], timeout: float = 60) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Method that waits until a tree node is available, refreshing the parent until it's
        found or the timeout is hit.
        
        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            parent_node_text_or_data (Union[str, dict]): The node text or data to use to find the nodes parent,
                                                         for refreshing purposes.
            timeout (int, optional): The number of seconds to wait for the row before erroring. Defaults to 60.
        
        Returns:
            WebElement: The DOM element for the node icon.

    `wait_until_tree_not_loading(self, tree_cq: str, timeout: float = 30)`
    :   Waits until the tree identified by the component query is not loading,
        or the timeout is hit
        
        Args:
            tree_cq (str): The component query for the tree.
            timeout (int, optional): The number of seconds to wait before erroring. Defaults to 30.