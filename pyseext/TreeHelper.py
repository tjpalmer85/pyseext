from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class TreeHelper(HasReferencedJavaScript):
    """A class to help with using trees, through Ext's interfaces.
    """

    # Class variables
    _FN_TEMPLATE = "return globalThis.PySeExt.TreeHelper.fn('{tree_cq}')"


    def __init__(self, driver):
        """Initialises an instance of this class

        Args:
            driver (selenium.webdriver): The webdriver to use
        """
        self._driver = driver

        # Initialise our base class
        super().__init__(driver)
