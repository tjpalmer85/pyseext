
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.LocalStorageHelper = {
    /**
     * Stores a value in our persistent storage (implemented as local storage).
     * If a value exists for the key it is overwritten.
     *
     * Values can be retrieved using #getStoredValue.
     *
     * Supports strings, numbers, booleans, dates, objects and arrays.
     *
     * @param  {String} key   The key to use when storing the value.
     * @param  {Mixed}  value The value to store.
     * @return {void}
     */
    storeValue: function(key, value) {
        var localStorage = Ext.create('Ext.util.LocalStorage', { id: 'PySeExt' }),
            valueType = typeof(value);

        // Also store a value indicating its type
        localStorage.setItem(key + '_TYPE', valueType);

        if (valueType === 'object') {
            localStorage.setItem(key, Ext.JSON.encode(value));
        } else {
            localStorage.setItem(key, value);
        }
    },

    /**
     * Clears a value in our persistent storage (implemented as local storage).
     *
     * @param  {String} key   The key to clear.
     * @return {void}
     */
    clearValue: function(key) {
        var localStorage = Ext.create('Ext.util.LocalStorage', { id: 'PySeExt' });

        localStorage.removeItem(key + '_TYPE');
        localStorage.removeItem(key);
    },

    /**
     * Retrieves a value that has been saved in #storedData using #storeValue.
     *
     * @param  {String} key The key to use to retrieve the data.
     * @return {Mixed}      The retrieved value or undefined if key does not exist.
     */
    getStoredValue: function(key) {
        var localStorage = Ext.create('Ext.util.LocalStorage', { id: 'PySeExt' }),
            valueType = localStorage.getItem(key + '_TYPE'),
            value = localStorage.getItem(key);

        if (valueType === 'object' && typeof(value) === 'string') {
            value = Ext.JSON.decode(value);
        } else if (valueType === 'number' && typeof(value) === 'string') {
            value = parseFloat(value);
        }

        // FIXME: Cast to other supported types...

        return value;
    }
};