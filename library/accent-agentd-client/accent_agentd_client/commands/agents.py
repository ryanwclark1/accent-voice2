# Copyright 2025 Accent Communications

"""Agent management commands for the Accent Agent Daemon client."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from accent_lib_rest_client import RESTCommand

from accent_agentd_client.helpers import ResponseProcessor
from accent_agentd_client.models import (
    AgentStatus,
    LoginRequest,
    QueueRequest,
    UserAgentLoginRequest,
)

# Configure logging
logger = logging.getLogger(__name__)

class AgentsCommand(RESTCommand):
    """Command for managing agents."""

    resource = "agents"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the agents command.

        Args:
            *args: Positional arguments passed to RESTCommand
            **kwargs: Keyword arguments passed to RESTCommand

        """
        super().__init__(*args, **kwargs)
        self._req_factory = _RequestFactory(self.base_url)
        self._resp_processor = ResponseProcessor()
        logger.debug("Initialized AgentsCommand")

    # Queue management methods
    def add_agent_to_queue(
        self, agent_id: str, queue_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Add an agent to a queue.

        Args:
            agent_id: Agent identifier
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Adding agent %s to queue %s", agent_id, queue_id)

        req = self._req_factory.add_to_queue_by_id(
            agent_id=agent_id, queue_id=queue_id, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def add_agent_to_queue_async(
        self, agent_id: str, queue_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Add an agent to a queue asynchronously.

        Args:
            agent_id: Agent identifier
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Adding agent %s to queue %s (async)", agent_id, queue_id)

        req = self._req_factory.add_to_queue_by_id(
            agent_id=agent_id, queue_id=queue_id, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def remove_agent_from_queue(
        self, agent_id: str, queue_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Remove an agent from a queue.

        Args:
            agent_id: Agent identifier
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Removing agent %s from queue %s", agent_id, queue_id)

        req = self._req_factory.remove_from_queue_by_id(
            agent_id=agent_id, queue_id=queue_id, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def remove_agent_from_queue_async(
        self, agent_id: str, queue_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Remove an agent from a queue asynchronously.

        Args:
            agent_id: Agent identifier
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Removing agent %s from queue %s (async)", agent_id, queue_id)

        req = self._req_factory.remove_from_queue_by_id(
            agent_id=agent_id, queue_id=queue_id, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    # Agent login methods
    def login_agent(
        self,
        agent_id: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None
    ) -> None:
        """Log in an agent.

        Args:
            agent_id: Agent identifier
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging in agent %s at extension %s", agent_id, extension)

        req = self._req_factory.login_by_id(
            agent_id=agent_id,
            extension=extension,
            context=context,
            tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def login_agent_async(
        self,
        agent_id: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None
    ) -> None:
        """Log in an agent asynchronously.

        Args:
            agent_id: Agent identifier
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging in agent %s at extension %s (async)", agent_id, extension)

        req = self._req_factory.login_by_id(
            agent_id=agent_id,
            extension=extension,
            context=context,
            tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def login_agent_by_number(
        self,
        agent_number: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None
    ) -> None:
        """Log in an agent by number.

        Args:
            agent_number: Agent number
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging in agent number %s at extension %s", agent_number, extension)

        req = self._req_factory.login_by_number(
            agent_number=agent_number,
            extension=extension,
            context=context,
            tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def login_agent_by_number_async(
        self,
        agent_number: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None
    ) -> None:
        """Log in an agent by number asynchronously.

        Args:
            agent_number: Agent number
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging in agent number %s at extension %s (async)", agent_number, extension)

        req = self._req_factory.login_by_number(
            agent_number=agent_number,
            extension=extension,
            context=context,
            tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def login_user_agent(
        self, line_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Log in a user agent.

        Args:
            line_id: Line identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging in user agent on line %s", line_id)

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.login_user_agent(
            line_id=line_id, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def login_user_agent_async(
        self, line_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Log in a user agent asynchronously.

        Args:
            line_id: Line identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging in user agent on line %s (async)", line_id)

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.login_user_agent(
            line_id=line_id, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    # Agent logoff methods
    def logoff_agent(
        self, agent_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Log off an agent.

        Args:
            agent_id: Agent identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off agent %s", agent_id)

        req = self._req_factory.logoff_by_id(
            agent_id=agent_id, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def logoff_agent_async(
        self, agent_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Log off an agent asynchronously.

        Args:
            agent_id: Agent identifier
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off agent %s (async)", agent_id)

        req = self._req_factory.logoff_by_id(
            agent_id=agent_id, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def logoff_agent_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> None:
        """Log off an agent by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off agent number %s", agent_number)

        req = self._req_factory.logoff_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def logoff_agent_by_number_async(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> None:
        """Log off an agent by number asynchronously.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off agent number %s (async)", agent_number)

        req = self._req_factory.logoff_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def logoff_user_agent(self, tenant_uuid: str | None = None) -> None:
        """Log off a user agent.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off user agent")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.logoff_user_agent(tenant_uuid=tenant_uuid)

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def logoff_user_agent_async(self, tenant_uuid: str | None = None) -> None:
        """Log off a user agent asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off user agent (async)")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.logoff_user_agent(tenant_uuid=tenant_uuid)

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def logoff_all_agents(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> None:
        """Log off all agents.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively log off agents in subtenants

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off all agents (recurse=%s)", recurse)

        req = self._req_factory.logoff_all(
            tenant_uuid=tenant_uuid, recurse=recurse
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def logoff_all_agents_async(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> None:
        """Log off all agents asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively log off agents in subtenants

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Logging off all agents (recurse=%s, async)", recurse)

        req = self._req_factory.logoff_all(
            tenant_uuid=tenant_uuid, recurse=recurse
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def relog_all_agents(
        self,
        tenant_uuid: str | None = None,
        recurse: bool = False,
        timeout: float | None = None
    ) -> None:
        """Relog all agents.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively relog agents in subtenants
            timeout: Request timeout in seconds (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        timeout = timeout if timeout is not None else self.timeout
        logger.info("Relogging all agents (recurse=%s)", recurse)

        req = self._req_factory.relog_all(
            tenant_uuid=tenant_uuid, recurse=recurse
        )

        resp = self.sync_client.send(req, timeout=timeout)
        self._resp_processor.generic(resp)

    async def relog_all_agents_async(
        self,
        tenant_uuid: str | None = None,
        recurse: bool = False,
        timeout: float | None = None
    ) -> None:
        """Relog all agents asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively relog agents in subtenants
            timeout: Request timeout in seconds (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        timeout = timeout if timeout is not None else self.timeout
        logger.info("Relogging all agents (recurse=%s, async)", recurse)

        req = self._req_factory.relog_all(
            tenant_uuid=tenant_uuid, recurse=recurse
        )

        resp = await self.async_client.send(req, timeout=timeout)
        await self._resp_processor.generic_async(resp)

    # Agent pause methods
    def pause_agent_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> None:
        """Pause an agent by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Pausing agent number %s", agent_number)

        req = self._req_factory.pause_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def pause_agent_by_number_async(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> None:
        """Pause an agent by number asynchronously.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Pausing agent number %s (async)", agent_number)

        req = self._req_factory.pause_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def pause_user_agent(self, tenant_uuid: str | None = None) -> None:
        """Pause a user agent.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Pausing user agent")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.pause_user_agent(tenant_uuid=tenant_uuid)

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def pause_user_agent_async(self, tenant_uuid: str | None = None) -> None:
        """Pause a user agent asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Pausing user agent (async)")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.pause_user_agent(tenant_uuid=tenant_uuid)

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def unpause_agent_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> None:
        """Unpause an agent by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Unpausing agent number %s", agent_number)

        req = self._req_factory.unpause_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def unpause_agent_by_number_async(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> None:
        """Unpause an agent by number asynchronously.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Unpausing agent number %s (async)", agent_number)

        req = self._req_factory.unpause_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    def unpause_user_agent(self, tenant_uuid: str | None = None) -> None:
        """Unpause a user agent.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Unpausing user agent")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.unpause_user_agent(tenant_uuid=tenant_uuid)

        resp = self.sync_client.send(req)
        self._resp_processor.generic(resp)

    async def unpause_user_agent_async(self, tenant_uuid: str | None = None) -> None:
        """Unpause a user agent asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Unpausing user agent (async)")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.unpause_user_agent(tenant_uuid=tenant_uuid)

        resp = await self.async_client.send(req)
        await self._resp_processor.generic_async(resp)

    # Agent status methods
    def get_agent_status(
        self, agent_id: str, tenant_uuid: str | None = None
    ) -> AgentStatus:
        """Get an agent's status.

        Args:
            agent_id: Agent identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting status for agent %s", agent_id)

        req = self._req_factory.status_by_id(agent_id=agent_id, tenant_uuid=tenant_uuid)

        resp = self.sync_client.send(req)
        return self._resp_processor.status(resp)

    async def get_agent_status_async(
        self, agent_id: str, tenant_uuid: str | None = None
    ) -> AgentStatus:
        """Get an agent's status asynchronously.

        Args:
            agent_id: Agent identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting status for agent %s (async)", agent_id)

        req = self._req_factory.status_by_id(agent_id=agent_id, tenant_uuid=tenant_uuid)

        resp = await self.async_client.send(req)
        return await self._resp_processor.status_async(resp)

    def get_agent_status_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> AgentStatus:
        """Get an agent's status by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting status for agent number %s", agent_number)

        req = self._req_factory.status_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = self.sync_client.send(req)
        return self._resp_processor.status(resp)

    async def get_agent_status_by_number_async(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> AgentStatus:
        """Get an agent's status by number asynchronously.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting status for agent number %s (async)", agent_number)

        req = self._req_factory.status_by_number(
            agent_number=agent_number, tenant_uuid=tenant_uuid
        )

        resp = await self.async_client.send(req)
        return await self._resp_processor.status_async(resp)

    def get_user_agent_status(self, tenant_uuid: str | None = None) -> AgentStatus:
        """Get a user agent's status.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting user agent status")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.status_user_agent(tenant_uuid=tenant_uuid)

        resp = self.sync_client.send(req)
        return self._resp_processor.status(resp)

    async def get_user_agent_status_async(
        self, tenant_uuid: str | None = None
    ) -> AgentStatus:
        """Get a user agent's status asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting user agent status (async)")

        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.status_user_agent(tenant_uuid=tenant_uuid)

        resp = await self.async_client.send(req)
        return await self._resp_processor.status_async(resp)

    def get_agent_statuses(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> list[AgentStatus]:
        """Get statuses for all agents.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively get statuses for agents in subtenants

        Returns:
            List of agent statuses

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting all agent statuses (recurse=%s)", recurse)

        req = self._req_factory.status_all(tenant_uuid=tenant_uuid, recurse=recurse)

        resp = self.sync_client.send(req)
        return self._resp_processor.status_all(resp)

    async def get_agent_statuses_async(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> list[AgentStatus]:
        """Get statuses for all agents asynchronously.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively get statuses for agents in subtenants

        Returns:
            List of agent statuses

        Raises:
            AgentdClientError: If the operation fails

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        logger.info("Getting all agent statuses (recurse=%s, async)", recurse)

        req = self._req_factory.status_all(tenant_uuid=tenant_uuid, recurse=recurse)

        resp = await self.async_client.send(req)
        return await self._resp_processor.status_all_async(resp)

class _RequestFactory:
    """Factory for creating HTTP requests."""

    def __init__(self, base_url: str) -> None:
        """Initialize the request factory.

        Args:
            base_url: Base URL for requests

        """
        self._base_url = base_url
        self._headers = {"Accept": "application/json"}

    # Queue methods
    def add_to_queue_by_id(
        self, agent_id: str, queue_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to add an agent to a queue by ID.

        Args:
            agent_id: Agent identifier
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._add_to_queue("by-id", agent_id, queue_id, tenant_uuid=tenant_uuid)

    def _add_to_queue(
        self, by: str, value: str, queue_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to add an agent to a queue.

        Args:
            by: Identifier type
            value: Identifier value
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}/add"
        obj = QueueRequest(queue_id=queue_id)
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(
            url, obj.model_dump(), additional_headers=additional_headers
        )

    def remove_from_queue_by_id(
        self, agent_id: str, queue_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to remove an agent from a queue by ID.

        Args:
            agent_id: Agent identifier
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._remove_from_queue(
            "by-id", agent_id, queue_id, tenant_uuid=tenant_uuid
        )

    def _remove_from_queue(
        self, by: str, value: str, queue_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to remove an agent from a queue.

        Args:
            by: Identifier type
            value: Identifier value
            queue_id: Queue identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}/remove"
        obj = QueueRequest(queue_id=queue_id)
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(
            url, obj.model_dump(), additional_headers=additional_headers
        )

    # Login methods
    def login_by_id(
        self,
        agent_id: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None,
    ) -> httpx.Request:
        """Create a request to log in an agent by ID.

        Args:
            agent_id: Agent identifier
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._login(
            "by-id", agent_id, extension, context, tenant_uuid=tenant_uuid
        )

    def login_by_number(
        self,
        agent_number: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None,
    ) -> httpx.Request:
        """Create a request to log in an agent by number.

        Args:
            agent_number: Agent number
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._login(
            "by-number", agent_number, extension, context, tenant_uuid=tenant_uuid
        )

    def _login(
        self,
        by: str,
        value: str,
        extension: str,
        context: str,
        tenant_uuid: str | None = None,
    ) -> httpx.Request:
        """Create a request to log in an agent.

        Args:
            by: Identifier type
            value: Identifier value
            extension: Extension number
            context: Context
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}/login"
        obj = LoginRequest(extension=extension, context=context)
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(
            url, obj.model_dump(), additional_headers=additional_headers
        )

    def login_user_agent(
        self, line_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to log in a user agent.

        Args:
            line_id: Line identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/users/me/agents/login"
        obj = UserAgentLoginRequest(line_id=line_id)
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(
            url, obj.model_dump(), additional_headers=additional_headers
        )

    # Logoff methods
    def logoff_by_id(
        self, agent_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to log off an agent by ID.

        Args:
            agent_id: Agent identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._logoff("by-id", agent_id, tenant_uuid=tenant_uuid)

    def logoff_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to log off an agent by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._logoff("by-number", agent_number, tenant_uuid=tenant_uuid)

    def _logoff(
        self, by: str, value: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to log off an agent.

        Args:
            by: Identifier type
            value: Identifier value
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}/logoff"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def logoff_user_agent(self, tenant_uuid: str | None = None) -> httpx.Request:
        """Create a request to log off a user agent.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/users/me/agents/logoff"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    # Pause methods
    def pause_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to pause an agent by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._pause("by-number", agent_number, tenant_uuid=tenant_uuid)

    def _pause(
        self, by: str, value: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to pause an agent.

        Args:
            by: Identifier type
            value: Identifier value
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}/pause"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def pause_user_agent(self, tenant_uuid: str | None = None) -> httpx.Request:
        """Create a request to pause a user agent.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/users/me/agents/pause"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    # Unpause methods
    def unpause_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to unpause an agent by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._unpause("by-number", agent_number, tenant_uuid=tenant_uuid)

    def _unpause(
        self, by: str, value: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to unpause an agent.

        Args:
            by: Identifier type
            value: Identifier value
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}/unpause"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def unpause_user_agent(self, tenant_uuid: str | None = None) -> httpx.Request:
        """Create a request to unpause a user agent.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/users/me/agents/unpause"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    # Status methods
    def status_by_id(
        self, agent_id: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to get an agent's status by ID.

        Args:
            agent_id: Agent identifier
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._status("by-id", agent_id, tenant_uuid=tenant_uuid)

    def status_by_number(
        self, agent_number: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to get an agent's status by number.

        Args:
            agent_number: Agent number
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        return self._status("by-number", agent_number, tenant_uuid=tenant_uuid)

    def _status(
        self, by: str, value: str, tenant_uuid: str | None = None
    ) -> httpx.Request:
        """Create a request to get an agent's status.

        Args:
            by: Identifier type
            value: Identifier value
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/{by}/{value}"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_get_request(url, additional_headers=additional_headers)

    def status_user_agent(self, tenant_uuid: str | None = None) -> httpx.Request:
        """Create a request to get a user agent's status.

        Args:
            tenant_uuid: Tenant UUID (optional)

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/users/me/agents"
        additional_headers = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        return self._new_get_request(url, additional_headers=additional_headers)

    # Batch methods
    def logoff_all(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> httpx.Request:
        """Create a request to log off all agents.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively log off agents in subtenants

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/logoff"
        additional_headers = {}
        params = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        if recurse:
            params["recurse"] = "true"
        return self._new_post_request(
            url, additional_headers=additional_headers, params=params
        )

    def relog_all(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> httpx.Request:
        """Create a request to relog all agents.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively relog agents in subtenants

        Returns:
            HTTP request

        """
        url = f"{self._base_url}/relog"
        additional_headers = {}
        params = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        if recurse:
            params["recurse"] = "true"
        return self._new_post_request(
            url, additional_headers=additional_headers, params=params
        )

    def status_all(
        self, tenant_uuid: str | None = None, recurse: bool = False
    ) -> httpx.Request:
        """Create a request to get all agent statuses.

        Args:
            tenant_uuid: Tenant UUID (optional)
            recurse: Whether to recursively get statuses for agents in subtenants

        Returns:
            HTTP request

        """
        url = self._base_url
        additional_headers = {}
        params = {}
        if tenant_uuid:
            additional_headers["Accent-Tenant"] = tenant_uuid
        if recurse:
            params["recurse"] = "true"
        return self._new_get_request(
            url, additional_headers=additional_headers, params=params
        )

    # Request creation helpers
    def _new_get_request(
        self,
        url: str,
        additional_headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Request:
        """Create a new GET request.

        Args:
            url: Request URL
            additional_headers: Additional headers (optional)
            params: Query parameters (optional)

        Returns:
            HTTP request

        """
        headers = dict(self._headers)
        if additional_headers:
            headers.update(additional_headers)
        return httpx.Request("GET", url, headers=headers, params=params)

    def _new_post_request(
        self,
        url: str,
        obj: dict[str, Any] | None = None,
        additional_headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Request:
        """Create a new POST request.

        Args:
            url: Request URL
            obj: Request body (optional)
            additional_headers: Additional headers (optional)
            params: Query parameters (optional)

        Returns:
            HTTP request

        """
        headers = dict(self._headers)
        if additional_headers:
            headers.update(additional_headers)
        data = None
        if obj is not None:
            data = json.dumps(obj)
            headers["Content-Type"] = "application/json"
        return httpx.Request("POST", url, headers=headers, content=data, params=params)
