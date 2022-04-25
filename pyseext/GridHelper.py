from selenium.webdriver.common.action_chains import ActionChains

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript
from pyseext.ComponentQuery import ComponentQuery

class GridHelper(HasReferencedJavaScript):
    """A class to help with interacting with Ext grid panels
    """
    _GET_VISIBLE_COLUMN_HEADER_TEMPLATE = "return globalThis.PySeExt.GridHelper.getColumnHeader('{grid_cq}', '{column_text_or_dataIndex}')"
    _GET_VISIBLE_COLUMN_HEADER_TRIGGER_TEMPLATE = "return globalThis.PySeExt.GridHelper.getColumnHeaderTrigger('{grid_cq}', '{column_text_or_dataIndex}')"

    _driver = None

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._driver = driver

        # Initialise our base class
        super().__init__(driver)

    def get_visible_column_header(self, grid_cq, column_text_or_dataIndex):
        """Gets the element for the specified visible column header

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_dataIndex (str): The header text or dataIndex of the grid column
        """

        # Check grid can be found and is visible
        ComponentQuery(self._driver).wait_for_single_query_visible(grid_cq)

        script = self._GET_VISIBLE_COLUMN_HEADER_TEMPLATE.format(grid_cq=grid_cq, column_text_or_dataIndex=column_text_or_dataIndex)
        column_header = self._driver.execute_script(script)

        if column_header:
            return column_header
        else:
            raise GridHelper.ColumnNotFoundException(grid_cq, column_text_or_dataIndex)

    def is_column_visible(self, grid_cq, column_text_or_dataIndex):
        """Determines whether the specified column is visible

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_dataIndex (str): The header text or dataIndex of the grid column

        Returns:
            True if the column was found and is visible, False otherwise.
        """

        # Check grid can be found and is visible
        ComponentQuery(self._driver).wait_for_single_query_visible(grid_cq)

        script = self._GET_VISIBLE_COLUMN_HEADER_TEMPLATE.format(grid_cq=grid_cq, column_text_or_dataIndex=column_text_or_dataIndex)
        column_header = self._driver.execute_script(script)

        return column_header != None

    def check_columns_are_visible(self, grid_cq, column_texts_or_dataIndexes):
        """Checks that the specified columns are all visible on the specified grid.
        
        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_dataIndex (array): An array containing the header text or dataIndex of the grid columns to check

        Returns:
            An array of columns that were not found or not visible, if any.
        """
        columns_not_found_or_visible = []

        for column_text_or_dataIndex in column_texts_or_dataIndexes:
            is_visible = self.is_column_visible(grid_cq, column_text_or_dataIndex)
            if is_visible == False:
                columns_not_found_or_visible.append(column_text_or_dataIndex)

        return columns_not_found_or_visible

    def click_column_header(self, grid_cq, column_text_or_dataIndex):
        """Clicks on the specified column header.
        The column must be visible.

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_dataIndex (str): The header text or dataIndex of the grid column
        """
        column_header = self.get_visible_column_header(grid_cq, column_text_or_dataIndex)
        column_header.click()

    def get_visible_column_header_trigger(self, grid_cq, column_text_or_dataIndex):
        """Gets the element for the specified visible column header's trigger

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_dataIndex (str): The header text or dataIndex of the grid column
        """

        # Check grid can be found and is visible
        ComponentQuery(self._driver).wait_for_single_query_visible(grid_cq)

        script = self._GET_VISIBLE_COLUMN_HEADER_TRIGGER_TEMPLATE.format(grid_cq=grid_cq, column_text_or_dataIndex=column_text_or_dataIndex)
        column_header_trigger = self._driver.execute_script(script)

        if column_header_trigger:
            return column_header_trigger
        else:
            raise GridHelper.ColumnNotFoundException(grid_cq, column_text_or_dataIndex)

    def click_column_header_trigger(self, grid_cq, column_text_or_dataIndex):
        """Clicks on the specified column header's trigger

        Args:
            grid_cq (str): The component query for the owning grid
            column_text_or_dataIndex (str): The header text or dataIndex of the grid column
        """
        # We need to move to the header before the trigger becomes interactable
        column_header = self.get_visible_column_header(grid_cq, column_text_or_dataIndex)
        actions = ActionChains(self._driver)
        actions.move_to_element(column_header).perform()

        column_header_trigger = self.get_visible_column_header_trigger(grid_cq, column_text_or_dataIndex)
        actions.move_to_element(column_header_trigger)
        actions.click()
        actions.perform()

    class ColumnNotFoundException(Exception):
        """Exception class thrown when we failed to find the specified column
        """

        _grid_cq = None
        _column_text_or_dataIndex = None

        def __init__(self, grid_cq, column_text_or_dataIndex, message="Failed to find column with text (or dataIndex) '{column_text_or_dataIndex}' on grid with CQ '{grid_cq}'."):
            """Initialises an instance of this exception

            Args:
                grid_cq (str): The CQ used to find the grid
                column_text_or_dataIndex (str): The header text or dataIndex of the grid column
                message (str, optional): The exception message. Defaults to "Failed to find column with text (or dataIndex) '{column_text_or_dataIndex}' on grid with CQ '{grid_cq}'.".
            """
            self.message = message
            self._grid_cq = grid_cq
            self._column_text_or_dataIndex = column_text_or_dataIndex

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            return self.message.format(column_text_or_dataIndex=self._column_text_or_dataIndex, grid_cq=self._grid_cq)