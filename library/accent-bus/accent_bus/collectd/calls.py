# collectd/calls.py
import string

from .common import CollectdEvent


def _validate_plugin_instance_fragment(plugin_instance_fragment: str) -> str:
    """Validate and sanitize a plugin instance fragment.

    Args:
        plugin_instance_fragment (str): the fragment to be validate.

    Returns:
        str: A validated plugin instance fragment.

    """
    result = "".join(
        c
        for c in plugin_instance_fragment
        if (c in string.ascii_letters or c in string.digits or c == "-")
    )
    return result or "<unknown>"


class _BaseCallCollectdEvent(CollectdEvent):
    """Base class for Call related Collectd Events.

    Args:
        application (str): The application.
        application_id (str | None): the application id, if any.
        time (str | int | None): Timestamp for the event.

    """

    routing_key_fmt = "collectd.calls"
    plugin = "calls"
    type_ = "counter"
    values = ("1",)

    def __init__(
        self,
        application: str,
        application_id: str | None,
        time: int | str | None = None,
    ):
        super().__init__()
        if time:
            self.time = int(time)

        application = _validate_plugin_instance_fragment(application)
        if application_id is not None:
            application_id = _validate_plugin_instance_fragment(application_id)
            self.plugin_instance = f"{application}.{application_id}"
        else:
            self.plugin_instance = application


class CallStartCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call starts.

    Args:
        application (str): The application.
        application_id (str | None): the application id, if any.
        time (str | int | None): Timestamp for the event.

    """

    name = "collectd_call_started"
    type_instance = "start"


class CallConnectCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call connects.

    Args:
        application (str): The application.
        application_id (str | None): the application id, if any.
        time (str | int | None): Timestamp for the event.

    """

    name = "collectd_call_connected"
    type_instance = "connect"


class CallEndCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call ends.

    Args:
        application (str): The application.
        application_id (str | None): the application id, if any.
        time (str | int | None): Timestamp for the event.

    """

    name = "collectd_call_ended"
    type_instance = "end"


class CallAbandonedCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call is abandoned.

    Args:
        application (str): The application.
        application_id (str | None): the application id, if any.
        time (str | int | None): Timestamp for the event.

    """

    name = "collectd_call_abandoned"
    type_instance = "abandoned"


class CallDurationCollectdEvent(_BaseCallCollectdEvent):
    """Event for tracking call duration.

    Args:
        application (str): The application.
        application_id (str | None): the application id, if any.
        duration (int): Call duration.
        time (str | int | None): Timestamp for the event.

    """

    name = "collectd_call_duration"
    type_ = "gauge"
    type_instance = "duration"

    def __init__(
        self,
        application: str,
        application_id: str | None,
        duration: int,
        time: str | int | None = None,
    ):
        super().__init__(application, application_id, time)
        self.values = (str(round(duration, 3)),)
