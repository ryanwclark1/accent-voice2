# src/accent_chatd/core/database.py
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from accent_chatd.core.config import get_settings

settings = get_settings()

# Create an async engine for SQLAlchemy
engine = create_async_engine(
    settings.db_uri.replace("postgresql://", "postgresql+asyncpg://", 1),
    echo=settings.db_echo,
    future=True,  # Use the 2.0 style engine (recommended)
)

# Create an async session maker
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.

    """

    @declared_attr
    def __tablename__(cls) -> str:
        return f"chatd_{cls.__name__.lower()}"  # Following the original naming scheme.

    id = Column(Integer, primary_key=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get an async database session.
    
    This function provides a database session for each request, and ensures
    it's closed after the request is completed.  It uses `yield` to provide
    the session, and the code after the `yield` runs after the request is
    finished.
    """
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
