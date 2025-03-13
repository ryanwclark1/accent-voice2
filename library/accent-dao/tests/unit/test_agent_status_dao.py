# Copyright 2025 Accent Communications

import pytest
from sqlalchemy.future import select
from accent_dao import agent_status_dao
from accent_dao.alchemy.agent_login_status import AgentLoginStatus
from accent_dao.alchemy.agent_membership_status import AgentMembershipStatus
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.alchemy.queuemember import QueueMember
from .test_dao import UNKNOWN_UUID, AsyncDAOTestCase


@pytest.mark.asyncio
class TestAgentStatusDao(AsyncDAOTestCase):
    async def test_log_in_agent(self, async_session):
        """Test logging in an agent and verifying login status."""
        agent_id = 1
        agent_number = "2"
        extension = "1001"
        context = "default"
        interface = "sip/abcdef"
        paused = False
        paused_reason = None
        state_interface = interface

        agent = await self.inserter.add_agent(id=agent_id, number=agent_number)
        user = await self.inserter.add_user(agentid=agent.id)

        await agent_status_dao.log_in_agent(
            async_session,
            agent_id,
            agent_number,
            extension,
            context,
            interface,
            paused,
            paused_reason,
            state_interface,
        )

        result = await async_session.execute(
            select(AgentLoginStatus).where(AgentLoginStatus.agent_id == agent_id)
        )
        login_status = result.scalar_one_or_none()

        assert login_status is not None
        assert login_status.agent_id == agent_id
        assert login_status.agent_number == agent_number
        assert login_status.extension == extension
        assert login_status.context == context
        assert login_status.interface == interface
        assert login_status.paused == paused
        assert login_status.paused_reason == paused_reason
        assert login_status.state_interface == state_interface

    async def test_log_out_agent(self, async_session):
        """Test logging out an agent and ensuring login status is removed."""
        agent = await self.inserter.add_agent()
        await agent_status_dao.log_in_agent(
            async_session,
            agent.id,
            "2",
            "1001",
            "default",
            "sip/abcdef",
            False,
            None,
            "sip/abcdef",
        )

        await agent_status_dao.log_out_agent(async_session, agent.id)

        result = await async_session.execute(
            select(AgentLoginStatus).where(AgentLoginStatus.agent_id == agent.id)
        )
        login_status = result.scalar_one_or_none()

        assert login_status is None

    async def test_get_agent_login_status(self, async_session):
        """Test retrieving an agent's login status."""
        agent = await self.inserter.add_agent()
        await agent_status_dao.log_in_agent(
            async_session,
            agent.id,
            "2",
            "1001",
            "default",
            "sip/abcdef",
            False,
            None,
            "sip/abcdef",
        )

        login_status = await agent_status_dao.get_agent_login_status(
            async_session, agent.id
        )

        assert login_status is not None
        assert login_status.agent_id == agent.id
        assert login_status.agent_number == "2"

    async def test_get_agent_login_status_not_found(self, async_session):
        """Test retrieving a login status for an agent that does not exist."""
        login_status = await agent_status_dao.get_agent_login_status(
            async_session, UNKNOWN_UUID
        )
        assert login_status is None

    async def test_update_agent_login_status(self, async_session):
        """Test updating an agent's login status."""
        agent = await self.inserter.add_agent()
        await agent_status_dao.log_in_agent(
            async_session,
            agent.id,
            "2",
            "1001",
            "default",
            "sip/abcdef",
            False,
            None,
            "sip/abcdef",
        )

        await agent_status_dao.update_agent_login_status(
            async_session, agent.id, paused=True, paused_reason="Break"
        )

        result = await async_session.execute(
            select(AgentLoginStatus).where(AgentLoginStatus.agent_id == agent.id)
        )
        login_status = result.scalar_one_or_none()

        assert login_status is not None
        assert login_status.paused is True
        assert login_status.paused_reason == "Break"
