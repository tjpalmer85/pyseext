# Imports

# Third-party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Ours
from pyseext.ComponentQuery import ComponentQuery
from pyseext.FormHelper import FormHelper

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

            client_id_field = form.find_field_input_element(self._LOGIN_WINDOW_QUERY_TEXT, self._CLIENT_ID_FIELDNAME)
            client_id_field.send_keys(str(client_id))
            username_field = form.find_field_input_element(self._LOGIN_WINDOW_QUERY_TEXT, self._USERNAME_FIELDNAME)
            username_field.send_keys(username)
            password_field = form.find_field_input_element(self._LOGIN_WINDOW_QUERY_TEXT, self._PASSWORD_FIELDNAME)
            password_field.send_keys(password)

            submit_button = cq.wait_for_single_query(self._SUBMIT_BUTTON_QUERY_TEXT, login_window.id)
            submit_button.click()
        else:
            raise NoSuchElementException('Could not find login window')
