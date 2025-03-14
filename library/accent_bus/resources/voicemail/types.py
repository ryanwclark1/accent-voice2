# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict


class VoicemailFolderDict(TypedDict, total=False):
    id: int
    name: str
    type: str


class VoicemailMessageDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_num: str
    duration: int
    tiemstamp: int
    folder: VoicemailFolderDict
