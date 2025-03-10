# Copyright 2025 Accent Communications

"""Configuration commands for AMID API.

This module defines the commands for managing AMID configuration.
"""

from __future__ import annotations

import logging

from accent_amid_client.command import AmidCommand
from accent_amid_client.models import JSON

logger = logging.getLogger(__name__)


class ConfigCommand(AmidCommand):
    """Command for managing AMID configuration."""

    resource = "config"

    def __call__(self) -> JSON:
        """Get the current AMID configuration synchronously.

        Returns:
            Current configuration

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Getting AMID configuration")
        headers = self._get_headers()
        url = self.base_url

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def async_call(self) -> JSON:
        """Get the current AMID configuration asynchronously.

        Returns:
            Current configuration

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Async getting AMID configuration")
        headers = self._get_headers()
        url = self.base_url

        r = await self.async_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def patch(self, config_patch: dict[str, JSON]) -> JSON:
        """Update the AMID configuration synchronously.

        Args:
            config_patch: Configuration values to update

        Returns:
            Updated configuration

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Patching AMID configuration: %s", config_patch)
        headers = self._get_headers()

        r = self.sync_client.patch(self.base_url, headers=headers, json=config_patch)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def async_patch(self, config_patch: dict[str, JSON]) -> JSON:
        """Update the AMID configuration asynchronously.

        Args:
            config_patch: Configuration values to update

        Returns:
            Updated configuration

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Async patching AMID configuration: %s", config_patch)
        headers = self._get_headers()

        r = await self.async_client.patch(
            self.base_url, headers=headers, json=config_patch
        )

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
