
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.TreeHelper = {
    /**
     * Determines whether the tree (any part of it) is currently loading.
     *
     * You should call this before calling any tree interaction methods,
     * since we cannot pass things back in callbacks!
     *
     * @param {String} treeSelector The selector to use to find the tree.
     */
    isTreeLoading: function(treeSelector) {
        var me = this,
            treePanel = me.__getTree(treeSelector),
            rootNode = treePanel.getRootNode();

        return me.__isBranchLoading(rootNode);
    },

    /**
     * Finds a node, then the child HTML element that holds it's expander UI.
     *
     * @param {String} treeSelector The selector to use to find the tree.
     * @param {String} nodeTextOrData The node text or data to find.
     * @returns {HTMLElement} The HTML element for the node's expander.
     */
     getNodeExpander: function(treeSelector, nodeTextOrData) {
        return this.getNodeElement(treeSelector, nodeTextOrData, '.x-tree-expander');
    },

    /**
     * Finds a node, then the child HTML element that holds it's icon.
     *
     * @param {String} treeSelector The selector to use to find the tree.
     * @param {String} nodeTextOrData The node text or data to find.
     * @returns {HTMLElement} The HTML element for the node's icon.
     */
     getNodeIcon: function(treeSelector, nodeTextOrData) {
        return this.getNodeElement(treeSelector, nodeTextOrData, '.x-tree-icon');
    },

    /**
     * Finds a node, then the child HTML element that holds it's text element.
     *
     * @param {String} treeSelector The selector to use to find the tree.
     * @param {String} nodeTextOrData The node text or data to find.
     * @returns {HTMLElement} The HTML element for the node's text.
     */
     getNodeText: function(treeSelector, nodeTextOrData) {
        return this.getNodeElement(treeSelector, nodeTextOrData, '.x-tree-node-text');
    },

    /**
     * Finds a node, then a child element by CSS query.
     *
     * @param {String} treeSelector The selector to use to find the tree.
     * @param {String} nodeTextOrData The node text or data to find.
     * @param {String} cssQuery The CSS to query for in the found node row element.
     *                          Expander UI element = '.x-tree-expander'
     *                          Node icon = '.x-tree-icon'
     *                          Node text = '.x-tree-node-text'
     * @returns {HTMLElement} The HTML element for the node part.
     */
     getNodeElement: function(treeSelector, nodeTextOrData, cssQuery) {
        var me = this,
            nodeData = nodeTextOrData,
            nodeRowElement,
            children,
            element;

        if (Ext.isString(nodeData)) {
            nodeData = me.__getDataForText(nodeData);
        }

        nodeRowElement = me.__getNodeRowElementByData(treeSelector, nodeData);
        if (nodeRowElement) {
            children = Ext.get(nodeRowElement).query(cssQuery);
            if (children && children.length) {
                element = children[0];
            }
        }

        return element;
    },

    /**
     * Finds a node, a causes it and its children to reload.
     *
     * @param {String} treeSelector The selector to use to find the tree.
     * @param {String} nodeTextOrData The node text or data to find.
     */
     reloadNode: function(treeSelector, nodeTextOrData) {
        var me = this,
            nodeData = nodeTextOrData,
            node;

        if (Ext.isString(nodeData)) {
            nodeData = me.__getDataForText(nodeData);
        }

        node = me.__getNodeByData(treeSelector, nodeData);
        if (node) {
            node.getTreeStore().load({ node: node });
        }
    },

    /**
     * Determines if the specified node or any of its children are currently loading.
     * @private
     * @param  {Ext.data.NodeInterface} node The node to check.
     * @return {Boolean} true if the node or any of its children are currently loading.
     */
    __isBranchLoading: function(node) {
        var t = this,
            isBranchLoading = node.isLoading();

        if (!isBranchLoading) {
            node.cascadeBy(function(child) {
                isBranchLoading = child.isLoading();
                return !isBranchLoading;
            });
        }
        return isBranchLoading;
    },

    /**
     * Gets the data to use when searching for a node by text.
     * @private
     * @param {String} nodeText The text for the node.
     * @returns {Object} An object that allows the path of the node text in a node to be found.
     */
    __getDataForText: function(nodeText) {
        return { 'data.text': nodeText };
    },

    /**
     * Attempts to retrieve a node row element in a single visible tree by data.
     * @private
     * @param  {String} treeSelector The selector to use to find the tree.
     * @param  {Object} nodeData     The node data to find.
     * @return {Element} The element for the tree node, or undefined if not found.
     */
     __getNodeRowElementByData: function(treeSelector, nodeData) {
        var me = this,
            foundNode,
            treePanel,
            treeView,
            nodeRowElement;

        foundNode = me.__getNodeByData(treeSelector, nodeData);

        if (foundNode) {
            // We need to get the row element for the node
            treePanel = me.__getTree(treeSelector)
            treeView = treePanel.getView();
            nodeRowElement = treeView.getNode(foundNode);

            // This row element has children that we may be interested in, with CSS classes:
            //   - x-tree-expander
            //   - x-tree-icon
            //   - x-tree-node-text
            // Get them using: Ext.get(nodeRowElement).query('.x-tree-node-text')[0];
        }

        return nodeRowElement;
    },

    /**
     * Attempts to retrieve a node in a single visible tree by data.
     * @private
     * @param  {String} treeSelector    The selector to use to find the tree.
     * @param  {Object} nodeData        The node data to find.
     * @param  {Object} parentNode      The optional node to use as the root for finding the child node.
     *                                  If omitted to whole tree is searched.
     * @return {Ext.data.NodeInterface} The tree node, or undefined if not found.
     */
    __getNodeByData: function(treeSelector, nodeData, parentNode) {
        var me = this,
            treePanel = me.__getTree(treeSelector),
            rootNode = parentNode || treePanel.getRootNode(),
            foundNode;

        if (me.__isBranchLoading(rootNode)) {
            globalThis.Ext.raise("The tree is still loading. You must wait for loading to have finished before interacting with the tree.");
        }

        foundNode = rootNode.findChildBy.call(rootNode, function(node) {
            var isMatch = true,
                prop;

            if (node.isLoading()) {
                globalThis.Ext.raise({ msg: "Found a node that is loading, which was not expected.", node });
            } else {
                for (prop in nodeData) {
                    if (nodeData.hasOwnProperty(prop)) {
                        if (globalThis.PySeExt.Core.getObjectMember(node, prop) !== nodeData[prop]) {
                            isMatch = false;
                            break;
                        }
                    }
                }
            }

            return isMatch;
        }, undefined, true);

        return foundNode;
    },

    /**
     * Method to get a single tree panel using CQ.
     *
     * If more than one tree is matched then an error is raised.
     * If the tree is not found then an error is raised.
     *
     * @param {String} treeSelector The selector to use to find the tree.
     * @returns {Ext.tree.Panel} The tree panel that the selector matches.
     */
    __getTree(treeSelector) {
        var me = this,
            treePanels,
            treePanel;

        treePanels = globalThis.Ext.ComponentQuery.query(treeSelector);

        if (treePanels && treePanels.length) {
            if (treePanels.length > 1) {
                globalThis.Ext.raise("Tree selector found multiple trees. Refine it so that it targets a single tree!");
            }

            treePanel = treePanels[0];
        } else {
            globalThis.Ext.raise("Tree selector did not match anything!");
        }

        return treePanel;
    }
};