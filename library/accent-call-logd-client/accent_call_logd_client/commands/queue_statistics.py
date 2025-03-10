# Copyright 2025 Accent Communications

"""Queue statistics commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class QueueStatisticsCommand(BaseCommand):
    """Command for queue statistics operations."""

    async def get_by_id_async(self, queue_id: str, **params: Any) -> dict[str, Any]:
        """Get statistics for a specific queue asynchronously.

        Args:
            queue_id: The queue identifier
            **params: Additional query parameters

        Returns:
            Queue statistics data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("queues", queue_id, "statistics")
        logger.debug("Fetching queue statistics for: %s", queue_id)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get_by_id(self, queue_id: str, **params: Any) -> dict[str, Any]:
        """Get statistics for a specific queue.

        Args:
            queue_id: The queue identifier
            **params: Additional query parameters

        Returns:
            Queue statistics data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("queues", queue_id, "statistics")
        logger.debug("Fetching queue statistics for: %s", queue_id)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def list_async(self, **params: Any) -> dict[str, Any]:
        """List statistics for all queues asynchronously.

        Args:
            **params: Query parameters

        Returns:
            Queue statistics data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("queues", "statistics")
        logger.debug("Listing queue statistics")

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list(self, **params: Any) -> dict[str, Any]:
        """List statistics for all queues.

        Args:
            **params: Query parameters

        Returns:
            Queue statistics data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("queues", "statistics")
        logger.debug("Listing queue statistics")

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def get_qos_by_id_async(self, queue_id: str, **params: Any) -> dict[str, Any]:
        """Get QoS statistics for a specific queue asynchronously.

        Args:
            queue_id: The queue identifier
            **params: Additional query parameters

        Returns:
            QoS statistics data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("queues", queue_id, "statistics", "qos")
        logger.debug("Fetching QoS statistics for queue: %s", queue_id)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get_qos_by_id(self, queue_id: str, **params: Any) -> dict[str, Any]:
        """Get QoS statistics for a specific queue.

        Args:
            queue_id: The queue identifier
            **params: Additional query parameters

        Returns:
            QoS statistics data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("queues", queue_id, "statistics", "qos")
        logger.debug("Fetching QoS statistics for queue: %s", queue_id)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()
