# tests/resources/common/test_routing_key.py
# Copyright 2025 Accent Communications

import pytest
from accent_bus.resources.common.routing_key import escape


@pytest.mark.parametrize(
    "input_key, expected_key",
    [
        ("my-id", "my-id"),
        ("my.id", "my__DOT__id"),
        ("my#id", "my__HASH__id"),
        ("my*id", "my__STAR__id"),
        ("my.*.#.id", "my__STAR_____DOT____HASH____DOT__id"),
        (
            "...***###",
            "______DOT______DOT______DOT______STAR______STAR______STAR______HASH______HASH______HASH__",
        ),
    ],
)
def test_escape(input_key, expected_key):
    assert escape(input_key) == expected_key
