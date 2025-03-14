# accent_bus/resources/conference/types.py
# Copyright 2025 Accent Communications

"""Conference types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class ParticipantDict(TypedDict, total=False):
    """Dictionary representing a conference participant."""

    id: str
    caller_id_name: str
    caller_id_number: str
    muted: bool
    join_time: int
    admin: bool
    language: str
    call_id: str
    user_uuid: UUIDStr
