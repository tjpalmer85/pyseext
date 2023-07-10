globalThis.None = null;

globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.ComponentQuery = {
    /**
     * Returns an array of matched element dom objects from within the dom.
     *
     * This wraps Ext.ComponentQuery.query, so see there for more detail.
     * Each component has it's dom object returned however.
     * You should never need this from Ext code. This will likely be useful for automated testing.
     *
     * Only supports the passing in of a single root (so no filtering), and an optional CSS selector,
     * to return a sub-element in the found component.
     *
     * @param {String} selector      The selector string to filter returned elements.
     * @param {String} [rootId]      The id of the dom element indicating the container within which to perform the query.
     *                               If omitted, all components within the document are included in the search.
     * @param {String} [cssSelector] An optional CSS selector that can be used to get child elements of a found component, e.g. a trigger on a field.
     * @return {Object[]}            The matched dom objects or an empty array if none found.
     */
    query: function(selector, rootId, cssSelector) {
        var components,
            results = [],
            root,
            len,
            i,
            component,
            el,
            j;

        // Get component for our root if specified
        if (rootId) {
            root = globalThis.Ext.getCmp(rootId);

            if (!root) {
                globalThis.Ext.Error.raise("Failed to find root component with id '" + rootId + "'! Are you passing in WebElement.get_attribute('id'), because that's what you need?");
            }
        }

        components = globalThis.Ext.ComponentQuery.query(selector, root);
        len = components && components.length;

        if (len) {
            for (i = 0; i < len; i += 1) {
                component = components[i];

                if (component && component.getEl) {
                    el = component.getEl();

                    if (el) {
                        if (cssSelector) {
                            el = el.query(cssSelector);

                            if (el && el.length) {
                                for (j = 0; j < el.length; j += 1) {
                                    if (el[j]) {
                                        // This will already be a DOM element,
                                        // since Element.query defaults to that.
                                        results.push(el[j]);
                                    }
                                }
                            }
                        } else {
                            results.push(el.dom);
                        }
                    }
                }
            }
        }

        return results;
    },

    /**
     * Determines whether all components for the specified CQ are an instance of the specified class name.
     *
     * Note, will return True if the components are a subclass of the type too.
     * @param {String} className The name of the class that we want to test for.
     * @param {String} selector The selector string to query for.
     * @param {String} rootId The id of the dom element indicating the container within which to perform the query.
     *                        If omitted, all components within the document are included in the search.
     * @return {Boolean} True if all components are an instance of the specified class, False if they are not, and
     *                   undefined if no components are found.
     */
    isComponentInstanceOf: function(className, selector, rootId) {
        var cls = Ext.ClassManager.get(className),
            components,
            root,
            len,
            i,
            component,
            el,
            isInstance;

        if (!cls) {
            globalThis.Ext.Error.raise("A class with the name '" + className + "' is not defined!");
        }

        // Get component for our root if specified
        if (rootId) {
            root = globalThis.Ext.getCmp(rootId);
        }

        components = globalThis.Ext.ComponentQuery.query(selector, root);
        len = components && components.length;

        if (len) {
            for (i = 0; i < len; i += 1) {
                component = components[i];

                if (component) {
                    isInstance = component instanceof cls;

                    if (!isInstance) {
                        break;
                    }
                }
            }
        }

        return isInstance;
    }
};