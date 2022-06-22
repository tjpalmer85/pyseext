Module pyseext.input_helper
===========================
Module that contains our InputHelper class.

Classes
-------

`InputHelper(driver: selenium.webdriver.remote.webdriver.WebDriver)`
:   A class to help with user input.
        
    
    Initialises an instance of this class
    
    Args:
        driver (WebDriver): The webdriver to use

    ### Class variables

    `TYPING_SLEEP_MAXIMUM: float`
    :   The maximum amount of time in seconds to wait between key presses when typing. Defaults to 0.002 seconds.

    `TYPING_SLEEP_MINIMUM: float`
    :   The minimum amount of time in seconds to wait between key presses when typing. Defaults to 0.0001 seconds.

    ### Methods

    `type(self, text: str)`
    :   Types into the currently focused element in a realistic manner.
        
        Args:
            text (str): The text to type.

    `type_into_element(self, element: selenium.webdriver.remote.webelement.WebElement, text: str, delay: Optional[float] = None, tab_off: Optional[bool] = False)`
    :   Types into an input element in a realistic manner.
        
        Args:
            element (WebElement): The element to type into.
            text (str): The text to type.
            delay (float, optional): The number of seconds to delay after typing. Defaults to None.
            tab_off (bool, optional): Indicates whether to tab off the field after typing, and delay. Defaults to False.

    `type_tab(self)`
    :   Type a tab character into the currently focused element.