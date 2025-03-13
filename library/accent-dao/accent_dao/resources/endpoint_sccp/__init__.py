# file: accent_dao/resources/endpoint_sccp/__init__.py  # noqa: ERA001
# Copyright 2025 Accent Communications
"""SCCP endpoint resource implementation."""

from .dao import (
    create,
    delete,
    edit,
    find_all_by,
    find_by,
    get,
    search,
)

__all__: list[str] = [
    "create",
    "delete",
    "edit",
    "find_all_by",
    "find_by",
    "get",
    "search",
]
