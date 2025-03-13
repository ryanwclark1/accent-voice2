# file: accent_dao/resources/user/__init__.py  # noqa: ERA001
# Copyright 2025 Accent Communications
"""User resource implementation."""

from .dao import (
    associate_all_groups,
    count_all_by,
    create,
    delete,
    edit,
    find,
    find_all_by,
    find_all_by_agent_id,
    find_by,
    find_by_id_uuid,
    get,
    get_by,
    get_by_id_uuid,
    list_outgoing_callerid_associated,
    search,
    search_collated,
)

__all__: list[str] = [
    "associate_all_groups",
    "count_all_by",
    "create",
    "delete",
    "edit",
    "find",
    "find_all_by",
    "find_all_by_agent_id",
    "find_by",
    "find_by_id_uuid",
    "get",
    "get_by",
    "get_by_id_uuid",
    "list_outgoing_callerid_associated",
    "search",
    "search_collated",
]
