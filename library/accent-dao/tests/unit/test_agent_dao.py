# Copyright 2025 Accent Communications

import pytest
from accent_dao import agent_dao
from accent_dao.alchemy.queuemember import QueueMember
from .test_dao import UNKNOWN_UUID, AsyncDAOTestCase


@pytest.mark.asyncio
class TestAgentDAO(AsyncDAOTestCase):
    agent_number = "1234"
    agent1_number = "1001"
    agent2_number = "1002"
    agent_context = "test"

    async def test_agent_with_id(self, async_session):
        """Test retrieving an agent by ID with queue membership."""
        agent = await self.add_agent(async_session)
        user = await self.add_user(async_session, agentid=agent.id)
        queue_member = await self._insert_queue_member(
            async_session, "foobar", "Agent/2", agent.id
        )
        queue = await self.add_queuefeatures(
            async_session, id=64, name=queue_member.queue_name
        )

        result = await agent_dao.agent_with_id(async_session, agent.id)

        assert result is not None
        assert result.id == agent.id
        assert result.number == agent.number
        assert len(result.queues) == 1
        assert result.queues[0].id == queue.id
        assert result.queues[0].name == queue_member.queue_name

    async def test_agent_with_unknown_id_returns_none(self, async_session):
        """Test retrieving an agent with an unknown ID returns None."""
        result = await agent_dao.agent_with_id(async_session, UNKNOWN_UUID)
        assert result is None

    async def test_list_agents(self, async_session):
        """Test listing all agents."""
        agent1 = await self.add_agent(async_session, number=self.agent1_number)
        agent2 = await self.add_agent(async_session, number=self.agent2_number)

        result = await agent_dao.list_agents(async_session)

        assert len(result) == 2
        assert result[0].id == agent1.id
        assert result[1].id == agent2.id

    async def test_list_agents_empty(self, async_session):
        """Test listing agents when there are none."""
        result = await agent_dao.list_agents(async_session)
        assert result == []
