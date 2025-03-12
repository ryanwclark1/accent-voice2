# helpers/db_utils.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, TypeVar

from accent_dao.helpers import db_manager
from accent_dao.helpers.db_manager import daosession

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session

T = TypeVar("T")


@contextmanager
def flush_session(session: Session) -> None:
    """Context manager that flushes the session on exit.

    Args:
        session: Database session

    Yields:
        None

    """
    try:
        yield
        session.flush()
    except Exception:
        session.rollback()
        raise


@asynccontextmanager
async def async_flush_session(session: AsyncSession) -> None:
    """Context manager that flushes the async session on exit.

    Args:
        session: Async database session

    Yields:
        None

    """
    try:
        yield
        await session.flush()
    except Exception:
        await session.rollback()
        raise


@daosession
def get_dao_session(session: Session) -> Session:
    """Get the current database session.

    Args:
        session: Database session (injected by decorator)

    Returns:
        Session: Database session

    """
    return session


@contextmanager
def session_scope(read_only: bool = False) -> Session:
    """Provide a transactional scope around a series of operations.

    Args:
        read_only: If True, session will not be committed

    Yields:
        Session: Database session

    """
    session = db_manager.SyncSession()
    try:
        yield session
        if not read_only:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        db_manager.SyncSession.remove()


@asynccontextmanager
async def async_session_scope(read_only: bool = False) -> AsyncSession:
    """Provide an async transactional scope around a series of operations.

    Args:
        read_only: If True, session will not be committed.

    Yields:
        AsyncSession: Async database session.

    """
    async with db_manager.get_async_session() as session:
        try:
            yield session
            if not read_only:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
