# collectd/channels.py

from .common import CollectdEvent


class _BaseChannelCollectdEvent(CollectdEvent):
    """
    Base class for Channel based Collectd Events.

    """

    routing_key_fmt = "collectd.channels"
    plugin = "channels"
    plugin_instance = "global"
    type_ = "counter"
    values = ("1",)


class ChannelCreatedCollectdEvent(_BaseChannelCollectdEvent):
    """Event for when a channel is created."""

    name = "collectd_channel_created"
    type_instance = "created"


class ChannelEndedCollectdEvent(_BaseChannelCollectdEvent):
    """Event for when a channel ends."""

    name = "collectd_channel_ended"
    type_instance = "ended"
