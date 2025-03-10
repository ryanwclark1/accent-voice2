# Copyright 2025 Accent Communications

"""Command execution for AMID API.

This module defines the command for executing raw commands on the AMID API.
"""

from __future__ import annotations

import logging

from accent_amid_client.command import AmidCommand
from accent_amid_client.models import JSON

logger = logging.getLogger(__name__)


class CommandCommand(AmidCommand):
    """Command for executing raw commands on the AMID API."""

    resource = "action"

    def __call__(self, command: str) -> JSON:
        """Execute a raw AMID command synchronously.

        Args:
            command: The command to execute

        Returns:
            Command execution result

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Executing command: %s", command)
        body = {"command": command}
        url = f"{self.base_url}/Command"

        r = self.sync_client.post(url, json=body)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def async_call(self, command: str) -> JSON:
        """Execute a raw AMID command asynchronously.

        Args:
            command: The command to execute

        Returns:
            Command execution result

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Async executing command: %s", command)
        body = {"command": command}
        url = f"{self.base_url}/Command"

        r = await self.async_client.post(url, json=body)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
