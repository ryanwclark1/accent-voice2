# accent_bus/collectd/calls.py
# Copyright 2025 Accent Communications

"""Collectd events for calls."""

from __future__ import annotations

import string

from .common import CollectdEvent


def _validate_plugin_instance_fragment(plugin_instance_fragment: str) -> str:
    """Validate a fragment of the plugin instance.

    Args:
        plugin_instance_fragment: The fragment to validate.

    Returns:
        str: The validated fragment.

    """
    result = "".join(
        c
        for c in plugin_instance_fragment
        if (c in string.ascii_letters or c in string.digits or c == "-")
    )
    return result or "<unknown>"


class _BaseCallCollectdEvent(CollectdEvent):
    """Base class for call-related Collectd events."""

    routing_key_fmt = "collectd.calls"
    plugin = "calls"
    type_ = "counter"
    values = ("1",)

    def __init__(
        self,
        application: str,
        application_id: str | None,
        time: int | str | None = None,
    ) -> None:
        """Initialize the event.

        Args:
            application (str): The application name.
            application_id (str | None): The application ID.
            time (int | str | None): The timestamp.

        """
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
    """Event for when a call starts."""

    name = "collectd_call_started"
    type_instance = "start"


class CallConnectCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call connects."""

    name = "collectd_call_connected"
    type_instance = "connect"


class CallEndCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call ends."""

    name = "collectd_call_ended"
    type_instance = "end"


class CallAbandonedCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call is abandoned."""

    name = "collectd_call_abandoned"
    type_instance = "abandoned"


class CallDurationCollectdEvent(_BaseCallCollectdEvent):
    """Event for call duration."""

    name = "collectd_call_duration"
    type_ = "gauge"
    type_instance = "duration"

    def __init__(
        self,
        application: str,
        application_id: str | None,
        duration: int,
        time: str | int | None = None,
    ) -> None:
        """Initialize the event.

        Args:
           application (str): The application name.
           application_id (str | None): The application ID.
           duration (int): The call duration.
           time (str | int | None): The event timestamp

        """
        super().__init__(application, application_id, time)
        self.values = (str(round(duration, 3)),)
