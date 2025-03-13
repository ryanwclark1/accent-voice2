# file: accent_dao/resources/directory_profile/__init__.py  # noqa: ERA001
# Copyright 2025 Accent Communications
"""Directory Profile resource implementation."""

from .dao import find_by_incall_id

__all__: list[str] = [
    "find_by_incall_id",
]
