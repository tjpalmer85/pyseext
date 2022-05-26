
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
     * Clears the current selection.
     *
     * Useful if want to quickly refresh a grid without having to process all the events.
     * This will only work if the grid supports deselection.
     *
     * @param  {String}   gridSelector The selector for the grid.
     * @return {void}
     */
    clearSelection: function(gridSelector) {
        var grids = globalThis.Ext.ComponentQuery.query(gridSelector);

        if (grids && grids.length) {
            grids[0].getSelectionModel().deselectAll();
        }
    },

    /**
     * Gets the row element with the specified data or index in the grid.
     * The row is scrolled into view ready for clicking by the caller.
     *
     * The grid must be visible.
     *
     * @param  {String}        gridSelector The selector for the grid.
     * @param  {Object|Number} rowData      The index of or an object containing the row data for the record to be found.
     * @return {Element} The element for the found row.
     */
    getRow: function(gridSelector, rowData) {
        var row,
            grids = globalThis.Ext.ComponentQuery.query(gridSelector),
            grid,
            store,
            foundIndex,
            prop;

        if (grids && grids.length) {
            grid = grids[0];
            store = grid.getStore();

            if (typeof(rowData) === 'number') {
                foundIndex = rowData;
            } else {
                foundIndex = store.findBy(function(record, id) {
                    var hasRecordBeenFound = true;

                    for (prop in rowData) {
                        if (rowData.hasOwnProperty(prop)) {
                            if (record.get(prop) !== rowData[prop]) {
                                hasRecordBeenFound = false;
                                break;
                            }
                        }
                    }

                    return hasRecordBeenFound;
                });

                if (foundIndex !== -1) {
                    row = grid.getView().getRow(foundIndex);
                }
            }
        }

        return row;
    },

    /**
     * Trims the specified row data to contain just the required fields.
     *
     * Useful when we have stored some row data, and want to select it again later, but some of the ids of times
     * may be different.
     *
     * @param  {Object} rowData        The row data to trim.
     * @param  {Array}  requiredFields An array of string indicating the fields that are required from the row data.
     * @return {Object} A copy of the row data object, with only the required fields included.
     */
    __trimRowData: function(rowData, requiredFields) {
        var trimmedRowData = {},
            i;

        for (i = 0; i < requiredFields.length; i += 1) {
            trimmedRowData[requiredFields[i]] = rowData[requiredFields[i]];
        }

        return trimmedRowData;
    },

    /**
     * Retrieves the selection of the specified grid.
     * @private
     * @param  {String}         gridSelector       The selector for the grid.
     * @param  {Function}       callback           The function to call when the done.
     * @param  {Array}          callback.selection The grids current selection.
     * @return {void}
     */
    __getSelection: function(gridSelector, callback) {
        var grids = globalThis.Ext.ComponentQuery.query(gridSelector);

        if (grids && grids.length) {
            globalThis.Ext.callback(callback, this, [grids[0].getSelectionModel().getSelection()]);
        }
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