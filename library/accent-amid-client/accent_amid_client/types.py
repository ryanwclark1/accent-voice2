# Copyright 2025 Accent Communications

"""Type definitions for the AMID client."""

from __future__ import annotations

# Use PEP 604 style union types
JSON = str | int | float | bool | None | list["JSON"] | dict[str, "JSON"]
