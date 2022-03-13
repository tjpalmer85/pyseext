# Imports

# Third-party
from http import client
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Ours
from pyseext.ComponentQuery import ComponentQuery
from pyseext.FormHelper import FormHelper
from pyseext.ButtonHelper import ButtonHelper

class Authentication:
    """Class that provides helper methods for authenticating with AMS
    """

    _LOGIN_WINDOW_QUERY_TEXT = 'window[$className="AltusProductsAccessManagementServer.view.LoginWindow"]{isVisible(true)}'
    _SUBMIT_BUTTON_QUERY_TEXT = 'altus-button[text="Submit"]'
    _CLIENT_ID_FIELDNAME = 'clientId'
    _USERNAME_FIELDNAME = 'username'
    _PASSWORD_FIELDNAME = 'password'

    _driver = None

    def __init__(self, driver):
        """Initialises an instance of this class.

        Args:
            driver (selenium.webdriver): The webdriver to use.
        """
        self._driver = driver

    def login(self, client_id, username, password):
        """Logs into the user interface when password authentication

        Args:
            client_id (int): The client id to use
            username (str): The username to use
            password (str): The password to use
        """
        # Get login window
        cq = ComponentQuery(self._driver)
        login_window = cq.wait_for_single_query(self._LOGIN_WINDOW_QUERY_TEXT)

        if (login_window != None):
            form = FormHelper(self._driver)

            form.set_form_values(self._LOGIN_WINDOW_QUERY_TEXT, {
                'clientId': client_id,
                'username': username,
                'password': password
            })

            ButtonHelper(self._driver).click_button_by_text('Submit', login_window.id)
        else:
            raise NoSuchElementException('Could not find login window')
