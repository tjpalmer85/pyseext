
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.Core = {
    /**
     * Retrieves the value of a member from an object.
     *
     * The member can contain periods, to access child objects.
     *
     * @param  {Object} object The object from which to retrieve the value.
     * @param  {String} member A string identifying the member value to retrieve. Can contain periods to access child objects.
     * @return {Object} The value of the object member, or undefined if it or any part of the path was not found.
     */
    getObjectMember: function(object, member) {
        var me = this,
            members = member.split('.'),
            value = object[members[0]];

        if (value && (members.length > 1)) {
            members.shift();
            value = me.getObjectMember(value, members.join('.'));
        }

        return value;
    },

    /**
     * Indicates whether there is currently an Ajax request in progress.
     * @return {Boolean} True if there is a request in progress, false otherwise.
     */
    isAjaxRequestInProgress: function() {
        return globalThis.Ext.Ajax.isLoading();
    }
};