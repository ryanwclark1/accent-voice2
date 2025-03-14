# accent_bus/resources/phone_number/types.py
# Copyright 2025 Accent Communications

"""Phone number types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class PhoneNumberDict(TypedDict, total=False):
    """Dictionary representing a phone number."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    number: str
    caller_id_name: str | None
    main: bool
    shareable: bool
