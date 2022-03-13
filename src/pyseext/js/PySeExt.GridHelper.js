
globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.GridHelper = {
    /**
     * Gets the element for a column header on the specified grid, by header text or dataIndex.
     * @param {String} gridSelector The CQ for the grid
     * @param {String} columnTextOrDataIndex The text or dataIndex of the column
     * @returns {Object} The DOM node for the column header
     */
    getColumnHeader: function(gridSelector, columnTextOrDataIndex) {
        var me = this,
            columnHeader = me.__findVisibleColumnHeader(gridSelector, columnTextOrDataIndex);

        return columnHeader && columnHeader.getEl().dom;
    },

    /**
     * Gets the element for a column header's trigger on the specified grid, by header text or dataIndex.
     * @param {String} gridSelector The CQ for the grid
     * @param {String} columnTextOrDataIndex The text or dataIndex of the column
     * @returns {Object} The DOM node for the column header's trigger
     */
     getColumnHeaderTrigger: function(gridSelector, columnTextOrDataIndex) {
        var me = this,
            columnHeader = me.__findVisibleColumnHeader(gridSelector, columnTextOrDataIndex),
            columnHeaderTrigger;

        if (columnHeader) {
            columnHeaderTrigger = columnHeader.getEl().down('.x-column-header-trigger', true);
        }

        return columnHeaderTrigger;
    },

    /**
     * Finds on a visible column header on a grid.
     * @private
     * @param  {String} gridSelector          The selector for the grid.
     * @param  {String} columnTextOrDataIndex The text or dataIndex of the column to find.
     * @return {Ext.Component}                The column header component
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