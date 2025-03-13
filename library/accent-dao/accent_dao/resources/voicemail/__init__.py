# file: accent_dao/resources/voicemail/__init__.py  # noqa: ERA001
# Copyright 2025 Accent Communications
"""Voicemail resource implementation."""

from .dao import (
    create,
    delete,
    edit,
    find,
    find_all_by,
    find_by,
    get,
    get_by,
    search,
)

__all__: list[str] = [
    "create",
    "delete",
    "edit",
    "find",
    "find_all_by",
    "find_by",
    "get",
    "get_by",
    "search",
]
