# Copyright 2025 Accent Communications

import pytest
from sqlalchemy.future import select
from accent_dao import queue_dao
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.alchemy.queuemember import QueueMember
from .test_dao import UNKNOWN_UUID, AsyncDAOTestCase


@pytest.mark.asyncio
class TestQueueDAO(AsyncDAOTestCase):
    async def test_create_queue(self, async_session):
        """Test creating a queue in the database."""
        queue_name = "SupportQueue"

        await queue_dao.create_queue(async_session, queue_name)

        result = await async_session.execute(
            select(QueueFeatures).where(QueueFeatures.name == queue_name)
        )
        queue = result.scalar_one_or_none()

        assert queue is not None
        assert queue.name == queue_name

    async def test_get_queue_by_id(self, async_session):
        """Test retrieving a queue by its ID."""
        queue = await self.inserter.add_queue(name="SalesQueue")

        result = await queue_dao.get_queue_by_id(async_session, queue.id)

        assert result is not None
        assert result.id == queue.id
        assert result.name == "SalesQueue"

    async def test_get_queue_by_unknown_id_returns_none(self, async_session):
        """Test retrieving a queue with an unknown ID returns None."""
        result = await queue_dao.get_queue_by_id(async_session, UNKNOWN_UUID)
        assert result is None

    async def test_list_queues(self, async_session):
        """Test listing all queues."""
        queue1 = await self.inserter.add_queue(name="Queue1")
        queue2 = await self.inserter.add_queue(name="Queue2")

        result = await queue_dao.list_queues(async_session)

        assert len(result) == 2
        assert result[0].id == queue1.id
        assert result[1].id == queue2.id

    async def test_add_queue_member(self, async_session):
        """Test adding a member to a queue."""
        queue = await self.inserter.add_queue(name="TechSupport")
        agent = await self.inserter.add_agent()

        await queue_dao.add_queue_member(async_session, queue.id, agent.id)

        result = await async_session.execute(
            select(QueueMember).where(QueueMember.queue_name == queue.name)
        )
        queue_member = result.scalar_one_or_none()

        assert queue_member is not None
        assert queue_member.queue_name == queue.name
        assert queue_member.userid == agent.id

    async def test_remove_queue_member(self, async_session):
        """Test removing a queue member."""
        queue = await self.inserter.add_queue(name="HelpDesk")
        agent = await self.inserter.add_agent()

        await queue_dao.add_queue_member(async_session, queue.id, agent.id)
        await queue_dao.remove_queue_member(async_session, queue.id, agent.id)

        result = await async_session.execute(
            select(QueueMember).where(QueueMember.queue_name == queue.name)
        )
        queue_member = result.scalar_one_or_none()

        assert queue_member is None
