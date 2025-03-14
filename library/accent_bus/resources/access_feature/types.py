# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict


class AccessFeatureDict(TypedDict, total=False):
    id: int
    host: str
    feature: str
    enabled: bool
