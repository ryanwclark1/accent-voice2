# accent_bus/resources/common/types.py
# Copyright 2025 Accent Communications

"""Common type definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Literal

_string_formats = Literal["date", "date-time", "uuid"]


@dataclass(frozen=True)
class Format:
    """String format descriptor."""

    format: _string_formats | None = field(default=None)


# Type aliases
UUIDStr = Annotated[str, Format("uuid")]
DateTimeStr = Annotated[str, Format("date-time")]
DateStr = Annotated[str, Format("date")]
