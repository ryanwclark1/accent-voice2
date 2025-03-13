# file: accent_dao/resources/endpoint_iax/__init__.py  # noqa: ERA001
# Copyright 2025 Accent Communications
"""IAX Endpoint resource implementation."""

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
