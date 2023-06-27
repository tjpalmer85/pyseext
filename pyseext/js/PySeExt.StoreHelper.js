
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.StoreHelper = {
    /**
     * Resets the load count on the specified store, provided the store is not configured with autoLoad set to true.
     * If set to auto load then this method does nothing.
     *
     * The load count on a store is incremented everytime a load occurs. It is not reset when the data is cleared.
     * A store's isLoaded method returns true if the load count is greater than zero.
     *
     * Calling this method is useful to use before performing an action that will trigger a load, since you can then
     * wait for the stores isLoaded method to return true.
     * This is far more reliable than waiting for the load event, since it may have already been fired by the time the
     * test gets that far.
     *
     * @param  {String} storeHolderCQ The component query to use to find the store holder.
     */
    resetStoreLoadCount: function(storeHolderCQ) {
        var store = globalThis.PySeExt.StoreHelper.__getStoreFromStoreHolder(storeHolderCQ);

        this.__resetStoreLoadCount(store);
    },

    /**
     * Resets the load count on the specified store, provided the store is not configured with autoLoad set to true.
     * If set to auto load then this method does nothing.
     *
     * The load count on a store is incremented everytime a load occurs. It is not reset when the data is cleared.
     * A store's isLoaded method returns true if the load count is greater than zero.
     *
     * @param  {Ext.data.Store} store The store to reset the load count on.
     */
    __resetStoreLoadCount: function(store) {
        if (!store.getAutoLoad()) {
            store.loadCount = 0;
        }
    },

    /**
     * Waits for the specified store to return true from its isLoaded method.
     *
     * Should generally be used after calling #resetStoreLoadCount and performing an
     * action that triggers a store load.
     *
     * @param  {String}   storeHolderCQ The component query to use to find the store holder.
     * @param  {Function} callback      The function to call when done.
     */
    waitForStoreLoaded: function(storeHolderCQ, callback) {
        var store = globalThis.PySeExt.StoreHelper.__getStoreFromStoreHolder(storeHolderCQ);

        globalThis.PySeExt.StoreHelper.__waitForStoreLoaded(store, callback);
    },

    /**
     * Waits for the specified store to return true from its isLoaded method.
     *
     * Should generally be used after calling #resetStoreLoadCount and performing an
     * action that triggers a store load.
     *
     * @param  {Ext.data.AbstractStore} store    The store to wait to be showing as loaded.
     * @param  {Function}               callback The function to call when done.
     */
    __waitForStoreLoaded: function(store, callback) {
        if (store.isLoaded()) {
            globalThis.Ext.callback(callback);
        } else {
            // Call ourselves
            globalThis.Ext.Function.defer(arguments.callee, 10, this, arguments);
        }
    },

    /**
     * Triggers a reload on the specified store.
     *
     * @param  {String} storeHolderCQ The component query to use to find the store holder.
     */
    reload: function(storeHolderCQ) {
        globalThis.PySeExt.StoreHelper.__getStoreFromStoreHolder(storeHolderCQ).reload();
    },

    /**
     * Method that checks that the store contains the specified data, and optionally only the specified data.
     *
     * Can be used to check combobox data, say.
     *
     * @param {String}   storeHolderCQ                  The component query to use to find the store holder.
     * @param {Object[]} data                           An array of JSON objects containing the data to check for.
     * @param {Boolean}  shouldOnlyContainSpecifiedData Indicates whether the store should only contain the passed in data.
     */
    checkStoreContains: function(storeHolderCQ, data, shouldOnlyContainSpecifiedData) {
        var store = globalThis.PySeExt.StoreHelper.__getStoreFromStoreHolder(storeHolderCQ),
            storeCount,
            dataLength,
            i,
            foundIndex,
            dataItem;

        storeCount = store.getCount();
        dataLength = data && data.length || 0;

        if (shouldOnlyContainSpecifiedData) {
            // Can check array lengths, to test a negative case of this.
            // Might be nice to do something better in future, so can give better feedback,
            // but this'll do for now.
            if (storeCount !== dataLength) {
                globalThis.Ext.raise('Store contains ' + storeCount + ' records, but was expecting ' + dataLength + '.');
            }
        }

        for (i = 0; i < dataLength; i += 1) {
            dataItem = data[i];

            foundIndex = store.findBy(function(record, id) {
                var hasRecordBeenFound = true;

                for (prop in dataItem) {
                    if (dataItem.hasOwnProperty(prop)) {
                        if (record.get(prop) !== dataItem[prop]) {
                            hasRecordBeenFound = false;
                            break;
                        }
                    }
                }

                return hasRecordBeenFound;
            });

            if (foundIndex === -1) {
                globalThis.Ext.raise('Expected store to contain item ' + globalThis.Ext.JSON.encode(dataItem) + ', but it was not found.');
            }
        }
    },

    /**
     * Attempts to retrieve the store from a store holder described by a component query.
     *
     * The component query must resolve to a single component.
     * @private
     * @param  {String} storeHolderCQ The component query to use to find the store holder.
     * @return {Ext.data.Store} The found store, or undefined if not found.
     */
    __getStoreFromStoreHolder: function(storeHolderCQ) {
        var t = this,
            storeHolders = globalThis.Ext.ComponentQuery.query(storeHolderCQ),
            storeHolder,
            store;

        if (storeHolders && storeHolders.length) {
            if (storeHolders.length > 1) {
                globalThis.Ext.raise('Store holder CQ matched multiple components: ' + storeHolderCQ);
            } else {
                storeHolder = storeHolders[0];

                if (storeHolder.getStore) {
                    store = storeHolder.getStore();

                    if (!store) {
                        globalThis.Ext.raise('Store holder CQ has a store which is undefined or null: ' + storeHolderCQ);
                    }
                } else {
                    globalThis.Ext.raise('Store holder CQ did not describe a StoreHolder instance: ' + storeHolderCQ);
                }
            }
        } else {
            globalThis.Ext.raise('Failed to find a store holder described by CQ: ' + storeHolderCQ);
        }

        return store;
    }
};