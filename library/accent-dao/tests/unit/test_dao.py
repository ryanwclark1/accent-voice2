# Copyright 2025 Accent Communications

import asyncio
import datetime
import itertools
import logging
import os
import random
import string
import uuid

import pytest
from accent_dao.helpers.db_manager import Base, get_async_session, init_async_db
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

TEST_DB_URL = os.getenv(
    "ACCENT_TEST_DB_URL",
    "postgresql+asyncpg://asterisk:asterisk@localhost/asterisktest",
)
DEFAULT_TENANT = "4dc2a55e-e83a-42ca-b3ca-87d3ff04ddaf"
UNKNOWN_ID = 999999999
UNKNOWN_UUID = "99999999-9999-4999-8999-999999999999"


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Initialize the async database before tests run."""
    await init_async_db(TEST_DB_URL)

    async with get_async_session() as session:
        async with session.begin():
            conn = await session.connection()
            await conn.run_sync(Base.metadata.create_all)

    yield  # Run tests

    async with get_async_session() as session:
        async with session.begin():
            conn = await session.connection()
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session():
    """Provide an async session per test with transaction rollback."""
    async with get_async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()


class AsyncItemInserter:
    """Provides helper methods for inserting test data into the database."""

    def __init__(self, session: AsyncSession, tenant_uuid: str = None):
        self.session = session
        self.default_tenant_uuid = tenant_uuid or DEFAULT_TENANT

    async def add_user(self, **kwargs):
        """Add a test user to the database."""
        from accent_dao.alchemy.userfeatures import UserFeatures

        kwargs.setdefault("id", self._generate_int())
        kwargs.setdefault("tenant_uuid", self.default_tenant_uuid)
        kwargs.setdefault("firstname", "John")

        fullname = kwargs["firstname"]
        if "lastname" in kwargs:
            fullname += " " + kwargs["lastname"]

        kwargs.setdefault("callerid", f'"{fullname}"')

        user = UserFeatures(**kwargs)
        self.session.add(user)
        await self.session.flush()
        return user

    async def add_tenant(self, **kwargs):
        """Add a test tenant."""
        from accent_dao.alchemy.tenant import Tenant

        tenant = Tenant(**kwargs)
        self.session.add(tenant)
        await self.session.flush()
        return tenant

    async def add_agent(self, **kwargs):
        """Add a test agent."""
        from accent_dao.alchemy.agentfeatures import AgentFeatures

        kwargs.setdefault("id", self._generate_int())
        kwargs.setdefault(
            "number", "".join(random.choice("123456789") for _ in range(6))
        )
        kwargs.setdefault("passwd", "")
        kwargs.setdefault("language", random.choice(["fr_FR", "en_US"]))
        kwargs.setdefault("description", "description")
        kwargs.setdefault("tenant_uuid", self.default_tenant_uuid)

        agent = AgentFeatures(**kwargs)
        self.session.add(agent)
        await self.session.flush()
        return agent

    def _generate_int(self):
        """Generate an incremental integer ID."""
        return next(self._generate_int_init)

    def _generate_uuid(self):
        """Generate a random UUID."""
        return str(uuid.uuid4())

    _generate_int_init = itertools.count(1)


@pytest.mark.asyncio
class DAOTestCase:
    """Base class for async DAO test cases."""

    @pytest.fixture(autouse=True)
    async def setup_test(self, async_session):
        """Setup each test with an isolated session."""
        self.session = async_session
        self.inserter = AsyncItemInserter(async_session)

        # Add a default tenant for test isolation
        self.default_tenant = await self.inserter.add_tenant(uuid=DEFAULT_TENANT)

        @event.listens_for(self.session.sync_session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.expire_all()
                session.begin_nested()

    async def teardown_test(self):
        """Rollback transactions after each test."""
        await self.session.rollback()
