# tests/resources/ami/tests/test_event.py
# Copyright 2025 Accent Communications

"""Tests for AMI events."""

from unittest.mock import sentinel  # Keep mock for sentinels

import pytest  # Use pytest

# The import needs to be from the full path, even within the same project
from accent_bus.resources.ami.event import AMIEvent


def test_marshal():
    """Test the marshal method."""
    event = AMIEvent(sentinel.name, {"vars": sentinel.variables})
    result = event.marshal()
    assert result == {"vars": sentinel.variables}  # Use pytest assert


def test_string_name():
    """Test setting string name"""
    event_name = "some-ami-event"
    event = AMIEvent(event_name, {"vars": sentinel.variables})
    assert event.name == event_name
