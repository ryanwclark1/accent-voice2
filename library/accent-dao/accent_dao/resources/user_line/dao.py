# file: accent_dao/resources/user_line/dao.py
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.user_line import UserLine
from accent_dao.helpers.db_manager import async_daosession

if TYPE_CHECKING:
    from accent_dao.alchemy.linefeatures import LineFeatures
    from accent_dao.alchemy.userfeatures import UserFeatures

logger = logging.getLogger(__name__)


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> UserLine:
    """Get a user line by criteria.

    Args:
        session: Database session.
        **criteria: Filtering criteria.

    Returns:
        The UserLine object.

    Raises:
        NotFoundError: If no matching user line is found.

    """
    return await UserLinePersistor(session).get_by(criteria)


@async_daosession
async def find_by(session: AsyncSession, **criteria: dict) -> UserLine | None:
    """Find a user line by criteria.

    Args:
        session: Database session.
        **criteria: Filtering criteria.

    Returns:
        The UserLine object or None if not found.

    """
    return await UserLinePersistor(session).find_by(criteria)


@async_daosession
async def find_all_by(session: AsyncSession, **criteria: dict) -> list[UserLine]:
    """Find all user lines by criteria.

    Args:
        session: Database session.
        **criteria: Filtering criteria.

    Returns:
        A list of UserLine objects.

    """
    return await UserLinePersistor(session).find_all_by(criteria)


@async_daosession
async def find_all_by_user_id(
    session: AsyncSession, user_id: int
) -> list[UserLine]:
    """Find all user lines for a user ID.

    Args:
        session: Database session.
        user_id: The user ID.

    Returns:
        A list of UserLine objects.

    """
    return await UserLinePersistor(session).find_all_by(user_id=user_id)


@async_daosession
async def find_main_user_line(
    session: AsyncSession, line_id: int
) -> UserLine | None:
    """Find the main user line for a line ID.

    Args:
        session: Database session.
        line_id: The line ID.

    Returns:
         The UserLine object or None if not found.

    """
    return await UserLinePersistor(session).find_by(line_id=line_id, main_user=True)


@async_daosession
async def associate(
    session: AsyncSession, user: UserFeatures, line: LineFeatures
) -> UserLine:
    """Associate a user with a line.

    Args:
        session: Database session.
        user: The UserFeatures object.
        line: The LineFeatures object.

    Returns:
        The created or existing UserLine object.

    """
    return await UserLinePersistor(session).associate_user_line(user, line)


@async_daosession
async def dissociate(
    session: AsyncSession, user: UserFeatures, line: LineFeatures
) -> UserLine | None:
    """Dissociate a user from a line.

    Args:
        session: Database session.
        user: The UserFeatures object.
        line: The LineFeatures object.

    Returns:
      The UserLine object or None

    """
    return await UserLinePersistor(session).dissociate_user_line(user, line)


@async_daosession
async def associate_all_lines(
    session: AsyncSession, user: UserFeatures, lines: list[LineFeatures]
) -> list[UserLine]:
    """Associate all provided lines with a user.

    Args:
        session: Database session.
        user: The UserFeatures object.
        lines: A list of LineFeatures objects.

    Returns:
        A list of associated UserLine objects.

    """
    return await UserLinePersistor(session).associate_all_lines(user, lines)
