# accent_bus/resources/voicemail/types.py
# Copyright 2025 Accent Communications

"""Voicemail types."""

from __future__ import annotations

from typing import TypedDict


class VoicemailFolderDict(TypedDict, total=False):
    """Dictionary representing a voicemail folder."""

    id: int
    name: str
    type: str


class VoicemailMessageDict(TypedDict, total=False):
    """Dictionary representing a voicemail message."""

    id: str
    caller_id_name: str
    caller_id_num: str
    duration: int
    tiemstamp: int
    folder: VoicemailFolderDict
