# accent_bus/resources/chatd/types.py
# Copyright 2025 Accent Communications

"""Chatd types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class LinePresenceDict(TypedDict, total=False):
    """Dictionary representing line presence."""

    id: int
    state: str


class MessageDict(TypedDict, total=False):
    """Dictionary representing a message."""

    uuid: UUIDStr
    content: str
    alias: str
    user_uuid: UUIDStr
    tenant_uuid: UUIDStr
    accent_uuid: UUIDStr
    created_at: str
    room: RoomDict


class RoomDict(TypedDict, total=False):
    """Dictionary representing a room."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    users: list[RoomUserDict]


class RoomUserDict(TypedDict, total=False):
    """Dictionary representing a room user."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    accent_uuid: UUIDStr


class UserPresenceDict(TypedDict, total=False):
    """Dictionary representing user presence."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    state: str
    status: str
    last_activity: str
    line_state: str
    mobile: bool
    do_not_disturb: bool
    connected: bool
    lines: list[LinePresenceDict]
