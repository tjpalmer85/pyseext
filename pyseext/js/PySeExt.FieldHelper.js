
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
     * Selects a value on a combobox field by finding a record with the specified data.
     *
     * Ensures that the select event is fired if the record is found and selected.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @param {Object} data The data to find in the combobox store and select.
     * @returns {Boolean} Indicates whether a record was found and selected.
     */
    selectComboBoxValue: function(formCQ, name, data) {
        var me = this,
            field = me.__getField(formCQ, name, true),
            store,
            index,
            record;

        if (field instanceof globalThis.Ext.form.field.ComboBox) {
            store = field.getStore();

            if (store.isLoaded()) {
                index = store.getData().findIndexBy(function(record) {
                    var prop,
                        doAllMembersMatch = true;

                    for (prop in data) {
                        if (data.hasOwnProperty(prop)) {
                            if (data[prop] !== record.get(prop)) {
                                doAllMembersMatch = false;
                                break;
                            }
                        }
                    }

                    return doAllMembersMatch;
                });

                if (index === -1) {
                    // Record was not found
                    return false;
                } else {
                    record = store.getAt(index);

                    field.select(record);
                    field.fireEvent('select', field, record);

                    return true;
                }
            } else {
                globalThis.Ext.Error.raise("The combobox store is not loaded!");
            }
        } else {
            globalThis.Ext.Error.raise("Field is not a combobox!");
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