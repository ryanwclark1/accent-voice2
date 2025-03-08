# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class PJSIPTransportDict(TypedDict, total=False):
    uuid: UUIDStr
    name: str
    options: list[str]
