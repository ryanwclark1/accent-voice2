# accent_bus/resources/external_app/types.py
# Copyright 2025 Accent Communications

"""External app types."""

from __future__ import annotations

from typing import TypedDict


class ExternalAppDict(TypedDict, total=False):
    """Dictionary representing an external app."""

    name: str
