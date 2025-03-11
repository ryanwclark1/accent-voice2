# helpers/db_manager.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from contextlib import asynccontextmanager, contextmanager
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    scoped_session,
    sessionmaker,
)
from sqlalchemy.types import String, TypeDecorator

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Callable

# Default configurations
DEFAULT_DB_URI = (
    "postgresql://asterisk:password123@localhost/asterisk?application_name=accent-dao"
)
DEFAULT_ASYNC_DB_URI = "postgresql+psycopg://asterisk:password123@localhost/asterisk?application_name=accent-dao-async"
DEFAULT_POOL_SIZE = 16

# Set up logging
logger = logging.getLogger(__name__)

# For regular sync operations
SyncSession = scoped_session(sessionmaker())
# For async operations
async_session_factory = None

# Type variables for generic functions
T = TypeVar("T")
R = TypeVar("R")


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    Provides utility methods for all models to inherit.
    """

    def __repr__(self) -> str:
        """Represent the model instance with its primary key values.

        Returns:
            str: String representation of the model instance.

        """
        attrs = {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.primary_key
        }
        attrs_fmt = ", ".join(f"{k}={v}" for k, v in attrs.items())
        return f"{self.__class__.__name__}({attrs_fmt})"

    def todict(self, exclude: list[str] | None = None) -> dict[str, Any]:
        """Convert SQLAlchemy model to dictionary.

        Args:
            exclude: Optional list of fields to exclude.

        Returns:
            Dictionary representation of the model.

        """
        exclude = exclude or []
        d = {}
        for c in self.__table__.columns:
            name = c.name.replace("-", "_")
            if name not in exclude:
                value = getattr(self, name)
                d[c.name] = value
        return d


# Type decorators for string conversions
class IntAsString(TypeDecorator):
    """Coerce integer->string type.

    This is needed only if the relationship() from
    string to int is writable, as SQLAlchemy will copy
    the int parent values into the string attribute
    on the child during a flush.
    """

    impl = String
    cache_ok = True

    def process_bind_param(self, value: int | str | None, dialect: Any) -> str | None:
        """Process a value before binding to the database.

        Args:
            value: The value to be processed.
            dialect: SQLAlchemy dialect.

        Returns:
            The processed value.

        """
        if value is not None:
            value = str(value)
        return value


class UUIDAsString(TypeDecorator):
    """Convert UUID to string for database storage."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """Process a value before binding to the database.

        Args:
            value: The value to be processed.
            dialect: SQLAlchemy dialect.

        Returns:
            The processed value.

        """
        if value is not None:
            value = str(value)
        return value


def daosession(func: Callable[..., R]) -> Callable[..., R]:
    """Decorator that passes a session to the decorated function.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.

    """

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> R:
        session = SyncSession()
        try:
            result = func(session, *args, **kwargs)
            return result
        finally:
            session.close()

    return wrapped


async def init_async_db(
    db_uri: str = DEFAULT_ASYNC_DB_URI, pool_size: int = DEFAULT_POOL_SIZE
) -> None:
    """Initialize the async database connection.

    Args:
        db_uri: Database connection string.
        pool_size: Connection pool size.

    """
    global async_session_factory
    engine = create_async_engine(
        db_uri, pool_size=pool_size, pool_pre_ping=True, echo=False
    )
    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


def init_db(db_uri: str = DEFAULT_DB_URI, pool_size: int = DEFAULT_POOL_SIZE) -> None:
    """Initialize the synchronous database connection.

    Args:
        db_uri: Database connection string.
        pool_size: Connection pool size.

    """
    engine = create_engine(db_uri, pool_size=pool_size, pool_pre_ping=True)
    SyncSession.configure(bind=engine)
    Base.metadata.bind = engine


def init_db_from_config(config: dict[str, Any] | None = None) -> None:
    """Initialize database from configuration.

    Args:
        config: Configuration dictionary, will be loaded from default if None.

    """
    config = config or default_config()
    url = config.get("db_uri", DEFAULT_DB_URI)
    async_url = config.get("async_db_uri", DEFAULT_ASYNC_DB_URI)

    try:
        pool_size = config["rest_api"]["max_threads"]
    except KeyError:
        pool_size = DEFAULT_POOL_SIZE

    init_db(url, pool_size=pool_size)
    # Note: async_db init should be handled separately with await


def default_config() -> dict[str, Any]:
    """Load default configuration.

    Returns:
        Configuration dictionary.

    """
    from accent.config_helper import ConfigParser, ErrorHandler

    config = {
        "config_file": "/etc/accent-dao/config.yml",
        "extra_config_files": "/etc/accent-dao/conf.d",
    }
    config_parser = ConfigParser(ErrorHandler())
    return config_parser.read_config_file_hierarchy(config)


@contextmanager
def get_session() -> Session:
    """Get a session for synchronous operations.

    Yields:
        Database session.

    """
    session = SyncSession()
    try:
        yield session
    finally:
        session.close()


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a session for asynchronous operations.

    Yields:
        Async database session.

    """
    if async_session_factory is None:
        await init_async_db()

    assert async_session_factory is not None, "Async session factory not initialized"

    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()


def async_daosession(func: Callable[..., R]) -> Callable[..., R]:
    """Decorator for async DAO operations.

    Args:
        func: Function to decorate.

    Returns:
        Decorated function with session automatically provided.

    """

    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any) -> R:
        async with get_async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapped
