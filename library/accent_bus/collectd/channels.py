# Copyright 2023 Accent Communications

from .common import CollectdEvent


class _BaseChannelCollectdEvent(CollectdEvent):
    routing_key_fmt = 'collectd.channels'
    plugin = 'channels'
    plugin_instance = 'global'
    type_ = 'counter'
    values = ('1',)


class ChannelCreatedCollectdEvent(_BaseChannelCollectdEvent):
    name = 'collectd_channel_created'
    type_instance = 'created'


class ChannelEndedCollectdEvent(_BaseChannelCollectdEvent):
    name = 'collectd_channel_ended'
    type_instance = 'ended'
