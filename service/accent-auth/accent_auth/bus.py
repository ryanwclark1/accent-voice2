# accent_auth/dependencies.py
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db.engine import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a new async database session per request.

    Yields:
        AsyncSession: An asynchronous database session.

    Raises:
        Exception: If any error occurs during commit or rollback.

    Closes the session after yielding it.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
