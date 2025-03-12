# accent_dao/user_dao.py
# Copyright 2025 Accent Communications

import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession, daosession

logger = logging.getLogger(__name__)


@daosession
def get(session: Session, user_id: int | UUID) -> UserFeatures:
    """Retrieve a user by their ID.

    Args:
        session: The database session.
        user_id: The ID of the user, which can be an integer or a UUID.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given ID.

    """
    if isinstance(user_id, int):
        result = session.execute(
            select(UserFeatures).where(UserFeatures.id == user_id)
        ).scalar_one_or_none()
    else:
        result = session.execute(
            select(UserFeatures).where(UserFeatures.uuid == user_id)
        ).scalar_one_or_none()

    if result is None:
        error_message = f"User with ID {user_id} not found"
        raise LookupError(error_message)
    return result


@async_daosession
async def get_async(session: AsyncSession, user_id: int | UUID) -> UserFeatures:
    """Retrieve a user by their ID asynchronously.

    Args:
        session: The async database session.
        user_id: The ID of the user, which can be an integer or a UUID.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given ID.

    """
    if isinstance(user_id, int):
        result = await session.execute(
            select(UserFeatures).where(UserFeatures.id == user_id)
        )
    else:
        result = await session.execute(
            select(UserFeatures).where(UserFeatures.uuid == user_id)
        )

    user = result.scalar_one_or_none()
    if user is None:
        msg = "User with ID %s not found"
        raise LookupError(msg, user_id)
    return user


@daosession
def get_user_by_agent_id(session: Session, agent_id: str) -> UserFeatures:
    """Retrieve a user by their agent ID.

    Args:
        session: The database session.
        agent_id: The agent ID of the user.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given agent ID.

    """
    result = session.execute(
        select(UserFeatures).where(UserFeatures.agent_id == agent_id)
    ).scalar_one_or_none()

    if not result:
        msg = "User with agent ID %s not found"
        raise LookupError(msg, agent_id)
    return result


@async_daosession
async def get_user_by_agent_id_async(
    session: AsyncSession, agent_id: str
) -> UserFeatures:
    """Retrieve a user by their agent ID asynchronously.

    Args:
        session: The async database session.
        agent_id: The agent ID of the user.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given agent ID.

    """
    result = await session.execute(
        select(UserFeatures).where(UserFeatures.agent_id == agent_id)
    )

    user = result.scalar_one_or_none()
    if not user:
        msg = "User with agent ID %s not found"
        raise LookupError(msg, agent_id)
    return user


@daosession
def get_user_by_number_context(
    session: Session, exten: str, context: str
) -> UserFeatures:
    """Retrieve a user by their extension number and context.

    Args:
        session: The database session.
        exten: The extension number.
        context: The context.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given extension and context.

    """
    stmt = (
        select(UserFeatures)
        .join(UserLine, UserFeatures.id == UserLine.user_id)
        .join(LineFeatures, UserLine.line_id == LineFeatures.id)
        .join(LineExtension, LineExtension.line_id == LineFeatures.id)
        .join(Extension, Extension.id == LineExtension.extension_id)
        .where(
            Extension.context == context,
            Extension.exten == exten,
            Extension.commented == 0,
            UserLine.main_line.is_(True),
            LineFeatures.commented == 0,
        )
    )

    result = session.execute(stmt).scalar_one_or_none()

    if not result:
        logger.info("No user with number %s in context %s", exten, context)
        msg = f"No user with number {exten} in context {context}"
        raise LookupError(msg)

    return result


@async_daosession
async def get_user_by_number_context_async(
    session: AsyncSession, exten: str, context: str
) -> UserFeatures:
    """Retrieve a user by their extension number and context asynchronously.

    Args:
        session: The async database session.
        exten: The extension number.
        context: The context.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given extension and context.

    """
    stmt = (
        select(UserFeatures)
        .join(UserLine, UserFeatures.id == UserLine.user_id)
        .join(LineFeatures, UserLine.line_id == LineFeatures.id)
        .join(LineExtension, LineExtension.line_id == LineFeatures.id)
        .join(Extension, Extension.id == LineExtension.extension_id)
        .where(
            Extension.context == context,
            Extension.exten == exten,
            Extension.commented == 0,
            UserLine.main_line.is_(True),
            LineFeatures.commented == 0,
        )
    )

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        logger.info("No user with number %s in context %s", exten, context)
        msg = f"No user with number {exten} in context {context}"
        raise LookupError(msg)

    return user
