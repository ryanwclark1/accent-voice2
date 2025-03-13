# line_dao.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Protocol

from sqlalchemy import select

from accent_dao.alchemy.extension import Extension as ExtensionTable
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# Set up logging
logger = logging.getLogger(__name__)


class EndpointRow(Protocol):
    """Protocol for endpoint row data."""

    endpoint_sip_uuid: str | None
    endpoint_sccp_id: str | None
    endpoint_custom_id: str | None
    name: str
    main_line: bool | None = None



@async_daosession
async def get_interface_from_exten_and_context(
    session: AsyncSession, extension: str, context: str
) -> str:
    """Get interface from extension and context (async version).

    Args:
        session: Async database session
        extension: Extension
        context: Context

    Returns:
        Interface string

    Raises:
        LookupError: If no line found with extension and context

    """
    stmt = (
        select(
            LineFeatures.endpoint_sip_uuid,
            LineFeatures.endpoint_sccp_id,
            LineFeatures.endpoint_custom_id,
            LineFeatures.name,
            UserLine.main_line,
        )
        .join(LineExtension, LineExtension.line_id == LineFeatures.id)
        .join(ExtensionTable, LineExtension.extension_id == ExtensionTable.id)
        .outerjoin(UserLine, UserLine.line_id == LineFeatures.id)
        .filter(ExtensionTable.exten == extension)
        .filter(ExtensionTable.context == context)
    )

    result = await session.execute(stmt)
    rows = result.all()

    interface = None
    for row in rows:
        interface = _format_interface(row)
        if row.main_line:
            return interface

    if not interface:
        error_message = f"no line with extension {extension} and context {context}"
        raise LookupError(error_message)

    return interface


@async_daosession
async def get_interface_from_line_id(session: AsyncSession, line_id: int) -> str:
    """Get interface from line ID (async version).

    Args:
        session: Async database session
        line_id: Line ID

    Returns:
        Interface string

    Raises:
        LookupError: If no line found with ID

    """
    stmt = select(
        LineFeatures.endpoint_sip_uuid,
        LineFeatures.endpoint_sccp_id,
        LineFeatures.endpoint_custom_id,
        LineFeatures.name,
    ).filter(LineFeatures.id == line_id)

    result = await session.execute(stmt)
    line_row = result.first()

    if not line_row:
        error_message = f"no line with id {line_id}"
        raise LookupError(error_message)

    return _format_interface(line_row)


@async_daosession
async def get_main_extension_context_from_line_id(
    session: AsyncSession, line_id: int
) -> tuple[str, str] | None:
    """Get main extension and context from line ID (async version).

    Args:
        session: Async database session
        line_id: Line ID

    Returns:
        Tuple of extension and context, or None if not found

    """
    stmt = (
        select(ExtensionTable.exten, ExtensionTable.context)
        .join(LineExtension, LineExtension.extension_id == ExtensionTable.id)
        .filter(LineExtension.line_id == line_id)
        .filter(LineExtension.main_extension.is_(True))
    )

    result = await session.execute(stmt)
    row = result.first()
    if row:
        return (row.exten, row.context)
    return None


@async_daosession
async def is_line_owned_by_user(
    session: AsyncSession, user_uuid: str, line_id: int
) -> bool:
    """Check if line is owned by user (async version).

    Args:
        session: Async database session
        user_uuid: User UUID
        line_id: Line ID

    Returns:
        True if line is owned by user, False otherwise

    """
    stmt = (
        select(UserLine)
        .join(UserFeatures)
        .filter(UserLine.line_id == line_id)
        .filter(UserFeatures.uuid == user_uuid)
    )

    result = await session.execute(stmt)
    user_line_row = result.first()
    return user_line_row is not None


def _format_interface(row: EndpointRow) -> str:
    """Format interface string from row.

    Args:
        row: Row with endpoint information

    Returns:
        Formatted interface string

    """
    if row.endpoint_sip_uuid:
        return f"PJSIP/{row.name}"
    if row.endpoint_sccp_id:
        return f"SCCP/{row.name}"
    if row.endpoint_custom_id:
        return row.name
    return ""
