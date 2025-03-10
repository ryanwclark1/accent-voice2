# Copyright 2025 Accent Communications

"""Wizard command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class WizardCommand(HTTPCommand):
    """Command for managing the wizard."""

    resource = "wizard"

    def create(self, body: dict[str, Any], timeout: int = 300) -> dict[str, Any]:
        """Create wizard configuration.

        Args:
            body: Wizard configuration
            timeout: Request timeout in seconds

        Returns:
            Created configuration

        """
        url = url_join(self.resource)
        response = self.sync_client.post(url, json=body, timeout=timeout)
        response.raise_for_status()
        return response.json()

    async def create_async(
        self, body: dict[str, Any], timeout: int = 300
    ) -> dict[str, Any]:
        """Create wizard configuration asynchronously.

        Args:
            body: Wizard configuration
            timeout: Request timeout in seconds

        Returns:
            Created configuration

        """
        url = url_join(self.resource)
        response = await self.async_client.post(url, json=body, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def get(self) -> dict[str, Any]:
        """Get wizard configuration.

        Returns:
            Wizard configuration

        """
        url = url_join(self.resource)
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get wizard configuration asynchronously.

        Returns:
            Wizard configuration

        """
        url = url_join(self.resource)
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()

    def discover(self) -> dict[str, Any]:
        """Discover wizard configuration.

        Returns:
            Discovered configuration

        """
        url = url_join(self.resource, "discover")
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def discover_async(self) -> dict[str, Any]:
        """Discover wizard configuration asynchronously.

        Returns:
            Discovered configuration

        """
        url = url_join(self.resource, "discover")
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()

    def __call__(self) -> dict[str, Any]:
        """Call the command as a function.

        Returns:
            Wizard configuration

        """
        return self.get()

    async def __call_async__(self) -> dict[str, Any]:
        """Call the command as a function asynchronously.

        Returns:
            Wizard configuration

        """
        return await self.get_async()
