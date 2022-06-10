
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.FieldHelper = {
    /**
     * Finds the specified field input element on the specified form.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns The DOM for the field's input element
     */
    findFieldInputElement: function(formCQ, name) {
        var field = this.__getField(formCQ, name);

        return field && field.inputEl.dom;
    },

    /**
     * Finds the specified field on the specified form and returns it's xtype.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns {String} The xtype of the field, if found.
     */
    getFieldXType: function(formCQ, name) {
        var field = this.__getField(formCQ, name);

        return field && field.xtype;
    },

    /**
     * Finds the specified field on the specified form and returns it's value.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns {Mixed} The value of the field, if found.
     */
    getFieldValue: function(formCQ, name) {
        var field = this.__getField(formCQ, name);

        return field && field.getValue();
    },

    /**
     * Finds the specified field and sets its value directly.
     *
     * Raises an error if the field was not found.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @param {Number} value The value of the field.
     */
    setFieldValue: function(formCQ, name, value) {
        this.__getField(formCQ, name, true).setValue(value);
    },

    /**
     * Determines whether the specified field is a remotely filtered combobox.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns {Boolean} True if the field was found, and is a remotely filtered combobox.
     *                    False otherwise.
     */
    isRemotelyFilteredComboBox: function(formCQ, name) {
        var field = this.__getField(formCQ, name),
            isRemotelyFilteredComboBox;

        isRemotelyFilteredComboBox = field instanceof globalThis.Ext.form.field.ComboBox &&
                                     field.queryMode === 'remote';

        return isRemotelyFilteredComboBox;
    },

    /**
     * Resets the load count on the specified combobox.
     *
     * Raises an error if the field was not found.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     */
    resetComboBoxStoreLoadCount: function(formCQ, name) {
        var field = this.__getField(formCQ, name, true);

        if (!field instanceof globalThis.Ext.form.field.ComboBox) {
            globalThis.Ext.Error.raise("Specified field is not a combobox!");
        }

        globalThis.PySeExt.StoreHelper.__resetStoreLoadCount(field.getStore());
    },

    /**
     * Waits for the store on the specified combobox to have loaded.
     *
     * Raises an error if the field was not found.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @param {Function} callback The callback to call when the store has loaded.
     */
    waitForComboBoxStoreLoaded: function(formCQ, name, callback) {
        var field = this.__getField(formCQ, name);

        if (!field instanceof globalThis.Ext.form.field.ComboBox) {
            globalThis.Ext.Error.raise("Specified field is not a combobox!");
        }

        globalThis.PySeExt.StoreHelper.__waitForStoreLoaded(field.getStore(), callback);
    },

    /**
     * Method to focus on a field on a form by (zero-based) index or name.
     *
     * Raises an error if the field was not found.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String|Integer} indexOrName The zero-based index or name of the field to focus.
     */
    focusField: function(formCQ, indexOrName) {
        var me = this;

        if (globalThis.Ext.isString(indexOrName)) {
            me.__getField(formCQ, indexOrName, true).focus();
        } else {
            me.__getFieldAtIndex(formCQ, indexOrName).focus();
        }
    },

    /**
     * Finds a field in a form panel.
     * Optionally raises an error if not found.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @param {Boolean} throwIfNotFound Indicates whether to raise an error if not found.
     *                                  If omitted then value is taken to be false.
     * @returns {Ext.form.field.Base} The field instance.
     */
    __getField: function(formCQ, name, throwIfNotFound) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().findField(name);
        } else if (throwIfNotFound) {
            globalThis.Ext.Error.raise("Form panel could not be found!");
        }

        if (!field && throwIfNotFound) {
            globalThis.Ext.Error.raise("Field could not be found!");
        }

        return field;
    },

    /**
     * Gets a field in a form panel by index.
     *
     * Raises an error if the index is outside of the bounds of the fields,
     * or is otherwise invalid.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {Number} index The index of the field.
     * @returns {Ext.form.field.Base} The field instance.
     */
     __getFieldAtIndex: function(formCQ, index) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().getFields().getAt(index);
        } else {
            globalThis.Ext.Error.raise("Form panel could not be found!");
        }

        if (!field) {
            globalThis.Ext.Error.raise("Field could not be found!");
        }

        return field;
    }

};