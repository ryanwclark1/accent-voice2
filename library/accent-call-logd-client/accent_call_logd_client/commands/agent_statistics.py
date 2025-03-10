# Copyright 2025 Accent Communications

"""Agent statistics commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class AgentStatisticsCommand(BaseCommand):
    """Command for agent statistics operations."""

    async def get_by_id_async(self, agent_id: str, **params: Any) -> dict[str, Any]:
        """Get statistics for a specific agent asynchronously.

        Args:
            agent_id: The agent identifier
            **params: Additional query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("agents", agent_id, "statistics")
        logger.debug("Fetching agent statistics for: %s", agent_id)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get_by_id(self, agent_id: str, **params: Any) -> dict[str, Any]:
        """Get statistics for a specific agent.

        Args:
            agent_id: The agent identifier
            **params: Additional query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("agents", agent_id, "statistics")
        logger.debug("Fetching agent statistics for: %s", agent_id)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def list_async(self, **params: Any) -> dict[str, Any]:
        """List statistics for all agents asynchronously.

        Args:
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("agents", "statistics")
        logger.debug("Listing agent statistics")

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list(self, **params: Any) -> dict[str, Any]:
        """List statistics for all agents.

        Args:
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("agents", "statistics")
        logger.debug("Listing agent statistics")

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()
