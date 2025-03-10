# Copyright 2025 Accent Communications

"""External applications command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.util import extract_name, url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class ExternalAppsCommand(MultiTenantCommand):
    """Command for managing external applications."""

    resource = "external/apps"

    @extract_name()
    def get(self, resource_id: str) -> dict[str, Any]:
        """Get an external application by name.

        Args:
            resource_id: External application name

        Returns:
            External application data

        """
        url = url_join(self.resource, resource_id)
        response = self.session.get(url)
        return response.json()

    @extract_name()
    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get an external application by name asynchronously.

        Args:
            resource_id: External application name

        Returns:
            External application data

        """
        url = url_join(self.resource, resource_id)
        response = await self.session.get_async(url)
        return response.json()

    @extract_name(pass_original=True)
    def create(self, name: str, body: dict[str, Any]) -> dict[str, Any]:
        """Create an external application.

        Args:
            name: External application name
            body: External application data

        Returns:
            Created external application data

        """
        url = url_join(self.resource, name)
        response = self.session.post(url, body)
        return response.json()

    @extract_name(pass_original=True)
    async def create_async(self, name: str, body: dict[str, Any]) -> dict[str, Any]:
        """Create an external application asynchronously.

        Args:
            name: External application name
            body: External application data

        Returns:
            Created external application data

        """
        url = url_join(self.resource, name)
        response = await self.session.post_async(url, body)
        return response.json()

    @extract_name(pass_original=True)
    def update(self, name: str, body: dict[str, Any]) -> None:
        """Update an external application.

        Args:
            name: External application name
            body: External application data

        """
        url = url_join(self.resource, name)
        body = {key: value for key, value in body.items() if key != "links"}
        self.session.put(url, body)

    @extract_name(pass_original=True)
    async def update_async(self, name: str, body: dict[str, Any]) -> None:
        """Update an external application asynchronously.

        Args:
            name: External application name
            body: External application data

        """
        url = url_join(self.resource, name)
        body = {key: value for key, value in body.items() if key != "links"}
        await self.session.put_async(url, body)

    @extract_name()
    def delete(self, resource_id: str) -> None:
        """Delete an external application.

        Args:
            resource_id: External application name

        """
        url = url_join(self.resource, resource_id)
        self.session.delete(url)

    @extract_name()
    async def delete_async(self, resource_id: str) -> None:
        """Delete an external application asynchronously.

        Args:
            resource_id: External application name

        """
        url = url_join(self.resource, resource_id)
        await self.session.delete_async(url)
