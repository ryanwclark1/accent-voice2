# tests/test_collectd_calls.py
# Copyright 2025 Accent Communications

import pytest
from accent_bus.collectd.calls import (
    CallAbandonedCollectdEvent,
    CallConnectCollectdEvent,
    CallDurationCollectdEvent,
    CallEndCollectdEvent,
    CallStartCollectdEvent,
    _validate_plugin_instance_fragment,
)


@pytest.mark.parametrize(
    "fragment, expected",
    [
        ("valid", "valid"),
        ("with spaces", "withspaces"),
        ("with.dots", "withdots"),
        ("with_underscores", "withunderscores"),
        ("12345", "12345"),
        ("", "<unknown>"),
        ("!@#$%^", "<unknown>"),
    ],
)
def test_validate_plugin_instance_fragment(fragment, expected):
    assert _validate_plugin_instance_fragment(fragment) == expected


@pytest.fixture
def base_event_args():
    return {
        "application": "test_app",
        "application_id": "test_id",
        "time": "1234567890",
    }


def test_base_call_collectd_event_init(base_event_args):
    from accent_bus.collectd.calls import _BaseCallCollectdEvent  # Late import to fix

    event = _BaseCallCollectdEvent(**base_event_args)
    assert event.plugin_instance == "test_app.test_id"
    assert event.time == 1234567890


def test_call_start_collectd_event(base_event_args):
    event = CallStartCollectdEvent(**base_event_args)
    assert event.name == "collectd_call_started"
    assert event.type_instance == "start"


def test_call_connect_collectd_event(base_event_args):
    event = CallConnectCollectdEvent(**base_event_args)
    assert event.name == "collectd_call_connected"
    assert event.type_instance == "connect"


def test_call_end_collectd_event(base_event_args):
    event = CallEndCollectdEvent(**base_event_args)
    assert event.name == "collectd_call_ended"
    assert event.type_instance == "end"


def test_call_abandoned_collectd_event(base_event_args):
    event = CallAbandonedCollectdEvent(**base_event_args)
    assert event.name == "collectd_call_abandoned"
    assert event.type_instance == "abandoned"


def test_call_duration_collectd_event(base_event_args):
    event = CallDurationCollectdEvent(**base_event_args, duration=10)
    assert event.name == "collectd_call_duration"
    assert event.type_ == "gauge"
    assert event.type_instance == "duration"
    assert event.values == ("10.000",)
