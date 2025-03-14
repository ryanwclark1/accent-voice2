# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Literal, TypedDict


class PluginErrorDict(TypedDict, total=False):
    error_id: str
    message: str
    resource: Literal['plugins']
    details: dict
