# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class ParticipantDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str
    muted: bool
    join_time: int
    admin: bool
    language: str
    call_id: str
    user_uuid: UUIDStr
