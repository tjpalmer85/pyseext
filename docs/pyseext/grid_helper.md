Module pyseext.grid_helper
==========================
Module that contains our GridHelper class.

Classes
-------

`GridHelper(driver)`
:   A class to help with interacting with Ext grid panels
        
    
    Initialises an instance of this class
    
    Args:
        driver (selenium.webdriver): The webdriver to use

    ### Ancestors (in MRO)

    * pyseext.has_referenced_javascript.HasReferencedJavaScript

    ### Class variables

    `ColumnNotFoundException`
    :   Exception class thrown when we failed to find the specified column

    `GRID_CQ: str`
    :

    `RowFoundExpectation`
    :   An expectation for checking that a row has been found

    `RowNotFoundException`
    :   Exception class thrown when we failed to find the specified row

    ### Methods

    `check_columns_are_hidden(self, grid_cq: str, column_texts_or_data_indexes: list[str]) ‑> list[selenium.webdriver.remote.webelement.WebElement]`
    :   Checks that the specified columns are all hidden on the specified grid.
        Throws a ColumnNotFoundException if the column does not exist.
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_texts_or_data_indexes (list[str]): An array containing the header text or dataIndex of the grid columns to check
        
        Returns:
            An array of columns that are not hidden, if any.

    `check_columns_are_visible(self, grid_cq: str, column_text_or_data_indexes: list[str]) ‑> list[selenium.webdriver.remote.webelement.WebElement]`
    :   Checks that the specified columns are all visible on the specified grid.
        Throws a ColumnNotFoundException if the column does not exist.
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_indexes (list[str]): An array containing the header text or dataIndex of the grid columns to check
        
        Returns:
            An array of columns that are not visible, if any.

    `clear_selection(self, grid_cq: str)`
    :   Clears the current selection.
        
        Useful if want to quickly refresh a grid without having to process all the events.
        This will only work if the grid supports deselection.
        
        Args:
            grid_cq (str): The component query for the grid

    `click_column_header(self, grid_cq: str, column_text_or_data_index: str)`
    :   Clicks on the specified column header.
        The column must be visible.
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column

    `click_column_header_trigger(self, grid_cq: str, column_text_or_data_index: str)`
    :   Clicks on the specified column header's trigger
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column

    `click_row(self, grid_cq: str, row_data: Union[int, dict])`
    :   Clicks the row with the specified data or index in the grid.
        
        The grid must be visible.
        
        Args:
            grid_cq (str): The component query for the grid
            row_data (Union[int, dict]): The row data or index for the record to be found and clicked.

    `get_column_header(self, grid_cq: str, column_text_or_data_index: str) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Gets the element for the specified column header
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column
        
        Returns:
            WebElement: The DOM element for the column header

    `get_column_header_trigger(self, grid_cq: str, column_text_or_data_index: str) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Gets the element for the specified column header's trigger
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column
        
        Returns:
            WebElement: The DOM element for the column header trigger.

    `get_row(self, grid_cq: str, row_data: Union[int, dict], should_throw_exception: bool = True) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Gets the element for the row with the specified data or index in the grid.
        
        The grid must be visible.
        
        Args:
            grid_cq (str): The component query for the grid
            row_data (Union[int, dict]): The row data or index for the record to be found.
            should_throw_exception (bool): Indicates whether this method should throw an exception
                                           if the row is not found. Defaults to True.
        
        Returns:
            WebElement: The DOM element for the row or None if not found (and not thrown)

    `is_column_hidden(self, grid_cq: str, column_text_or_data_index: str) ‑> bool`
    :   Determines whether the specified column is hidden.
        Throws a ColumnNotFoundException if the column does not exist.
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column
        
        Returns:
            True if the column is hidden, False otherwise.

    `is_column_visible(self, grid_cq: str, column_text_or_data_index: str) ‑> bool`
    :   Determines whether the specified column is visible,
        Throws a ColumnNotFoundException if the column does not exist.
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column
        
        Returns:
            True if the column is visible, False otherwise.

    `wait_for_row(self, grid_cq: str, row_data: Union[int, dict], timeout: float = 60) ‑> selenium.webdriver.remote.webelement.WebElement`
    :   Waits for the specified row to appear in the grid, reloading the store until
        it is found, or until the timeout is hit.
        
        Args:
            grid_cq (str): The component query for the grid.
            row_data (Union[int, dict]): The row data or index of the record we are waiting for.
            timeout (int, optional): The number of seconds to wait for the row before erroring. Defaults to 60.
        
        Returns:
            WebElement: The DOM element for the row

    `wait_to_click_row(self, grid_cq: str, row_data: Union[int, dict], timeout: float = 60)`
    :   Waits for the specified row to appear in the grid, reloading the store until
        it is found, or until the timeout is hit.
        Once we have found the row it is clicked.
        
        Args:
            grid_cq (str): The component query for the grid.
            row_data (Union[int, dict]): The row data or index of the record we are waiting for.
            timeout (int, optional): The number of seconds to wait for the row before erroring. Defaults to 60.