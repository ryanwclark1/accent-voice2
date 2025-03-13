# file: accent_dao/resources/func_key_template/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.func_key_template import FuncKeyTemplate
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import FuncKeyTemplatePersistor

logger = logging.getLogger(__name__)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for function key templates.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await FuncKeyTemplatePersistor(session, tenant_uuids=tenant_uuids).search(
        parameters
    )


@async_daosession
async def async_create(
    session: AsyncSession, template: FuncKeyTemplate
) -> FuncKeyTemplate:
    """Create a new function key template.

    Args:
        session: The database session.
        template: The function key template object to create.

    Returns:
        The created function key template object.

    """
    return await FuncKeyTemplatePersistor(session).create(template)


@async_daosession
async def async_get(
    session: AsyncSession, template_id: int, tenant_uuids: list[str] | None = None
) -> FuncKeyTemplate:
    """Get a function key template by ID.

    Args:
        session: The database session.
        template_id: The ID of the function key template.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The function key template object.

    """
    return await FuncKeyTemplatePersistor(session, tenant_uuids).get_by(
        {"id": template_id}
    )


@async_daosession
async def async_edit(session: AsyncSession, template: FuncKeyTemplate) -> None:
    """Edit an existing function key template.

    Args:
        session: The database session.
        template: The function key template object to edit.

    """
    await FuncKeyTemplatePersistor(session).edit(template)


@async_daosession
async def async_delete(session: AsyncSession, template: FuncKeyTemplate) -> None:
    """Delete a function key template.

    Args:
        session: The database session.
        template: The function key template object to delete.

    """
    await FuncKeyTemplatePersistor(session).delete(template)
