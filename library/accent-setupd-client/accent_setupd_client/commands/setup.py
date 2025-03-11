# Copyright 2025 Accent Communications

"""Setup commands for Setupd client."""

from __future__ import annotations

import logging
import time
from typing import Any

from accent_setupd_client.command import SetupdCommand

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 60.0


class SetupCommand(SetupdCommand):
    """Command for managing setup operations."""

    resource = "setup"
    _headers = {"Content-Type": "application/json", "Accept": "application/json"}

    async def create_async(
        self, body: dict[str, Any], timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        """Create a new setup task asynchronously.

        Args:
            body: Setup configuration data
            timeout: Request timeout in seconds

        """
        headers = self._get_headers()
        logger.info("Creating setup task")
        logger.debug("Setup data: %s", body)

        start_time = logger.isEnabledFor(logging.DEBUG) and time.time()

        response = await self.async_client.post(
            self.base_url, json=body, headers=headers, timeout=timeout
        )
        self.raise_from_response(response)

        if start_time:
            logger.debug("Setup task created in %.2fs", time.time() - start_time)

    def create(self, body: dict[str, Any], timeout: float = DEFAULT_TIMEOUT) -> None:
        """Create a new setup task.

        Args:
            body: Setup configuration data
            timeout: Request timeout in seconds

        """
        headers = self._get_headers()
        logger.info("Creating setup task")
        logger.debug("Setup data: %s", body)

        start_time = logger.isEnabledFor(logging.DEBUG) and time.time()

        response = self.sync_client.post(
            self.base_url, json=body, headers=headers, timeout=timeout
        )
        self.raise_from_response(response)

        if start_time:
            logger.debug("Setup task created in %.2fs", time.time() - start_time)
