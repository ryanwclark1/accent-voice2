# accent_bus/resources/access_feature/types.py
# Copyright 2025 Accent Communications

"""Access Feature Types."""

from __future__ import annotations

from typing import TypedDict


class AccessFeatureDict(TypedDict, total=False):
    """Dictionary representing an access feature."""

    id: int
    host: str
    feature: str
    enabled: bool
