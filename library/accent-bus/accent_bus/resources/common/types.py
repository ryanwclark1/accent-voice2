# Copyright 2023 Accent Communications

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Literal

_string_formats = Literal['date', 'date-time', 'uuid']


@dataclass(frozen=True)
class Format:
    format: _string_formats | None = field(default=None)


# Type aliases
UUIDStr = Annotated[str, Format('uuid')]
DateTimeStr = Annotated[str, Format('date-time')]
DateStr = Annotated[str, Format('date')]
