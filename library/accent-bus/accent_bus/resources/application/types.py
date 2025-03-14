# accent_bus/resources/application/types.py
# Copyright 2025 Accent Communications

"""Application types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class ApplicationDict(TypedDict, total=False):
    """Dictionary representing an application."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    destination: str | None
    destination_options: dict[str, str]
