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

    routing_key_fmt: str = "collectd.calls"  # Class variable
    plugin: str = "calls"  # Class variable
    type_: str = "counter"  # Class variable
    values: tuple[str, ...] = ("1",)  # Class variable

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

    name: str = "collectd_call_started"  # Class variable
    type_instance: str = "start"  # Class variable


class CallConnectCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call connects."""

    name: str = "collectd_call_connected"  # Class variable
    type_instance: str = "connect"  # Class variable


class CallEndCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call ends."""

    name: str = "collectd_call_ended"  # Class variable
    type_instance: str = "end"  # Class variable


class CallAbandonedCollectdEvent(_BaseCallCollectdEvent):
    """Event for when a call is abandoned."""

    name: str = "collectd_call_abandoned"  # Class variable
    type_instance: str = "abandoned"  # Class variable


class CallDurationCollectdEvent(_BaseCallCollectdEvent):
    """Event for call duration."""

    name: str = "collectd_call_duration"  # Class variable
    type_: str = "gauge"  # Class variable
    type_instance: str = "duration"  # Class variable

    def __init__(
        self,
        application: str,
        application_id: str | None,
        duration: int,
        time: str | int | None = None,
    ):
        """Initialize the event.

        Args:
           application (str): The application name.
           application_id (str | None): The application ID.
           duration (int): The call duration.
           time (str | int | None): The event timestamp

        """
        super().__init__(application, application_id, time)
        self.values = (str(round(duration, 3)),)
