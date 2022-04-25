
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
            columnHeader = me.__findColumnHeader(gridSelector, columnTextOrDataIndex);

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
            columnHeader = me.__findColumnHeader(gridSelector, columnTextOrDataIndex),
            columnHeaderTrigger;

        if (columnHeader) {
            columnHeaderTrigger = columnHeader.getEl().down('.x-column-header-trigger', true);
        }

        return columnHeaderTrigger;
    },

    /**
     * Finds on a column header on a grid.
     * @private
     * @param  {String} gridSelector          The selector for the grid.
     * @param  {String} columnTextOrDataIndex The text or dataIndex of the column to find.
     * @return {Ext.Component}                The column header component
     */
     __findColumnHeader: function(gridSelector, columnTextOrDataIndex) {
        var me = this,
            grid,
            dataColumns,
            i,
            dataColumn,
            columnHeader;

        components = Ext.ComponentQuery.query(gridSelector);
        if (components && components.length) {
            grid = components[0];

            dataColumns = grid.headerCt.gridDataColumns

            // Find column header
            for (i = 0; i < dataColumns.length; i += 1) {
                dataColumn = dataColumns[i];

                if ((dataColumn.dataIndex === columnTextOrDataIndex) ||
                    (dataColumn.text === columnTextOrDataIndex)) {

                    columnHeader = dataColumn;
                    break;
                }
            }
        }

        return columnHeader;
    }    
};