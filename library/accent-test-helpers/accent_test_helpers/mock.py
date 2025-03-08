# Copyright 2023 Accent Communications
from __future__ import annotations

import uuid
from typing import Any


class _UUIDMatcher:
    def __eq__(self, other: str | Any) -> bool:
        try:
            uuid.UUID(hex=other)
            return True
        except (ValueError, TypeError):
            return False

    def __ne__(self, other: str | Any) -> bool:
        return not self == other


ANY_UUID = _UUIDMatcher()
