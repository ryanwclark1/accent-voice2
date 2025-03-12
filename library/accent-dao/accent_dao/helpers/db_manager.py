# helpers/db_manager.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from contextlib import asynccontextmanager, contextmanager
from datetime import timedelta
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar, overload

# Import cachetools at the top
from cachetools import TTLCache, cached
from sqlalchemy import Engine, String, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
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
from sqlalchemy.types import TypeDecorator

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Callable, Generator

# Type variables for generic functions
T = TypeVar("T")
R = TypeVar("R")

# Default configurations
DEFAULT_DB_URI = (
    "postgresql://asterisk:password123@localhost/asterisk?application_name=accent-dao"
)
DEFAULT_ASYNC_DB_URI = "postgresql+psycopg://asterisk:password123@localhost/asterisk?application_name=accent-dao-async"
DEFAULT_POOL_SIZE = 16

# Default cache settings
DEFAULT_CACHE_MAXSIZE = 128
DEFAULT_CACHE_TTL = timedelta(minutes=5).total_seconds()

# Set up logging
logger = logging.getLogger(__name__)

# Engine instances
sync_engine: Engine | None = None
async_engine: AsyncEngine | None = None

# Session factories
SyncSession = scoped_session(sessionmaker())
async_session_factory: async_sessionmaker[AsyncSession] | None = None

# Create a TTL cache for database results
db_cache: TTLCache = TTLCache(maxsize=DEFAULT_CACHE_MAXSIZE, ttl=DEFAULT_CACHE_TTL)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    Provides utility methods for all models to inherit.
    """

    def __repr__(self) -> str:
        """Generate string representation of the model instance.

        Returns:
            String representation with primary key values.

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
    """Coerce integer to string type.

    This is needed only if the relationship() from
    string to int is writable, as SQLAlchemy will copy
    the int parent values into the string attribute
    on the child during a flush.
    """

    impl = String
    cache_ok = True

    def process_bind_param(
        self, value: int | str | None, dialect: Any
    ) -> str | None:
        """Process a value before binding to the database.

        Args:
            value: The value to be processed.
            dialect: SQLAlchemy dialect (not used).

        Returns:
            The processed value as string or None.

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
            dialect: SQLAlchemy dialect (not used).

        Returns:
            The processed value as string or None.

        """
        if value is not None:
            value = str(value)
        return value


def daosession(func: Callable[..., R]) -> Callable[..., R]:
    """Pass a session to the decorated function.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function with session handling.

    """

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> R:
        session = SyncSession()
        try:
            return func(session, *args, **kwargs)
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
    # Use a class for state management instead of global variables
    global async_engine, async_session_factory

    if async_engine:
        await async_engine.dispose()

    async_engine = create_async_engine(
        db_uri, pool_size=pool_size, pool_pre_ping=True, echo=False
    )

    async_session_factory = async_sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )

    logger.info("Initialized async database connection to %s", db_uri)


def init_db(db_uri: str = DEFAULT_DB_URI, pool_size: int = DEFAULT_POOL_SIZE) -> None:
    """Initialize the synchronous database connection.

    Args:
        db_uri: Database connection string.
        pool_size: Connection pool size.

    """
    global sync_engine

    if sync_engine:
        sync_engine.dispose()

    sync_engine = create_engine(db_uri, pool_size=pool_size, pool_pre_ping=True)

    SyncSession.configure(bind=sync_engine)

    # In SQLAlchemy 2.0, we use this instead of Base.metadata.bind
    if hasattr(Base, "registry"):
        Base.registry.metadata.create_all(sync_engine)

    logger.info("Initialized sync database connection to %s", db_uri)


async def init_db_from_config(config: dict[str, Any] | None = None) -> None:
    """Initialize database from configuration.

    Args:
        config: Configuration dictionary, will be loaded from default if None.

    """
    config = config or await default_config()
    url = config.get("db_uri", DEFAULT_DB_URI)
    async_url = config.get("async_db_uri", DEFAULT_ASYNC_DB_URI)

    try:
        pool_size = config["rest_api"]["max_threads"]
    except KeyError:
        pool_size = DEFAULT_POOL_SIZE

    init_db(url, pool_size=pool_size)
    await init_async_db(async_url, pool_size=pool_size)
    logger.info("Initialized database connections from config")


async def default_config() -> dict[str, Any]:
    """Load default configuration.

    Returns:
        Configuration dictionary.

    """
    # This import can't be type-checked, so we silence Mypy with TYPE_CHECKING
    from accent.config_helper import ConfigParser, ErrorHandler  # type: ignore  # noqa: PGH003

    config = {
        "config_file": "/etc/accent-dao/config.yml",
        "extra_config_files": "/etc/accent-dao/conf.d",
    }
    config_parser = ConfigParser(ErrorHandler())
    return await config_parser.read_config_file_hierarchy_async(config)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get a session for synchronous operations.

    Yields:
        Database session.

    """
    session = SyncSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
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

    # Use logging instead of assert for production code
    if async_session_factory is None:
        logger.error("Async session factory not initialized")
        raise RuntimeError("Async session factory not initialized")

    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


@overload
def async_daosession(
    func: Callable[..., Awaitable[R]],
) -> Callable[..., Awaitable[R]]: ...


@overload
def async_daosession() -> Callable[
    [Callable[..., Awaitable[R]]],
    Callable[..., Awaitable[R]],
]: ...


def async_daosession(
    func: Callable[..., Awaitable[R]] | None = None,
) -> (
    Callable[..., Awaitable[R]]
    | Callable[
        [Callable[..., Awaitable[R]]],
        Callable[..., Awaitable[R]],
    ]
):
    """Decorate async DAO operations.

    Can be used with or without arguments:
    @async_daosession
    async def func(session, ...): ...

    or

    @async_daosession()
    async def func(session, ...): ...

    Args:
        func: Function to decorate.

    Returns:
        Decorated function with session automatically provided.

    """

    def decorator(
        fn: Callable[..., Awaitable[R]],
    ) -> Callable[..., Awaitable[R]]:
        @wraps(fn)
        async def wrapped(*args: Any, **kwargs: Any) -> R:
            async with get_async_session() as session:
                return await fn(session, *args, **kwargs)

        return wrapped

    if func is None:
        return decorator

    return decorator(func)


def cached_query(
    maxsize: int = DEFAULT_CACHE_MAXSIZE, ttl: float = DEFAULT_CACHE_TTL
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Create a caching decorator for database queries.

    Args:
        maxsize: Maximum size of the cache.
        ttl: Time-to-live for cache entries in seconds.

    Returns:
        A decorator that caches function results.

    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        cache: TTLCache = TTLCache(maxsize=maxsize, ttl=ttl)

        @cached(cache)
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> R:
            return func(*args, **kwargs)

        return wrapped

    return decorator

