# accent_bus/resources/pjsip/types.py
# Copyright 2025 Accent Communications

"""PJSIP types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class PJSIPTransportDict(TypedDict, total=False):
    """Dictionary representing a PJSIP transport."""

    uuid: UUIDStr
    name: str
    options: list[str]
