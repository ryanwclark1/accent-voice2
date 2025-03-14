# resources/switchboard/types.py
from typing import TypedDict, Any, List

from pydantic import UUID4


class ExtensionDict(TypedDict, total=False):
    """Represents an extension."""

    id: int
    exten: str
    context: str


class IncallDict(TypedDict, total=False):
    """Represents an incall."""

    id: int
    extensions: list[ExtensionDict]


class HeldCallDict(TypedDict, total=False):
    """Represents a held call."""

    id: str
    caller_id_name: str
    caller_id_number: str


class QueuedCallDict(TypedDict, total=False):
    """Represents a queued call."""

    id: str
    caller_id_name: str
    caller_id_number: str


class SwitchboardFallbackDict(TypedDict, total=False):
    """Represents a switchboard fallback."""

    noanswer_destination: Any


class UserDict(TypedDict, total=False):
    """Represents a user."""

    uuid: UUID4
    firstname: str
    lastname: str


class SwitchboardDict(TypedDict, total=False):
    """Represents a switchboard."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    timeout: int
    queue_music_on_hold: str
    waiting_room_music_on_hold: str
    extensions: ExtensionDict
    incalls: list[IncallDict]
    user_members: list[UserDict]
    fallbacks: list[SwitchboardFallbackDict]
