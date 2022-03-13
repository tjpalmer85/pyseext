
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.ComponentQuery = {
    /**
     * Returns an array of matched element dom objects from within the dom.
     *
     * This wraps Ext.ComponentQuery.query, so see there for more detail.
     * Each component has it's dom object returned however.
     * You should never need this from Ext code. This will likely be useful for automated testing.
     *
     * Only supports the passing in of a single root (so no filtering).
     *
     * @param {String} selector The selector string to filter returned elements.
     * @param {String} [rootId] The id of the dom element indicating the container within which to perform the query.
     *                          If omitted, all components within the document are included in the search.
     * @return {Object[]} The matched dom objects or an empty array if none found.
     */
    query: function(selector, rootId) {
        var components,
            results = [],
            root,
            len,
            i,
            component,
            el;

        // Get component for our root if specified
        if (rootId) {
            root = Ext.getCmp(rootId);
        }

        components = Ext.ComponentQuery.query(selector, root);
        len = components && components.length;

        if (len) {
            for (i = 0; i < len; i += 1) {
                component = components[i];

                if (component && component.getEl) {
                    el = component.getEl();

                    if (el) {
                        results.push(el.dom);
                    }
                }
            }
        }

        return results;
    }
};