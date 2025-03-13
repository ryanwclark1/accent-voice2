# helpers/db_utils.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, TypeVar

from accent_dao.helpers import db_manager
from accent_dao.helpers.db_manager import async_daosession, daosession

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session

T = TypeVar("T")

# Set up logging
logger = logging.getLogger(__name__)


@contextmanager
def flush_session(session: Session) -> Generator[None, None, None]:
    """Flush the session on exit.

    Args:
        session: Database session

    Yields:
        None

    """
    try:
        yield
        session.flush()
    except Exception as e:
        session.rollback()
        logger.exception("Error during session flush: %s", str(e))
        raise


@asynccontextmanager
async def async_flush_session(session: AsyncSession) -> AsyncGenerator[None, None]:
    """Flush the async session on exit.

    Args:
        session: Async database session

    Yields:
        None

    """
    try:
        yield
        await session.flush()
    except Exception as e:
        await session.rollback()
        logger.exception("Error during async session flush: %s", str(e))
        raise


@daosession
def get_dao_session(session: Session) -> Session:
    """Get the current database session.

    Args:
        session: Database session (injected by decorator)

    Returns:
        Database session

    """
    return session


@async_daosession
async def get_async_dao_session(session: AsyncSession) -> AsyncSession:
    """Get the current async database session.

    Args:
        session: Async database session (injected by decorator)

    Returns:
        Async database session

    """
    return session


@contextmanager
def session_scope(read_only: bool = False) -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations.

    Args:
        read_only: If True, session will not be committed

    Yields:
        Database session

    """
    session = db_manager.SyncSession()
    try:
        yield session
        if not read_only:
            session.commit()
    except Exception as e:
        session.rollback()
        logger.exception("Error during session scope: %s", str(e))
        raise
    finally:
        # In SQLAlchemy 2.x, session.remove() is deprecated for scoped_session
        # We should use SyncSession.remove() instead
        db_manager.SyncSession.remove()


@asynccontextmanager
async def async_session_scope(
    read_only: bool = False,
) -> AsyncGenerator[AsyncSession, None]:
    """Provide an async transactional scope around a series of operations.

    Args:
        read_only: If True, session will not be committed

    Yields:
        Async database session

    """
    async with db_manager.get_async_session() as session:
        try:
            yield session
            if not read_only:
                await session.commit()
        except Exception as e:
            await session.rollback()
            logger.exception("Error during async session scope: %s", str(e))
            raise
