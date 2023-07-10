globalThis.None = null;

globalThis.PySeExt = globalThis.PySeExt || {};
globalThis.PySeExt.ObservableHelper = {
    /**
     * Method to find an observable using a component query, optionally access a member on it
     * (to get an owned observable), and then wait for an event with the specified name.
     *
     * Returns when the event has been caught, or when the timeout is reached.
     *
     * @param {String} componentCQ The component query to find the observable object, or the
     *                             owner of the observable member.
     * @param {String} eventName The name of the event to wait for.
     * @param {Float} timeout The maximum amount of time to wait for the event, in seconds.
     * @param {String} member_accessor The optional name of the member to access on the component
     *                                 to find the observable to watch.
     * @param {Function} callback The function to call when done.
     *                            The boolean value true is passed if the event was seen, otherwise
     *                            an error message is passed.
     *                            This comes back into the Python as the result of the execute_async_script call.
     */
    waitForEvent: function(componentCQ, eventName, timeout, member_accessor, callback) {
        var me = this,
            components = globalThis.Ext.ComponentQuery.query(componentCQ),
            observable,
            eventHandler,
            timerId;

        if (components && components.length) {
            if (components.length === 1) {
                observable = components[0];

                if (member_accessor) {
                    observable = observable[member_accessor];

                    if (globalThis.Ext.isFunction(observable)) {
                        observable = observable.apply(me);
                    }

                    if (!observable) {
                        globalThis.Ext.callback(callback, me, ['Member accessor did not find anything.']);
                        return;
                    }
                }

                if (observable.isObservable) {
                    // Create our handler
                    eventHandler = function() {
                        if (timerId) {
                            globalThis.Ext.undefer(timerId);
                        }

                        globalThis.Ext.callback(callback, me, [true]);
                    };

                    // Need to start a timer
                    timerId = globalThis.Ext.defer(function() {
                        // Timeout hit!

                        // Cancel event handler
                        observable.un(eventName, eventHandler);

                        // Return error
                        globalThis.Ext.callback(callback, me, ['Event was not received.']);
                    }, timeout * 1000);

                    // Register for event
                    observable.on(eventName, eventHandler);
                } else {
                    globalThis.Ext.callback(callback, me, ['Found component is not observable.']);
                }
            } else {
                globalThis.Ext.callback(callback, me, ['Multiple components found.']);
            }
        } else {
            globalThis.Ext.callback(callback, me, ['Component not found.']);
        }
    }
};