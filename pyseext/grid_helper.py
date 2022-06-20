"""
Module that contains our GridHelper class.
"""
import logging
from typing import Union

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pyseext.has_referenced_javascript import HasReferencedJavaScript
from pyseext.component_query import ComponentQuery
from pyseext.store_helper import StoreHelper

class GridHelper(HasReferencedJavaScript):
    """A class to help with interacting with Ext grid panels
    """

    # Public class properties
    GRID_CQ: str = "gridpanel"

    # Private class variables
    _GET_COLUMN_HEADER_TEMPLATE: str = "return globalThis.PySeExt.GridHelper.getColumnHeader('{grid_cq}', '{column_text_or_data_index}')"
    _GET_COLUMN_HEADER_TRIGGER_TEMPLATE: str = "return globalThis.PySeExt.GridHelper.getColumnHeaderTrigger('{grid_cq}', '{column_text_or_data_index}')"
    _CLEAR_SELECTION_TEMPLATE: str = "return globalThis.PySeExt.GridHelper.clearSelection('{grid_cq}')"
    _GET_ROW_TEMPLATE: str = "return globalThis.PySeExt.GridHelper.getRow('{grid_cq}', {row_data})"

    def __init__(self, driver: WebDriver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """

        # Instance variables
        self._logger = logging.getLogger(__name__)
        self._driver = driver
        self._cq = ComponentQuery(driver)
        self._action_chains = ActionChains(driver)

        # Initialise our base class
        super().__init__(driver, self._logger)

    def get_column_header(self, grid_cq: str, column_text_or_data_index: str) -> WebElement:
        """Gets the element for the specified column header

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column

        Returns:
            WebElement: The DOM element for the column header
        """

        # Check grid can be found and is visible
        self._cq.wait_for_single_query_visible(grid_cq)

        script = self._GET_COLUMN_HEADER_TEMPLATE.format(grid_cq=grid_cq, column_text_or_data_index=column_text_or_data_index)
        self.ensure_javascript_loaded()
        column_header = self._driver.execute_script(script)

        if column_header:
            return column_header

        raise GridHelper.ColumnNotFoundException(grid_cq, column_text_or_data_index)

    def is_column_visible(self, grid_cq: str, column_text_or_data_index: str) -> bool:
        """Determines whether the specified column is visible,
        Throws a ColumnNotFoundException if the column does not exist.

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column

        Returns:
            True if the column is visible, False otherwise.
        """
        return self.get_column_header(grid_cq, column_text_or_data_index).is_displayed()

    def is_column_hidden(self, grid_cq: str, column_text_or_data_index: str) -> bool:
        """Determines whether the specified column is hidden.
        Throws a ColumnNotFoundException if the column does not exist.

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column

        Returns:
            True if the column is hidden, False otherwise.
        """
        return not self.get_column_header(grid_cq, column_text_or_data_index).is_displayed()

    def check_columns_are_visible(self, grid_cq: str, column_text_or_data_indexes: list[str]) -> list[WebElement]:
        """Checks that the specified columns are all visible on the specified grid.
        Throws a ColumnNotFoundException if the column does not exist.

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_indexes (list[str]): An array containing the header text or dataIndex of the grid columns to check

        Returns:
            An array of columns that are not visible, if any.
        """
        columns_not_visible = []

        for column_text_or_data_index in column_text_or_data_indexes:
            is_visible = self.is_column_visible(grid_cq, column_text_or_data_index)
            if not is_visible:
                columns_not_visible.append(column_text_or_data_index)

        return columns_not_visible

    def check_columns_are_hidden(self, grid_cq: str, column_texts_or_data_indexes: list[str]) -> list[WebElement]:
        """Checks that the specified columns are all hidden on the specified grid.
        Throws a ColumnNotFoundException if the column does not exist.

        Args:
            grid_cq (str): The component query for the owning grid
            column_texts_or_data_indexes (list[str]): An array containing the header text or dataIndex of the grid columns to check

        Returns:
            An array of columns that are not hidden, if any.
        """
        column_not_hidden = []

        for column_text_or_data_index in column_texts_or_data_indexes:
            is_hidden = self.is_column_hidden(grid_cq, column_text_or_data_index)
            if not is_hidden:
                column_not_hidden.append(column_text_or_data_index)

        return column_not_hidden

    def click_column_header(self, grid_cq: str, column_text_or_data_index: str):
        """Clicks on the specified column header.
        The column must be visible.

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column
        """
        column_header = self.get_column_header(grid_cq, column_text_or_data_index)

        self._logger.info("Clicking column header '%s' on grid with CQ '%s'", column_text_or_data_index, grid_cq)

        self._action_chains.move_to_element(column_header)
        self._action_chains.click()
        self._action_chains.perform()

    def get_column_header_trigger(self, grid_cq: str, column_text_or_data_index: str) -> WebElement:
        """Gets the element for the specified column header's trigger

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column

        Returns:
            WebElement: The DOM element for the column header trigger.
        """

        # Check grid can be found and is visible
        self._cq.wait_for_single_query_visible(grid_cq)

        script = self._GET_COLUMN_HEADER_TRIGGER_TEMPLATE.format(grid_cq=grid_cq, column_text_or_data_index=column_text_or_data_index)
        self.ensure_javascript_loaded()
        column_header_trigger = self._driver.execute_script(script)

        if column_header_trigger:
            return column_header_trigger

        raise GridHelper.ColumnNotFoundException(grid_cq, column_text_or_data_index)

    def click_column_header_trigger(self, grid_cq: str, column_text_or_data_index: str):
        """Clicks on the specified column header's trigger

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_data_index (str): The header text or dataIndex of the grid column
        """
        # We need to move to the header before the trigger becomes interactable
        column_header = self.get_column_header(grid_cq, column_text_or_data_index)
        self._action_chains.move_to_element(column_header).perform()

        column_header_trigger = self.get_column_header_trigger(grid_cq, column_text_or_data_index)

        self._logger.info("Clicking column header trigger '%s' on grid with CQ '%s'", column_text_or_data_index, grid_cq)

        self._action_chains.move_to_element(column_header_trigger)
        self._action_chains.click()
        self._action_chains.perform()

    def clear_selection(self, grid_cq: str):
        """ Clears the current selection.

        Useful if want to quickly refresh a grid without having to process all the events.
        This will only work if the grid supports deselection.

        Args:
            grid_cq (str): The component query for the grid
        """
        # Check grid can be found and is visible
        self._cq.wait_for_single_query_visible(grid_cq)

        self._logger.info("Clearing selection on grid with CQ '%s'", grid_cq)

        script = self._CLEAR_SELECTION_TEMPLATE.format(grid_cq=grid_cq)
        self.ensure_javascript_loaded()
        self._driver.execute_script(script)

    def get_row(self, grid_cq: str, row_data: Union[int, dict], should_throw_exception: bool = True) -> WebElement:
        """ Gets the element for the row with the specified data or index in the grid.

        The grid must be visible.

        Args:
            grid_cq (str): The component query for the grid
            row_data (Union[int, dict]): The row data or index for the record to be found.
            should_throw_exception (bool): Indicates whether this method should throw an exception
                                           if the row is not found. Defaults to True.

        Returns:
            WebElement: The DOM element for the row or None if not found (and not thrown)
        """
        # Check grid can be found and is visible
        self._cq.wait_for_single_query_visible(grid_cq)

        script = self._GET_ROW_TEMPLATE.format(grid_cq=grid_cq, row_data=row_data)
        self.ensure_javascript_loaded()
        row = self._driver.execute_script(script)

        if row or not should_throw_exception:
            return row

        raise GridHelper.RowNotFoundException(grid_cq, row_data)

    def click_row(self, grid_cq: str, row_data: Union[int, dict]):
        """ Clicks the row with the specified data or index in the grid.

        The grid must be visible.

        Args:
            grid_cq (str): The component query for the grid
            row_data (Union[int, dict]): The row data or index for the record to be found and clicked.
        """
        # Check grid can be found and is visible
        row = self.get_row(grid_cq, row_data)

        self._logger.info("Clicking clicking row '%s' on grid with CQ '%s'", row_data, grid_cq)

        self._action_chains.move_to_element(row)
        self._action_chains.click()
        self._action_chains.perform()

    def wait_for_row(self, grid_cq: str, row_data: Union[int, dict], timeout: float = 60) -> WebElement:
        """Waits for the specified row to appear in the grid, reloading the store until
        it is found, or until the timeout is hit.

        Args:
            grid_cq (str): The component query for the grid.
            row_data (Union[int, dict]): The row data or index of the record we are waiting for.
            timeout (int, optional): The number of seconds to wait for the row before erroring. Defaults to 60.

        Returns:
            WebElement: The DOM element for the row
        """
        WebDriverWait(self._driver, timeout).until(GridHelper.RowFoundExpectation(grid_cq, row_data))
        return self.get_row(grid_cq, row_data)

    def wait_to_click_row(self, grid_cq: str, row_data: Union[int, dict], timeout: float = 60):
        """Waits for the specified row to appear in the grid, reloading the store until
        it is found, or until the timeout is hit.
        Once we have found the row it is clicked.

        Args:
            grid_cq (str): The component query for the grid.
            row_data (Union[int, dict]): The row data or index of the record we are waiting for.
            timeout (int, optional): The number of seconds to wait for the row before erroring. Defaults to 60.
        """
        WebDriverWait(self._driver, timeout).until(GridHelper.RowFoundExpectation(grid_cq, row_data))
        self.click_row(grid_cq, row_data)

    class ColumnNotFoundException(Exception):
        """Exception class thrown when we failed to find the specified column
        """

        def __init__(self,
                     grid_cq: str,
                     column_text_or_data_index: str,
                     message: str = "Failed to find column with text (or dataIndex) '{column_text_or_data_index}' on grid with CQ '{grid_cq}'."):
            """Initialises an instance of this exception

            Args:
                grid_cq (str): The CQ used to find the grid
                column_text_or_data_index (str): The header text or dataIndex of the grid column
                message (str, optional): The exception message. Defaults to "Failed to find column with text (or dataIndex) '{column_text_or_data_index}' on grid with CQ '{grid_cq}'.".
            """
            self.message = message
            self._grid_cq = grid_cq
            self._column_text_or_data_index = column_text_or_data_index

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(column_text_or_data_index=self._column_text_or_data_index, grid_cq=self._grid_cq)

    class RowNotFoundException(Exception):
        """Exception class thrown when we failed to find the specified row
        """

        def __init__(self,
                     grid_cq: str,
                     row_data: Union[int, dict],
                     message: str = "Failed to find row with data (or index) '{row_data}' on grid with CQ '{grid_cq}'."):
            """Initialises an instance of this exception

            Args:
                grid_cq (str): The CQ used to find the grid
                row_data (Union[int, dict]): The row data or index for the record
                message (str, optional): The exception message. Defaults to "Failed to find row with data (or index) '{row_data}' on grid with CQ '{grid_cq}'.".
            """
            self.message = message
            self._grid_cq = grid_cq
            self._row_data = row_data

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(row_data=self._row_data, grid_cq=self._grid_cq)

    class RowFoundExpectation():
        """ An expectation for checking that a row has been found
        """

        def __init__(self, grid_cq: str, row_data: Union[int, dict]):
            """Initialises an instance of this class.

            Args:
                grid_cq (str): The component query for the grid.
                row_data (Union[int, dict]): The row data or index of the record we are waiting for.
            """
            self._grid_cq = grid_cq
            self._row_data = row_data

        def __call__(self, driver):
            """Method that determines whether a row was found.

            If the row is not found the grid is refreshed and the load waited for.
            """
            grid_helper = GridHelper(driver)

            row = grid_helper.get_row(self._grid_cq, self._row_data, False)
            if row:
                return True

            # Trigger a reload, and wait for it to complete
            store_helper = StoreHelper(driver)
            store_helper.reset_store_load_count(self._grid_cq)
            store_helper.trigger_reload(self._grid_cq)
            store_helper.wait_for_store_loaded(self._grid_cq)
            return False
