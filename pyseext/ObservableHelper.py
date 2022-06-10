import logging

from pyseext.HasReferencedJavaScript import HasReferencedJavaScript

class ObservableHelper(HasReferencedJavaScript):
    """A class to help with observable objects in Ext.
    """

    _WAIT_FOR_EVENT_TEMPLATE: str = "return globalThis.PySeExt.ObservableHelper.waitForEvent('{component_cq}', '{event_name}', {timeout}, {member_accessor}, callback)"

    def __init__(self, driver):
        """Initialises an instance of this class.

        Args:
            driver (selenium.webdriver): The webdriver to use.
        """

        # Instance variables
        self._logger = logging.getLogger(__name__)
        self._driver = driver

        # Initialise our base class
        super().__init__(driver, self._logger)

    def wait_for_event(self, component_cq: str, event_name: str, timeout: float = 10, member_accessor: str = None):
        """Method to find an observable using a component query, optionally access a member on it (to get an owned observable),
        and then wait for an event with the specified name.

        Returns when the event has been caught, or throws if the timeout was reached or the observable could not be found or resolve to a single object.

        Args:
            component_cq (str): The component query to find the observable object, or the owner of the observable member.
            event_name (str): The name of the event to wait for.
            timeout (float, optional): The maximum amount of time to wait for the event, in seconds. Defaults to 10.
            member_accessor (str, optional): The name of the member to access on the component to find the observable to watch. Defaults to None.
        """
        if member_accessor:
            self._logger.debug(f"Waiting for event '{event_name}' on '{component_cq}[{member_accessor}]'")
            # Wrap in quotes
            member_accessor = f"'{member_accessor}'"
        else:
            self._logger.debug(f"Waiting for event '{event_name}' on '{component_cq}'")
            member_accessor = 'undefined'

        async_script = self.get_async_script_content(self._WAIT_FOR_EVENT_TEMPLATE).format(component_cq = component_cq,
                                                                                           event_name =  event_name,
                                                                                           timeout = timeout,
                                                                                           member_accessor = member_accessor)
        self.ensure_javascript_loaded()

        result = self._driver.execute_async_script(async_script)

        if isinstance(result, str):
            # An error has been returned!
            raise ObservableHelper.WaitForEventException(component_cq, event_name, member_accessor, result)

        if member_accessor:
            self._logger.debug(f"Event '{event_name}' on '{component_cq}[{member_accessor}]' received!")
        else:
            self._logger.debug(f"Event '{event_name}' on '{component_cq}' received!")

    class WaitForEventException(Exception):
        """Exception class thrown when waiting for event returned an error.
        """

        def __init__(self, component_cq: str, event_name: str, member_accessor: str, error: str):
            """Initialises an instance of this exception

            Args:
                component_cq (str): The component query to find the observable object, or the owner of the observable member.
                event_name (str): The name of the event to wait for.
                member_accessor (str): The name of the member to access on the component to find the observable to watch.
                error (str): The error that was returned from the JavaScript.
            """
            self._component_cq = component_cq
            self._event_name = event_name
            self._member_accessor = member_accessor
            self._error = error

            if member_accessor:
                self.message = "Waiting for event '{event_name}' on '{component_cq}[{member_accessor}]' failed with error: {error}"
            else:
                self.message = "Waiting for event '{event_name}' on '{component_cq}' failed with error: {error}"

            super().__init__(self.message)

        def __str__(self):
            """Returns a string representation of this exception
            """
            if (self._member_accessor):
                return self.message.format(event_name = self._event_name,
                                           component_cq = self._component_cq,
                                           member_accessor = self._member_accessor,
                                           error = self._error)
            else:
                return self.message.format(event_name = self._event_name,
                                           component_cq = self._component_cq,
                                           error = self._error)
