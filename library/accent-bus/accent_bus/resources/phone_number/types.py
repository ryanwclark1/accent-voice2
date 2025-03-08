# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class PhoneNumberDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    number: str
    caller_id_name: str | None
    main: bool
    shareable: bool
