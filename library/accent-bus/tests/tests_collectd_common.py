# tests/test_collectd_common.py
# Copyright 2025 Accent Communications

"""Tests for accent_bus.collectd.common."""

from abc import ABC, abstractmethod

import pytest
from accent_bus.collectd.common import CollectdEvent


# Create a concrete subclass of CollectdEvent for testing purposes
class ConcreteCollectdEvent(CollectdEvent):
    name = "test_event"
    routing_key_fmt: str = "test.routing.key"
    plugin = "test_plugin"
    type_ = "test_type"


@pytest.fixture
def collectd_event():
    """Provides a basic CollectdEvent instance."""
    return ConcreteCollectdEvent()


def test_collectd_event_initialization(collectd_event):
    """Test that the CollectdEvent initializes correctly."""
    assert collectd_event.content == {}  # Default content
    event_with_content = ConcreteCollectdEvent(content={"key": "value"})
    assert event_with_content.content == {"key": "value"}


def test_collectd_event_is_valid(collectd_event):
    """Test cases for event is valid"""
    assert not collectd_event.is_valid()
    collectd_event.plugin_instance = "instance"
    collectd_event.type_instance = "some_type"
    collectd_event.values = ("1",)
    assert collectd_event.is_valid()
    collectd_event.values = tuple()
    assert not collectd_event.is_valid()


def test_collectd_event_string_representation(collectd_event):
    """Test the string representation of CollectdEvent."""
    collectd_event.plugin_instance = "test_instance"
    collectd_event.type_instance = "test_type_instance"
    collectd_event.values = ("1", "2", "3")

    expected_string = (
        "CollectdEvent(plugin='test_plugin', "
        "plugin_instance='test_instance', "
        "type='test_type', "
        "type_instance='test_type_instance', "
        "values=('1', '2', '3'))"
    )
    assert str(collectd_event) == expected_string
