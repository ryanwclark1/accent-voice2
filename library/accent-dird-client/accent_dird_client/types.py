# Copyright 2025 Accent Communications

"""Type definitions for the Directory Service API."""

from __future__ import annotations

from typing import TypeAlias

JSON: TypeAlias = str | int | float | bool | None | list["JSON"] | dict[str, "JSON"]
