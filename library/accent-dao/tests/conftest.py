import asyncio

import pytest
from accent_dao.helpers.db_manager import (
    DEFAULT_ASYNC_DB_URI,
    Base,
    async_session_factory,
    get_async_session,
    init_async_db,
)
from sqlalchemy.ext.asyncio import AsyncSession


# Ensure pytest-asyncio uses the correct event loop policy
@pytest.fixture(scope="session")
def event_loop():
    """Override pytest default function-scoped event loop to session scope."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Initialize the async database for testing."""
    await init_async_db(db_uri=DEFAULT_ASYNC_DB_URI)

    # Create tables in the test database
    async with async_session_factory() as session:
        async with session.begin():
            conn = await session.connection()
            await conn.run_sync(Base.metadata.create_all)

    yield  # Run tests

    # Drop tables after tests
    async with async_session_factory() as session:
        async with session.begin():
            conn = await session.connection()
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session():
    """Provide an async database session for tests with rollback."""
    async with get_async_session() as session:
        yield session
        await session.rollback()  # Ensure isolation between tests
