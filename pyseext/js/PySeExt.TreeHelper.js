
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.TreeHelper = {
    /**
     * Determine whether the tree (any part of it) is currently loading.
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
     * Attempts to find a node in a single visible tree by text.
     * @private
     * @param  {String} treeSelector The selector to use to find the tree.
     * @param  {String} nodeText     The node text to find.
     * @return {Element} The element for the tree node.
     */
    __findNodeByText: function(treeSelector, nodeText) {
        var me = this;

        return me.__findNodeByData(treeSelector, { 'data.text': nodeText });
    },

    /**
     * Attempts to find a node in a single visible tree by data.
     * @private
     * @param  {String} treeSelector The selector to use to find the tree.
     * @param  {Object} nodeData     The node data to find.
     * @return {Element} The element for the tree node, or undefined if not found.
     */
    __findNodeByData: function(treeSelector, nodeData) {
        var me = this,
            treePanel = me.__getTree(treeSelector),
            rootNode;

        treePanels = globalThis.Ext.ComponentQuery.query(treeSelector);
        rootNode = treePanel.getRootNode();

        if (me.__isBranchLoading(rootNode)) {
            globalThis.Ext.raise("The tree is still loading. You must wait for loading to have finished before interacting with the tree.");
        }

        foundNode = rootNode.findChildBy.call(rootNode, function(node) {
            var isMatch = true,
                prop;

            if (node.isLoading()) {
                globalThis.Ext.raise({ msg: "Found a node that is loading, which was not expected,", node });
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

        debugger;
        // FIXME: How to get the element from the node?!
        return foundNode && foundNode.getEl();
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