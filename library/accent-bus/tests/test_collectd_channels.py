# tests/test_collectd_channels.py
# Copyright 2025 Accent Communications

import pytest
from accent_bus.collectd.channels import (
    ChannelCreatedCollectdEvent,
    ChannelEndedCollectdEvent,
    _BaseChannelCollectdEvent,  # import to tests
)


def test_base_channel_collectd_event_init():
    event = _BaseChannelCollectdEvent()
    assert event.routing_key_fmt == "collectd.channels"
    assert event.plugin == "channels"
    assert event.plugin_instance == "global"
    assert event.type_ == "counter"
    assert event.values == ("1",)


def test_channel_created_collectd_event():
    event = ChannelCreatedCollectdEvent()
    assert event.name == "collectd_channel_created"
    assert event.type_instance == "created"


def test_channel_ended_collectd_event():
    event = ChannelEndedCollectdEvent()
    assert event.name == "collectd_channel_ended"
    assert event.type_instance == "ended"
