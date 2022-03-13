from pyseext.ComponentQuery import ComponentQuery

class ButtonHelper:
    """A class to help with interacting with Ext buttons
    """

    _BUTTON_TEMPLATE = 'button[text="{text}"][disabled=false]'

    _cq = None

    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._cq = ComponentQuery(driver)

    def click_button_by_text(self, text, root_id=None):
        """Finds a visible, enabled button with the specified text and clicks it.

        Args:
            text (str): The text on the button
            root_id (str, optional):
                The id of the container within which to perform the query.
                If omitted, all components within the document are included in the search.
        """
        button = self._cq.wait_for_single_query_visible(self._BUTTON_TEMPLATE.format(text=text), root_id)
        button.click()