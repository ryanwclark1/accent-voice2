# accent_bus/collectd/channels.py
# Copyright 2025 Accent Communications

"""Collectd events for channels."""

from .common import CollectdEvent


class _BaseChannelCollectdEvent(CollectdEvent):
    """Base class for channel-related Collectd events."""

    routing_key_fmt: str = "collectd.channels"  # Class variable
    plugin: str = "channels"  # Class variable
    plugin_instance: str = "global"  # Class variable
    type_: str = "counter"  # Class variable
    values: tuple[str, ...] = ("1",)  # Class variable


class ChannelCreatedCollectdEvent(_BaseChannelCollectdEvent):
    """Event for when a channel is created."""

    name: str = "collectd_channel_created"  # Class variable
    type_instance: str = "created"  # Class variable


class ChannelEndedCollectdEvent(_BaseChannelCollectdEvent):
    """Event for when a channel ends."""

    name: str = "collectd_channel_ended"  # Class variable
    type_instance: str = "ended"  # Class variable
