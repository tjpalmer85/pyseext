
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.GridHelper = {
    /**
     *
     * @param {String} gridSelector The CQ for the grid
     * @param {String} columnTextOrDataIndex The text or dataIndex of the column
     */
    getColumnHeader: function(gridSelector, columnTextOrDataIndex) {
        var me = this;

        columnHeader = me.__findVisibleColumnHeader(gridSelector, columnTextOrDataIndex);
        return columnHeader && columnHeader.getEl().dom;
    },

    /**
     * Finds on a visible column header on a grid.
     * @private
     * @param  {String}                 gridSelector          The selector for the grid.
     * @param  {String}                 columnTextOrDataIndex The text or dataIndex of the column to find.
     * @return {void}
     */
    __findVisibleColumnHeader: function(gridSelector, columnTextOrDataIndex) {
        var me = this,
            grid,
            visibleColumns,
            i,
            visibleColumn,
            columnHeader;

        components = Ext.ComponentQuery.query(gridSelector);
        if (components && components.length) {
            grid = components[0];
            visibleColumns = grid.headerCt.gridVisibleColumns

            // Find column header
            for (i = 0; i < visibleColumns.length; i += 1) {
                visibleColumn = visibleColumns[i];

                if ((visibleColumn.dataIndex === columnTextOrDataIndex) ||
                    (visibleColumn.text === columnTextOrDataIndex)) {

                    columnHeader = visibleColumn;
                    break;
                }
            }
        }

        return columnHeader;
    }
};