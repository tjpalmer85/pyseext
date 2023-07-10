globalThis.None = null;

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
    isTreeLoading: function (treeSelector) {
        var me = this,
            treePanel = me.__getTree(treeSelector),
            rootNode = treePanel.getRootNode();

        return me.__isBranchLoading(rootNode);
    },

    /**
     * Finds a node, then a child element by CSS query.
     *
     * @param {String} treeSelector          The selector to use to find the tree.
     * @param {String} nodeTextOrData        The node text or data to find.
     * @param {String} cssQuery              The CSS to query for in the found node row element.
     *                                       Expander UI element = '.x-tree-expander'
     *                                       Node icon = '.x-tree-icon'
     *                                       Node text = '.x-tree-node-text'
     * @param  {Object} parentNodeTextOrData The optional text or data identifying the node to use as the root for finding the child node.
     *                                       If omitted to whole tree is searched.
     * @returns {HTMLElement}                The HTML element for the node part.
     */
    getNodeElement: function (treeSelector, nodeTextOrData, cssQuery, parentNodeTextOrData) {
        var me = this,
            nodeData = nodeTextOrData,
            parentNodeData = parentNodeTextOrData,
            nodeRowElement,
            children,
            element;

        if (Ext.isString(nodeData)) {
            nodeData = me.__getDataForText(nodeData);
        }

        if (Ext.isString(parentNodeData)) {
            parentNodeData = me.__getDataForText(parentNodeData);
        }

        nodeRowElement = me.__getNodeRowElementByData(treeSelector, nodeData, parentNodeData);
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
     * @param {String} treeSelector          The selector to use to find the tree.
     * @param {String} nodeTextOrData        The node text or data to find.
     * @param  {Object} parentNodeTextOrData The optional text or data identifying the node to use as the root for finding the child node.
     *                                       If omitted to whole tree is searched.
     */
    reloadNode: function (treeSelector, nodeTextOrData, parentNodeTextOrData) {
        var me = this,
            nodeData = nodeTextOrData,
            parentNodeData = parentNodeTextOrData,
            parentNode,
            node;

        if (Ext.isString(nodeData)) {
            nodeData = me.__getDataForText(nodeData);
        }

        if (Ext.isString(parentNodeData)) {
            parentNodeData = me.__getDataForText(parentNodeData);
        }

        if (parentNodeData) {
            parentNode = me.__getNodeByData(treeSelector, parentNodeData);

            if (!parentNode) {
                globalThis.Ext.raise("Could not find requested parent node!");
            }
        }

        node = me.__getNodeByData(treeSelector, nodeData, parentNode);
        if (node) {
            node.getTreeStore().load({ node: node });
        }
    },

    /**
     * Determines if the specified node or any of its children are currently loading.
     * @private
     * @param  {Ext.data.NodeInterface} node The node to check.
     * @return {Boolean}                     true if the node or any of its children are currently loading.
     */
    __isBranchLoading: function (node) {
        var t = this,
            isBranchLoading = node.isLoading();

        if (!isBranchLoading) {
            node.cascadeBy(function (child) {
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
     * @returns {Object}        An object that allows the path of the node text in a node to be found.
     */
    __getDataForText: function (nodeText) {
        return { 'data.text': nodeText };
    },

    /**
     * Attempts to retrieve a node row element in a single visible tree by data.
     * @private
     * @param  {String} treeSelector   The selector to use to find the tree.
     * @param  {Object} nodeData       The node data to find.
     * @param  {Object} parentNodeData The optional data identifying the node to use as the root for finding the child node.
     *                                 If omitted to whole tree is searched.
     * @return {Element}               The element for the tree node, or undefined if not found.
     */
    __getNodeRowElementByData: function (treeSelector, nodeData, parentNodeData) {
        var me = this,
            foundNode,
            treePanel,
            treeView,
            nodeRowElement,
            parentNode;

        if (parentNodeData) {
            parentNode = me.__getNodeByData(treeSelector, parentNodeData);

            if (!parentNode) {
                globalThis.Ext.raise("Could not find requested parent node!");
            }
        }

        foundNode = me.__getNodeByData(treeSelector, nodeData, parentNode);

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
    __getNodeByData: function (treeSelector, nodeData, parentNode) {
        var me = this,
            treePanel = me.__getTree(treeSelector),
            rootNode = treePanel.getRootNode(),
            foundNode;

        if (me.__isBranchLoading(rootNode)) {
            globalThis.Ext.raise("The tree is still loading. You must wait for loading to have finished before interacting with the tree.");
        }

        // If we have a parent node then use that rather than root
        foundNode = (parentNode || rootNode).findChildBy(function(node) {
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
     * @returns {Ext.tree.Panel}    The tree panel that the selector matches.
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