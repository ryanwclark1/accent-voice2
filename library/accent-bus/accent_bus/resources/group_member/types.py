# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict


class GroupExtensionDict(TypedDict, total=False):
    exten: str
    context: str
