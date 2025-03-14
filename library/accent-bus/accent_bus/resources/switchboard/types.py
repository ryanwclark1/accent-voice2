# accent_bus/resources/switchboard/types.py
# Copyright 2025 Accent Communications

"""Switchboard types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class ExtensionDict(TypedDict, total=False):
    """Dictionary representing an extension."""

    id: int
    exten: str
    context: str


class IncallDict(TypedDict, total=False):
    """Dictionary representing an incall."""

    id: int
    extensions: list[ExtensionDict]


class HeldCallDict(TypedDict, total=False):
    """Dictionary representing a held call."""

    id: str
    caller_id_name: str
    caller_id_number: str


class QueuedCallDict(TypedDict, total=False):
    """Dictionary representing a queued call."""

    id: str
    caller_id_name: str
    caller_id_number: str


class SwitchboardDict(TypedDict, total=False):
    """Dictionary representing a switchboard."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    timeout: int
    queue_music_on_hold: str
    waiting_room_music_on_hold: str
    extensions: ExtensionDict
    incalls: list[IncallDict]
    user_members: list[UserDict]
    fallbacks: list[SwitchboardFallbackDict]


class SwitchboardFallbackDict(TypedDict, total=False):
    """Dictionary representing a switchboard fallback."""

    noanswer_destination: Any


class UserDict(TypedDict, total=False):
    """Dictionary representing a user."""

    uuid: UUIDStr
    firstname: str
    lastname: str
