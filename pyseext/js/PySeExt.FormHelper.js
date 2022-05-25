
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.FormHelper = {
    /**
     * Finds the specified field input element on the specified form.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns The DOM for the field's input element
     */
    findFieldInputElement: function(formCQ, name) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().findField(name);
        }

        return field && field.inputEl.dom;
    },

    /**
     * Finds the specified field on the specified form and returns it's xtype.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns {String} The xtype of the field, if found.
     */    
    getFieldXType: function(formCQ, name) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().findField(name);
        }

        return field && field.xtype;
    },

    /**
     * Finds the specified checkbox field and sets its value.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @param {Boolean} checked The checked state of the field.
     */
     setCheckboxValue: function(formCQ, name, checked) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().findField(name);

            if (field && field.isCheckbox) {
                field.setValue(checked);
            } else {
                Ext.Error.raise("Field could not be found or was not a checkbox!");
            }
        }
    },

    /**
     * Finds the specified field and sets its value directly.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @param {Number} value The value of the field.
     */
     setFieldNumericValue: function(formCQ, name, value) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().findField(name);

            if (field) {
                field.setValue(value);
            } else {
                Ext.Error.raise("Field could not be found!");
            }
        }
    }    
};