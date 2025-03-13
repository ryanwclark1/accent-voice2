# file: accent_dao/resources/user/__init__.py  # noqa: ERA001
# Copyright 2025 Accent Communications
"""User resource implementation."""

from .dao import (
    async_associate_all_groups,
    async_count_all_by,
    async_create,
    async_delete,
    async_edit,
    async_find,
    async_find_all_by,
    async_find_all_by_agent_id,
    async_find_by,
    async_find_by_id_uuid,
    async_get,
    async_get_by,
    async_get_by_id_uuid,
    async_list_outgoing_callerid_associated,
    async_search,
    async_search_collated,
)

__all__: list[str] = [
    "async_associate_all_groups",
    "async_count_all_by",
    "async_create",
    "async_delete",
    "async_edit",
    "async_find",
    "async_find_all_by",
    "async_find_all_by_agent_id",
    "async_find_by",
    "async_find_by_id_uuid",
    "async_get",
    "async_get_by",
    "async_get_by_id_uuid",
    "async_list_outgoing_callerid_associated",
    "async_search",
    "async_search_collated",
]
