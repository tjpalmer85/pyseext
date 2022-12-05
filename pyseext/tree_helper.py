"""
Module that contains our TreeHelper class.
"""
import logging
import time
from typing import Union
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pyseext.has_referenced_javascript import HasReferencedJavaScript
from pyseext.core import Core

class TreeHelper(HasReferencedJavaScript):
    """A class to help with using trees, through Ext's interfaces."""

    # Class variables
    _IS_TREE_LOADING_TEMPLATE: str = "return globalThis.PySeExt.TreeHelper.isTreeLoading('{tree_cq}')"
    """The script template to use to call the JavaScript method PySeExt.TreeHelper.isTreeLoading
    Requires the inserts: {tree_cq}"""

    _GET_NODE_ELEMENT_TEMPLATE: str = "return globalThis.PySeExt.TreeHelper.getNodeElement('{tree_cq}', {node_text_or_data}, '{css_query}')"
    """The script template to use to call the JavaScript method PySeExt.TreeHelper.getNodeElement
    Requires the inserts: {tree_cq}, {node_text_or_data}, {css_query}"""

    _GET_NODE_ELEMENT_WITH_ROOT_TEMPLATE: str = "return globalThis.PySeExt.TreeHelper.getNodeElement('{tree_cq}', {node_text_or_data}, '{css_query}', {root_node_text_or_data})"
    """The script template to use to call the JavaScript method PySeExt.TreeHelper.getNodeElement including a root node to search from
    Requires the inserts: {tree_cq}, {node_text_or_data}, {css_query}, {root_node_text_or_data}"""

    _RELOAD_NODE_TEMPLATE: str = "return globalThis.PySeExt.TreeHelper.reloadNode('{tree_cq}', {node_text_or_data})"
    """The script template to use to call the JavaScript method PySeExt.TreeHelper.reloadNode
    Requires the inserts: {tree_cq}, {node_text_or_data}"""

    _RELOAD_NODE_WITH_ROOT_TEMPLATE: str = "return globalThis.PySeExt.TreeHelper.reloadNode('{tree_cq}', {node_text_or_data}, {root_node_text_or_data})"
    """The script template to use to call the JavaScript method PySeExt.TreeHelper.reloadNode including a root node to search from
    Requires the inserts: {tree_cq}, {node_text_or_data}, {root_node_text_or_data}"""

    _ICON_CSS_SELECTOR: str = ".x-tree-icon"
    """The CSS selector to use with get_node_element to find the node icon element.
    """

    _EXPANDER_CSS_SELECTOR: str = ".x-tree-expander"
    """The CSS selector to use with get_node_element to find the node expander element.
    """

    _NODE_TEXT_CSS_SELECTOR: str = ".x-tree-node-text"
    """The CSS selector to use with get_node_element to find the node text element.
    """

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (WebDriver): The webdriver to use
        """
        self._logger = logging.getLogger(__name__)
        """The Logger instance for this class instance"""

        self._driver = driver
        """The WebDriver instance for this class instance"""

        self._action_chains = ActionChains(driver)
        """The ActionChains instance for this class instance"""

        self._core = Core(driver)
        """The `Core` instance for this class instance"""

        # Initialise our base class
        super().__init__(driver, self._logger)

    def is_tree_loading(self, tree_cq: str):
        """Determine whether the tree (any part of it) is currently loading.

        You should call this before calling any tree interaction methods,
        since we cannot pass things back in callbacks!

        Args:
            tree_cq (str): The component query to use to find the tree.

        Returns:
            bool: True if the tree is loaded, False otherwise.
        """
        script = self._IS_TREE_LOADING_TEMPLATE.format(tree_cq=tree_cq)
        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def wait_until_tree_not_loading(self,
                                    tree_cq: str,
                                    timeout: float = 30,
                                    poll_frequecy: float = 0.2,
                                    recheck_time_if_false: float = 0.2):
        """Waits until the tree identified by the component query is not loading,
        or the timeout is hit

        Args:
            tree_cq (str): The component query for the tree.
            timeout (float, optional): The number of seconds to wait before erroring. Defaults to 30.
            poll_frequency (float, optional): Number of seconds to poll. Defaults to 0.2.
            recheck_time_if_false (float, optional): If we get a result such that no Ajax calls are in progress, this is the amount of time to wait to check again. Defaults to 0.2.
        """
        WebDriverWait(self._driver, timeout, poll_frequency = poll_frequecy).until(TreeHelper.TreeNotLoadingExpectation(tree_cq, recheck_time_if_false))

    def get_node_icon_element(self,
                              tree_cq: str,
                              node_text_or_data: Union[str, dict],
                              root_node_text_or_data: Union[str, dict, None] = None) -> WebElement:
        """Finds a node by text or data, then the child HTML element that holds it's icon.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.

        Returns:
            WebElement: The DOM element for the node icon.
        """
        return self.get_node_element(tree_cq, node_text_or_data, self._ICON_CSS_SELECTOR, root_node_text_or_data)

    def get_node_text_element(self,
                              tree_cq: str,
                              node_text_or_data: Union[str, dict],
                              root_node_text_or_data: Union[str, dict, None] = None) -> WebElement:
        """Finds a node by text or data, then the child HTML element that holds it's text.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.

        Returns:
            WebElement: The DOM element for the node text.
        """
        return self.get_node_element(tree_cq, node_text_or_data, self._NODE_TEXT_CSS_SELECTOR, root_node_text_or_data)

    def get_node_expander_element(self,
                                  tree_cq: str,
                                  node_text_or_data: Union[str, dict],
                                  root_node_text_or_data: Union[str, dict, None] = None) -> WebElement:
        """Finds a node by text or data, then the child HTML element that holds it's expander UI element.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.

        Returns:
            WebElement: The DOM element for the node's expander.
        """
        return self.get_node_element(tree_cq, node_text_or_data, self._EXPANDER_CSS_SELECTOR, root_node_text_or_data)

    def get_node_element(self,
                         tree_cq: str,
                         node_text_or_data: Union[str, dict],
                         css_query: str,
                         root_node_text_or_data: Union[str, dict, None] = None) -> WebElement:
        """Finds a node by text or data, then a child element by CSS query.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            css_query (str): The CSS to query for in the found node row element.
                             Some expected ones:
                                Expander UI element = '.x-tree-expander'
                                Node icon = '.x-tree-icon'
                                Node text = '.x-tree-node-text'
                             If need those you'd use one of the other methods though.
                             This is in case need to click on another part of the node's row.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.

        Returns:
            WebElement: The DOM element for the node's expander.
        """
        self.wait_until_tree_not_loading(tree_cq)

        if isinstance(node_text_or_data, str):
            node_text_or_data = f"'{node_text_or_data}'"

        if isinstance(root_node_text_or_data, str):
            root_node_text_or_data = f"'{root_node_text_or_data}'"

        if root_node_text_or_data:
            script = self._GET_NODE_ELEMENT_WITH_ROOT_TEMPLATE.format(tree_cq=tree_cq, node_text_or_data=node_text_or_data, css_query=css_query, root_node_text_or_data=root_node_text_or_data)
        else:
            script = self._GET_NODE_ELEMENT_TEMPLATE.format(tree_cq=tree_cq, node_text_or_data=node_text_or_data, css_query=css_query)

        self.ensure_javascript_loaded()
        return self._driver.execute_script(script)

    def open_node_context_menu(self,
                               tree_cq: str,
                               node_text_or_data: Union[str, dict],
                               root_node_text_or_data: Union[str, dict, None] = None):
        """Finds a node's text element by text or data, then right clicks on it.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.
        """
        node = self.get_node_icon_element(tree_cq, node_text_or_data, root_node_text_or_data)

        if node:
            if root_node_text_or_data:
                self._logger.info("Opening context menu on node '%s' (under root '%s') on tree with CQ '%s'", node_text_or_data, root_node_text_or_data, tree_cq)
            else:
                self._logger.info("Opening context menu on node '%s' on tree with CQ '%s'", node_text_or_data, tree_cq)

            self._action_chains.move_to_element(node)
            self._action_chains.context_click(node)
            self._action_chains.perform()
        else:
            raise TreeHelper.NodeNotFoundException(tree_cq, node_text_or_data, root_node_text_or_data)

    def click_node_expander(self,
                            tree_cq: str,
                            node_text_or_data: Union[str, dict],
                            root_node_text_or_data: Union[str, dict, None] = None):
        """Finds a node's expander element by text or data, then clicks on it.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.
        """
        node = self.get_node_expander_element(tree_cq, node_text_or_data, root_node_text_or_data)

        if node:
            if root_node_text_or_data:
                self._logger.info("Clicking expander on node '%s' (under root '%s') on tree with CQ '%s'", node_text_or_data, root_node_text_or_data, tree_cq)
            else:
                self._logger.info("Clicking expander on node '%s' on tree with CQ '%s'", node_text_or_data, tree_cq)

            self._action_chains.move_to_element(node)
            self._action_chains.click(node)
            self._action_chains.perform()
        else:
            raise TreeHelper.NodeNotFoundException(tree_cq, node_text_or_data, root_node_text_or_data)

    def click_node_element(self,
                           tree_cq: str,
                           node_text_or_data: Union[str, dict],
                           css_query: str,
                           root_node_text_or_data: Union[str, dict, None] = None):
        """Finds a node by text or data, then a child element by CSS query, then clicks on it.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            css_query (str): The CSS to query for in the found node row element.
                             Some expected ones:
                                Expander UI element = '.x-tree-expander'
                                Node icon = '.x-tree-icon'
                                Node text = '.x-tree-node-text'
                             If need those you'd use one of the other methods though.
                             This is in case need to click on another part of the node's row.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.
        """
        node = self.get_node_element(tree_cq, node_text_or_data, css_query, root_node_text_or_data)

        if node:
            if root_node_text_or_data:
                self._logger.info("Clicking on node '%s' (under root '%s'), with CSS query '%s' on tree with CQ '%s'", node_text_or_data, root_node_text_or_data, css_query, tree_cq)
            else:
                self._logger.info("Clicking on node '%s' with CSS query '%s' on tree with CQ '%s'", node_text_or_data, css_query, tree_cq)

            self._action_chains.move_to_element(node)
            self._action_chains.click(node)
            self._action_chains.perform()
        else:
            raise TreeHelper.NodeNotFoundException(tree_cq, node_text_or_data, root_node_text_or_data)

    def wait_for_tree_node(self,
                           tree_cq: str,
                           node_text_or_data: Union[str, dict],
                           parent_node_text_or_data: Union[str, dict],
                           timeout: float = 60) -> WebElement:
        """Method that waits until a tree node is available, refreshing the parent until it's
        found or the timeout is hit.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            parent_node_text_or_data (Union[str, dict]): The node text or data to use to find the nodes parent,
                                                         for refreshing purposes.
            timeout (int, optional): The number of seconds to wait for the row before erroring. Defaults to 60.

        Returns:
            WebElement: The DOM element for the node icon.
        """
        WebDriverWait(self._driver, timeout).until(TreeHelper.NodeFoundExpectation(tree_cq, node_text_or_data, parent_node_text_or_data))
        return self.get_node_icon_element(tree_cq, node_text_or_data)

    def reload_node(self,
                    tree_cq: str,
                    node_text_or_data: Union[str, dict],
                    root_node_text_or_data: Union[str, dict, None] = None):
        """Finds a node by text or data, and triggers a reload on it, and its children.

        Args:
            tree_cq (str): The component query to use to find the tree.
            node_text_or_data (Union[str, dict]): The node text or data to find.
            root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                 Can be an immediate parent, or higher up in the tree.
        """
        self.wait_until_tree_not_loading(tree_cq)

        if isinstance(node_text_or_data, str):
            node_text_or_data = f"'{node_text_or_data}'"

        if isinstance(root_node_text_or_data, str):
            root_node_text_or_data = f"'{root_node_text_or_data}'"

        if root_node_text_or_data:
            script = self._RELOAD_NODE_WITH_ROOT_TEMPLATE.format(tree_cq=tree_cq, node_text_or_data=node_text_or_data, root_node_text_or_data=root_node_text_or_data)
        else:
            script = self._RELOAD_NODE_TEMPLATE.format(tree_cq=tree_cq, node_text_or_data=node_text_or_data)

        if root_node_text_or_data:
            self._logger.info("Reloading node '%s' (under root '%s') on tree with CQ '%s'", node_text_or_data, root_node_text_or_data, tree_cq)
        else:
            self._logger.info("Reloading node '%s' on tree with CQ '%s'", node_text_or_data, tree_cq)

        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    class NodeNotFoundException(Exception):
        """Exception class thrown when we failed to find the specified node"""

        def __init__(self,
                     tree_cq: str,
                     node_text_or_data: Union[str, dict],
                     root_node_text_or_data: Union[str, dict, None] = None,
                     css_query: Union[str, None] = None):
            """Initialises an instance of this exception

            Args:
                tree_cq (str): The CQ used to find the tree
                node_text_or_data (Union[str, dict]): The node text or data that we were looking for
                root_node_text_or_data (Union[str, dict], optional): The text or data indicating the root node under which to search for the node.
                                                                    Can be an immediate parent, or higher up in the tree.
                css_query (str, optional): The CSS that was queryed for in the node that we were looking for.
            """
            if root_node_text_or_data:
                if css_query:
                    self.message = "Failed to find node with data (or text) '{node_text_or_data}' (under root '{root_node_text_or_data}') with CSS query '{css_query}' on tree with CQ '{tree_cq}'."
                else:
                    self.message = "Failed to find node with data (or text) '{node_text_or_data}' (under root '{root_node_text_or_data}') on tree with CQ '{tree_cq}'."
            else:
                if css_query:
                    self.message = "Failed to find node with data (or text) '{node_text_or_data}' with CSS query '{css_query}' on tree with CQ '{tree_cq}'."
                else:
                    self.message = "Failed to find node with data (or text) '{node_text_or_data}' on tree with CQ '{tree_cq}'."

            self._tree_cq = tree_cq
            self._node_text_or_data = node_text_or_data
            self._root_node_text_or_data = root_node_text_or_data
            self._css_query = css_query

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception"""

            if self._root_node_text_or_data:
                return self.message.format(node_text_or_data=self._node_text_or_data, root_node_text_or_data=self._root_node_text_or_data, css_query=self._css_query, tree_cq=self._tree_cq)
            else:
                return self.message.format(node_text_or_data=self._node_text_or_data, css_query=self._css_query, tree_cq=self._tree_cq)

    class TreeNotLoadingExpectation:
        """ An expectation for checking that a tree is not loading."""

        def __init__(self, tree_cq: str, recheck_time_if_false: Union[float, None] = None):
            """Initialises an instance of this class.

            Args:
                tree_cq (str): The CQ used to find the tree
                recheck_time_if_false (float, optional): If we get a value of false (so there is not a call in progress),
                                                         this is the amount of time to wait to check again. Defaults to None.
            """
            self._tree_cq = tree_cq
            self._recheck_time_if_false = recheck_time_if_false

        def __call__(self, driver):
            """Method that determines whether the tree is loading."""
            tree_helper = TreeHelper(driver)

            is_tree_loading = tree_helper.is_tree_loading(self._tree_cq)

            if not is_tree_loading and self._recheck_time_if_false:
                time.sleep(self._recheck_time_if_false)
                is_tree_loading = tree_helper.is_tree_loading(self._tree_cq)

            return not is_tree_loading

    class NodeFoundExpectation:
        """ An expectation for checking that a node has been found"""

        def __init__(self,
                     tree_cq: str,
                     node_text_or_data: Union[str, dict],
                     parent_node_text_or_data: Union[str, dict]):
            """Initialises an instance of this class.

            Args:
                tree_cq (str): The component query to use to find the tree.
                node_text_or_data (Union[str, dict]): The node text or data to find.
                parent_node_text_or_data (Union[str, dict]): The node text or data to use to find the nodes parent,
                                                            for refreshing purposes.
            """
            self._tree_cq = tree_cq
            self._node_text_or_data = node_text_or_data
            self._parent_node_text_or_data = parent_node_text_or_data

        def __call__(self, driver):
            """Method that determines whether a node was found.

            If the node is not found the parent tree node is refreshed and the load waited for.
            """
            tree_helper = TreeHelper(driver)

            node = tree_helper.get_node_icon_element(self._tree_cq, self._node_text_or_data, self._parent_node_text_or_data)
            if node:
                return True

            # Trigger a reload of the parent
            tree_helper.reload_node(self._tree_cq, self._parent_node_text_or_data)
            return False
