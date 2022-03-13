
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.FormHelper = {
    /**
     * Finds the specified field inoput element on the specified form.
     * @param {String} formCQ The CQ to get to the form panel.
     * @param {String} name The name of the field.
     * @returns
     */
    findFieldInputElement: function(formCQ, name) {
        var formPanel = Ext.ComponentQuery.query(formCQ),
            field;

        if (formPanel && formPanel.length) {
            formPanel = formPanel[0];
            field = formPanel.getForm().findField(name);
        }

        return field && field.inputEl.dom;
    }
};